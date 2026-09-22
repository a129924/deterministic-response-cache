# Copyright (c) 2026 deterministic-response-cache contributors

"""RED regression contracts for Loaded Runtime Cache bounded-context independence."""

import ast
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).parents[1] / "src" / "deterministic_response_cache"
_FORBIDDEN_DYNAMIC_IMPORT_NAMES = frozenset({"import_module", "__import__"})
_IDENTITY_BC = "deterministic_response_cache.identity"
_RUNTIME_CACHE_BC = "deterministic_response_cache.loaded_runtime_cache"


def _direct_imports_from(
    source_directory: Path,
    *,
    package_root: Path = SOURCE_ROOT,
) -> set[str]:
    """Return normalized absolute package import targets below one BC directory."""
    imports: set[str] = set()
    for source_path in source_directory.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for statement in ast.walk(tree):
            if isinstance(statement, ast.Import):
                imports.update(alias.name for alias in statement.names)
            elif isinstance(statement, ast.ImportFrom):
                imports.update(
                    _normalized_import_from_targets(
                        statement,
                        source_path=source_path,
                        package_root=package_root,
                    ),
                )
    return imports


def _normalized_import_from_targets(
    statement: ast.ImportFrom,
    *,
    source_path: Path,
    package_root: Path,
) -> set[str]:
    """Resolve an ``ImportFrom`` statement to absolute module and alias targets."""
    package_parts = (package_root.name, *source_path.relative_to(package_root).parent.parts)
    base_parts = (
        () if statement.level == 0 else package_parts[: len(package_parts) - (statement.level - 1)]
    )
    module_parts = () if statement.module is None else tuple(statement.module.split("."))
    module_target = ".".join((*base_parts, *module_parts))
    return {
        target
        for target in (
            module_target,
            *(f"{module_target}.{alias.name}" for alias in statement.names),
        )
        if target
    }


def _uses_dynamic_import_substitution(source_directory: Path) -> bool:
    """Detect direct and alias-based import or module-cache substitution constructs."""
    for source_path in source_directory.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        imported_modules, imported_callables = _import_aliases(tree)
        for statement in ast.walk(tree):
            if _is_forbidden_dynamic_import_call(statement, imported_modules, imported_callables):
                return True
            if _is_module_cache_access(statement, imported_modules, imported_callables):
                return True
    return False


def _import_aliases(tree: ast.AST) -> tuple[dict[str, str], dict[str, str]]:
    """Map imports and assignment aliases to forbidden standard-library surfaces."""
    modules, callables = _aliases_from_imports(tree)
    _add_assignment_aliases(tree, modules, callables)
    return modules, callables


def _aliases_from_imports(tree: ast.AST) -> tuple[dict[str, str], dict[str, str]]:
    """Map only import statements to their standard-library targets."""
    modules: dict[str, str] = {}
    callables: dict[str, str] = {}
    for statement in ast.walk(tree):
        if isinstance(statement, ast.Import):
            for alias in statement.names:
                if alias.name in {"builtins", "importlib", "sys"}:
                    modules[alias.asname or alias.name] = alias.name
        elif isinstance(statement, ast.ImportFrom) and statement.module in {
            "builtins",
            "importlib",
            "sys",
        }:
            for alias in statement.names:
                if alias.name in _FORBIDDEN_DYNAMIC_IMPORT_NAMES | {"modules"}:
                    callables[alias.asname or alias.name] = f"{statement.module}.{alias.name}"
    return modules, callables


def _add_assignment_aliases(
    tree: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
) -> None:
    """Resolve fixed-point local aliases for forbidden modules and callables."""
    assignments = [
        statement
        for statement in ast.walk(tree)
        if isinstance(statement, (ast.Assign, ast.AnnAssign))
    ]
    for _ in range(len(assignments) + 1):
        changed = False
        for statement in assignments:
            value = statement.value
            targets = _assignment_target_names(statement)
            if not targets or value is None:
                continue
            resolved = _resolve_forbidden_alias(value, modules, callables)
            if resolved is None:
                continue
            kind, imported_name = resolved
            aliases = modules if kind == "module" else callables
            for target in targets:
                if aliases.get(target) != imported_name:
                    aliases[target] = imported_name
                    changed = True
        if not changed:
            break


def _assignment_target_names(statement: ast.Assign | ast.AnnAssign) -> tuple[str, ...]:
    """Return all-simple local targets, rejecting mixed assignment targets atomically."""
    if isinstance(statement, ast.AnnAssign):
        return (statement.target.id,) if isinstance(statement.target, ast.Name) else ()
    names: list[str] = []
    for target in statement.targets:
        if not isinstance(target, ast.Name):
            return ()
        names.append(target.id)
    return tuple(names)


def _resolve_forbidden_alias(
    value: ast.expr,
    modules: dict[str, str],
    callables: dict[str, str],
) -> tuple[str, str] | None:
    """Resolve one direct or assignment-based alias without executing source code."""
    if isinstance(value, ast.Name):
        return _resolve_name_alias(value.id, modules, callables)
    if isinstance(value, ast.Attribute):
        return _resolve_attribute_alias(value, modules)
    return None


