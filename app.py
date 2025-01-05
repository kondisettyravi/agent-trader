import streamlit as st
import pandas as pd
import requests
import json
from io import StringIO
import base64

st.title("ETRM Data Retrieval Tool")

# Function to execute a query and return a pandas DataFrame
def execute_query(query):
    # Replace with your Azure Function endpoint
    azure_function_endpoint = "YOUR_AZURE_FUNCTION_ENDPOINT"  

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
        df = pd.read_json(data)
        return df
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
query = st.text_area("Enter your query:", height = 150)

if st.button("Retrieve Data"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Executing query..."):
           df = execute_query(query)
        if df is not None:
            st.write("Query Results:")
            st.dataframe(df) # Display dataframe

            # Download Button
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download Results as CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
