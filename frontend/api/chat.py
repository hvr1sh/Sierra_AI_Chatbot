"""
Vercel Serverless function for chat endpoint
Handles user queries using RAG (Retrieval Augmented Generation)
File: api/chat.py
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
import logging

# Add lib directory to path (adjust pathing for Vercel structure if needed)
# In Vercel, the 'api' directory is the root context.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from lib.retrieval import Retriever
from lib.openai_client import OpenAIClient

# Initialize global instances (cold start optimization)
retriever = None
openai_client = None


def initialize():
    """Initialize RAG components"""
    global retriever, openai_client

    if retriever is None:
        chroma_path = os.path.join(os.path.dirname(__file__), 'lib', 'chroma_db')
        retriever = Retriever(chroma_path=chroma_path)
        if hasattr(retriever, 'initialize'):
            retriever.initialize()

    if openai_client is None:
        openai_client = OpenAIClient()


class handler(BaseHTTPRequestHandler):
    """Vercel built-in Python runtime handler"""

    def _set_cors(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        # Preflight
        self._set_cors(200)

    def do_POST(self):
        self.wfile.write(json.dumps({"hello": "hello"}).encode("utf-8"))
        initialize()
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(raw_body.decode("utf-8") or "{}")
        except Exception:
            print('DEBUG: Issue 1')
            self._set_cors(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON body"}).encode("utf-8"))
            return

        # 🔴 Also note: "Message" vs "message"
        user_message = (data.get("message") or "").strip()
        if not user_message:
            self._set_cors(400)
            self.wfile.write(json.dumps({"error": "Message is required"}).encode("utf-8"))
            return

        try:
            top_k = data.get("top_k", 5)

            relevant_docs = retriever.retrieve(user_message, top_k=top_k)

            if not relevant_docs:
                self._set_cors(200)
                self.wfile.write(json.dumps({
                    "answer": "I don't have any relevant information in my knowledge base to answer this question.",
                    "sources": []
                }).encode("utf-8"))
                return

            context = retriever.format_context(relevant_docs)
            result = openai_client.generate_response(user_message, context)
            sources = retriever.get_unique_sources(relevant_docs)

            self._set_cors(200)
            self.wfile.write(json.dumps({
                "answer": result["answer"],
                "sources": sources,
                "usage": result.get("usage")
            }).encode("utf-8"))

        except Exception as e:
            self._set_cors(500)
            self.wfile.write(json.dumps({
                "error": "Failed to generate response",
                "details": str(e)
            }).encode("utf-8"))
