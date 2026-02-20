def match_schemes(query: str, schemes: list, max_results: int):
    q = query.lower().split()
    results = []

    for scheme in schemes:
        name = (
            scheme.get("name", "")
            or scheme.get("name_hi", "")
            or scheme.get("name_en", "")
        ).lower()
        elig = (
            scheme.get("elig", [])
            or scheme.get("eligibility_hi", "")
            or scheme.get("eligibility_en", "")
        )
        elig_text = " ".join(elig) if isinstance(elig, list) else str(elig).lower()
        desc_text = (
            f"{scheme.get('description_hi', '')} {scheme.get('description_en', '')}"
        ).lower()
        tags = " ".join(scheme.get("tags", [])).lower()

        score = 0

        for word in q:
            if word in name:
                score += 2
            if word in elig_text:
                score += 1
            if word in desc_text:
                score += 1
            if word in tags:
                score += 2

        if score > 0:
            results.append((score, scheme))

    results.sort(reverse=True, key=lambda x: x[0])

    return [s for _, s in results[:max_results]]
