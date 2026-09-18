# Copyright (c) 2026 deterministic-response-cache contributors

"""Regression checks that Identity and Loaded Runtime Cache remain independent BCs."""

import ast
from pathlib import Path

SOURCE_ROOT = Path(__file__).parents[1] / "src" / "deterministic_response_cache"


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
    """Resolve an ``ImportFrom`` statement to its absolute module and alias targets."""
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


def test_loaded_runtime_cache_does_not_directly_import_identity_bc() -> None:
    """Loaded Runtime Cache owns local semantics and never imports Identity BC."""
    imports = _direct_imports_from(SOURCE_ROOT / "loaded_runtime_cache")

    assert not any(module == "deterministic_response_cache.identity" for module in imports)
    assert not any(
        module.startswith("deterministic_response_cache.identity.") for module in imports
    )


def test_identity_bc_does_not_directly_import_loaded_runtime_cache() -> None:
    """Identity remains the sole owner of model identity without cache coupling."""
    imports = _direct_imports_from(SOURCE_ROOT / "identity")

    assert not any(
        module == "deterministic_response_cache.loaded_runtime_cache" for module in imports
    )
    assert not any(
        module.startswith("deterministic_response_cache.loaded_runtime_cache.")
        for module in imports
    )


def test_bc_independence_import_scan_detects_package_alias_import(tmp_path: Path) -> None:
    """Package aliases cannot conceal a direct import of the Identity BC."""
    package_root = tmp_path / "deterministic_response_cache"
    source_directory = package_root / "loaded_runtime_cache"
    source_directory.mkdir(parents=True)
    (source_directory / "module.py").write_text(
        "from deterministic_response_cache import identity as identity_bc\n",
        encoding="utf-8",
    )

    imports = _direct_imports_from(source_directory, package_root=package_root)

    assert "deterministic_response_cache.identity" in imports


def test_bc_independence_import_scan_detects_relative_package_alias_import(
    tmp_path: Path,
) -> None:
    """Relative package aliases cannot conceal a direct import of the Identity BC."""
    package_root = tmp_path / "deterministic_response_cache"
    source_directory = package_root / "loaded_runtime_cache"
    source_directory.mkdir(parents=True)
    (source_directory / "module.py").write_text(
        "from .. import identity as identity_bc\n",
        encoding="utf-8",
    )

    imports = _direct_imports_from(source_directory, package_root=package_root)

    assert "deterministic_response_cache.identity" in imports
