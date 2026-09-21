# Copyright (c) 2026 deterministic-response-cache contributors

"""RED regression contracts for Loaded Runtime Cache bounded-context independence."""

import ast
from pathlib import Path

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
    """Map local aliases to the standard-library modules and callables they expose."""
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


def _is_forbidden_dynamic_import_call(
    statement: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
) -> bool:
    """Return whether one call reaches ``importlib`` or ``builtins`` import machinery."""
    if not isinstance(statement, ast.Call):
        return False
    if isinstance(statement.func, ast.Name):
        return statement.func.id == "__import__" or (
            statement.func.id in callables
            and callables[statement.func.id] in {"builtins.__import__", "importlib.import_module"}
        )
    if not isinstance(statement.func, ast.Attribute) or not isinstance(
        statement.func.value,
        ast.Name,
    ):
        return False
    module = modules.get(statement.func.value.id)
    return (module, statement.func.attr) in {
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
        return callables.get(statement.id) == "sys.modules"
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
            if isinstance(statement, (ast.ClassDef, ast.TypeAlias)) and statement.name == type_name:
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


def test_bc_independence_rejects_direct_and_alias_dynamic_import_bypasses(tmp_path: Path) -> None:
    """The parser rejects direct, callable-alias, and module-alias bypass forms."""
    package_root = tmp_path / "deterministic_response_cache"
    source_directory = package_root / "loaded_runtime_cache"
    source_directory.mkdir(parents=True)
    (source_directory / "direct_importlib.py").write_text(
        "import importlib\nimportlib.import_module('identity')\n",
        encoding="utf-8",
    )
    (source_directory / "direct_builtin.py").write_text(
        "__import__('deterministic_response_cache.identity')\n",
        encoding="utf-8",
    )
    (source_directory / "module_aliases.py").write_text(
        "import builtins as native\nimport importlib as loader\n"
        "native.__import__('identity')\nloader.import_module('identity')\n",
        encoding="utf-8",
    )
    (source_directory / "callable_aliases.py").write_text(
        "from builtins import __import__ as native_import\n"
        "from importlib import import_module as load_module\n"
        "native_import('identity')\nload_module('identity')\n",
        encoding="utf-8",
    )
    (source_directory / "module_cache.py").write_text(
        "import sys as runtime_modules\n"
        "from sys import modules as module_cache\n"
        "runtime_modules.modules['identity'] = object()\n"
        "module_cache['identity'] = object()\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(source_directory)


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


def test_bc_independence_accepts_current_sources_only_when_no_boundary_bypass_exists() -> None:
    """Production sources must remain free of dynamic imports and duplicate semantics."""
    loaded_runtime_cache = SOURCE_ROOT / "loaded_runtime_cache"
    identity = SOURCE_ROOT / "identity"

    assert not _uses_dynamic_import_substitution(loaded_runtime_cache)
    assert not _uses_dynamic_import_substitution(identity)
    assert not _declares_forbidden_semantic_type(loaded_runtime_cache, "ModelIdentity")
    assert not _declares_forbidden_semantic_type(identity, "RuntimeReuseKey")
