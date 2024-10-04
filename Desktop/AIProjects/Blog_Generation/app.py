import streamlit as st
from langchain.prompts import PromptTemplate
# from langchain.llms import Ctransformers
from ctransformers import AutoModelForCausalLM
import sys

print(sys.executable)

# Function to get response from LLaMA 2 model
def get_llama_response(input_text, no_words, blog_style):
    # LLaMA 2 model path
    model_path = '/Users/suryapratapsingh/Desktop/AIProjects/Blog Generation/models/llama-2-7b-chat.ggmlv3.q8_0.bin'
    
    # Initialize the LLaMA model
    # llm = Ctransformers(model=model_path,
    #                     model_type='llama',
    #                     config={'max_new_tokens': 256,
    #                             'temperature': 0.01})
    llm = AutoModelForCausalLM.from_pretrained(model_path, model_type="llama")

    # Prompt template
    template = """Write a blog for {style} job 
    profile for a topic {text} within {n_words} words."""

    # Create the template
    prompt = PromptTemplate(input_variables=["style", "text", "n_words"],
                            template=template)
    
    # Generate the response from the LLaMA model
    response = llm(prompt.format(style=blog_style, text=input_text, n_words=no_words))
    print(response)
    return response

# Set up Streamlit
st.set_page_config(page_title="Generate Blogs",
                   page_icon="🧊",
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🧊")

input_text = st.text_input('Enter the blog topic')

# Creating two more columns for additional two fields
col1, col2 = st.columns(2)

with col1:
    no_words = st.text_input('No of words', value='100')  # Default value for words
with col2:
    blog_style = st.selectbox('Writing the blog for', ('Researchers', 'Data Scientist', 'Common Use'), index=0)

submit = st.button('Generate')

# Final response
if submit:
    try:
        # Ensure no_words is an integer
        no_words = int(no_words)
        if no_words <= 0:
            st.error("Please enter a positive number for the number of words.")
        else:
            result = get_llama_response(input_text, no_words, blog_style)
            st.write(result)
    except ValueError:
        st.error("Invalid input! Please enter a valid number for the number of words.")