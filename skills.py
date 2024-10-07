import streamlit as st
import requests
import os
from groq import Groq
from bs4 import BeautifulSoup
# Initialize Groq client (make sure your API key is set in environment variables)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function to scrape the first 3 <p> tags from website content
def scrape_first_paragraphs(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all('p', limit=3)
            return ' '.join([p.get_text() for p in paragraphs])
        else:
            return "Failed to retrieve content from the website."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to query the Groq API LLM
def query_groq_llm(content):
    prompt = f"""Analyze the following website content and provide:
    1. The type of content (e.g., Deep Learning, Software Development, etc.)
    2. Required skills for this domain.
    3. Required software modules or libraries.

    Content: {content}
    """
    
    # Send the prompt to Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

# Streamlit App
st.title("Website Content Analyzer")
st.write("Enter a website URL and get insights about the content, skills, and software modules required.")

# URL Input
url = st.text_input("Enter the website URL", "https://example.com")

if st.button("Analyze"):
    # Scrape first 3 paragraphs from the website
    with st.spinner("Scraping the website..."):
        website_content = scrape_first_paragraphs(url)
    
    if website_content.startswith("Failed") or website_content.startswith("An error occurred"):
        st.error(website_content)
    else:
        # Show scraped content
        st.subheader("Scraped Website Content (First 3 paragraphs)")
        st.write(website_content)
        
        # Query Groq LLM
        with st.spinner("Analyzing the content with Groq LLM..."):
            llm_response = query_groq_llm(website_content)
        
        # Display LLM output
        st.subheader("Analysis Result")
        st.write(llm_response)