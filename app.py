import os
from flask import Flask, render_template, request, jsonify
from image_analyzer import ImageAnalyzer
from web_searcher import WebSearcher
from brain_synthesizer import BrainSynthesizer
import tempfile

app = Flask(__name__)

# Initialize AI components
try:
    analyzer = ImageAnalyzer()
    searcher = WebSearcher()
    brain = BrainSynthesizer()
    print("AI Components Initialized Successfully")
except Exception as e:
    print(f"Error initializing AI components: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        # 1. Analyze Image
        description = analyzer.analyze(temp_path)
        
        # 2. Generate Search Queries
        queries = brain.generate_search_queries(description)
        
        # 3. Deep Search (Run all queries)
        all_results = []
        seen_urls = set()
        
        for q in queries:
            results = searcher.search(q, max_results=3)
            for res in results:
                if res['href'] not in seen_urls:
                    all_results.append(res)
                    seen_urls.add(res['href'])
        
        # 4. Synthesize Report
        report = brain.synthesize_report(description, all_results)
        
        # Cleanup
        os.remove(temp_path)

        return jsonify({
            'description': description,
            'queries': queries,
            'report': report,
            'results': all_results[:5] # Send top 5 sources back
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
