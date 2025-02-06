import streamlit as st
import pandas as pd
import requests
import json
from io import StringIO
import base64
import plotly.express as px

# Set page config for a wider layout
st.set_page_config(layout="wide")

# Add some styling
st.markdown("""
    <style>
        .stApp {
            max-width: 100%;
            padding: 2rem;
        }
        .stTextInput > div > div > input {
            background-color: #f8f9fa;
            color: #333;  /* Set font color to a dark gray */
        }
        .stTextArea > div > div > textarea {
            background-color: #f8f9fa;
            color: #333; /* Set font color to a dark gray */
        }
        .stButton > button {
          background-color: #007bff;
          color: white;
        }
        .stSelectbox > div > div > div > input {
             background-color:#f8f9fa;
          }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for the title
st.markdown("""
    <style>
        .big-font {
            font-size:3rem !important;
            font-weight: bold;
            color:#007bff;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">ETRM Data Retrieval and Visualization Tool</p>', unsafe_allow_html=True)

# Function to execute a query and return a pandas DataFrame
@st.cache_data
def execute_query(query):
    # Replace with your Azure Function endpoint
    azure_function_endpoint = "https://agent-trader.azurewebsites.net/api/*?"

    try:
        response = requests.post(
            azure_function_endpoint,
            json={"query": query},
             headers={'Content-type': 'application/json'}
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        response_json = response.json()
        if not response_json or 'result' not in response_json or not response_json['result']:
             st.warning("No data found for the given query.")
             return None

        data = response_json['result']
        try:
            df = pd.read_json(data)
            return df
        except:
             return {"Result": data} #Just return the value to be used by streamlit.
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during API call: {e}")
        return None
    except json.JSONDecodeError as e:
         st.error(f"Error decoding API response: {e}")
         return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input for the user query
query = st.text_area("Enter your query:", height=150)

# Display chat history in reverse order
for message in reversed(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f'<div style="background-color:#f0f2f6;padding:10px;border-radius:5px;margin-bottom:10px;">User: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background-color:#e5f6e3;padding:10px;border-radius:5px;margin-bottom:10px;">Assistant: {message["content"]}</div>', unsafe_allow_html=True)

if st.button("Retrieve Data"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Executing query..."):
            result = execute_query(query)
            if result is not None:
                #Add user message to the state
                st.session_state.messages.append({"role": "user", "content": query})
                if isinstance(result, pd.DataFrame):
                    st.session_state.messages.append({"role": "assistant", "content": "Showing Results as a Table"})
                     #Display results
                    st.markdown("### Query Results")
                    st.dataframe(result) # Display dataframe

                     # Visualization options
                    st.markdown("### Visualization Options")
                    if len(result.columns) > 1:
                        x_axis = st.selectbox("Select X-axis", options=result.columns, key="x_axis")
                        y_axis = st.selectbox("Select Y-axis", options=result.columns, key="y_axis")
                        if st.button("Plot Chart"):
                            try:
                                 fig = px.bar(result, x=x_axis, y=y_axis)
                                 st.plotly_chart(fig)
                            except Exception as e:
                                 st.error(f"Error while plotting:{e}")
                        # Download Button
                    csv = result.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download Results as CSV</a>'
                    st.markdown(href, unsafe_allow_html=True)

                elif isinstance(result, dict) and "Result" in result:
                    st.session_state.messages.append({"role": "assistant", "content": f"Value at Risk: {result['Result']}"})
                    st.markdown("### Query Results")
                    st.write(f"Result: {result['Result']}")
            else:
                st.session_state.messages.append({"role": "assistant", "content": "There were no results, please try again."})
                st.write("No Results/ Unsupported Operation")
    if len(st.session_state.messages) > 15:
         st.session_state.messages = st.session_state.messages[-15:]

# Function to execute a query and return a pandas DataFrame
@st.cache_data
def execute_query(query):
    # Replace with your Azure Function endpoint
    azure_function_endpoint = "https://agent-trader.azurewebsites.net/api/*?"

    try:
        response = requests.post(
            azure_function_endpoint,
            json={"query": query},
             headers={'Content-type': 'application/json'}
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        response_json = response.json()
        if not response_json or 'result' not in response_json or not response_json['result']:
             st.warning("No data found for the given query.")
             return None

        data = response_json['result']
        try:
            df = pd.read_json(data)
            return df
        except:
             return {"Result": data} #Just return the value to be used by streamlit.

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during API call: {e}")
        return None
    except json.JSONDecodeError as e:
         st.error(f"Error decoding API response: {e}")
         return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
