class BrainSynthesizer:
    def __init__(self):
        # Chat model is not available in this version of ddgs/duckduckgo_search
        pass

    def generate_search_queries(self, image_description):
        """
        Generates 3 specific search queries based on rule-based logic.
        """
        print(f"Brain: Generating queries for '{image_description}'...")
        
        queries = [
            image_description,
            f"what is {image_description}",
            f"facts about {image_description}",
            f"{image_description} explained"
        ]
        
        # Remove duplicates and limit
        return list(dict.fromkeys(queries))[:3]

    def synthesize_report(self, image_description, search_results):
        """
        Synthesizes a report by structuring the best search results.
        """
        print(f"Brain: Synthesizing report from {len(search_results)} results...")
        
        if not search_results:
            return f"I analyzed the image as '{image_description}', but I couldn't find any specific information online."

        # Create a structured markdown report from the raw data
        report = f"# Analysis of: {image_description}\n\n"
        report += "Based on my visual analysis and a deep web search, here is what I found:\n\n"
        
        # Group by source to avoid repetition
        unique_snippets = []
        seen_titles = set()
        
        for res in search_results:
            title = res.get('title', 'Unknown Source')
            body = res.get('body', '')
            href = res.get('href', '#')
            
            if title not in seen_titles and body:
                seen_titles.add(title)
                unique_snippets.append((title, body, href))

        # Construct the narrative
        for title, body, href in unique_snippets[:5]:
            report += f"### [{title}]({href})\n"
            report += f"{body}\n\n"

        report += "---\n"
        report += "*This report was compiled by aggregating live search results.*"
        
        return report

if __name__ == "__main__":
    brain = BrainSynthesizer()
    print(brain.synthesize_report("test", [{'title': 'Test Title', 'body': 'Test Body', 'href': 'http://test.com'}]))
