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
    azure_function_endpoint = "https://agent-trader-app.azurewebsites.net/api/*?"

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
             return {"Result": data} # Create a Dataframe, if there is only single value.
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during API call: {e}")
        return None
    except json.JSONDecodeError as e:
         st.error(f"Error decoding API response: {e}")
         return None
    except Exception as e:
         st.error(f"An unexpected error occurred: {e}")
         return None
 # Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Enter your query:")

if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Execute the query
    results = execute_query(query)
    if results is not None:
        st.session_state.messages.append({"role": "assistant", "content": "Executed Query Successfully"})
        with st.chat_message("assistant"):
            st.markdown("Executed Query Successfully")
        st.markdown("### Query Results")
        if isinstance(results, dict):
          st.write(results["Result"])
        else:
          st.dataframe(results) # Display dataframe
         # Visualization options
          st.markdown("### Visualization Options")
          chart_types = ['line', 'bar', 'scatter', 'pie', 'area']

          if len(results.columns)>1:
            x_axis = st.selectbox("Select X-axis", options=results.columns, key="x_axis")
            y_axis = st.selectbox("Select Y-axis", options=results.columns, key="y_axis")
            chart_type = st.selectbox("Select Chart Type", options=chart_types, key="chart_type")
            if st.button("Plot Chart"):
               try:
                   if chart_type == 'line':
                       fig = px.line(results, x=x_axis, y=y_axis)
                   elif chart_type == 'bar':
                       fig = px.bar(results, x=x_axis, y=y_axis)
                   elif chart_type == 'scatter':
                        fig = px.scatter(results, x=x_axis, y=y_axis)
                   elif chart_type == 'pie':
                       fig = px.pie(results, values=y_axis, names=x_axis)
                   elif chart_type == 'area':
                       fig = px.area(results, x=x_axis, y=y_axis)
                   st.plotly_chart(fig)
               except Exception as e:
                    st.error(f"Error while plotting:{e}")

    else:
         st.session_state.messages.append({"role": "assistant", "content": "An error occurred, please check the prompt"})
         with st.chat_message("assistant"):
             st.markdown("An error occurred, please check the prompt")
