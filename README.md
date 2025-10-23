# Blue Enigma - Vietnam Travel Assistant

A hybrid AI chat system that combines vector search and graph database technologies to provide intelligent travel recommendations for Vietnam.

## Features

- **Hybrid Search**: Combines Pinecone vector search with Neo4j graph database
- **AI-Powered Chat**: Intelligent travel recommendations using sentence transformers
- **Web Interface**: Flask-based web application with real-time chat
- **Graph Visualization**: Interactive visualization of travel data relationships
- **RESTful API**: Web API for integration with other applications

## Tech Stack

- **Backend**: Python, Flask
- **AI/ML**: SentenceTransformers, OpenAI
- **Databases**: Neo4j (graph), Pinecone (vector)
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Vis.js, PyVis

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `config.py`:
   - Neo4j credentials
   - Pinecone API key
   - OpenAI API key (if used)

3. Load data to Neo4j:
   ```bash
   python load_to_neo4j.py
   ```

4. Upload data to Pinecone:
   ```bash
   python pinecone_upload.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Usage

- Access the web interface at `http://localhost:5000`
- Use the chat interface to ask questions about Vietnam travel
- View graph visualizations at `/visualize`

## Files

- `app.py` - Main Flask application
- `hybrid_chat.py` - Core hybrid search functionality
- `config.py` - Configuration settings
- `load_to_neo4j.py` - Data loading script for Neo4j
- `pinecone_upload.py` - Data upload script for Pinecone
- `vietnam_travel_dataset.json` - Travel dataset
- `templates/` - HTML templates
- `static/` - CSS and JavaScript assets

## Testing

Run tests using the provided test files:
- `test_chat_query.py`
- `test_connection.py`
- `test_hybrid_system.py`
- `test_web_api.py`