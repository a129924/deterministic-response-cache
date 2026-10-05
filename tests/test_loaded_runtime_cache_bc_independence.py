# Copyright (c) 2026 deterministic-response-cache contributors

"""RED regression contracts for Loaded Runtime Cache bounded-context independence."""

import ast
import json
import re
from itertools import product
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).parents[1] / "src" / "deterministic_response_cache"
DATAFLOW_SOURCE = (
    Path(__file__).parents[1]
    / "docs"
    / "architecture"
    / "loaded-runtime-cache"
    / "loaded-runtime-cache.dataflow.json"
)
_FORBIDDEN_DYNAMIC_IMPORT_NAMES = frozenset({"import_module", "__import__"})
_GETATTR_ARGUMENT_COUNT = 2
_IDENTITY_BC = "deterministic_response_cache.identity"
_RUNTIME_CACHE_BC = "deterministic_response_cache.loaded_runtime_cache"


@pytest.mark.parametrize(
    "source",
    [
        "import importlib\nimportlib.__import__('identity')\n",
        "import importlib as il\nil.__import__('identity')\n",
        "from importlib import __import__ as load\nload('identity')\n",
        "import importlib\nload = importlib.__import__\nload('identity')\n",
        "import importlib\nil = importlib\nload = il.__import__\nload('identity')\n",
        "from importlib import __import__ as first\nload = first\nload('identity')\n",
        "import importlib\nexecutor.submit(importlib.__import__, 'identity')\n",
    ],
)
def test_c42_rejects_importlib_builtin_import_callable_use(
    tmp_path: Path,
    source: str,
) -> None:
    """The importlib import surface remains forbidden through known aliases and uses."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "import_use.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        "import importlib\nload = importlib.__import__\n",
        "from importlib import __import__ as load\n",
        "import importlib\nload = importlib.__import__\nlen('identity')\n",
        "import importlib\nordinary = len\nordinary('identity')\n",
        "unknown.__import__('identity')\n",
    ],
)
def test_c42_preserves_unused_and_ordinary_import_callables(
    tmp_path: Path,
    source: str,
) -> None:
    """Possession of an unused callable is not a new forbidden-use rule."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "unused.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize("definition", ["def", "async def"])
def test_c42_rejects_foreign_semantic_function_definition_names(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    definition: str,
) -> None:
    """Sync and async definition names establish the same foreign local binding."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "definition.py").write_text(
        f"{definition} {foreign_name}():\n    return object()\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize(
    "source",
    [
        "def ordinary():\n    return object()\n",
        "async def ordinary():\n    return object()\n",
        "def ordinary():\n    return '{name}'\n",
        "async def ordinary():\n    return holder.{name}\n",
    ],
)
def test_c42_preserves_benign_definition_names_strings_and_attributes(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    source: str,
) -> None:
    """Only definition names, not strings or attribute labels, establish ownership."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "definition.py").write_text(
        source.format(name=foreign_name),
        encoding="utf-8",
    )

    assert not _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize("literal", ["({elements},)", "[{elements}]"])
@pytest.mark.parametrize(
    ("elements", "condition", "operation"),
    [
        ("importlib, builtins", "importlib", "loader.import_module('identity')"),
        ("builtins, importlib", "importlib", "loader.import_module('identity')"),
        ("builtins, importlib", "builtins", "loader.__import__('identity')"),
        ("importlib, builtins", "builtins", "loader.__import__('identity')"),
        ("sys, importlib", "sys", "loader.modules['identity'] = object()"),
        ("importlib, sys", "sys", "loader.modules['identity'] = object()"),
        ("importlib", "importlib", "loader.import_module('identity')"),
        ("builtins", "builtins", "loader.__import__('identity')"),
        ("sys", "sys", "loader.modules['identity'] = object()"),
        ("importlib, ordinary, unknown", "importlib", "loader.import_module('identity')"),
    ],
)
def test_c42_rejects_forbidden_use_of_any_known_for_module_alternative(
    tmp_path: Path,
    literal: str,
    elements: str,
    condition: str,
    operation: str,
) -> None:
    """Finite literal module alternatives must not be overwritten by the last element."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "alternatives.py").write_text(
        "import importlib\nimport builtins\nimport sys\n"
        f"for loader in {literal.format(elements=elements)}:\n"
        f"    if loader is {condition}:\n        {operation}\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        "import importlib\nimport builtins\nfor loader in (importlib, builtins):\n    pass\n",
        "import importlib\nimport builtins\nfor loader in [builtins, importlib]:\n    pass\n",
        "for loader in [ordinary, unknown]:\n    loader.import_module('identity')\n",
        "for loader in unknown_values:\n    loader.import_module('identity')\n",
        (
            "import importlib\nfor loader in [*unknown_values]:\n"
            "    loader.import_module('identity')\n"
        ),
        (
            "import importlib\nasync def run():\n"
            "    async for loader in (importlib,):\n        loader.import_module('identity')\n"
        ),
        "import builtins\nfor loader in [builtins]:\n    loader.len('identity')\n",
        "import importlib\nfor loader in []:\n    loader.import_module('identity')\n",
    ],
)
def test_c42_preserves_unused_and_out_of_scope_for_module_bindings(
    tmp_path: Path,
    source: str,
) -> None:
    """Unknown iterables and async syntax cannot acquire new module alternatives."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "controls.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        "load, *rest = (__import__, len)\nload('identity')\n",
        "import importlib\nfor load in (importlib.import_module,):\n    load('identity')\n",
        "*rest, load = (len, str, __import__)\nload('identity')\n",
        "*rest, load = [len, str, __import__]\nload('identity')\n",
        "[load, *rest] = [__import__, len, str]\nload('identity')\n",
        "first, *rest, load = (len, str, __import__)\nload('identity')\n",
        "[load, *rest, last] = [__import__, len, str]\nload('identity')\n",
        "holder.value, *rest, load = (len, str, __import__)\nload('identity')\n",
        "[load, *rest, holder.value] = [__import__, len, str]\nload('identity')\n",
        ("import importlib\nloader, *rest = (importlib, None)\nloader.import_module('identity')\n"),
        "import builtins\n*rest, loader = [None, builtins]\nloader.__import__('identity')\n",
        ("import importlib\nfor load in [len, importlib.import_module]:\n    load('identity')\n"),
        "for load in (__import__, len):\n    load('identity')\n",
        (
            "import importlib\nfor loader in [None, importlib]:\n"
            "    loader.import_module('identity')\n"
        ),
        "import builtins\nfor loader in (builtins,):\n    loader.__import__('identity')\n",
        (
            "import sys\n*rest, module_cache = [None, sys.modules]\n"
            "module_cache['identity'] = object()\n"
        ),
        (
            "import sys\nfor module_cache in [sys.modules]:\n"
            "    module_cache['identity'] = object()\n"
        ),
    ],
)
def test_c40_rejects_forbidden_uses_after_literal_only_bindings(
    tmp_path: Path,
    source: str,
) -> None:
    """Known literal prefix/suffix and For aliases retain use-based import restrictions."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "binding.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        "load, *rest = (__import__, len)\n",
        "import importlib\nfor load in [importlib.import_module]:\n    pass\n",
        "load, *rest = (len, str)\nload('identity')\n",
        "for load in [len, str]:\n    load('identity')\n",
        "for load in []:\n    load('identity')\n",
        "first, *rest, load = [__import__]\nload('identity')\n",
        "load, *rest = unknown_values\nload('identity')\n",
        "load, *rest = (*unknown_values, __import__)\nload('identity')\n",
        "*rest, load = (len, *unknown_values)\nload('identity')\n",
        "*load, other = (__import__, len)\nload('identity')\n",
        "holder.load, *rest = (__import__, len)\nholder.load('identity')\n",
        "for load in unknown_values:\n    load('identity')\n",
        "for load in [*unknown_values]:\n    load('identity')\n",
        "async def run():\n    async for load in (__import__,):\n        load('identity')\n",
        "[load('identity') for load in (__import__,)]\n",
        "(load('identity') for load in [__import__])\n",
    ],
)
def test_c40_preserves_unused_benign_and_out_of_scope_bindings(
    tmp_path: Path,
    source: str,
) -> None:
    """Unknown, starred-container and non-synchronous iterables do not acquire aliases."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "binding.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize(
    "target",
    [
        "{name}, other",
        "[other, {name}]",
        "[other, ({name}, tail)]",
        "(other, [tail, {name}])",
        "*{name}, other",
        "[other, *{name}]",
        "(other, [tail, *{name}])",
        "holder.value, {name}",
    ],
)
def test_c37_rejects_foreign_semantic_assignment_targets(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    target: str,
) -> None:
    """Target syntax declares foreign local names independently of unknown RHS values."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "target.py").write_text(
        f"{target.format(name=foreign_name)} = unknown_values\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize(
    "target",
    [
        "local, other",
        "[local, (other, tail)]",
        "[other, *local]",
        "holder.{name}, other",
        "[other, (holder.{name}, tail)]",
        "[other, *holder.{name}]",
    ],
)
def test_c37_accepts_benign_and_attribute_assignment_targets(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    target: str,
) -> None:
    """Attribute labels are not local semantic declarations, even inside nested targets."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "target.py").write_text(
        f"{target.format(name=foreign_name)} = unknown_values\n",
        encoding="utf-8",
    )

    assert not _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
