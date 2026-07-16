from pathlib import Path

import yaml


class MkDocsSafeLoader(yaml.SafeLoader):
    pass


def _python_name(loader, tag_suffix, node):
    return tag_suffix


MkDocsSafeLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    _python_name,
)


def load_mkdocs_config(root: Path):
    source = (root / "mkdocs.yml").read_text(encoding="utf-8")
    return yaml.load(source, Loader=MkDocsSafeLoader)
