import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import pandas as pd

# Set up SQL database (SQLite for simplicity)
engine = create_engine('sqlite:///responses.db')
metadata = MetaData()

# Create responses table (if it doesn't exist)
responses = Table('responses', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('researcher', String),
                  Column('topic', String),
                  Column('question', String),
                  Column('answer', String))
metadata.create_all(engine)

st.title("Researcher Questionnaire")

# Input researcher name
researcher = st.text_input("Researcher Name")

# Organize questionnaire into sections (topics)
tabs = st.tabs(["Topic A", "Topic B", "Topic C"])

responses_to_store = []

with tabs[0]:
    st.header("Topic A")
    answer1 = st.text_area("A1: Please provide multiple lines if needed:")
    answer2 = st.selectbox("A2: Choose an option", ["Option 1", "Option 2", "Option 3"])

    responses_to_store.append(("Topic A", "A1", answer1))
    responses_to_store.append(("Topic A", "A2", answer2))

with tabs[1]:
    st.header("Topic B")
    answer3 = st.text_input("B1: Short answer question")
    responses_to_store.append(("Topic B", "B1", answer3))

with tabs[2]:
    st.header("Topic C")
    answers_multi = st.text_area("C1: Provide each item on a new line")
    if answers_multi.strip():
        multi_lines = [line.strip() for line in answers_multi.strip().split('\n') if line.strip()]
        for line in multi_lines:
            responses_to_store.append(("Topic C", "C1", line))

if st.button("Submit Responses"):
    if not researcher.strip():
        st.error("Please enter your name before submitting.")
    else:
        # Insert responses into SQL
        df_responses = pd.DataFrame(responses_to_store, columns=["topic", "question", "answer"])
        df_responses["researcher"] = researcher

        # Save each response as a separate row
        df_responses.to_sql('responses', con=engine, if_exists='append', index=False)
        st.success("Responses saved successfully!")
