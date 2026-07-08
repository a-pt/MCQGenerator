import os
import json
import pandas as pd
import traceback
import streamlit as st
from src.mcqgen.logger import logging
from src.mcqgen.utils import read_file,get_table_data
from src.mcqgen.MCQGenerator import generate_evaluate_chain
from langchain_community.callbacks.manager import get_openai_callback

# loading json file
with open('response.json','r') as file:
    RESPONSE_JSON = json.load(file)

# creating title for the app
st.title("MCQ Generator Application with Langchain")

# Create a form usint st.form
with st.form("user_inputs"):
    # text area input for the user
    uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf"])

    # Radio button selection for the number of MCQs
    mcq_count = st.slider("Number of MCQs", min_value=1, max_value=20, value=5)

    # Subject
    subject = st.text_input("Subject")

    # Tone Selector
    tone = st.selectbox("Tone", ["Easy", "Intermediate", "Hard"])

    # Submit button
    submit_button = st.form_submit_button("Generate MCQs")

    if submit_button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                
                # Count tokens and cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain.invoke({"text": text, "number": mcq_count, "subject": subject, "tone": tone, "response_json": RESPONSE_JSON})
            except Exception as e:
                traceback.print_exception(e)
                st.error("Error generating MCQs")
            else:
                print(f'Total Tokens:{cb.total_tokens}')
                print(f'Prompt Tokens:{cb.prompt_tokens}')
                print(f'Completion Tokens:{cb.completion_tokens}')
                print(f'Total Cost:{cb.total_cost}')

                st.success("Quiz generated successfully!")
                
                # Extract quiz from response
                quiz = response.get('quiz',None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data:
                        df = pd.DataFrame(table_data)
                        df.index = df.index+1
                        st.table(df)
                        st.markdown("#### Review")
                        st.write(response.get("review", None))
                    else:
                        st.error("No table data generated")
                else:
                    st.error("No quiz generated")

                