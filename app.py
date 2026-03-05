
# PART 3 — Session State Application (Streamlit)


import streamlit as st
import re
from langchain_community.llms import Ollama

# STEP 1 — Load LLM
llm = Ollama(model="llama3.2:1b", temperature=0)



# STEP 2 — Calculator

def calculator(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Calculation Error"



# STEP 3 — Expression Cleaner

def clean_expression(expr):

    expr = expr.lower()
    expr = expr.replace("x", "*").replace("×", "*")

    if "=" in expr:
        expr = expr.split("=")[0]

    expr = re.sub(r"[^0-9\.\+\-\*\/\(\)\% ]", "", expr)
    expr = expr.replace(" ", "")

    return expr



# STEP 4 — Text-to-Math Solver

def solve_text_math(problem):

    prompt = f"""
    Convert this word problem into ONLY a math expression.
    Do not explain.

    Problem: {problem}
    Expression:
    """

    raw_expression = llm.invoke(prompt).strip()
    expression = clean_expression(raw_expression)
    result = calculator(expression)

    return expression, result



# STEP 5 — Streamlit UI


st.title("Text-to-Math Agent")

# session memory
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Enter a math word problem")

if st.button("Solve") and user_input:

    expr, answer = solve_text_math(user_input)

    st.session_state.history.append({
        "question": user_input,
        "expression": expr,
        "answer": answer
    })

# display history
st.subheader("Conversation History")

for item in reversed(st.session_state.history):
    st.write("**Problem:**", item["question"])
    st.write("**Expression:**", item["expression"])
    st.write("**Answer:**", item["answer"])
    st.write("---")