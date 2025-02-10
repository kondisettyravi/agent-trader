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
             if isinstance(data, dict) and "result" in data:
                  return pd.DataFrame([{"Result":data['result']}]) # Create a Dataframe, if there is only single value.
             else:
                 return pd.DataFrame([{"Result":data}])
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during API call: {e}")
        return None
    except json.JSONDecodeError as e:
         st.error(f"Error decoding API response: {e}")
         return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Input for the user query
query = st.text_area("Enter your query:", height=150)
if 'query_result' not in st.session_state:
     st.session_state.query_result = None

if st.button("Retrieve Data"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Agent at work. Parsing your request and fetching results..."):
           df = execute_query(query)
        st.session_state.query_result = df
if st.session_state.query_result is not None:
    df = st.session_state.query_result
    st.markdown("### Query Results")
    st.dataframe(df) # Display dataframe

    # Visualization options
    st.markdown("### Visualization Options")
    if len(df.columns)>1:
         x_axis = st.selectbox("Select X-axis", options=df.columns, key="x_axis")
         y_axis = st.selectbox("Select Y-axis", options=df.columns, key="y_axis")
         if st.button("Plot Chart"):
            try:
                fig = px.bar(df, x=x_axis, y=y_axis)
                st.plotly_chart(fig)
            except Exception as e:
                 st.error(f"Error while plotting:{e}")

    # Download Button
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download Results as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
