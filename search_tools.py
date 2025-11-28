import requests
from ddgs import DDGS
import mlflow

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

@mlflow.trace(span_type="RETRIEVER")
def search_duckduckgo(query):
    """Search DuckDuckGo and return the top results as a list of dicts with content key.
    This format is required for RetrievalGroundedness evaluation in Databricks."""
    
    results = DDGS().text(query, max_results=5)
    
    # Format results as list of dicts with "content" key for RetrievalGroundedness
    formatted_results = []
    for item in results:
        # Extract content from the result
        content = item.get("body", "") or item.get("snippet", "") or str(item)
        doc = {
            "content": content
        }
        # Preserve metadata
        if "title" in item:
            doc["title"] = item["title"]
        if "href" in item:
            doc["url"] = item["href"]
        formatted_results.append(doc)
    
    return formatted_results

if __name__ == "__main__":
    results = search_duckduckgo("What is the weather in Tokyo?")
    print(results)