"""
Flask API server for Sierra AI chatbot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from rag.retrieval import Retriever
from rag.openai_client import OpenAIClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize RAG components
retriever = None
openai_client = None
is_ready = False


def initialize_rag():
    """Initialize RAG system"""
    global retriever, openai_client, is_ready

    print("\n🚀 Initializing Sierra AI Chatbot API...\n")

    try:
        # Initialize retriever
        retriever = Retriever()
        retriever.initialize()
        print("✓ Initialized ChromaDB")

        # Initialize OpenAI client
        openai_client = OpenAIClient()
        print(f"✓ OpenAI client initialized (model: {openai_client.model})")

        is_ready = True
        print("\n✅ System ready!\n")

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}\n")
        is_ready = False


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ready' if is_ready else 'initializing',
        'message': 'Sierra AI Chatbot API' if is_ready else 'System is initializing...'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    if not is_ready:
        return jsonify({
            'error': 'System is still initializing. Please try again in a moment.'
        }), 503

    try:
        # Get user message
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'error': 'Message is required'
            }), 400

        print(f"\n📩 Query: {user_message}")

        # Retrieve relevant documents
        top_k = data.get('top_k', 5)
        relevant_docs = retriever.retrieve(user_message, top_k=top_k)

        print(f"📚 Retrieved {len(relevant_docs)} relevant chunks")

        if not relevant_docs:
            return jsonify({
                'answer': "I don't have any relevant information in my knowledge base to answer this question. My knowledge is limited to Sierra AI's website content.",
                'sources': []
            })

        # Format context
        context = retriever.format_context(relevant_docs)

        # Generate response with OpenAI
        print("🤖 Generating response with OpenAI...")
        result = openai_client.generate_response(user_message, context)

        # Extract unique sources
        sources = retriever.get_unique_sources(relevant_docs)

        print(f"✓ Response generated ({result['usage']['output_tokens']} tokens)\n")

        return jsonify({
            'answer': result['answer'],
            'sources': sources,
            'usage': result['usage']
        })

    except Exception as e:
        print(f"❌ Error in /api/chat: {e}\n")
        return jsonify({
            'error': 'Failed to generate response',
            'details': str(e)
        }), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Sierra AI Chatbot API',
        'status': 'ready' if is_ready else 'initializing',
        'endpoints': {
            'health': '/api/health',
            'chat': '/api/chat (POST)'
        }
    })


if __name__ == '__main__':
    # Initialize RAG system
    initialize_rag()

    # Start Flask server
    port = int(os.getenv('PORT', 5000))
    print(f"🌟 Starting Flask server on http://localhost:{port}\n")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
