from pathlib import Path

from pypdf import PdfReader


class DocumentLoader:
    def load(self, file_path: str | Path) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {path}"
            )

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return path.read_text(encoding="utf-8")

        if suffix == ".pdf":
            reader = PdfReader(str(path))

            pages = []
            for page in reader.pages:
                text = page.extract_text() or ""
                pages.append(text)

            return "\n".join(pages).strip()

        raise ValueError(
            f"Unsupported document type: {suffix}"
        )