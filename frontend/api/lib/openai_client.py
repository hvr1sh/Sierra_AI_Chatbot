"""
OpenAI API client for generating responses
"""

import os
from openai import OpenAI
from typing import Dict
from dotenv import load_dotenv


SYSTEM_PROMPT = """You are a helpful AI assistant specializing in answering questions about Sierra AI, their products, values, and opportunities.

Your knowledge comes exclusively from the provided context documents from Sierra's website. Follow these rules strictly:

1. ONLY answer based on information in the provided context
2. If the answer is not clearly supported by the context, say "I don't have enough information in my knowledge base to answer that question accurately."
3. When you provide an answer, be specific and professional
4. Cite which source you're drawing from when relevant
5. Maintain Sierra's tone: professional, clear, customer-obsessed, and helpful
6. Never make up or hallucinate information - stick to the facts provided

Remember: It's better to say you don't know than to provide inaccurate information."""


class OpenAIClient:
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"

    def generate_response(self, user_message: str, context: str) -> Dict[str, str]:
        """Generate a response using OpenAI ChatGPT"""

        prompt = f"""Context information from Sierra AI's website:

{context}

---

User question: {user_message}

Please answer the user's question based solely on the context provided above. If the context doesn't contain enough information to answer accurately, say so."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract text content
            answer = response.choices[0].message.content

            return {
                "answer": answer,
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens
                }
            }

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise


# Test the client
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    client = OpenAIClient()

    test_context = """
    [Source 1: About Sierra]
    Sierra is building the conversational AI platform for businesses.
    Founded by Bret Taylor and Clay Bavor.
    """

    test_question = "Who founded Sierra?"

    print(f"🤖 Testing OpenAI client...\n")
    print(f"Question: {test_question}\n")

    result = client.generate_response(test_question, test_context)

    print(f"Answer: {result['answer']}\n")
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")

