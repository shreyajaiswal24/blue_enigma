#!/usr/bin/env python3
# Fixed Flask Web API for Vietnam Travel Assistant
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from neo4j import GraphDatabase
import config
import time
import threading

app = Flask(__name__)
CORS(app)

# Initialize AI components
print("🚀 Initializing Vietnam Travel Assistant...")
model = SentenceTransformer('all-MiniLM-L6-v2')
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)

# Neo4j driver with better connection management
driver = None
driver_lock = threading.Lock()

def get_neo4j_driver():
    """Get or create Neo4j driver with proper error handling"""
    global driver
    
    with driver_lock:
        if driver is None:
            try:
                driver = GraphDatabase.driver(
                    config.NEO4J_URI, 
                    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
                    max_connection_lifetime=300,  # 5 minutes
                    max_connection_pool_size=5,
                    connection_acquisition_timeout=30
                )
                print("✅ Neo4j driver initialized")
            except Exception as e:
                print(f"❌ Failed to create Neo4j driver: {e}")
                return None
        return driver

def safe_neo4j_query(query, parameters=None):
    """Execute Neo4j query with proper error handling and reconnection"""
    neo4j_driver = get_neo4j_driver()
    if not neo4j_driver:
        return []
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with neo4j_driver.session() as session:
                result = session.run(query, parameters or {})
                return list(result)
        except Exception as e:
            print(f"Neo4j query attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
                # Reset driver on connection errors
                if "defunct" in str(e) or "connection" in str(e).lower():
                    with driver_lock:
                        global driver
                        if driver:
                            try:
                                driver.close()
                            except:
                                pass
                            driver = None
            else:
                print(f"❌ Neo4j query failed after {max_retries} attempts")
                return []

def search_vietnam_api(query_text, top_k=5):
    """Search function for API endpoint"""
    try:
        # Get embeddings and search Pinecone
        vec = model.encode([query_text])[0].tolist()
        results = index.query(
            vector=vec, 
            top_k=top_k, 
            include_metadata=True,
            include_values=False
        )
        
        # Format results
        places = []
        node_ids = []
        
        for match in results["matches"]:
            meta = match["metadata"]
            score = match.get("score", 0)
            place = {
                "id": match["id"],
                "name": meta.get('name', 'Unknown'),
                "type": meta.get('type', 'Unknown'),
                "location": meta.get('city', 'Unknown'),
                "tags": meta.get('tags', []),
                "score": round(score, 3)
            }
            places.append(place)
            node_ids.append(match["id"])
        
        # Get graph connections with safe query
        connections = []
        for nid in node_ids[:3]:  # Top 3 only
            query = (
                "MATCH (n:Entity {id:$nid})-[r]-(m:Entity) "
                "RETURN m.name AS name, m.id AS id, type(r) AS relationship, m.type AS type "
                "LIMIT 3"
            )
            records = safe_neo4j_query(query, {"nid": nid})
            for record in records:
                connections.append({
                    "from": nid,
                    "to": record["name"],
                    "relationship": record["relationship"],
                    "type": record["type"]
                })
        
        return {
            "success": True,
            "query": query_text,
            "results": places,
            "connections": connections,
            "total_found": len(places)
        }
        
    except Exception as e:
        print(f"Search error: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query_text
        }

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for search"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"success": False, "error": "Query is required"}), 400
    
    # Add small delay to show loading effect
    time.sleep(0.5)
    
    result = search_vietnam_api(query)
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Test Neo4j connection
    neo4j_status = "connected"
    try:
        records = safe_neo4j_query("RETURN 1 as test")
        if not records:
            neo4j_status = "error"
    except:
        neo4j_status = "error"
    
    return jsonify({
        "status": "healthy",
        "components": {
            "pinecone": "connected",
            "neo4j": neo4j_status,
            "embeddings": "loaded"
        }
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        # Get Pinecone stats
        pinecone_stats = index.describe_index_stats()
        
        # Get Neo4j stats with safe query
        neo4j_count = 0
        records = safe_neo4j_query("MATCH (n:Entity) RETURN count(n) as count")
        if records:
            neo4j_count = records[0]["count"]
        
        return jsonify({
            "success": True,
            "stats": {
                "total_places": pinecone_stats.total_vector_count,
                "graph_nodes": neo4j_count,
                "embedding_model": "all-MiniLM-L6-v2",
                "vector_dimensions": 384
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.teardown_appcontext
def close_neo4j(error):
    """Clean up Neo4j connections"""
    pass  # Driver will be closed on app shutdown

if __name__ == '__main__':
    print("✅ Vietnam Travel Assistant API Ready!")
    print("🌐 Open: http://localhost:5000")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Clean up on shutdown
        if driver:
            driver.close()
            print("🔄 Neo4j driver closed")