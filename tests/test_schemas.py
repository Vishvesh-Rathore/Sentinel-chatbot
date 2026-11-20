"""Tests for Sentinel's shared data schemas."""

from sentinel.schemas import Answer, Chunk, Document, Hit


def test_document_and_chunk_default_access_groups_are_independent():
    first = Document("doc-1", "one", "text", "source")
    second = Document("doc-2", "two", "text", "source")
    chunk = Chunk("chunk-1", first.doc_id, first.text, "text", "source")

    first.access_groups.append("finance")

    assert second.access_groups == []
    assert chunk.access_groups == []


def test_hit_and_answer_retain_payload():
    chunk = Chunk("chunk-1", "doc-1", "evidence", "text", "source")
    hit = Hit(chunk=chunk, score=0.87)
    answer = Answer(text="The answer [1].", citations=[1])

    assert hit.chunk is chunk
    assert hit.score == 0.87
    assert answer.citations == [1]
    assert answer.refused is False
