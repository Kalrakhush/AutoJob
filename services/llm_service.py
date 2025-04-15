# services/llm_services.py
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv(override=True)

# Import configuration from your config file (assumed to be named config.py)
try:
    from config import GEMINI_API_KEY, SERPAPI_API_KEY  # Additional config values if needed
except ImportError:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-gemini-api-key")

# Placeholder for Gemini embedding plugin: assumes your embedding endpoint accepts a JSON POST request.
class GeminiEmbeddingPlugin:
    def __init__(self, model, deployment_name, api_key, endpoint):
        self.model = model
        self.deployment_name = deployment_name
        self.api_key = api_key
        self.endpoint = endpoint

    def embed(self, text):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "deployment": self.deployment_name,
            "text": text
        }
        try:
            response = requests.post(self.endpoint, json=data, headers=headers)
            response.raise_for_status()
            embedding = response.json().get("embedding")
            return embedding
        except Exception as e:
            print("Error using Gemini embedding:", e)
            return None

# Fallback embedding using Hugging Face's SentenceTransformers
class HuggingFaceEmbeddingPlugin:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        return self.model.encode(text, convert_to_tensor=True)

class LLMService:
    def __init__(self):
        """
        Initialize the LLM service using environment variables and default settings.
        The default parameters can be updated as needed.
        """
        self.api_key = GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        # Default LLM settings: you can add more parameters or load them from your config file if needed
        self.model = "models/chat-bison-001"
        self.temperature = 0.3
        self.max_tokens = 1000
        self.system_prompt = (
            "Strictly avoid using sensitive, jailbreak, hate or offensive language."
        )

        # Embedding-related settings
        self.gemini_embedding_endpoint = os.getenv("GEMINI_EMBEDDING_ENDPOINT")
        self.embedding_model = "models/embedding-gemini"
        self.embedding_deployment = "gemini-embedding-deployment"

        self.initialize_llm()
        self.initialize_embedding()

    def initialize_llm(self):
        """
        Configure the Gemini LLM using the google.generativeai library.
        Reference: https://developers.google.com/generativeai
        """
        genai.configure(api_key=self.api_key)
        # If the API offers additional endpoint settings, include them as needed.

    def generate_response(self, prompt):
        """
        Generate a text response using the Gemini LLM.
        Combines the system prompt with the user prompt.
        """
        full_prompt = f"{self.system_prompt}\n{prompt}"
        response = genai.generate_text(
            model=self.model,
            prompt=full_prompt,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens
        )
        if response and response.result:
            return response.result
        else:
            return "No response generated."

    def initialize_embedding(self):
        """
        Initialize embeddings using Gemini if the endpoint is available,
        otherwise fallback to Hugging Face embeddings.
        """
        if self.gemini_embedding_endpoint:
            self.embedding = GeminiEmbeddingPlugin(
                model=self.embedding_model,
                deployment_name=self.embedding_deployment,
                api_key=self.api_key,
                endpoint=self.gemini_embedding_endpoint
            )
            # Test the Gemini embedding functionality with a simple input.
            test_emb = self.embedding.embed("test")
            if test_emb is None:
                print("Gemini embedding failed; switching to Hugging Face.")
                self.embedding = HuggingFaceEmbeddingPlugin()
            else:
                print("Using Gemini embedding service.")
        else:
            self.embedding = HuggingFaceEmbeddingPlugin()
            print("GEMINI_EMBEDDING_ENDPOINT not set; using Hugging Face embeddings.")

    def get_llm(self):
        """
        Return configuration and parameters for the Gemini LLM.
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt
        }

    def get_embedding(self):
        """
        Return the current embedding instance (Gemini or Hugging Face).
        """
        return self.embedding

# Example usage:
if __name__ == "__main__":
    service = LLMService()
    response = service.generate_response("What is the capital of France?")
    print("LLM Response:", response)
    embedding = service.get_embedding().embed("This is a sample sentence for generating embeddings.")
    print("Embedding:", embedding)
