from backend.app.models.evidence import Evidence


class KeywordRetriever:
    def __init__(self, documents: list[Evidence]):
        self.documents = documents

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Evidence]:
        query_terms = {
            term.lower()
            for term in query.split()
            if len(term) > 2
        }

        scored: list[tuple[int, Evidence]] = []

        for document in self.documents:
            content = document.content.lower()

            score = sum(
                1
                for term in query_terms
                if term in content
            )

            if score > 0:
                scored.append((score, document))

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for _, document in scored[:top_k]
        ]