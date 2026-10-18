def unique_sources(results: list[dict]) -> list[dict]:
    """
    Keep only the highest-ranked result from each source.
    """

    seen_sources = set()
    unique_results = []

    for result in results:
        source = result["metadata"]["source"]

        if source not in seen_sources:
            seen_sources.add(source)
            unique_results.append(result)

    return unique_results