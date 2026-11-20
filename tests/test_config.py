"""Tests for Sentinel configuration loading."""

import pytest
import yaml

from sentinel.config import load_config


def test_load_config_reads_yaml_mapping(tmp_path):
    config_path = tmp_path / "sentinel.yaml"
    config_path.write_text("retrieval:\n  top_k: 5\n", encoding="utf-8")

    assert load_config(config_path) == {"retrieval": {"top_k": 5}}


@pytest.mark.parametrize("contents", ["", "- item", "null"])
def test_load_config_rejects_non_mapping_root(tmp_path, contents):
    config_path = tmp_path / "sentinel.yaml"
    config_path.write_text(contents, encoding="utf-8")

    with pytest.raises(ValueError, match="root.*mapping"):
        load_config(config_path)


def test_load_config_surfaces_invalid_yaml(tmp_path):
    config_path = tmp_path / "sentinel.yaml"
    config_path.write_text("retrieval: [", encoding="utf-8")

    with pytest.raises(yaml.YAMLError):
        load_config(config_path)