def test_c37_rejects_foreign_semantic_named_expression(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
) -> None:
    """A direct walrus target declares the opposite BC's semantic name."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "target.py").write_text(
        f"({foreign_name} := unknown_value)\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
def test_c37_accepts_benign_named_expression_without_rhs_inference(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
) -> None:
    """A foreign name on the RHS does not make a benign target a declaration."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "target.py").write_text(
        f"(local := {foreign_name})\n",
        encoding="utf-8",
    )

    assert not _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize("getter", ["getattr", "read_attribute"])
@pytest.mark.parametrize(
    ("module", "attribute", "operation"),
    [
        ("builtins", "__import__", "('identity')"),
        ("importlib", "import_module", "('identity')"),
        ("sys", "modules", "['identity'] = object()"),
    ],
)
def test_c37_rejects_direct_imported_builtins_getattr(
    tmp_path: Path,
    getter: str,
    module: str,
    attribute: str,
    operation: str,
) -> None:
    """Direct known-builtins imports retain literal forbidden-attribute detection."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    import_name = "getattr" if getter == "getattr" else f"getattr as {getter}"
    (directory / "getter.py").write_text(
        f"from builtins import {import_name}\nimport {module} as known_module\n"
        f"{getter}(known_module, '{attribute}'){operation}\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        "from builtins import getattr\nimport builtins\ngetattr(builtins, 'len')([])\n",
        (
            "from builtins import getattr as read_attribute\nimport builtins\n"
            "read_attribute(builtins, 'len')([])\n"
        ),
        (
            "from other_library import getattr as read_attribute\nimport importlib\n"
            "read_attribute(importlib, 'import_module')('identity')\n"
        ),
        (
            "from builtins import getattr as read_attribute\n"
            "read_attribute(unknown_module, 'import_module')('identity')\n"
        ),
        (
            "from builtins import getattr as read_attribute\nimport importlib\n"
            "read_attribute(importlib, unknown_attribute)('identity')\n"
        ),
        (
            "from builtins import getattr as read_attribute\nimport importlib\n"
            "read_attribute(importlib, 'import_module', None)('identity')\n"
        ),
        (
            "from builtins import getattr as read_attribute\nimport importlib\n"
            "read_attribute(importlib, name='import_module')('identity')\n"
        ),
    ],
)
def test_c37_accepts_benign_unknown_or_out_of_bounds_imported_getters(
    tmp_path: Path,
    source: str,
) -> None:
    """Known module/literal/exact-arity bounds exclude unrelated imported callables."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "getter.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(directory)


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
        contexts, preserved_modules = _for_module_alias_contexts(
            tree,
            imported_modules,
            imported_callables,
        )
        for modules in contexts:
            callables = imported_callables.copy()
            _add_assignment_aliases(tree, modules, callables, preserved_modules)
            for statement in ast.walk(tree):
                if _is_forbidden_dynamic_import_call(statement, modules, callables):
                    return True
                if _is_module_cache_access(statement, modules, callables):
                    return True
    return False


def _for_module_alias_contexts(
    tree: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
) -> tuple[list[dict[str, str]], frozenset[str]]:
    """Retain finite known module alternatives from For literals and conditional bindings."""
    alternatives: dict[str, set[str]] = {}
    for statement in ast.walk(tree):
        if not (
            isinstance(statement, ast.For)
            and isinstance(statement.target, ast.Name)
            and isinstance(statement.iter, (ast.Tuple, ast.List))
        ):
            continue
        for element in statement.iter.elts:
            if isinstance(element, ast.Starred):
                continue
            resolved = _resolve_forbidden_alias(element, modules, callables)
            if resolved is not None and resolved[0] == "module":
                alternatives.setdefault(statement.target.id, set()).add(resolved[1])
    _add_conditional_module_alternatives(tree, modules, callables, alternatives)
    return _module_alternative_contexts(modules, alternatives), frozenset(alternatives)


