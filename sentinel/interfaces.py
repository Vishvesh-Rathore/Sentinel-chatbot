"""Swappable interfaces for Sentinel's processing components."""

from abc import ABC, abstractmethod
from typing import Any

from sentinel.schemas import Chunk, Document, Hit


class Loader(ABC):
    """Load source content into documents."""

    @abstractmethod
    def load(self, source: str) -> list[Document]:
        """Load documents from a source identifier or path."""


class Chunker(ABC):
    """Split documents into retrieval-sized chunks."""

    @abstractmethod
    def split(self, doc: Document) -> list[Chunk]:
        """Split one document into chunks."""


class Embedder(ABC):
    """Convert text into embedding vectors."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""


class VectorStore(ABC):
    """Store and search embedded document chunks."""

    @abstractmethod
    def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Insert or replace chunks and their corresponding vectors."""

    @abstractmethod
    def search(
        self,
        vector: list[float],
        k: int,
        filters: dict[str, Any] | None = None,
    ) -> list[Hit]:
        """Return the closest matching chunks."""


class LLM(ABC):
    """Generate text from a prompt using a local language model."""

    @abstractmethod
    def generate(self, prompt: str, **params: Any) -> str:
        """Generate a response to a prompt."""
