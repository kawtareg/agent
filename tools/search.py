from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 3) -> str:
    """Search for query on the internet"""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            output = ""
            for i, result in enumerate(results):
                output += f"{i} {result['title']}:  {result['body']}. Source: {result['href']}\n\n"
            return output
    except Exception as e:
        return f"Error: could not search for '{query}': {e}"