def _add_conditional_module_alternatives(
    tree: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
    alternatives: dict[str, set[str]],
) -> None:
    """Preserve finite known module branches for existing static conditional bindings."""
    conditional_bindings = [
        (target, value)
        for target, value in _static_alias_bindings(tree)
        if isinstance(value, ast.IfExp)
    ]
    for _ in range(len(conditional_bindings) + 1):
        changed = False
        contexts = _module_alternative_contexts(modules, alternatives)
        for target, value in conditional_bindings:
            known: set[str] = set()
            for context in contexts:
                known.update(_conditional_module_alternatives(value, context, callables))
            if known and not known <= alternatives.get(target, set()):
                alternatives.setdefault(target, set()).update(known)
                changed = True
        if not changed:
            break


def _conditional_module_alternatives(
    value: ast.expr,
    modules: dict[str, str],
    callables: dict[str, str],
) -> set[str]:
    """Collect only finite known conditional module branches without evaluating conditions."""
    if isinstance(value, ast.IfExp):
        return _conditional_module_alternatives(
            value.body,
            modules,
            callables,
        ) | _conditional_module_alternatives(value.orelse, modules, callables)
    resolved = _resolve_forbidden_alias(value, modules, callables)
    return {resolved[1]} if resolved is not None and resolved[0] == "module" else set()


def _module_alternative_contexts(
    modules: dict[str, str],
    alternatives: dict[str, set[str]],
) -> list[dict[str, str]]:
    """Enumerate the bounded known module alternatives used by the existing USE checks."""
    if not alternatives:
        return [modules.copy()]
    names = list(alternatives)
    return [
        modules | dict(zip(names, values, strict=True))
        for values in product(*(sorted(alternatives[name]) for name in names))
    ]


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
                elif alias.name.startswith("importlib.") and alias.asname is None:
                    # ``import importlib.util`` binds ``importlib`` at module scope.
                    modules["importlib"] = "importlib"
        elif isinstance(statement, ast.ImportFrom) and statement.module in {
            "builtins",
            "importlib",
            "sys",
        }:
            for alias in statement.names:
                if alias.name in _FORBIDDEN_DYNAMIC_IMPORT_NAMES | {"modules"}:
                    callables[alias.asname or alias.name] = f"{statement.module}.{alias.name}"
                elif statement.module == "builtins" and alias.name == "getattr":
                    callables[alias.asname or alias.name] = "builtins.getattr"
    return modules, callables


def _add_assignment_aliases(
    tree: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
    preserved_modules: frozenset[str] = frozenset(),
) -> None:
    """Resolve fixed-point local aliases for forbidden modules and callables."""
    assignments = _static_alias_bindings(tree)
    for _ in range(len(assignments) + 1):
        changed = False
        for target, value in assignments:
            resolved = _resolve_forbidden_alias(value, modules, callables)
            if resolved is None:
                continue
            kind, imported_name = resolved
            if kind == "module" and target in preserved_modules:
                continue
            aliases = modules if kind == "module" else callables
            if aliases.get(target) != imported_name:
                aliases[target] = imported_name
                changed = True
        if not changed:
            break


def _paired_literal_bindings(target: ast.expr, value: ast.expr) -> list[tuple[str, ast.expr]]:
    """Pair literal elements without inferring unpacked or arbitrary iterable values."""
    if isinstance(target, ast.Name):
        return [(target.id, value)]
    if isinstance(target, (ast.Tuple, ast.List)) and isinstance(value, (ast.Tuple, ast.List)):
        starred_positions = [
            index for index, element in enumerate(target.elts) if isinstance(element, ast.Starred)
        ]
        if (
            len(starred_positions) == 1
            and len(value.elts) >= len(target.elts) - 1
            and not any(isinstance(element, ast.Starred) for element in value.elts)
        ):
            star_index = starred_positions[0]
            suffix_count = len(target.elts) - star_index - 1
            definite_pairs = list(
                zip(target.elts[:star_index], value.elts[:star_index], strict=True),
            )
            if suffix_count:
                definite_pairs.extend(
                    zip(target.elts[-suffix_count:], value.elts[-suffix_count:], strict=True),
                )
            return [
                (child_target.id, child_value)
                for child_target, child_value in definite_pairs
                if isinstance(child_target, ast.Name)
            ]
    if (
        isinstance(target, (ast.Tuple, ast.List))
        and isinstance(value, (ast.Tuple, ast.List))
        and len(target.elts) == len(value.elts)
        and not any(isinstance(item, ast.Starred) for item in (*target.elts, *value.elts))
    ):
        return [
            binding
            for child_target, child_value in zip(target.elts, value.elts, strict=True)
            for binding in _paired_literal_bindings(child_target, child_value)
        ]
    return []


def _static_alias_bindings(tree: ast.AST) -> list[tuple[str, ast.expr]]:
    """Collect literal assignment pairs and actual parameter/default pairs."""
    bindings: list[tuple[str, ast.expr]] = []
    for statement in ast.walk(tree):
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                bindings.extend(_paired_literal_bindings(target, statement.value))
        elif isinstance(statement, (ast.AnnAssign, ast.NamedExpr)):
            if statement.value is not None:
                bindings.extend(_paired_literal_bindings(statement.target, statement.value))
        elif (
            isinstance(statement, ast.For)
            and isinstance(statement.target, ast.Name)
            and isinstance(statement.iter, (ast.Tuple, ast.List))
        ):
            bindings.extend(
                (statement.target.id, element)
                for element in statement.iter.elts
                if not isinstance(element, ast.Starred)
            )
        elif isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            arguments = statement.args
            positional = [*arguments.posonlyargs, *arguments.args]
            default_parameters = positional[len(positional) - len(arguments.defaults) :]
            bindings.extend(
                (parameter.arg, value)
                for parameter, value in zip(default_parameters, arguments.defaults, strict=True)
            )
            bindings.extend(
                (parameter.arg, value)
                for parameter, value in zip(
                    arguments.kwonlyargs,
                    arguments.kw_defaults,
                    strict=True,
                )
                if value is not None
            )
    return bindings


