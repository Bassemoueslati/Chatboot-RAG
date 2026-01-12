import streamlit as st
from chatbot import get_response
import json
import os
from datetime import datetime

st.title("Gym Exercise and Diet Chatbot")

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialize session state for showing archives
if 'show_archives' not in st.session_state:
    st.session_state.show_archives = False

# Function to auto-archive conversation
def auto_archive_conversation():
    if st.session_state.conversation and len(st.session_state.conversation) >= 2:  # At least one Q&A pair
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_archive_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(st.session_state.conversation, f, indent=4)
        return filename
    return None

# Function to load archived conversations
def load_archived_conversations():
    archives = []
    for file in os.listdir('.'):
        if file.startswith('conversation_archive_') and file.endswith('.json'):
            archives.append(file)
    return sorted(archives, reverse=True)

# Function to load a specific conversation
def load_conversation(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return []

st.sidebar.header("User Profile")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.sidebar.number_input("Weight (kg)", min_value=1.0, value=70.0)
height = st.sidebar.number_input("Height (m)", min_value=0.5, value=1.75)
bmi = weight / (height ** 2)
st.sidebar.text(f"BMI: {bmi:.2f}")

# Format profile as string
profile = f"Age: {age}, Gender: {gender}, Weight: {weight}kg, Height: {height}m, BMI: {bmi:.2f}"

st.header("Chat Interface")

# Display conversation history
for message in st.session_state.conversation:
    if message['role'] == 'user':
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")

# Initialize query in session state if not present
if 'query' not in st.session_state:
    st.session_state.query = ""

query = st.text_input("Enter your query:", value=st.session_state.query, key="query_input")
if st.button("Submit"):
    if query:
        # Add user message to conversation
        st.session_state.conversation.append({'role': 'user', 'content': query})
        
        with st.spinner("Generating response..."):
            response = get_response(query, profile, st.session_state.conversation)
        
        # Add bot response to conversation
        st.session_state.conversation.append({'role': 'assistant', 'content': response})
        
        # Clear the query input
        st.session_state.query = ""
        
        # Rerun to update the display
        st.rerun()
    else:
        st.write("Please enter a query.")

# Archive and view archives section
col1, col2 = st.columns(2)
with col1:
    if st.button("View Archives"):
        st.session_state.show_archives = not st.session_state.show_archives
        st.rerun()
with col2:
    if st.button("Delete Conversation"):
        st.session_state.conversation = []
        st.success("Conversation deleted.")
        st.rerun()

if st.session_state.show_archives:
    st.subheader("Archived Conversations")
    archives = load_archived_conversations()
    if archives:
        for archive in archives:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"Load {archive}"):
                    # Auto-archive current conversation if exists
                    archived_filename = auto_archive_conversation()
                    if archived_filename:
                        st.info(f"Current conversation archived as {archived_filename}")
                    # Load the selected archived conversation
                    st.session_state.conversation = load_conversation(archive)
                    st.session_state.show_archives = False  # Close the view after loading
                    st.success(f"Loaded conversation from {archive}")
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{archive}"):
                    try:
                        os.remove(archive)
                        st.success(f"Deleted {archive}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to delete {archive}: {e}")
    else:
        st.write("No archived conversations found.")
    
    # Manual archive button
    if st.button("Manual Archive Current Conversation"):
        if st.session_state.conversation:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_archive_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(st.session_state.conversation, f, indent=4)
            st.success(f"Conversation archived as {filename}")
        else:
            st.warning("No conversation to archive.")
    
    # Close archives button
    if st.button("Close Archives"):
        st.session_state.show_archives = False
        st.rerun()
