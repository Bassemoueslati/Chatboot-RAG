from sentence_transformers import SentenceTransformer
import faiss
import pickle

def main():
    # Load documents
    with open('documents.txt', 'r', encoding='utf-8') as f:
        documents = f.readlines()
    documents = [doc.strip() for doc in documents if doc.strip()]

    # Load model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings
    embeddings = model.encode(documents, show_progress_bar=True)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index and model
    faiss.write_index(index, 'models/faiss_index.idx')
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/documents.pkl', 'wb') as f:
        pickle.dump(documents, f)

    print(f"Indexed {len(documents)} documents.")

if __name__ == "__main__":
    main()