def _resolve_forbidden_alias(
    value: ast.expr,
    modules: dict[str, str],
    callables: dict[str, str],
) -> tuple[str, str] | None:
    """Resolve one direct or assignment-based alias without executing source code."""
    if isinstance(value, ast.Name):
        return _resolve_name_alias(value.id, modules, callables)
    if isinstance(value, ast.Attribute):
        return _resolve_import_callable_attribute(value, modules, callables)
    if isinstance(value, ast.IfExp):
        body = _resolve_forbidden_alias(value.body, modules, callables)
        alternative = _resolve_forbidden_alias(value.orelse, modules, callables)
        for resolved in (body, alternative):
            if resolved is not None and resolved[0] == "callable":
                return resolved
        return body or alternative
    if isinstance(value, ast.Call):
        return _resolve_getattr_alias(value, modules, callables)
    return (
        _resolve_namespace_import_callable(value, modules)
        if isinstance(value, ast.Subscript)
        else None
    )


def _resolve_import_callable_attribute(
    value: ast.Attribute,
    modules: dict[str, str],
    callables: dict[str, str],
) -> tuple[str, str] | None:
    """Recognize __call__ only on a known forbidden import callable receiver."""
    if value.attr == "__call__":
        resolved = _resolve_forbidden_alias(value.value, modules, callables)
        if resolved in {
            ("callable", "builtins.__import__"),
            ("callable", "importlib.__import__"),
            ("callable", "importlib.import_module"),
        }:
            return resolved
    return _resolve_attribute_alias(value, modules)


def _resolve_namespace_import_callable(
    value: ast.Subscript,
    modules: dict[str, str],
) -> tuple[str, str] | None:
    """Resolve direct literal __dict__ import entries on known module receivers only."""
    namespace = value.value
    key = value.slice
    if not (
        isinstance(namespace, ast.Attribute)
        and namespace.attr == "__dict__"
        and isinstance(namespace.value, ast.Name)
        and isinstance(key, ast.Constant)
        and isinstance(key.value, str)
    ):
        return None
    module = modules.get(namespace.value.id)
    if (module, key.value) in {
        ("builtins", "__import__"),
        ("importlib", "__import__"),
        ("importlib", "import_module"),
    }:
        return "callable", f"{module}.{key.value}"
    return None


def _resolve_getattr_alias(
    value: ast.Call,
    modules: dict[str, str],
    callables: dict[str, str],
) -> tuple[str, str] | None:
    """Resolve bare, qualified, or directly imported known-builtins ``getattr``."""
    getter = value.func
    is_getattr = (
        isinstance(getter, ast.Name)
        and (getter.id == "getattr" or callables.get(getter.id) == "builtins.getattr")
    ) or (
        isinstance(getter, ast.Attribute)
        and getter.attr == "getattr"
        and isinstance(getter.value, ast.Name)
        and modules.get(getter.value.id) == "builtins"
    )
    if (
        not is_getattr
        or len(value.args) != _GETATTR_ARGUMENT_COUNT
        or value.keywords
        or not isinstance(value.args[0], ast.Name)
        or not isinstance(value.args[1], ast.Constant)
        or not isinstance(value.args[1].value, str)
    ):
        return None
    module = modules.get(value.args[0].id)
    attribute = value.args[1].value
    if (module, attribute) in {
        ("builtins", "__import__"),
        ("importlib", "__import__"),
        ("importlib", "import_module"),
        ("sys", "modules"),
    }:
        return "callable", f"{module}.{attribute}"
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
    if name in callables and callables[name] != "builtins.getattr":
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
        "importlib.__import__",
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
    if isinstance(value.value, ast.NamedExpr):
        named_expression = value.value
        resolved = _resolve_forbidden_alias(named_expression.value, modules, {})
        if type(named_expression.target) is ast.Name and resolved is not None:
            kind, module = resolved
            if kind == "module":
                return f"{module}.{value.attr}"
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
    return any(
        _is_forbidden_import_callable_expression(expression, modules, callables)
        for expression in (
            statement.func,
            *statement.args,
            *(keyword.value for keyword in statement.keywords),
        )
    )


def _is_forbidden_import_callable_expression(
    expression: ast.expr,
    modules: dict[str, str],
    callables: dict[str, str],
) -> bool:
    """Return whether a callable expression can reach forbidden import machinery."""
    resolved = _resolve_forbidden_alias(expression, modules, callables)
    if resolved in {
        ("callable", "builtins.__import__"),
        ("callable", "importlib.__import__"),
        ("callable", "importlib.import_module"),
    } or (
        isinstance(expression, ast.IfExp)
        and (
            _is_forbidden_import_callable_expression(expression.body, modules, callables)
            or _is_forbidden_import_callable_expression(expression.orelse, modules, callables)
        )
    ):
        return True
    if isinstance(expression, ast.NamedExpr):
        resolved = _resolve_forbidden_alias(expression.value, modules, callables)
        return resolved in {
            ("callable", "builtins.__import__"),
            ("callable", "importlib.__import__"),
            ("callable", "importlib.import_module"),
        }
    if isinstance(expression, ast.Attribute) and isinstance(expression.value, ast.NamedExpr):
        named_expression = expression.value
        resolved = _resolve_forbidden_alias(named_expression.value, modules, callables)
        return (
            type(named_expression.target) is ast.Name
            and resolved == ("module", "importlib")
            and expression.attr in _FORBIDDEN_DYNAMIC_IMPORT_NAMES
        )
    if isinstance(expression, ast.Name):
        return expression.id == "__import__" or (
            expression.id in callables
            and callables[expression.id]
            in {"builtins.__import__", "importlib.__import__", "importlib.import_module"}
        )
    if not isinstance(expression, ast.Attribute) or not isinstance(expression.value, ast.Name):
        return False
    module = modules.get(expression.value.id)
    return (module, expression.attr) in {
        ("builtins", "__import__"),
        ("importlib", "__import__"),
        ("importlib", "import_module"),
    }


