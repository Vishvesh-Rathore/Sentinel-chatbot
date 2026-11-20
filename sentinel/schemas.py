"""Typed data structures shared by Sentinel's pipeline components."""

from dataclasses import dataclass, field


@dataclass
class Document:
    """A source document and its basic provenance metadata."""

    doc_id: str
    text: str
    source_type: str
    source_name: str
    title: str = ""
    section: str = ""
    page_or_row: str = ""
    url_or_path: str = ""
    last_updated: str = ""
    ingested_at: str = ""
    access_groups: list[str] = field(default_factory=list)


@dataclass
class Chunk:
    """A searchable part of a document with provenance and access metadata."""

    chunk_id: str
    doc_id: str
    text: str
    source_type: str
    source_name: str
    title: str = ""
    section: str = ""
    page_or_row: str = ""
    url_or_path: str = ""
    last_updated: str = ""
    ingested_at: str = ""
    index_version: str = ""
    access_groups: list[str] = field(default_factory=list)


@dataclass
class Hit:
    """A retrieved chunk and its similarity score."""

    chunk: Chunk
    score: float


@dataclass
class Answer:
    """A final answer, its context citation numbers, and refusal status."""

    text: str
    citations: list[int] = field(default_factory=list)
    refused: bool = False
