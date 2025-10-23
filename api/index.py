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
    <title>Blue Enigma - Vietnam Travel Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f8f9fa;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .header p {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
            height: calc(100vh - 140px);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .message {
            max-width: 80%;
            animation: slideIn 0.3s ease-out;
        }
        
        .user-message {
            align-self: flex-end;
            background: #667eea;
            color: white;
            padding: 12px 20px;
            border-radius: 20px 20px 5px 20px;
            font-weight: 500;
        }
        
        .bot-message {
            align-self: flex-start;
            background: white;
            padding: 15px;
            border-radius: 20px 20px 20px 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        
        .bot-message .message-text {
            margin-bottom: 15px;
            color: #2d3748;
            font-weight: 500;
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }
        
        .result-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        
        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2d3748;
        }
        
        .card-badge {
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-city { background: #38d9a9; color: white; }
        .badge-beach { background: #4299e1; color: white; }
        .badge-cultural { background: #f6ad55; color: white; }
        .badge-food { background: #f56565; color: white; }
        .badge-nature { background: #48bb78; color: white; }
        
        .card-location {
            display: flex;
            align-items: center;
            color: #64748b;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }
        
        .card-location::before {
            content: "📍";
            margin-right: 5px;
        }
        
        .card-description {
            color: #4a5568;
            font-size: 0.9rem;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        
        .card-tags {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: #edf2f7;
            color: #4a5568;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.7rem;
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e2e8f0;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .chat-input:focus {
            border-color: #667eea;
        }
        
        .send-btn {
            background: #667eea;
            color: white;
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            background: #5a67d8;
            transform: scale(1.05);
        }
        
        .send-btn:disabled {
            background: #a0aec0;
            cursor: not-allowed;
            transform: none;
        }
        
        .quick-suggestions {
            padding: 0 20px 10px;
            background: white;
            border-top: 1px solid #e2e8f0;
        }
        
        .suggestions-list {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        
        .suggestion-chip {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 8px 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            color: #4a5568;
        }
        
        .suggestion-chip:hover {
            background: #667eea;
            color: white;
            transform: translateY(-1px);
        }
        
        .welcome-message {
            text-align: center;
            padding: 40px 20px;
            color: #64748b;
        }
        
        .welcome-title {
            font-size: 1.5rem;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @media (max-width: 768px) {
            .results-grid {
                grid-template-columns: 1fr;
            }
            .suggestions-list {
                justify-content: center;
            }
            .message {
                max-width: 90%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🇻🇳 Blue Enigma</h1>
        <p>AI-Powered Vietnam Travel Assistant</p>
    </div>
    
    <div class="chat-container">
        <div class="chat-messages" id="chatMessages">
            <div class="welcome-message">
                <h2 class="welcome-title">Welcome to Vietnam Travel Assistant!</h2>
                <p>Ask me about Vietnamese destinations, food, culture, and travel tips. Try asking about beaches, cultural sites, or specific cities like Hanoi!</p>
            </div>
        </div>
        
        <div class="quick-suggestions">
            <div class="suggestions-list">
                <div class="suggestion-chip" onclick="sendQuickMessage('Best places to visit in Hanoi')">🏛️ Best places in Hanoi</div>
                <div class="suggestion-chip" onclick="sendQuickMessage('Beach destinations in Vietnam')">🏖️ Beach destinations</div>
                <div class="suggestion-chip" onclick="sendQuickMessage('Cultural attractions')">🎭 Cultural attractions</div>
                <div class="suggestion-chip" onclick="sendQuickMessage('Food experiences')">🍜 Food experiences</div>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" 
                   class="chat-input" 
                   id="chatInput" 
                   placeholder="Ask me about Vietnam travel..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
                </svg>
            </button>
        </div>
    </div>
    
    <script>
        let isLoading = false;
        
        function sendQuickMessage(message) {
            document.getElementById('chatInput').value = message;
            sendMessage();
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const sendBtn = document.getElementById('sendBtn');
            const query = input.value.trim();
            
            if (!query || isLoading) return;
            
            // Add user message
            addUserMessage(query);
            
            // Clear input and disable button
            input.value = '';
            isLoading = true;
            sendBtn.disabled = true;
            
            // Add typing indicator
            const typingId = addTypingIndicator();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                // Remove typing indicator
                removeTypingIndicator(typingId);
                
                // Add bot response
                addBotMessage(data, query);
                
            } catch (error) {
                removeTypingIndicator(typingId);
                addBotMessage({
                    response: "Sorry, I encountered an error. Please try again.",
                    results_count: 0,
                    results: []
                });
            } finally {
                isLoading = false;
                sendBtn.disabled = false;
            }
        }
        
        function addUserMessage(message) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }
        
        function addBotMessage(data, query = '') {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot-message';
            
            let responseText = data.response;
            if (data.results_count > 0) {
                responseText = `Found ${data.results_count} great recommendations for you!`;
            }
            
            messageDiv.innerHTML = `
                <div class="message-text">${responseText}</div>
                ${data.results && data.results.length > 0 ? createResultsGrid(data.results) : ''}
            `;
            
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }
        
        function createResultsGrid(results) {
            const gridHtml = results.map(place => `
                <div class="result-card">
                    <div class="card-header">
                        <div class="card-title">${place.name}</div>
                        <div class="card-badge badge-${place.category.toLowerCase()}">${place.category}</div>
                    </div>
                    <div class="card-location">${place.location}</div>
                    <div class="card-description">${place.description}</div>
                    <div class="card-tags">
                        ${place.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                </div>
            `).join('');
            
            return `<div class="results-grid">${gridHtml}</div>`;
        }
        
        function addTypingIndicator() {
            const chatMessages = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot-message';
            typingDiv.id = 'typing-indicator';
            typingDiv.innerHTML = '<div class="message-text">Thinking...</div>';
            chatMessages.appendChild(typingDiv);
            scrollToBottom();
            return 'typing-indicator';
        }
        
        function removeTypingIndicator(id) {
            const indicator = document.getElementById(id);
            if (indicator) {
                indicator.remove();
            }
        }
        
        function scrollToBottom() {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    </script>
</body>
</html>
'''

# Enhanced travel data with multiple categories
travel_data = [
    # Cities and Cultural Places
    {
        "name": "Hanoi",
        "description": "Vietnam's capital with rich history and culture",
        "location": "Northern Vietnam",
        "category": "City",
        "tags": ["culture", "food", "heritage", "hanoi"]
    },
    {
        "name": "Ho Chi Minh City",
        "description": "Vibrant metropolis and economic center",
        "location": "Southern Vietnam", 
        "category": "City",
        "tags": ["urban", "history", "markets", "nightlife"]
    },
    {
        "name": "Hue Imperial City",
        "description": "Ancient imperial capital with royal tombs",
        "location": "Central Vietnam",
        "category": "Cultural",
        "tags": ["heritage", "culture", "imperial", "history"]
    },
    {
        "name": "Hoi An Ancient Town",
        "description": "UNESCO World Heritage ancient trading port",
        "location": "Quang Nam Province",
        "category": "Cultural",
        "tags": ["heritage", "culture", "lanterns", "unesco"]
    },
    
    # Beach Destinations
    {
        "name": "Nha Trang Beach",
        "description": "Popular beach resort with clear waters",
        "location": "Khanh Hoa Province",
        "category": "Beach",
        "tags": ["beach", "swimming", "resort", "coast"]
    },
    {
        "name": "Phu Quoc Island",
        "description": "Tropical paradise with pristine beaches",
        "location": "Kien Giang Province",
        "category": "Beach",
        "tags": ["beach", "island", "tropical", "resort"]
    },
    {
        "name": "Da Nang Beach",
        "description": "Modern coastal city with beautiful beaches",
        "location": "Central Vietnam",
        "category": "Beach",
        "tags": ["beach", "modern", "surfing", "coast"]
    },
    {
        "name": "Mui Ne Beach",
        "description": "Beach destination famous for red sand dunes",
        "location": "Binh Thuan Province",
        "category": "Beach",
        "tags": ["beach", "sand-dunes", "windsurfing", "resort"]
    },
    {
        "name": "Vung Tau Beach",
        "description": "Popular weekend beach getaway from Ho Chi Minh City",
        "location": "Ba Ria-Vung Tau Province",
        "category": "Beach",
        "tags": ["beach", "nearby", "weekend", "coast"]
    },
    
    # Cultural Attractions
    {
        "name": "Temple of Literature",
        "description": "Vietnam's first university and Confucian temple",
        "location": "Hanoi",
        "category": "Cultural",
        "tags": ["culture", "temple", "education", "hanoi"]
    },
    {
        "name": "Cu Chi Tunnels",
        "description": "Historic underground tunnel network",
        "location": "Ho Chi Minh City",
        "category": "Cultural",
        "tags": ["culture", "history", "war", "tunnels"]
    },
    {
        "name": "My Son Sanctuary",
        "description": "Ancient Cham temple complex",
        "location": "Quang Nam Province",
        "category": "Cultural",
        "tags": ["culture", "heritage", "cham", "ancient"]
    },
    
    # Food Experiences
    {
        "name": "Ben Thanh Market",
        "description": "Famous market for Vietnamese street food",
        "location": "Ho Chi Minh City",
        "category": "Food",
        "tags": ["food", "market", "street-food", "shopping"]
    },
    {
        "name": "Dong Xuan Market",
        "description": "Traditional market with authentic Vietnamese food",
        "location": "Hanoi",
        "category": "Food",
        "tags": ["food", "market", "local", "hanoi"]
    },
    {
        "name": "Pho Gia Truyen",
        "description": "Famous pho restaurant in Hanoi",
        "location": "Hanoi",
        "category": "Food",
        "tags": ["food", "pho", "restaurant", "authentic"]
    },
    
    # Natural Attractions
    {
        "name": "Ha Long Bay",
        "description": "UNESCO World Heritage bay with limestone islands",
        "location": "Quang Ninh Province",
        "category": "Nature",
        "tags": ["nature", "cruise", "limestone", "unesco"]
    },
    {
        "name": "Sapa Rice Terraces",
        "description": "Stunning mountain rice terraces",
        "location": "Lao Cai Province",
        "category": "Nature",
        "tags": ["nature", "mountains", "trekking", "terraces"]
    },
    {
        "name": "Phong Nha-Ke Bang National Park",
        "description": "National park famous for spectacular caves",
        "location": "Quang Binh Province",
        "category": "Nature",
        "tags": ["nature", "caves", "national-park", "adventure"]
    },
    {
        "name": "Mekong Delta",
        "description": "Vast river delta with floating markets",
        "location": "Southern Vietnam",
        "category": "Nature",
        "tags": ["nature", "river", "boat-tour", "rural"]
    }
]

def simple_search(query, data):
    """Enhanced search with category-specific filtering"""
    query_lower = query.lower()
    results = []
    
    # Enhanced search logic - more flexible matching
    filtered_data = []
    
    # Check for specific categories first
    if 'beach' in query_lower or 'coast' in query_lower or 'island' in query_lower:
        filtered_data = [item for item in data if 
                        item.get('category') == 'Beach' or 
                        any(tag in ['beach', 'coast', 'island', 'swimming', 'resort'] 
                            for tag in item.get('tags', []))]
    elif 'culture' in query_lower or 'heritage' in query_lower or 'temple' in query_lower or 'cultural' in query_lower:
        filtered_data = [item for item in data if 
                        item.get('category') == 'Cultural' or 
                        any(tag in ['culture', 'heritage', 'temple', 'history', 'traditional'] 
                            for tag in item.get('tags', []))]
    elif 'food' in query_lower or 'eating' in query_lower or 'restaurant' in query_lower or 'market' in query_lower:
        filtered_data = [item for item in data if 
                        item.get('category') == 'Food' or 
                        any(tag in ['food', 'market', 'restaurant', 'street-food', 'pho', 'banh-mi'] 
                            for tag in item.get('tags', []))]
    elif 'nature' in query_lower or 'mountain' in query_lower or 'cave' in query_lower or 'park' in query_lower:
        filtered_data = [item for item in data if 
                        item.get('category') == 'Nature' or 
                        any(tag in ['nature', 'mountains', 'caves', 'national-park', 'trekking'] 
                            for tag in item.get('tags', []))]
    
    # If no category match found, check for location-based searches
    if not filtered_data:
        if 'hanoi' in query_lower:
            filtered_data = [item for item in data if 
                            'hanoi' in item.get('location', '').lower() or 
                            'hanoi' in item.get('tags', []) or
                            'hanoi' in item.get('name', '').lower()]
        elif 'ho chi minh' in query_lower or 'saigon' in query_lower:
            filtered_data = [item for item in data if 
                            'ho chi minh' in item.get('location', '').lower() or 
                            'saigon' in item.get('location', '').lower() or
                            'ho chi minh' in item.get('name', '').lower()]
    
    # If still no matches, do general search
    if not filtered_data:
        filtered_data = data
    
    # Score the filtered results
    query_words = query_lower.split()
    
    for item in filtered_data:
        score = 0
        
        # Check each word in the query
        for word in query_words:
            # Skip common words
            if word in ['in', 'to', 'the', 'of', 'and', 'or', 'a', 'an', 'best', 'places']:
                continue
                
            # Check name (highest priority)
            if word in item.get('name', '').lower():
                score += 10
                
            # Check description
            if word in item.get('description', '').lower():
                score += 5
                
            # Check location
            if word in item.get('location', '').lower():
                score += 8  # Higher score for location matches
                
            # Check category
            if word in item.get('category', '').lower():
                score += 3
                
            # Check tags
            for tag in item.get('tags', []):
                if word in tag.lower():
                    score += 6
        
        # Also check for exact phrase matches (bonus points)
        if query_lower in item.get('name', '').lower():
            score += 15
        if query_lower in item.get('description', '').lower():
            score += 10
                
        if score > 0:
            item_copy = item.copy()
            item_copy['relevance_score'] = score
            results.append(item_copy)
    
    # Sort by relevance score and return top results
    results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return results[:6]  # Return top 6 results

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
        
        # Format results for frontend
        formatted_results = []
        for result in search_results:
            formatted_result = {
                'name': result['name'],
                'location': result['location'],
                'description': result['description'],
                'category': result['category'],
                'tags': result.get('tags', []),
                'relevance': round(result.get('relevance_score', 0) / 20, 3)  # Normalize to 0-1 scale
            }
            formatted_results.append(formatted_result)
        
        # Generate text response for backwards compatibility
        if search_results:
            response = f"Found {len(search_results)} travel recommendations for '{user_query}'"
        else:
            response = f"I couldn't find specific information about '{user_query}'. However, I can help you with information about popular Vietnamese destinations like Ha Long Bay, Hoi An, or Ho Chi Minh City. What would you like to know?"
        
        return jsonify({
            'response': response,
            'query': user_query,
            'results_count': len(search_results),
            'results': formatted_results,
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

# For Vercel, the Flask app should be available at module level
# No additional handler needed - Vercel handles WSGI automatically

if __name__ == '__main__':
    app.run(debug=True, port=5001)