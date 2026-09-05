from backend.app.rag.chunker import TextChunker


def test_chunker_splits_text_into_chunks():
    text = (
        "Compressor C-101 operates at normal temperature. "
        "The maximum operating temperature is 85 C. "
        "Inspection is required above the permitted threshold. "
        "Operators must notify maintenance when abnormal conditions persist."
    )

    chunker = TextChunker(chunk_size=80, overlap=20)

    chunks = chunker.split(text)

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)


def test_chunker_preserves_all_content():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunker = TextChunker(chunk_size=10, overlap=2)

    chunks = chunker.split(text)

    reconstructed = "".join(
        chunk.replace(" ", "") for chunk in chunks
    )

    for char in text:
        assert char in reconstructed