def _resolve_name_alias(
    name: str,
    modules: dict[str, str],
    callables: dict[str, str],
) -> tuple[str, str] | None:
    """Resolve a direct name into an already-known forbidden alias target."""
    if name in modules:
        return "module", modules[name]
    if name == "__import__":
        return "callable", "builtins.__import__"
    if name in callables:
        return "callable", callables[name]
    return None


def _resolve_attribute_alias(
    value: ast.Attribute,
    modules: dict[str, str],
) -> tuple[str, str] | None:
    """Resolve a module attribute that exposes forbidden import/cache machinery."""
    qualified_name = _qualified_module_attribute(value, modules)
    if qualified_name is None:
        return None
    if qualified_name in {
        "builtins.__import__",
        "importlib.import_module",
        "sys.modules",
    } or qualified_name.startswith("sys.modules."):
        return "callable", qualified_name
    return None


def _qualified_module_attribute(value: ast.Attribute, modules: dict[str, str]) -> str | None:
    """Return a dotted module attribute path rooted in a known module alias."""
    if isinstance(value.value, ast.Name):
        module = modules.get(value.value.id)
        return f"{module}.{value.attr}" if module is not None else None
    if not isinstance(value.value, ast.Attribute):
        return None
    parent = _qualified_module_attribute(value.value, modules)
    return f"{parent}.{value.attr}" if parent is not None else None


def _is_forbidden_dynamic_import_call(
    statement: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
) -> bool:
    """Return whether one call reaches ``importlib`` or ``builtins`` import machinery."""
    if not isinstance(statement, ast.Call):
        return False
    return _is_forbidden_import_callable_expression(statement.func, modules, callables)


def _is_forbidden_import_callable_expression(
    expression: ast.expr,
    modules: dict[str, str],
    callables: dict[str, str],
) -> bool:
    """Return whether a callable expression can reach forbidden import machinery."""
    if isinstance(expression, ast.IfExp):
        return _is_forbidden_import_callable_expression(
            expression.body,
            modules,
            callables,
        ) or _is_forbidden_import_callable_expression(expression.orelse, modules, callables)
    if isinstance(expression, ast.Name):
        return expression.id == "__import__" or (
            expression.id in callables
            and callables[expression.id] in {"builtins.__import__", "importlib.import_module"}
        )
    if not isinstance(expression, ast.Attribute) or not isinstance(expression.value, ast.Name):
        return False
    module = modules.get(expression.value.id)
    return (module, expression.attr) in {
        ("builtins", "__import__"),
        ("importlib", "import_module"),
    }


def _is_module_cache_access(
    statement: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
) -> bool:
    """Return whether an expression reaches ``sys.modules``, including aliases."""
    if isinstance(statement, ast.Name):
        target = callables.get(statement.id)
        return target == "sys.modules" or (target is not None and target.startswith("sys.modules."))
    return (
        isinstance(statement, ast.Attribute)
        and isinstance(statement.value, ast.Name)
        and modules.get(statement.value.id) == "sys"
        and statement.attr == "modules"
    )


def _declares_forbidden_semantic_type(source_directory: Path, type_name: str) -> bool:
    """Detect a local nominal or type-alias declaration of the foreign BC semantic type."""
    for source_path in source_directory.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for statement in ast.walk(tree):
            if isinstance(statement, ast.ClassDef) and statement.name == type_name:
                return True
            if isinstance(statement, ast.TypeAlias) and statement.name.id == type_name:
                return True
            if isinstance(statement, (ast.Assign, ast.AnnAssign)) and _assignment_names(
                statement,
                type_name,
            ):
                return True
    return False


def _assignment_names(statement: ast.Assign | ast.AnnAssign, name: str) -> bool:
    """Return whether an assignment gives a local binding the forbidden type name."""
    if isinstance(statement, ast.AnnAssign):
        return isinstance(statement.target, ast.Name) and statement.target.id == name
    return any(isinstance(target, ast.Name) and target.id == name for target in statement.targets)


def test_loaded_runtime_cache_does_not_directly_import_identity_bc() -> None:
    """Loaded Runtime Cache owns local semantics and never imports Identity BC."""
    imports = _direct_imports_from(SOURCE_ROOT / "loaded_runtime_cache")

    assert not any(
        module == _IDENTITY_BC or module.startswith(f"{_IDENTITY_BC}.") for module in imports
    )


def test_identity_bc_does_not_directly_import_loaded_runtime_cache() -> None:
    """Identity remains the sole owner of model identity without cache coupling."""
    imports = _direct_imports_from(SOURCE_ROOT / "identity")

    assert not any(
        module == _RUNTIME_CACHE_BC or module.startswith(f"{_RUNTIME_CACHE_BC}.")
        for module in imports
    )


