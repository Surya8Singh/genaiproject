import streamlit as st
import os
from langchain_openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Debug: Print current working directory and list files
st.write(f"Current working directory: {os.getcwd()}")
st.write(f"Files in current directory: {os.listdir()}")

# Load environment variables from .env file
dotenv_path = find_dotenv()
st.write(f".env file found: {'Yes' if dotenv_path else 'No'}")
if dotenv_path:
    st.write(f".env file path: {dotenv_path}")
    load_dotenv(dotenv_path)

# Function to load OpenAI model and get a response
def get_openai_response(question):
    api_key = os.getenv("OPENAI_API_KEY")
    st.write(f"API Key retrieved: {'Yes' if api_key else 'No'}")
    if api_key:
        st.write(f"API Key length: {len(api_key)}")
        st.write(f"API Key starts with: {api_key[:5]}...")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    try:
        llm = OpenAI(api_key=api_key, model_name="gpt-3.5-turbo-instruct", temperature=0.5)
        response = llm(question)
        return response
    except Exception as e:
        raise Exception(f"Error initializing OpenAI model: {str(e)}")

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Langchain Application")

# Input field for user question
input_text = st.text_input("Input: ", key="input")

# Submit button
submit = st.button("Ask the question")

# If the ask button is clicked
if submit:
    if input_text:
        try:
            response = get_openai_response(input_text)
            st.subheader("The Response is")
            st.write(response)
        except ValueError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.write("Please enter a question.")
