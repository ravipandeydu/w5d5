import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Quick Commerce Deal Finder",
    page_icon="🛒",
    layout="centered"
)

# --- API Endpoint ---
API_URL = "http://127.0.0.1:8000/query"

# --- UI Elements ---
st.title("🛒 Quick Commerce Deal Finder")
st.caption("Ask me to find the best prices across Blinkit, Zepto, and Instamart!")

# Pre-defined query examples
example_queries = [
    "Which app has cheapest onions right now?",
    "Show products with 30%+ discount on Blinkit",
    "Compare fruit prices between Zepto and Instamart",
    "Find best deals for a ₹500 grocery list with 1kg Potato, 1kg Tomato, and 1 litre Milk"
]

query = st.text_area(
    "What are you looking for?",
    value=example_queries[0],
    height=100,
    help="You can ask simple questions or complex ones with a budget."
)

st.write("---")
st.write("**Or try one of these examples:**")
cols = st.columns(2)
for i, example in enumerate(example_queries):
    if cols[i % 2].button(example, use_container_width=True):
        query = example

if st.button("🔍 Find Deals", use_container_width=True, type="primary"):
    if query:
        with st.spinner("🤖 Thinking... Contacting the AI agent..."):
            try:
                payload = {"query": query}
                response = requests.post(API_URL, json=payload)
                response.raise_for_status() # Raise an exception for bad status codes
                
                result = response.json()
                st.markdown(result.get("response", "Sorry, I couldn't get a response."))

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend API. Is it running? Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a query.")