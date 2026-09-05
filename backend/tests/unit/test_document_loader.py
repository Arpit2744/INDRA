from reportlab.pdfgen import canvas

from backend.app.rag.document_loader import DocumentLoader


def test_document_loader_can_load_text_file(tmp_path):
    file_path = tmp_path / "manual.txt"

    file_path.write_text(
        "Compressor C-101 maximum operating temperature is 85 C.",
        encoding="utf-8",
    )

    loader = DocumentLoader()

    text = loader.load(file_path)

    assert "Compressor C-101" in text
    assert "85 C" in text


def test_document_loader_can_load_pdf(tmp_path):
    file_path = tmp_path / "manual.pdf"

    pdf = canvas.Canvas(str(file_path))
    pdf.drawString(
        72,
        720,
        "Compressor C-101 maximum operating temperature is 85 C.",
    )
    pdf.save()

    loader = DocumentLoader()

    text = loader.load(file_path)

    assert "Compressor C-101" in text
    assert "85 C" in text