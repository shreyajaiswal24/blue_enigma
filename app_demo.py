#!/usr/bin/env python3
# Demo Flask App for Vietnam Travel Assistant (Loom Video)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app)

print("🚀 Initializing Vietnam Travel Assistant Demo...")

# Load sample data for demo
try:
    with open('vietnam_travel_dataset.json', 'r', encoding='utf-8') as f:
        travel_data = json.load(f)
    print(f"✅ Loaded {len(travel_data)} travel locations")
except Exception as e:
    print(f"⚠️ Using mock data: {e}")
    travel_data = [
        {
            "name": "Ha Long Bay",
            "description": "UNESCO World Heritage site famous for its emerald waters and limestone islands",
            "location": "Quang Ninh Province",
            "category": "Natural Wonder"
        },
        {
            "name": "Hoi An Ancient Town", 
            "description": "Historic trading port with beautiful architecture and lantern festivals",
            "location": "Quang Nam Province",
            "category": "Cultural Heritage"
        },
        {
            "name": "Ho Chi Minh City",
            "description": "Vibrant metropolis known for its French colonial architecture and street food",
            "location": "South Vietnam",
            "category": "City"
        }
    ]

def simple_search(query, data):
    """Simple keyword-based search for demo purposes"""
    query_lower = query.lower()
    results = []
    
    for item in data:
        score = 0
        
        # Check name
        if query_lower in item.get('name', '').lower():
            score += 10
            
        # Check description
        if query_lower in item.get('description', '').lower():
            score += 5
            
        # Check location
        if query_lower in item.get('location', '').lower():
            score += 3
            
        # Check category
        if query_lower in item.get('category', '').lower():
            score += 2
            
        if score > 0:
            item_copy = item.copy()
            item_copy['relevance_score'] = score
            results.append(item_copy)
    
    # Sort by relevance score
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results[:5]  # Return top 5 results

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat queries"""
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        print(f"🔍 Processing query: {user_query}")
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Perform simple search
        search_results = simple_search(user_query, travel_data)
        
        # Generate response
        if search_results:
            response = f"Found {len(search_results)} travel recommendations for '{user_query}':\n\n"
            
            for i, result in enumerate(search_results, 1):
                response += f"{i}. **{result['name']}** ({result['location']})\n"
                response += f"   {result['description']}\n"
                response += f"   Category: {result['category']}\n\n"
                
            response += "Would you like more details about any of these destinations?"
        else:
            response = f"I couldn't find specific information about '{user_query}'. However, I can help you with information about popular Vietnamese destinations like Ha Long Bay, Hoi An, or Ho Chi Minh City. What would you like to know?"
        
        return jsonify({
            'response': response,
            'query': user_query,
            'results_count': len(search_results),
            'processing_time': '0.5s',
            'status': 'success'
        })
        
    except Exception as e:
        print(f"❌ Error processing chat: {e}")
        return jsonify({
            'error': 'Sorry, I encountered an error processing your request. Please try again.',
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Vietnam Travel Assistant',
        'data_loaded': len(travel_data),
        'timestamp': time.time()
    })

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Get all available destinations"""
    return jsonify({
        'destinations': travel_data,
        'total_count': len(travel_data)
    })

# For Vercel deployment
handler = app

if __name__ == '__main__':
    print("🌟 Vietnam Travel Assistant Demo is ready!")
    print("📱 Access the web interface at: http://localhost:5000")
    print("🔍 Try searching for: 'bay', 'ancient town', 'food', 'heritage'")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)