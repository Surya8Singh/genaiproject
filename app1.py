import streamlit as st
import os
from langchain_openai import OpenAI  # Updated import
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to load OpenAI model and get a response
def get_openai_response(question):
    api_key = os.getenv("OPENAI_API_KEY")
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

# Debug: Print the API key status (remove in production)
api_key_status = "Loaded" if os.getenv("OPENAI_API_KEY") else "Not found"
st.write(f"API Key Status: {api_key_status}")

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
