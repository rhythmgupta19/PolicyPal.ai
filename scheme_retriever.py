import re
from typing import List, Dict


class SchemeRetriever:
    def __init__(self, scheme_db):
        """
        :param scheme_db: Instance of SchemeDatabase
        """
        self.scheme_db = scheme_db

    def search(self, query: str, entities: dict = None) -> List[Dict]:
        """
        Search schemes using keyword overlap and simple relevance scoring.

        :param query: Normalized user query
        :param entities: Extracted entities (category, demographic)
        :return: Top 3 matching schemes
        """
        entities = entities or {}
        query_tokens = self._tokenize(query)

        scored = []
        for scheme in self.scheme_db.get_all():
            score = self._score_scheme(scheme, query_tokens, entities)
            if score > 0:
                scored.append((score, scheme))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [scheme for _, scheme in scored[:3]]

    def _score_scheme(self, scheme: Dict, query_tokens: set, entities: dict) -> int:
        """
        Compute relevance score for a scheme.
        """
        score = 0

        searchable_text = " ".join([
            scheme.get("name_hi", ""),
            scheme.get("name_en", ""),
            scheme.get("description_hi", ""),
            scheme.get("description_en", ""),
            " ".join(scheme.get("tags", []))
        ]).lower()

        scheme_tokens = self._tokenize(searchable_text)

        # Keyword overlap
        score += len(query_tokens & scheme_tokens)

        # Category bonus
        if entities.get("category") and scheme.get("category") == entities["category"]:
            score += 3

        # Demographic bonus (via tags)
        if entities.get("demographic") and entities["demographic"] in scheme.get("tags", []):
            score += 2

        return score

    def _tokenize(self, text: str) -> set:
        return set(re.findall(r"\w+", text.lower()))
