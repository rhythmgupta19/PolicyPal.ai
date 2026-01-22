from scheme_database import SchemeDatabase
from scheme_retriever import SchemeRetriever
from empty_result_handler import EmptyResultHandler


def test_empty_results_provide_alternatives():
    """
    Property 8: Empty Results Provide Alternatives

    Ensures that when no schemes are found:
    - Suggested categories are returned
    - Clarifying questions are generated

    Validates: Requirement 3.4
    """
    db = SchemeDatabase("data/schemes.json")
    retriever = SchemeRetriever(db)
    empty_handler = EmptyResultHandler()

    # Intentionally ambiguous / unmatched query
    query = "xyzabc completely unknown query"
    entities = {}  # no category or demographic

    results = retriever.search(query, entities)

    # Sanity check: ensure retrieval is empty
    assert results == []

    fallback = empty_handler.handle(entities, lang="hi")

    # Property 1: Suggested categories exist
    assert "suggested_categories" in fallback
    assert len(fallback["suggested_categories"]) > 0

    # Property 2: Clarifying questions exist
    assert "clarifying_questions" in fallback
    assert len(fallback["clarifying_questions"]) > 0

    # Property 3: User-facing message is not empty
    assert "message" in fallback
    assert fallback["message"].strip() != ""
