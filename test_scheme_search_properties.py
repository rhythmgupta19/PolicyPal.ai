from scheme_database import SchemeDatabase
from scheme_retriever import SchemeRetriever


def test_search_results_bounded_and_ranked():
    """
    Property 6: Search Results Bounded and Ranked

    Ensures:
    - No more than 3 results are returned
    - Results are ordered by relevance score (descending)

    Validates: Requirements 3.2, 3.6
    """
    db = SchemeDatabase("data/schemes.json")
    retriever = SchemeRetriever(db)

    query = "छात्र शिक्षा योजना लाभ"
    entities = {
        "category": "education",
        "demographic": "student"
    }

    results = retriever.search(query, entities)

    # Property 1: Bounded results
    assert len(results) <= 3

    # Property 2: Ranked by relevance
    # Re-score results using the retriever's scoring logic
    query_tokens = retriever._tokenize(query)

    scores = [
        retriever._score_scheme(scheme, query_tokens, entities)
        for scheme in results
    ]

    # Ensure scores are non-increasing
    assert scores == sorted(scores, reverse=True), (
        f"Results not ordered by relevance: {scores}"
    )
