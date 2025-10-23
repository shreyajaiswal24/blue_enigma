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
            color: #333;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 60px 20px;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.3rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .search-section {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .search-box {
            display: flex;
            max-width: 600px;
            margin: 0 auto 30px;
            background: white;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            padding: 8px;
        }
        
        .search-input {
            flex: 1;
            border: none;
            outline: none;
            padding: 15px 25px;
            font-size: 16px;
            background: transparent;
        }
        
        .search-btn {
            background: #667eea;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .search-btn:hover {
            background: #5a67d8;
            transform: scale(1.05);
        }
        
        .search-btn svg {
            width: 20px;
            height: 20px;
            fill: white;
        }
        
        .categories {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            margin-bottom: 40px;
        }
        
        .category-chip {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 25px;
            padding: 12px 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            color: #64748b;
        }
        
        .category-chip:hover {
            border-color: #667eea;
            color: #667eea;
            transform: translateY(-2px);
        }
        
        .results-section {
            display: none;
        }
        
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }
        
        .results-title {
            font-size: 2rem;
            font-weight: 600;
            color: #2d3748;
        }
        
        .results-count {
            background: #f6ad55;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }
        
        .result-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-color: #667eea;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2d3748;
        }
        
        .card-badge {
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-city { background: #38d9a9; color: white; }
        .badge-attraction { background: #f6ad55; color: white; }
        
        .card-location {
            display: flex;
            align-items: center;
            color: #64748b;
            margin-bottom: 15px;
        }
        
        .card-location svg {
            width: 16px;
            height: 16px;
            margin-right: 8px;
            fill: #ef4444;
        }
        
        .relevance-bar {
            margin-bottom: 15px;
        }
        
        .relevance-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #64748b;
        }
        
        .progress-bar {
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: #667eea;
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        
        .card-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: #f1f5f9;
            color: #64748b;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        
        .related-section {
            margin-top: 50px;
        }
        
        .related-title {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
        }
        
        .related-title svg {
            width: 24px;
            height: 24px;
            margin-right: 10px;
            fill: #667eea;
        }
        
        .related-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .related-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #f6ad55;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .related-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        .related-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .related-card-title {
            font-weight: 600;
            color: #2d3748;
        }
        
        .related-card-subtitle {
            color: #64748b;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5rem; }
            .header p { font-size: 1.1rem; }
            .search-box { margin: 0 20px 30px; }
            .categories { padding: 0 20px; }
            .results-grid { grid-template-columns: 1fr; }
            .related-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Blue Enigma</h1>
        <p>AI-Powered Vietnam Travel Assistant</p>
    </div>
    
    <div class="container">
        <div class="search-section">
            <div class="search-box">
                <input type="text" class="search-input" id="searchInput" placeholder="Best places to visit in Hanoi" onkeypress="if(event.key==='Enter') performSearch()">
                <button class="search-btn" onclick="performSearch()">
                    <svg viewBox="0 0 24 24">
                        <path d="M8,13V17.5L15,12L8,6.5V11H2V13H8Z" />
                    </svg>
                </button>
            </div>
            
            <div class="categories">
                <div class="category-chip" onclick="quickSearch('Best places in Hanoi')">
                    🏛️ Best places in Hanoi
                </div>
                <div class="category-chip" onclick="quickSearch('Beach destinations')">
                    🏖️ Beach destinations
                </div>
                <div class="category-chip" onclick="quickSearch('Cultural attractions')">
                    🏛️ Cultural attractions
                </div>
                <div class="category-chip" onclick="quickSearch('Food experiences')">
                    🍜 Food experiences
                </div>
            </div>
        </div>
        
        <div class="results-section" id="resultsSection">
            <div class="results-header">
                <h2 class="results-title" id="resultsTitle">Results for "Search Query"</h2>
                <div class="results-count" id="resultsCount">0 places found</div>
            </div>
            
            <div class="results-grid" id="resultsGrid">
                <!-- Results will be populated here -->
            </div>
            
            <div class="related-section">
                <h3 class="related-title">
                    <svg viewBox="0 0 24 24">
                        <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z" />
                    </svg>
                    Related Places
                </h3>
                <div class="related-grid" id="relatedGrid">
                    <!-- Related places will be populated here -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const sampleRelatedPlaces = [
            { name: 'Hue', badge: 'City' },
            { name: 'Nha Trang', badge: 'City' },
            { name: 'Hoi An', badge: 'City' },
            { name: 'Mekong Delta', badge: 'City' },
            { name: 'Sapa', badge: 'City' }
        ];
        
        function quickSearch(query) {
            document.getElementById('searchInput').value = query;
            performSearch();
        }
        
        async function performSearch() {
            const input = document.getElementById('searchInput');
            const query = input.value.trim();
            if (!query) return;
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                displayResults(query, data);
                
            } catch (error) {
                console.error('Search error:', error);
            }
        }
        
        function displayResults(query, data) {
            const resultsSection = document.getElementById('resultsSection');
            const resultsTitle = document.getElementById('resultsTitle');
            const resultsCount = document.getElementById('resultsCount');
            const resultsGrid = document.getElementById('resultsGrid');
            const relatedGrid = document.getElementById('relatedGrid');
            
            resultsSection.style.display = 'block';
            resultsTitle.textContent = `Results for "${query}"`;
            
            // Simulate results based on our travel data
            const mockResults = generateMockResults(query);
            resultsCount.textContent = `${mockResults.length} places found`;
            
            // Clear and populate results
            resultsGrid.innerHTML = '';
            mockResults.forEach(result => {
                const card = createResultCard(result);
                resultsGrid.appendChild(card);
            });
            
            // Populate related places
            relatedGrid.innerHTML = '';
            sampleRelatedPlaces.forEach(place => {
                const card = createRelatedCard(place);
                relatedGrid.appendChild(card);
            });
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        function generateMockResults(query) {
            const allTravelData = [
                // Cities and Cultural Places
                { name: 'Hanoi', location: 'Northern Vietnam', relevance: 0.85, category: 'City', tags: ['culture', 'food', 'heritage', 'hanoi'], description: 'Vietnam\'s capital with rich history and culture' },
                { name: 'Ho Chi Minh City', location: 'Southern Vietnam', relevance: 0.82, category: 'City', tags: ['urban', 'history', 'markets', 'nightlife'], description: 'Vibrant metropolis and economic center' },
                { name: 'Hue Imperial City', location: 'Central Vietnam', relevance: 0.78, category: 'Attraction', tags: ['heritage', 'culture', 'imperial', 'history'], description: 'Ancient imperial capital with royal tombs' },
                { name: 'Hoi An Ancient Town', location: 'Quang Nam Province', relevance: 0.76, category: 'Attraction', tags: ['heritage', 'culture', 'lanterns', 'unesco'], description: 'UNESCO World Heritage ancient trading port' },
                
                // Beach Destinations
                { name: 'Nha Trang Beach', location: 'Khanh Hoa Province', relevance: 0.88, category: 'Beach', tags: ['beach', 'swimming', 'resort', 'coast'], description: 'Popular beach resort with clear waters' },
                { name: 'Phu Quoc Island', location: 'Kien Giang Province', relevance: 0.85, category: 'Beach', tags: ['beach', 'island', 'tropical', 'resort'], description: 'Tropical paradise with pristine beaches' },
                { name: 'Da Nang Beach', location: 'Central Vietnam', relevance: 0.80, category: 'Beach', tags: ['beach', 'modern', 'surfing', 'coast'], description: 'Modern coastal city with beautiful beaches' },
                { name: 'Mui Ne Beach', location: 'Binh Thuan Province', relevance: 0.75, category: 'Beach', tags: ['beach', 'sand-dunes', 'windsurfing', 'resort'], description: 'Beach destination famous for red sand dunes' },
                { name: 'Vung Tau Beach', location: 'Ba Ria-Vung Tau Province', relevance: 0.70, category: 'Beach', tags: ['beach', 'nearby', 'weekend', 'coast'], description: 'Popular weekend beach getaway from Ho Chi Minh City' },
                
                // Cultural Attractions
                { name: 'Temple of Literature', location: 'Hanoi', relevance: 0.82, category: 'Cultural', tags: ['culture', 'temple', 'education', 'hanoi'], description: 'Vietnam\'s first university and Confucian temple' },
                { name: 'Cu Chi Tunnels', location: 'Ho Chi Minh City', relevance: 0.79, category: 'Cultural', tags: ['culture', 'history', 'war', 'tunnels'], description: 'Historic underground tunnel network' },
                { name: 'My Son Sanctuary', location: 'Quang Nam Province', relevance: 0.77, category: 'Cultural', tags: ['culture', 'heritage', 'cham', 'ancient'], description: 'Ancient Cham temple complex' },
                { name: 'One Pillar Pagoda', location: 'Hanoi', relevance: 0.74, category: 'Cultural', tags: ['culture', 'pagoda', 'buddhist', 'hanoi'], description: 'Historic Buddhist temple in Hanoi' },
                { name: 'Cao Dai Temple', location: 'Tay Ninh Province', relevance: 0.71, category: 'Cultural', tags: ['culture', 'religion', 'unique', 'temple'], description: 'Sacred temple of Cao Daism religion' },
                
                // Food Experiences
                { name: 'Ben Thanh Market', location: 'Ho Chi Minh City', relevance: 0.84, category: 'Food', tags: ['food', 'market', 'street-food', 'shopping'], description: 'Famous market for Vietnamese street food' },
                { name: 'Dong Xuan Market', location: 'Hanoi', relevance: 0.81, category: 'Food', tags: ['food', 'market', 'local', 'hanoi'], description: 'Traditional market with authentic Vietnamese food' },
                { name: 'Pho Gia Truyen', location: 'Hanoi', relevance: 0.78, category: 'Food', tags: ['food', 'pho', 'restaurant', 'authentic'], description: 'Famous pho restaurant in Hanoi' },
                { name: 'Banh Mi 25', location: 'Hanoi', relevance: 0.75, category: 'Food', tags: ['food', 'banh-mi', 'street-food', 'hanoi'], description: 'Legendary banh mi sandwich shop' },
                { name: 'Saigon Street Food Tour', location: 'Ho Chi Minh City', relevance: 0.72, category: 'Food', tags: ['food', 'tour', 'street-food', 'experience'], description: 'Guided street food exploration tour' },
                
                // Natural Attractions
                { name: 'Ha Long Bay', location: 'Quang Ninh Province', relevance: 0.90, category: 'Nature', tags: ['nature', 'cruise', 'limestone', 'unesco'], description: 'UNESCO World Heritage bay with limestone islands' },
                { name: 'Sapa Rice Terraces', location: 'Lao Cai Province', relevance: 0.86, category: 'Nature', tags: ['nature', 'mountains', 'trekking', 'terraces'], description: 'Stunning mountain rice terraces' },
                { name: 'Phong Nha-Ke Bang National Park', location: 'Quang Binh Province', relevance: 0.83, category: 'Nature', tags: ['nature', 'caves', 'national-park', 'adventure'], description: 'National park famous for spectacular caves' },
                { name: 'Mekong Delta', location: 'Southern Vietnam', relevance: 0.80, category: 'Nature', tags: ['nature', 'river', 'boat-tour', 'rural'], description: 'Vast river delta with floating markets' },
                { name: 'Ba Na Hills', location: 'Da Nang', relevance: 0.77, category: 'Nature', tags: ['nature', 'mountains', 'golden-bridge', 'theme-park'], description: 'Mountain resort with famous Golden Bridge' }
            ];
            
            const queryLower = query.toLowerCase();
            let filteredResults = [];
            
            // Enhanced search logic
            if (queryLower.includes('beach') || queryLower.includes('coast') || queryLower.includes('island')) {
                filteredResults = allTravelData.filter(item => 
                    item.category === 'Beach' || 
                    item.tags.some(tag => ['beach', 'coast', 'island', 'swimming', 'resort'].includes(tag))
                );
            } else if (queryLower.includes('culture') || queryLower.includes('heritage') || queryLower.includes('temple') || queryLower.includes('cultural')) {
                filteredResults = allTravelData.filter(item => 
                    item.category === 'Cultural' || 
                    item.tags.some(tag => ['culture', 'heritage', 'temple', 'history', 'traditional'].includes(tag))
                );
            } else if (queryLower.includes('food') || queryLower.includes('eating') || queryLower.includes('restaurant') || queryLower.includes('market')) {
                filteredResults = allTravelData.filter(item => 
                    item.category === 'Food' || 
                    item.tags.some(tag => ['food', 'market', 'restaurant', 'street-food', 'pho', 'banh-mi'].includes(tag))
                );
            } else if (queryLower.includes('hanoi')) {
                filteredResults = allTravelData.filter(item => 
                    item.location.toLowerCase().includes('hanoi') || 
                    item.tags.includes('hanoi') ||
                    item.name.toLowerCase().includes('hanoi')
                );
            } else if (queryLower.includes('nature') || queryLower.includes('mountain') || queryLower.includes('cave') || queryLower.includes('park')) {
                filteredResults = allTravelData.filter(item => 
                    item.category === 'Nature' || 
                    item.tags.some(tag => ['nature', 'mountains', 'caves', 'national-park', 'trekking'].includes(tag))
                );
            } else {
                // General search - look in names, locations, tags, and descriptions
                filteredResults = allTravelData.filter(item => 
                    item.name.toLowerCase().includes(queryLower) ||
                    item.location.toLowerCase().includes(queryLower) ||
                    item.description.toLowerCase().includes(queryLower) ||
                    item.tags.some(tag => tag.toLowerCase().includes(queryLower))
                );
            }
            
            // Sort by relevance and return top 6 results
            return filteredResults
                .sort((a, b) => b.relevance - a.relevance)
                .slice(0, 6);
        }
        
        function createResultCard(result) {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            const badgeClass = result.category === 'City' ? 'badge-city' : 'badge-attraction';
            const relevancePercent = Math.round(result.relevance * 100);
            
            card.innerHTML = `
                <div class="card-header">
                    <h3 class="card-title">${result.name}</h3>
                    <span class="card-badge ${badgeClass}">${result.category}</span>
                </div>
                <div class="card-location">
                    <svg viewBox="0 0 24 24">
                        <path d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z" />
                    </svg>
                    ${result.location}
                </div>
                <div class="relevance-bar">
                    <div class="relevance-label">
                        <span>Relevance:</span>
                        <span>${result.relevance.toFixed(3)}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${relevancePercent}%"></div>
                    </div>
                </div>
                <div class="card-tags">
                    ${result.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            `;
            
            return card;
        }
        
        function createRelatedCard(place) {
            const card = document.createElement('div');
            card.className = 'related-card';
            
            card.innerHTML = `
                <div class="related-card-header">
                    <span class="related-card-title">${place.name}</span>
                    <span class="card-badge badge-city">${place.badge}</span>
                </div>
                <div class="related-card-subtitle">Connected To</div>
            `;
            
            return card;
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
    
    # Enhanced search logic matching frontend
    if 'beach' in query_lower or 'coast' in query_lower or 'island' in query_lower:
        # Filter for beach destinations
        filtered_data = [item for item in data if 
                        item.get('category') == 'Beach' or 
                        any(tag in ['beach', 'coast', 'island', 'swimming', 'resort'] 
                            for tag in item.get('tags', []))]
    elif 'culture' in query_lower or 'heritage' in query_lower or 'temple' in query_lower or 'cultural' in query_lower:
        # Filter for cultural attractions
        filtered_data = [item for item in data if 
                        item.get('category') == 'Cultural' or 
                        any(tag in ['culture', 'heritage', 'temple', 'history', 'traditional'] 
                            for tag in item.get('tags', []))]
    elif 'food' in query_lower or 'eating' in query_lower or 'restaurant' in query_lower or 'market' in query_lower:
        # Filter for food experiences
        filtered_data = [item for item in data if 
                        item.get('category') == 'Food' or 
                        any(tag in ['food', 'market', 'restaurant', 'street-food', 'pho', 'banh-mi'] 
                            for tag in item.get('tags', []))]
    elif 'hanoi' in query_lower:
        # Filter for Hanoi-related places
        filtered_data = [item for item in data if 
                        'hanoi' in item.get('location', '').lower() or 
                        'hanoi' in item.get('tags', []) or
                        'hanoi' in item.get('name', '').lower()]
    elif 'nature' in query_lower or 'mountain' in query_lower or 'cave' in query_lower or 'park' in query_lower:
        # Filter for natural attractions
        filtered_data = [item for item in data if 
                        item.get('category') == 'Nature' or 
                        any(tag in ['nature', 'mountains', 'caves', 'national-park', 'trekking'] 
                            for tag in item.get('tags', []))]
    else:
        # General search across all fields
        filtered_data = data
    
    # Score the filtered results
    for item in filtered_data:
        score = 0
        
        # Check name (highest priority)
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
            
        # Check tags
        for tag in item.get('tags', []):
            if query_lower in tag.lower():
                score += 4
                
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

# For Vercel, the Flask app should be available at module level
# No additional handler needed - Vercel handles WSGI automatically

if __name__ == '__main__':
    app.run(debug=True)