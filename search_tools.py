tools = [
    {
        "type": "function",
        "function": {
            "name": "search_duckduckgo",
            "description": "Perform a web search using DuckDuckGo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up online.",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

def search_duckduckgo(query):
    """Search DuckDuckGo and return the top results as a list of dicts with title, url, and snippet."""
    results = ["The weather in Tokyo is sunny."]
    return results