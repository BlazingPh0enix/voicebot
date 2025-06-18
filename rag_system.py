import os
import streamlit as st
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import torch

# Load environment variables (assuming this is already done in app.py, but good for standalone testing)
from dotenv import load_dotenv
load_dotenv()

torch.classes.__path__ = []

# Set API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Please set your OPENAI_API_KEY in the .env file")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Directory for FAISS index
FAISS_INDEX_PATH = "faiss_index"
RESUME_PATH = "my_resume.txt"

def load_and_split_resume(file_path):
    """Loads the resume from a text file and splits it into chunks."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            resume_content = f.read()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(resume_content)
        return chunks
    except FileNotFoundError:
        st.error(f"Error: Resume file not found at {file_path}")
        return []
    except Exception as e:
        st.error(f"Error loading or splitting resume: {e}")
        return []

def get_vector_store():
    """
    Initializes and returns the FAISS vector store.
    If the database exists, it loads it; otherwise, it creates and persists it.
    """
    # Initialize the Sentence Transformer model for embeddings
    model_name = "all-MiniLM-L6-v2" # Or any other suitable Sentence Transformer model
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Check if the FAISS index directory exists
    if os.path.exists(FAISS_INDEX_PATH) and os.listdir(FAISS_INDEX_PATH):
        print(f"Loading existing FAISS index from {FAISS_INDEX_PATH}...")
        # When loading, we need to pass the embedding function again
        vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print(f"Creating new FAISS index and embedding resume into {FAISS_INDEX_PATH}...")
        resume_chunks = load_and_split_resume(RESUME_PATH)
        if not resume_chunks:
            st.error("Could not load resume chunks. RAG system will not function.")
            return None
        
        vector_store = FAISS.from_texts(
            texts=resume_chunks, 
            embedding=embeddings,
        )
        vector_store.save_local(FAISS_INDEX_PATH)
        print("FAISS index created and persisted.")
        
    return vector_store

def retrieve_info(query, vector_store, k=3):
    """
    Retrieves the top k most relevant documents from the vector store based on the query.
    """
    if vector_store is None:
        return []
    
    # FAISS search returns (document, score) tuples
    docs_with_scores = vector_store.similarity_search_with_score(query, k=k)
    return [doc.page_content for doc, score in docs_with_scores]

if __name__ == "__main__":
    # This block is for testing the RAG system independently
    # It will create/load the vector store and perform a sample retrieval
    st.set_page_config(layout="wide") # Set a wide layout for testing if run directly
    st.title("RAG System Test")

    # Load environment variables if running independently
    # from dotenv import load_dotenv # Already imported at the top
    # load_dotenv() # Already loaded at the top

    # Ensure API key is set for standalone test
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY not set in .env. Please set it to test the RAG system.")
    else:
        vector_db = get_vector_store()

        if vector_db:
            st.success("FAISS vector store initialized.")
            test_query = st.text_input("Enter a test query for resume retrieval:", "What is MohammedAnas's experience?")
            
            if st.button("Retrieve Information"):
                with st.spinner("Retrieving relevant information..."):
                    retrieved_docs = retrieve_info(test_query, vector_db)
                
                if retrieved_docs:
                    st.subheader("Retrieved Information:")
                    for i, doc in enumerate(retrieved_docs):
                        st.write(f"**Document {i+1}:**")
                        st.write(doc)
                        st.markdown("---")
                else:
                    st.info("No relevant information found.")
        else:
            st.error("Failed to initialize FAISS. Check errors above.") 