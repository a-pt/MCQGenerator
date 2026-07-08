import os
import json
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# Load enviornment variables
load_dotenv()

key =  os.getenv("GROQ_API_KEY")

openaiModel =  ChatGroq(model="openai/gpt-oss-120b",temperature = 0.5)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
    )

TEMPLATE1="""
You are an expert in {subject}. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a crisp analysis of the quiz. Only use at max 200 words for analysis. 
Quiz_MCQs:
{quiz}

Check from an subject expert for the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE1)

quiz_chain = (
    quiz_generation_prompt
    | openaiModel
    | StrOutputParser()
)

review_chain = (
    quiz_evaluation_prompt
    | openaiModel
    | StrOutputParser()
)

generate_evaluate_chain = (
    RunnablePassthrough.assign(
        quiz=quiz_chain
    )
    .assign(
        review=(
            lambda x: {
                "quiz": x["quiz"],
                "subject": x["subject"],
            }
        )
        | review_chain
    )
)