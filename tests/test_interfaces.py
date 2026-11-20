"""Tests for the component interface contracts."""

import inspect

import pytest

from sentinel.interfaces import Chunker, Embedder, LLM, Loader, VectorStore


@pytest.mark.parametrize(
    "interface",
    [Loader, Chunker, Embedder, VectorStore, LLM],
)
def test_interfaces_are_abstract(interface):
    assert inspect.isabstract(interface)
