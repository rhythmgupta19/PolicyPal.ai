def match_schemes(query: str, schemes: list, max_results: int):
    q = query.lower().split()
    results = []

    for scheme in schemes:
        name = scheme["name"].lower()
        elig = scheme.get("elig", [])

        score = 0

        for word in q:
            if word in name:
                score += 2
            if word in elig:
                score += 1

        if score > 0:
            results.append((score, scheme))

    results.sort(reverse=True, key=lambda x: x[0])

    return [s for _, s in results[:max_results]]
