# Gym Exercise and Diet Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that provides personalized gym exercise and diet recommendations using Streamlit, FAISS, Sentence Transformers, and Ollama LLM.

## Features

- **Personalized Recommendations**: Takes user profile (age, gender, weight, height, BMI) into account for tailored advice
- **RAG Architecture**: Uses FAISS for efficient document retrieval and Ollama LLM for response generation
- **Interactive UI**: Built with Streamlit for easy web-based interaction
- **Conversation History**: Maintains chat history and allows archiving conversations
- **Data-Driven**: Trained on multiple datasets including gym exercises, diet recommendations, and obesity data
- **Docker Support**: Containerized application with Dockerfile and docker-compose
- **Kubernetes Ready**: Kubernetes manifests for deployment

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Gemma2:2b model pulled in Ollama (`ollama pull gemma2:2b`)
- Docker (for containerized deployment)
- Kubernetes (for K8s deployment)

## Installation

### Local Installation

1. **Clone or download the project files** to your local machine.

2. **Create a virtual environment** (recommended):
   
```
bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
```

3. **Install required Python packages**:
   
```
bash
   pip install streamlit faiss-cpu sentence-transformers langchain-ollama numpy
   
```

### Docker Installation

1. **Build the Docker image**:
   
```
bash
   docker build -t chatboot-rag:latest .
   
```

2. **Run the container**:
   
```
bash
   docker run -p 8501:8501 -e OLLAMA_HOST=http://host.docker.internal:11434 chatboot-rag:latest
   
```

### Docker Compose Installation

Run with docker-compose:
```
bash
docker-compose up -d
```

The application will be available at `http://localhost:8501`

## Setup

1. **Process the data** (if not already done):
   
```
bash
   python data_processor.py
   
```
   This script processes the CSV datasets and creates `documents.txt` with processed text data.

2. **Build the FAISS index**:
   
```
bash
   python rag_setup.py
   
```
   This creates the FAISS index (`faiss_index.idx`), saves the SentenceTransformer model (`model.pkl`), and documents (`documents.pkl`) for efficient retrieval.

3. **Ensure Ollama is running** and the model is available:
   
```
bash
   ollama pull gemma2:2b
   ollama serve  # If not already running
   
```

## Running the Chatbot

### Local Mode
Start the Streamlit application:
```
bash
streamlit run app.py
```

The chatbot will be accessible at `http://localhost:8501` in your web browser.

### Docker Mode
```
bash
docker-compose up -d
```

### Kubernetes Mode
```
bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Kubernetes Deployment

The project includes Kubernetes manifests in the `k8s/` directory:

- **namespace.yaml**: Creates the `chatboot-rag` namespace
- **deployment.yaml**: Defines the deployment with resource limits
- **service.yaml**: Exposes the application via LoadBalancer
- **ingress.yaml**: Optional ingress for external access

### Deploy to Kubernetes

```
bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n chatboot-rag
kubectl get svc -n chatboot-rag

# View logs
kubectl logs -n chatboot-rag -l app=chatboot-rag
```

## Usage

1. **Enter User Profile**: Use the sidebar to input your age, gender, weight, and height. The BMI is automatically calculated.

2. **Chat Interface**: Type your query in the text input field (e.g., "What exercises should I do for weight loss?" or "Suggest a diet plan").

3. **Submit Query**: Click the "Submit" button to get a personalized response based on your profile and the retrieved context.

4. **Conversation History**: All messages are displayed in the chat interface. You can archive the conversation by clicking "Archive Conversation" (saves as JSON file with timestamp).

## Data Sources

The chatbot uses the following datasets:
- `dataset/diet_recommendations_dataset.csv`: Diet and nutrition recommendations
- `dataset/gym_members_exercise_tracking_synthetic_data.csv`: Synthetic gym member exercise data
- `dataset/megaGymDataset.csv`: Comprehensive gym exercise database
- `dataset/Nutrition__Physical_Activity__and_Obesity.csv`: CDC data on nutrition, physical activity, and obesity

## Architecture

- **Frontend**: Streamlit web application (`app.py`)
- **Backend Logic**: RAG chatbot implementation (`chatbot.py`)
- **Data Processing**: Converts CSV data to text documents (`data_processor.py`)
- **Index Building**: Creates FAISS vector index for retrieval (`rag_setup.py`)
- **Retrieval**: FAISS index with SentenceTransformer embeddings
- **Generation**: Ollama Gemma2:2b model for response generation
- **Containerization**: Docker and Docker Compose
- **Orchestration**: Kubernetes manifests

## Troubleshooting

- **Ollama not responding**: Ensure Ollama is installed, the model is pulled, and the service is running (`ollama serve`).
- **Import errors**: Verify all required packages are installed.
- **Index not found**: Run `rag_setup.py` to build the FAISS index.
- **Documents not found**: Run `data_processor.py` to process the CSV files.
- **Docker issues**: Ensure Docker daemon is running and ports are available.
- **Kubernetes issues**: Check kubectl configuration and cluster status.

## Contributing

Feel free to contribute by:
- Adding more datasets
- Improving the prompt engineering
- Enhancing the UI/UX
- Optimizing performance
- Adding more Kubernetes configurations

## License

This project is for educational purposes. Please check the licenses of the datasets used.
