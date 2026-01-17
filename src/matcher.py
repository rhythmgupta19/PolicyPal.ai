def match_schemes(query: str, schemes: list, max_results: int):
    """
    Very simple keyword-based matching.
    No ML. No overthinking.
    """

    q = query.lower()
    results = []

    for scheme in schemes:
        if q in scheme["name"].lower():
            results.append(scheme)

        if len(results) >= max_results:
            break

    return results
