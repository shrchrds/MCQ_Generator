import os
import json
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.MCQ_Gen.mcq_generator import generate_evaluate_chain
from src.MCQ_Gen.utils import read_file, get_table_data
from src.MCQ_Gen.logger import logging

#loading json file
with open("./response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

# creating a title for the app
st.title("MCQ Generator App")

# create a form
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a pdf or text file")

    #input fields
    mcq_count = st.number_input("No. of MCQs", min_value = 1, max_value=50)

    #subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #quiz tone
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    # add button
    button = st.form_submit_button("Generate MCQs")

    # Check if button is clicked

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading....."):
            try:
                text = read_file(uploaded_file)

                #count tokens and cost of API call

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )
                # st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), value=e, tb=e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")

                if isinstance(response, dict):
                    #extract quiz data from the response
                    quiz = response.get("quiz", None)                     
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                      
                        if table_data is not None:
                            #save quiz data to a csv file
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review in a text area
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)