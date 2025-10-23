#!/usr/bin/env python3
# Vercel-compatible entry point for Vietnam Travel Assistant
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__)
CORS(app)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vietnam Travel Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin: 20px 0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user-message { background-color: #007bff; color: white; text-align: right; }
        .bot-message { background-color: #f8f9fa; border-left: 4px solid #007bff; }
        input[type="text"] { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .header { text-align: center; color: #007bff; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🇻🇳 Vietnam Travel Assistant</h1>
        <p>Ask me about Vietnamese destinations, food, culture, and travel tips!</p>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot-message">
            <strong>Assistant:</strong> Hello! I'm your Vietnam Travel Assistant. Ask me about places to visit, local food, cultural sites, or any travel advice for Vietnam!
        </div>
    </div>
    
    <div style="display: flex; gap: 10px;">
        <input type="text" id="userInput" placeholder="Ask about Vietnam travel..." onkeypress="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const query = input.value.trim();
            if (!query) return;
            
            const chatContainer = document.getElementById('chatContainer');
            
            // Add user message
            chatContainer.innerHTML += `<div class="message user-message"><strong>You:</strong> ${query}</div>`;
            input.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                // Add bot response
                chatContainer.innerHTML += `<div class="message bot-message"><strong>Assistant:</strong> ${data.response}</div>`;
                
            } catch (error) {
                chatContainer.innerHTML += `<div class="message bot-message"><strong>Assistant:</strong> Sorry, I encountered an error. Please try again.</div>`;
            }
            
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
</body>
</html>
'''

# Sample travel data
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
    },
    {
        "name": "Sapa",
        "description": "Mountain town famous for terraced rice fields and ethnic minority culture",
        "location": "Lao Cai Province",
        "category": "Mountain"
    },
    {
        "name": "Phong Nha-Ke Bang National Park",
        "description": "UNESCO site with spectacular caves and underground rivers",
        "location": "Quang Binh Province",
        "category": "National Park"
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat queries"""
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Perform simple search
        search_results = simple_search(user_query, travel_data)
        
        # Generate response
        if search_results:
            response = f"Found {len(search_results)} travel recommendations for '{user_query}':\\n\\n"
            
            for i, result in enumerate(search_results, 1):
                response += f"{i}. **{result['name']}** ({result['location']})\\n"
                response += f"   {result['description']}\\n"
                response += f"   Category: {result['category']}\\n\\n"
                
            response += "Would you like more details about any of these destinations?"
        else:
            response = f"I couldn't find specific information about '{user_query}'. However, I can help you with information about popular Vietnamese destinations like Ha Long Bay, Hoi An, or Ho Chi Minh City. What would you like to know?"
        
        return jsonify({
            'response': response,
            'query': user_query,
            'results_count': len(search_results),
            'status': 'success'
        })
        
    except Exception as e:
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

# Vercel entry point
def handler(request):
    return app(request)

if __name__ == '__main__':
    app.run(debug=True)