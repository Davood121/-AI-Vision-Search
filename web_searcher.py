from ddgs import DDGS
import traceback

class WebSearcher:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query, max_results=5):
        """
        Searches the web for the given query with fallback strategies.
        """
        print(f"Searching for: '{query}'...")
        
        # Strategy 1: Full Query
        results = self._perform_search(query, max_results)
        if results:
            return results
            
        # Strategy 2: First 10 words (if long)
        words = query.split()
        if len(words) > 10:
            short_query = " ".join(words[:10])
            print(f"Retrying with shorter query: '{short_query}'...")
            results = self._perform_search(short_query, max_results)
            if results:
                return results

        # Strategy 3: First 5 words (Keywords)
        if len(words) > 5:
            key_query = " ".join(words[:5])
            print(f"Retrying with keywords: '{key_query}'...")
            results = self._perform_search(key_query, max_results)
            if results:
                return results

        print("No results found after retries.")
        return []

    def _perform_search(self, query, max_results):
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            if results:
                print(f"Found {len(results)} results.")
            return results
        except Exception as e:
            print(f"Search attempt failed for '{query}': {e}")
            # traceback.print_exc() # Optional: uncomment for deep debugging
            return []

if __name__ == "__main__":
    searcher = WebSearcher()
    # Test specific failed query
    q = "sad potato cartoon character stock vector illustration"
    res = searcher.search(q)
    for r in res:
        print(r['title'])