def _is_module_cache_access(
    statement: ast.AST,
    modules: dict[str, str],
    callables: dict[str, str],
) -> bool:
    """Return whether an expression reaches ``sys.modules``, including aliases."""
    resolved = (
        _resolve_forbidden_alias(statement, modules, callables)
        if isinstance(statement, ast.expr)
        else None
    )
    if resolved is not None and resolved[1] == "sys.modules":
        return True
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
    """Detect local declarations or Identity imports of a foreign semantic type."""
    for source_path in source_directory.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for statement in ast.walk(tree):
            if (
                isinstance(statement, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                and statement.name == type_name
            ):
                return True
            if isinstance(statement, ast.TypeAlias) and statement.name.id == type_name:
                return True
            if _imports_identity_semantic_type(statement, type_name):
                return True
            if _binds_foreign_semantic_name(statement, type_name):
                return True
            if isinstance(
                statement,
                (ast.Assign, ast.AnnAssign, ast.NamedExpr),
            ) and _assignment_names(statement, type_name):
                return True
    return False


def _binds_foreign_semantic_name(statement: ast.AST, type_name: str) -> bool:
    """Inspect authorized import, loop, and context-manager local binding syntax."""
    if isinstance(statement, ast.Import):
        return any(
            (alias.asname or alias.name.split(".", 1)[0]) == type_name for alias in statement.names
        )
    if isinstance(statement, ast.ImportFrom):
        return any((alias.asname or alias.name) == type_name for alias in statement.names)
    if isinstance(statement, (ast.For, ast.AsyncFor)):
        return _semantic_target_names(statement.target, type_name)
    if isinstance(statement, (ast.With, ast.AsyncWith)):
        return any(
            item.optional_vars is not None and _semantic_target_names(item.optional_vars, type_name)
            for item in statement.items
        )
    return False


def _imports_identity_semantic_type(statement: ast.AST, type_name: str) -> bool:
    """Return whether an Identity-BC ImportFrom imports the semantic source name."""
    return (
        isinstance(statement, ast.ImportFrom)
        and type_name == "ModelIdentity"
        and statement.module is not None
        and (statement.module == _IDENTITY_BC or statement.module.startswith(f"{_IDENTITY_BC}."))
        and any(alias.name == type_name for alias in statement.names)
    )


def _assignment_names(statement: ast.Assign | ast.AnnAssign | ast.NamedExpr, name: str) -> bool:
    """Return whether an assignment gives a local binding the forbidden type name."""
    if isinstance(statement, (ast.AnnAssign, ast.NamedExpr)):
        return _semantic_target_names(statement.target, name)
    return any(_semantic_target_names(target, name) for target in statement.targets)


def _semantic_target_names(target: ast.expr, name: str) -> bool:
    """Inspect local target syntax only, without interpreting values or attribute labels."""
    if isinstance(target, ast.Name):
        return target.id == name
    if isinstance(target, (ast.Tuple, ast.List)):
        return any(_semantic_target_names(element, name) for element in target.elts)
    if isinstance(target, ast.Starred):
        return _semantic_target_names(target.value, name)
    return False


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
        (
            "getattr-importlib-callable-alias",
            (
                "import importlib as loader\n"
                "load = getattr(loader, 'import_module')\n"
                "load('identity')\n"
            ),
        ),
        (
            "getattr-sys-modules-alias",
            (
                "import sys as runtime\n"
                "module_cache = getattr(runtime, 'modules')\n"
                "module_cache['identity'] = object()\n"
            ),
        ),
        (
            "direct-getattr-importlib-callable",
            ("import importlib\ngetattr(importlib, 'import_module')('identity')\n"),
        ),
        (
            "direct-getattr-sys-modules-base",
            ("import sys\ngetattr(sys, 'modules')['identity'] = object()\n"),
        ),
        (
            "importlib-submodule-top-level-binding",
            ("import importlib.util\nimportlib.import_module('identity')\n"),
        ),
        (
            "if-expression-assignment-import-alias",
            (
                "import importlib\n"
                "fallback = object()\n"
                "load = importlib.import_module if enabled else fallback\n"
                "load('identity')\n"
            ),
        ),
        (
            "if-expression-assignment-import-alias-in-else-branch",
            (
                "import importlib\n"
                "fallback = object()\n"
                "load = fallback if enabled else importlib.import_module\n"
                "load('identity')\n"
            ),
        ),
        (
            "if-expression-module-before-forbidden-callable",
            ("import importlib\nload = importlib if enabled else __import__\nload('identity')\n"),
        ),
        (
            "if-expression-forbidden-callable-before-module",
            ("import importlib\nload = __import__ if enabled else importlib\nload('identity')\n"),
        ),
        (
            "if-expression-direct-named-expression-in-body",
            "((load := __import__) if enabled else fallback)('identity')\n",
        ),
        (
            "if-expression-direct-named-expression-in-else-branch",
            "(fallback if enabled else (load := __import__))('identity')\n",
        ),
        (
            "attribute-base-named-expression-importlib-alias",
            "import importlib\n(loader := importlib).import_module('identity')\n",
        ),
        (
            "attribute-base-named-expression-sys-modules-alias",
            ("import sys\n(runtime := sys).modules['identity'] = object()\n"),
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


def test_bc_independence_rejects_named_expression_import_alias_without_executing_source(
    tmp_path: Path,
) -> None:
    """A direct-name walrus alias is rejected by static AST analysis only."""
    source_directory = tmp_path / "deterministic_response_cache" / "loaded_runtime_cache"
    source_directory.mkdir(parents=True)
    execution_marker = tmp_path / "source-was-executed"
    (source_directory / "bypass.py").write_text(
        "import importlib\n"
        "(load := importlib.import_module)('identity')\n"
        f"open({str(execution_marker)!r}, 'w').write('executed')\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(source_directory)
    assert not execution_marker.exists()


def test_bc_independence_resolves_every_simple_target_of_chained_import_alias() -> None:
    """Every simple target of a chained assignment retains the resolved import alias."""
    _, callables = _import_aliases(
        ast.parse("import importlib\nfirst = second = importlib.import_module\n"),
    )

    assert callables["first"] == "importlib.import_module"
    assert callables["second"] == "importlib.import_module"


def test_bc_independence_retains_simple_target_from_mixed_assignment() -> None:
    """A mixed assignment retains its simple local alias but ignores attributes."""
    _, callables = _import_aliases(
        ast.parse("import importlib\nload = holder.loader = importlib.import_module\n"),
    )

    assert callables["load"] == "importlib.import_module"
    assert "holder" not in callables


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


def test_bc_independence_rejects_foreign_semantic_import_from_alias(tmp_path: Path) -> None:
    """A foreign semantic type remains foreign when its local import name changes."""
    loaded_runtime_cache = tmp_path / "deterministic_response_cache" / "loaded_runtime_cache"
    loaded_runtime_cache.mkdir(parents=True)
    (loaded_runtime_cache / "foreign_identity_alias.py").write_text(
        "from deterministic_response_cache.identity.contracts import "
        "ModelIdentity as LocalModelIdentity\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(loaded_runtime_cache, "ModelIdentity")


def test_dataflow_preserves_lookup_return_and_only_registry_failure_signal() -> None:
    """The normal return and expected failure are distinct Registry relationships."""
    dataflow = json.loads(DATAFLOW_SOURCE.read_text(encoding="utf-8"))
    nodes_by_label = {node["label"]: node["id"] for node in dataflow["nodes"]}
    runtime_registry = nodes_by_label["RuntimeRegistry"]
    lookup_return = nodes_by_label["RuntimeT | None"]
    unavailable_signal = nodes_by_label["RuntimeRegistryLookupUnavailable"]

    assert any(
        edge["from"] == runtime_registry
        and edge["to"] == lookup_return
        and edge["label"] == "RuntimeRegistry.lookup(key: RuntimeReuseKey) -> RuntimeT | None"
        for edge in dataflow["flows"]
    )
    assert [
        (edge["from"], edge["to"])
        for edge in dataflow["flows"]
        if unavailable_signal in (edge["from"], edge["to"])
    ] == [(runtime_registry, unavailable_signal)]

    forbidden_lookup_targets = {
        node["id"]
        for node in dataflow["nodes"]
        if node["label"] in {"Available", "Missing", "Unavailable"}
        or "mapper" in node["label"].casefold()
    }
    lookup_connections = {
        endpoint
        for edge in dataflow["flows"]
        if runtime_registry in (edge["from"], edge["to"])
        for endpoint in (edge["from"], edge["to"])
    }
    assert not lookup_connections & forbidden_lookup_targets


def test_dataflow_keeps_registry_retain_separate_from_retention_outcomes() -> None:
    """Registry retention declares its inputs and ``None`` completion without outcomes."""
    dataflow = json.loads(DATAFLOW_SOURCE.read_text(encoding="utf-8"))
    nodes_by_label = {node["label"]: node["id"] for node in dataflow["nodes"]}
    runtime_registry = nodes_by_label["RuntimeRegistry"]
    reuse_key = nodes_by_label["RuntimeReuseKey"]
    initialized_runtime = nodes_by_label["已初始化 runtime"]
    retain_label = "RuntimeRegistry.retain(key: RuntimeReuseKey, runtime: RuntimeT) -> None"

    assert any(
        edge["from"] == reuse_key
        and edge["to"] == runtime_registry
        and edge["label"] == retain_label
        for edge in dataflow["flows"]
    )
    assert any(
        edge["from"] == initialized_runtime
        and edge["to"] == runtime_registry
        and edge["label"] == "runtime: RuntimeT"
        for edge in dataflow["flows"]
    )
    assert not any(
        edge["from"] == runtime_registry
        and edge["to"]
        in {
            nodes_by_label["Retained(runtime)"],
            nodes_by_label["NotRetained(runtime)"],
        }
        for edge in dataflow["flows"]
    )


def test_bc_independence_accepts_current_sources_only_when_no_boundary_bypass_exists() -> None:
    """Production sources must remain free of dynamic imports and duplicate semantics."""
    loaded_runtime_cache = SOURCE_ROOT / "loaded_runtime_cache"
    identity = SOURCE_ROOT / "identity"

    assert not _uses_dynamic_import_substitution(loaded_runtime_cache)
    assert not _uses_dynamic_import_substitution(identity)
    assert not _declares_forbidden_semantic_type(loaded_runtime_cache, "ModelIdentity")
    assert not _declares_forbidden_semantic_type(identity, "RuntimeReuseKey")


@pytest.mark.parametrize(
    "source",
    [
        "import importlib\nload, other = importlib.import_module, len\nload('identity')\n",
        "import importlib\n[other, load] = [len, importlib.import_module]\nload('identity')\n",
        (
            "import importlib\n[other, (load, tail)] = [len, (importlib.import_module, str)]\n"
            "load('identity')\n"
        ),
        "import importlib\nholder.loader, load = len, importlib.import_module\nload('identity')\n",
        "import builtins as bi\nload = getattr(bi, '__import__')\nload('identity')\n",
        "import builtins as bi\ngetattr(bi, '__import__')('identity')\n",
        "import importlib\ndef run(first, load=importlib.import_module):\n    load('identity')\n",
        "def run(first, *, ordinary, load=__import__):\n    load('identity')\n",
        (
            "import importlib\ndef run(first=len, load=importlib.import_module):\n"
            "    load('identity')\n"
        ),
        "import importlib\nexecutor.submit(importlib.import_module, 'identity')\n",
        (
            "import importlib\nload = importlib.import_module\n"
            "executor.submit(fn=load, name='identity')\n"
        ),
        "map(__import__, ['identity'])\n",
        "import importlib\nload = importlib.import_module\nmap(load, ['identity'])\n",
    ],
)
def test_c31_rejects_static_forbidden_callable_bindings_and_arguments(
    tmp_path: Path,
    source: str,
) -> None:
    """Declared static alias/default/argument forms cannot bypass the BC scanner."""
    source_directory = tmp_path / "loaded_runtime_cache"
    source_directory.mkdir()
    (source_directory / "bypass.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(source_directory)


@pytest.mark.parametrize(
    "source",
    [
        "import importlib\nload, ordinary = importlib.import_module, len\nordinary('identity')\n",
        (
            "import importlib\n[ordinary, load] = [len, importlib.import_module]\n"
            "ordinary('identity')\n"
        ),
        (
            "import importlib\nholder.loader, ordinary = importlib.import_module, len\n"
            "ordinary('identity')\n"
        ),
        "import builtins as bi\ngetattr(bi, 'len')('identity')\n",
        (
            "import importlib\ndef run(load=importlib.import_module, ordinary=len):\n"
            "    ordinary('identity')\n"
        ),
        "def run(*, ordinary=len):\n    ordinary('identity')\n",
        "executor.submit(len, 'identity')\n",
        "executor.submit(fn=len, value='identity')\n",
        "map(len, ['identity'])\n",
    ],
)
def test_c31_accepts_benign_paired_bindings_defaults_and_arguments(
    tmp_path: Path,
    source: str,
) -> None:
    """Recognizing forbidden callables must not reject ordinary sibling callables."""
    source_directory = tmp_path / "loaded_runtime_cache"
    source_directory.mkdir()
    (source_directory / "benign.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(source_directory)


@pytest.mark.parametrize(
    "target",
    [
        ("import builtins", "builtins", "__import__", "('identity')"),
        ("import importlib", "importlib", "import_module", "('identity')"),
        ("import sys", "sys", "modules", "['identity'] = object()"),
    ],
    ids=["builtin-import", "importlib-import", "module-cache"],
)
@pytest.mark.parametrize(
    "getter",
    [
        ("import builtins", "builtins", False),
        ("import builtins as bi", "bi", False),
        ("import builtins as bi\ngetter_module = bi", "getter_module", False),
        ("import builtins as bi", "bi", True),
    ],
    ids=["direct", "import-alias", "module-assignment-alias", "retained-value"],
)
def test_c33_rejects_qualified_known_builtins_getattr(
    tmp_path: Path,
    target: tuple[str, str, str, str],
    getter: tuple[str, str, bool],
) -> None:
    """Known builtins receivers cannot hide forbidden callable/cache lookup."""
    target_import, target_name, attribute, use = target
    getter_import, getter_name, retain = getter
    lookup = f"{getter_name}.getattr({target_name}, {attribute!r})"
    operation = f"retained = {lookup}\nretained{use}" if retain else f"{lookup}{use}"
    source_directory = tmp_path / "loaded_runtime_cache"
    source_directory.mkdir()
    (source_directory / "bypass.py").write_text(
        f"{getter_import}\n{target_import}\n{operation}\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(source_directory)


@pytest.mark.parametrize(
    "source",
    [
        "import builtins\nbuiltins.getattr(builtins, 'len')('identity')\n",
        "import builtins as bi\nordinary = bi.getattr(bi, 'len')\nordinary('identity')\n",
        "import builtins as bi\ngetter_module = bi\ngetter_module.getattr(bi, 'len')('identity')\n",
        "import importlib\nunknown.getattr(importlib, 'import_module')('identity')\n",
        "import sys\nunknown.getattr(sys, 'modules')['identity'] = object()\n",
    ],
)
def test_c33_preserves_benign_and_unknown_getattr_receivers(
    tmp_path: Path,
    source: str,
) -> None:
    """Qualified lookup recognition is limited to known builtins receivers."""
    source_directory = tmp_path / "loaded_runtime_cache"
    source_directory.mkdir()
    (source_directory / "benign.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(source_directory)


@pytest.mark.parametrize(
    "source",
    [
        "import builtins\ngetattr(builtins, '__import__')('identity')\n",
        "import importlib\nload = getattr(importlib, 'import_module')\nload('identity')\n",
        "import sys\ngetattr(sys, 'modules')['identity'] = object()\n",
    ],
)
def test_c33_preserves_bare_getattr_detection(tmp_path: Path, source: str) -> None:
    """Existing bare getattr behavior remains part of the bounded contract."""
    source_directory = tmp_path / "loaded_runtime_cache"
    source_directory.mkdir()
    (source_directory / "bypass.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(source_directory)


def test_c31_paired_destructuring_preserves_alignment_and_ignores_attributes() -> None:
    """Nested literal pairing retains only corresponding simple-name aliases."""
    modules, callables = _import_aliases(
        ast.parse(
            "import importlib\nimport builtins\n"
            "[ordinary, (load, module)] = [len, (importlib.import_module, builtins)]\n"
            "holder.loader, sibling = len, importlib.import_module\n"
            "ignored, holder.other = len, importlib.import_module\n",
        ),
    )

    assert callables.get("load") == "importlib.import_module"
    assert callables.get("sibling") == "importlib.import_module"
    assert modules.get("module") == "builtins"
    assert not {"ordinary", "ignored", "holder"} & (modules.keys() | callables.keys())


def test_c31_miss_terminates_at_labelled_future_integration_boundary() -> None:
    """Miss points to an external future integration boundary, not a runtime BC."""
    architecture = Path(__file__).parents[1] / "docs" / "architecture" / "business-capability"
    scene = (architecture / "scene.js").read_text(encoding="utf-8")
    miss_edges = re.findall(
        r"\{ from: 'reuse-decision', to: '([^']+)',[^\n]*t: '([^']*miss[^']*)'[^\n]*\}",
        scene,
        flags=re.IGNORECASE,
    )

    assert len(miss_edges) == 1
    target, label = miss_edges[0]
    assert target not in {"runtime-cache", "runtime-registry", "execution", "runtime-preparation"}
    assert "future integration" in label.casefold()
    boxes = scene.split("const BOXES = [", 1)[1].split("\n];", 1)[0]
    target_box = re.search(
        r"\{ id: '" + re.escape(target) + r"',.*?(?=\n  \{ id:|\Z)",
        boxes,
        re.DOTALL,
    )
    assert target_box is not None
    assert "future integration" in target_box.group().casefold()


def test_c31_architecture_inline_scene_matches_source() -> None:
    """The standalone viewer embeds exactly the committed scene recipe."""
    architecture = Path(__file__).parents[1] / "docs" / "architecture" / "business-capability"
    scene = (architecture / "scene.js").read_text(encoding="utf-8")
    viewer = (architecture / "index.html").read_text(encoding="utf-8")

    assert scene.strip() in viewer


@pytest.mark.parametrize(
    "source",
    [
        "import builtins\nbuiltins.__dict__['__import__']('identity')\n",
        "import importlib\nimportlib.__dict__['import_module']('identity')\n",
        "import importlib as il\nil.__dict__['__import__']('identity')\n",
        "import builtins as bi\nmodule = bi\nmodule.__dict__['__import__']('identity')\n",
        "import importlib\nload = importlib.__dict__['import_module']\nload('identity')\n",
        "import builtins\nexecutor.submit(builtins.__dict__['__import__'], 'identity')\n",
    ],
)
def test_c47_rejects_known_namespace_import_callable_use(tmp_path: Path, source: str) -> None:
    """Direct literal namespace lookup retains known forbidden callable use."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "namespace.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        "import importlib\nimportlib.import_module.__call__('identity')\n",
        "__import__.__call__('identity')\n",
        "from importlib import import_module as load\nload.__call__('identity')\n",
        "import builtins\nload = builtins.__import__\nload.__call__('identity')\n",
        "import importlib\ninvoke = importlib.import_module.__call__\ninvoke('identity')\n",
        "import importlib\nexecutor.submit(importlib.import_module.__call__, 'identity')\n",
    ],
)
def test_c47_rejects_known_forbidden_callable_dunder_call_use(tmp_path: Path, source: str) -> None:
    """Only known forbidden import callables confer forbidden __call__ use."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "call.py").write_text(source, encoding="utf-8")

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    ("branches", "operation"),
    [
        ("builtins if enabled else importlib", "loader.import_module('identity')"),
        ("importlib if enabled else builtins", "loader.import_module('identity')"),
        ("importlib if enabled else sys", "loader.modules['identity'] = object()"),
        ("sys if enabled else importlib", "loader.modules['identity'] = object()"),
        ("unknown if enabled else importlib", "loader.import_module('identity')"),
        ("importlib if enabled else unknown", "loader.import_module('identity')"),
        ("builtins if enabled else unknown", "loader.__import__('identity')"),
        ("unknown if enabled else builtins", "loader.__import__('identity')"),
    ],
)
def test_c47_rejects_use_of_any_known_if_expression_module_alternative(
    tmp_path: Path,
    branches: str,
    operation: str,
) -> None:
    """Conditional module alternatives preserve existential forbidden use."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "conditional.py").write_text(
        f"import builtins\nimport importlib\nimport sys\nloader = {branches}\n{operation}\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize("loop", ["for", "async for"])
@pytest.mark.parametrize(
    "target",
    ["{name}", "({name}, other)", "[other, {name}]", "(other, *{name})"],
)
def test_c47_rejects_foreign_semantic_loop_target_names(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    loop: str,
    target: str,
) -> None:
    """Loop target syntax establishes local names without iterable inference."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "loop.py").write_text(
        f"async def ordinary():\n    {loop} {target.format(name=foreign_name)} in values:\n"
        "        pass\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize(
    "source",
    [
        "import helpers as {name}\n",
        "from helpers import Factory as {name}\n",
        "import {name}\n",
        "import {name}.helpers\n",
        "from helpers import {name}\n",
    ],
)
def test_c47_rejects_foreign_semantic_local_import_binding(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    source: str,
) -> None:
    """Import ownership follows Python local binding rather than source provenance."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "local_import.py").write_text(source.format(name=foreign_name), encoding="utf-8")

    assert _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize("context", ["with", "async with"])
@pytest.mark.parametrize(
    "target",
    ["{name}", "({name}, other)", "[other, {name}]", "(other, *{name})"],
)
def test_c47_rejects_foreign_semantic_context_target_names(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    context: str,
    target: str,
) -> None:
    """Context-manager targets use syntactic ownership, never returned-value evaluation."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "context.py").write_text(
        f"async def ordinary():\n    {context} factory() as {target.format(name=foreign_name)}:\n"
        "        pass\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(directory, foreign_name)


@pytest.mark.parametrize(
    "source",
    [
        "import builtins\nload = builtins.__dict__['__import__']\n",
        "import importlib\nload = importlib.import_module.__call__\n",
        "import builtins\nbuiltins.__dict__['len']('identity')\n",
        "unknown.__dict__['__import__']('identity')\n",
        "import builtins\nbuiltins.__dict__[key]('identity')\n",
        "ordinary.__call__('identity')\n",
        "import importlib\nimportlib.ordinary.__call__('identity')\n",
        "import builtins\nbuiltins.len.__call__('identity')\n",
        "import importlib\nimport builtins\nloader = builtins if enabled else importlib\n",
        "loader = ordinary if enabled else unknown\nloader.import_module('identity')\n",
        "import builtins\nloader = builtins if enabled else unknown\nloader.len('identity')\n",
        "import importlib\ngetattr(importlib, 'import_module', None)('identity')\n",
        "[load('identity') for load in (__import__,)]\n",
    ],
)
def test_c47_preserves_unused_ordinary_unknown_and_locked_callable_controls(
    tmp_path: Path,
    source: str,
) -> None:
    """New forms do not reject possession or expand locked alias grammar."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "controls.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    ("bc", "foreign_name"),
    [("loaded_runtime_cache", "ModelIdentity"), ("identity", "RuntimeReuseKey")],
)
@pytest.mark.parametrize(
    "source",
    [
        "for holder.{name} in values:\n    pass\n",
        "for ordinary in values:\n    pass\n",
        "async def ordinary():\n    async for holder.{name} in values:\n        pass\n",
        "with factory() as holder.{name}:\n    pass\n",
        "with factory():\n    pass\n",
        "with factory() as ordinary:\n    pass\n",
        "async def ordinary():\n    async with factory() as holder.{name}:\n        pass\n",
        "async def ordinary():\n    async with factory():\n        pass\n",
        "import helpers.{name}\n",
        "from helpers import Factory as ordinary\n",
        "label = '{name}'\n",
    ],
)
def test_c47_preserves_benign_semantic_targets_and_local_import_names(
    tmp_path: Path,
    bc: str,
    foreign_name: str,
    source: str,
) -> None:
    """Attribute labels, strings, and ordinary local bindings do not imply ownership."""
    directory = tmp_path / bc
    directory.mkdir()
    (directory / "controls.py").write_text(source.format(name=foreign_name), encoding="utf-8")

    assert not _declares_forbidden_semantic_type(directory, foreign_name)


def test_c47_preserves_identity_source_name_import_rejection_when_renamed(tmp_path: Path) -> None:
    """Local import repair must not weaken the existing Identity source-name ban."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "renamed.py").write_text(
        "from deterministic_response_cache.identity.model_identity "
        "import ModelIdentity as ordinary\n",
        encoding="utf-8",
    )

    assert _declares_forbidden_semantic_type(directory, "ModelIdentity")


@pytest.mark.parametrize(
    ("first", "second"),
    [
        ("builtins if enabled else importlib", "b if enabled else builtins"),
        ("importlib if enabled else builtins", "b if enabled else builtins"),
        ("builtins if enabled else importlib", "builtins if enabled else b"),
        ("importlib if enabled else builtins", "builtins if enabled else b"),
    ],
)
def test_c47_rework_rejects_conditional_module_alternatives_through_plain_alias_chain(
    tmp_path: Path,
    first: str,
    second: str,
) -> None:
    """A plain alias between conditional bindings cannot erase a known module alternative."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "alias_chain.py").write_text(
        "import builtins\nimport importlib\n"
        f"a = {first}\nb = a\nloader = {second}\nloader.import_module('identity')\n",
        encoding="utf-8",
    )

    assert _uses_dynamic_import_substitution(directory)


@pytest.mark.parametrize(
    "source",
    [
        (
            "import builtins\nimport importlib\na = builtins if enabled else importlib\n"
            "b = a\nloader = b if enabled else builtins\n"
        ),
        (
            "import builtins\nimport importlib\na = importlib if enabled else builtins\n"
            "b = a\nloader = builtins if enabled else b\n"
        ),
        (
            "a = ordinary if enabled else unknown\nb = a\n"
            "loader = b if enabled else ordinary\nloader.import_module('identity')\n"
        ),
        (
            "import builtins\na = builtins if enabled else unknown\nb = a\n"
            "loader = b if enabled else builtins\nloader.len('identity')\n"
        ),
    ],
)
def test_c47_rework_preserves_unused_and_ordinary_conditional_alias_chains(
    tmp_path: Path,
    source: str,
) -> None:
    """Conditional alias-chain possession and ordinary uses remain benign."""
    directory = tmp_path / "loaded_runtime_cache"
    directory.mkdir()
    (directory / "controls.py").write_text(source, encoding="utf-8")

    assert not _uses_dynamic_import_substitution(directory)
