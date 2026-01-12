import faiss
import pickle
import numpy as np
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class RAGChatbot:
    def __init__(self):
        self.index = faiss.read_index('models/faiss_index.idx')
        with open('models/model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open('models/documents.pkl', 'rb') as f:
            self.documents = pickle.load(f)
        self.llm = OllamaLLM(model="gemma2:2b")

    def retrieve(self, query, k=2):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        retrieved_docs = [self.documents[i] for i in indices[0]]
        return retrieved_docs

    def generate_response(self, query, profile, retrieved_docs):
        context = "\n".join(retrieved_docs)
        prompt = f"""
        You are a professional gym exercise and diet chatbot. Use the following context to provide personalized advice.

        User Profile: {profile}
        User Query: {query}

        Context:
        {context}

        Provide a precise, professional response covering diet, exercises, and health aspects as relevant.
        """
        response = self.llm.invoke(prompt)
        return response

def get_response(query, profile, conversation=None):
    chatbot = RAGChatbot()
    retrieved_docs = chatbot.retrieve(query + " " + profile)
    response = chatbot.generate_response(query, profile, retrieved_docs)
    return response