@pytest.mark.parametrize(
    ("case_name", "source"),
    [
        (
            "direct-importlib",
            "import importlib\nimportlib.import_module('identity')\n",
        ),
        (
            "direct-builtins",
            "__import__('deterministic_response_cache.identity')\n",
        ),
        (
            "module-alias",
            "import importlib as loader\nloader.import_module('identity')\n",
        ),
        (
            "callable-alias",
            "from importlib import import_module as load_module\nload_module('identity')\n",
        ),
        (
            "assignment-callable-importlib-alias",
            "import importlib\nload = importlib.import_module\nload('identity')\n",
        ),
        (
            "mixed-assignment-callable-importlib-alias",
            (
                "import importlib\nload = holder.loader = importlib.import_module\n"
                "load('identity')\n"
            ),
        ),
        (
            "chained-assignment-callable-importlib-alias",
            (
                "import importlib\nfirst = second = importlib.import_module\n"
                "first('identity')\nsecond('identity')\n"
            ),
        ),
        (
            "chained-assignment-callable-importlib-alias-through-conditional-expression",
            (
                "import importlib\nfirst = second = importlib.import_module\n"
                "(first if True else second)('identity')\n"
            ),
        ),
        (
            "assignment-callable-builtins-alias",
            "import builtins\nload = builtins.__import__\nload('identity')\n",
        ),
        (
            "sys-modules-module-alias",
            "import sys as runtime\ncache = runtime.modules\ncache['identity'] = object()\n",
        ),
        (
            "sys-modules-callable-alias",
            "import sys\nlookup = sys.modules.get\nlookup('identity')\n",
        ),
    ],
)
def test_bc_independence_rejects_each_dynamic_import_bypass(
    tmp_path: Path,
    case_name: str,
    source: str,
) -> None:
    """Each dynamic bypass is independently rejected without fixture cross-contamination."""
    package_root = tmp_path / "deterministic_response_cache"
    source_directory = package_root / case_name / "loaded_runtime_cache"
    source_directory.mkdir(parents=True)
    (source_directory / "bypass.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(source_directory)


def test_bc_independence_resolves_every_simple_target_of_chained_import_alias() -> None:
    """Every simple target of a chained assignment retains the resolved import alias."""
    _, callables = _import_aliases(
        ast.parse("import importlib\nfirst = second = importlib.import_module\n"),
    )

    assert callables["first"] == "importlib.import_module"
    assert callables["second"] == "importlib.import_module"


def test_bc_independence_rejects_mixed_assignment_targets_atomically() -> None:
    """A mixed-target assignment never grants an alias to only one target."""
    _, callables = _import_aliases(
        ast.parse("import importlib\nfirst = holder.value = importlib.import_module\n"),
    )

    assert "first" not in callables


def test_bc_independence_rejects_duplicate_foreign_semantic_types(tmp_path: Path) -> None:
    """Neither BC may redeclare the other BC's nominal semantic type."""
    package_root = tmp_path / "deterministic_response_cache"
    loaded_runtime_cache = package_root / "loaded_runtime_cache"
    identity = package_root / "identity"
    loaded_runtime_cache.mkdir(parents=True)
    identity.mkdir(parents=True)
    (loaded_runtime_cache / "duplicate.py").write_text(
        "class ModelIdentity:\n    pass\n",
        encoding="utf-8",
    )
    (identity / "duplicate.py").write_text(
        "RuntimeReuseKey: type[object] = object\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(loaded_runtime_cache, "ModelIdentity")
    assert _declares_forbidden_semantic_type(identity, "RuntimeReuseKey")


def test_bc_independence_rejects_pep695_duplicate_foreign_semantic_type_aliases(
    tmp_path: Path,
) -> None:
    """Python 3.12 TypeAlias names remain subject to BC semantic ownership."""
    package_root = tmp_path / "deterministic_response_cache"
    loaded_runtime_cache = package_root / "loaded_runtime_cache"
    identity = package_root / "identity"
    loaded_runtime_cache.mkdir(parents=True)
    identity.mkdir(parents=True)
    (loaded_runtime_cache / "duplicate.py").write_text(
        "type ModelIdentity = object\n",
        encoding="utf-8",
    )
    (identity / "duplicate.py").write_text(
        "type RuntimeReuseKey = object\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(loaded_runtime_cache, "ModelIdentity")
    assert _declares_forbidden_semantic_type(identity, "RuntimeReuseKey")


def test_bc_independence_accepts_current_sources_only_when_no_boundary_bypass_exists() -> None:
    """Production sources must remain free of dynamic imports and duplicate semantics."""
    loaded_runtime_cache = SOURCE_ROOT / "loaded_runtime_cache"
    identity = SOURCE_ROOT / "identity"

    assert not _uses_dynamic_import_substitution(loaded_runtime_cache)
    assert not _uses_dynamic_import_substitution(identity)
    assert not _declares_forbidden_semantic_type(loaded_runtime_cache, "ModelIdentity")
    assert not _declares_forbidden_semantic_type(identity, "RuntimeReuseKey")
