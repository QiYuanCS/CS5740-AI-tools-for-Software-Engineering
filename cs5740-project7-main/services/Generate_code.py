import asyncio
import traceback

import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES

import helpers.sidebar
import helpers.util
import services.extract
import services.llm
import services.prompts
from helpers import util

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide"
)

# Add comments to explain the purpose of the code sections
# Initialize session state variables
if 'code_review_history' not in st.session_state:
    st.session_state.code_review_history = []

if 'debug_history' not in st.session_state:
    st.session_state.debug_history = []

if 'modify_history' not in st.session_state:
    st.session_state.modify_history = []

if 'modify_code' not in st.session_state:
    st.session_state.modify_code = ""
# Show sidebar
helpers.sidebar.show()

st.title("Code Assistant")

tab1, tab2, tab3 = st.tabs(["Code Review", "Debug Code", "Modify Code"])
with tab1:
    st.subheader("Code Review")
    code_review = st_ace(
        language=LANGUAGES[57],
        theme=THEMES[0],
        keybinding=KEYBINDINGS[0],
        height=300,
        key="code_review_editor"
    )

    if st.button("Get Code Review"):
        if not code_review.strip():
            st.error("Please enter some code to review")
        else:
            try:
                with st.spinner("Generating code review..."):
                    prompt = services.prompts.get_code_review_prompt(code_review)
                    review = services.llm.ask_llm(prompt)
                    st.session_state.code_review_history.append(
                        (code_review, review)
                    )
            except Exception as e:
                st.error(f"Error generating code review: {str(e)}")
                st.error(traceback.format_exc())

    for idx, (code, review) in enumerate(st.session_state.code_review_history):
        st.markdown(f"### Review #{idx + 1}")
        st.code(code, language='python')
        st.markdown(review)

with tab2:
    st.subheader("Debug Code")
    debug_code = st_ace(
        language=LANGUAGES[57],
        theme=THEMES[0],
        keybinding=KEYBINDINGS[0],
        height=300,
        key="debug_editor"
    )
    error_message = st.text_input("Error Message (optional)")

    if st.button("Debug Code"):
        if not debug_code.strip():
            st.error("Please enter some code to debug")
        else:
            try:
                with st.spinner("Analyzing code..."):
                    prompt = services.prompts.get_debug_prompt(debug_code, error_message)
                    debug_response = services.llm.ask_llm(prompt)
                    st.session_state.debug_history.append(
                        (debug_code, error_message, debug_response)
                    )
            except Exception as e:
                st.error(f"Error debugging code: {str(e)}")
                st.error(traceback.format_exc())

    for idx, (code, error, response) in enumerate(st.session_state.debug_history):
        st.markdown(f"### Debug Session #{idx + 1}")
        st.code(code, language='python')
        if error:
            st.error(f"Associated error: {error}")
        st.markdown(response)

with tab3:
    st.subheader("Modify Code")
    current_code = st_ace(
        value=st.session_state.modify_code,
        language=LANGUAGES[57],
        theme=THEMES[0],
        keybinding=KEYBINDINGS[0],
        height=300,
        key="modify_editor"
    )
    modification_request = st.text_input("Modification Request")

    if st.button("Apply Modification"):
        if not current_code.strip():
            st.error("Please enter some code to modify")
        elif not modification_request.strip():
            st.error("Please enter a modification request")
        else:
            try:
                with st.spinner("Modifying code..."):
                    prompt = services.prompts.get_modification_prompt(
                        current_code, modification_request
                    )
                    response = services.llm.ask_llm(prompt)
                    modified_code = services.extract.extract_code(response)
                    explanation = services.extract.extract_explanation(response)

                    if modified_code:
                        st.session_state.modify_code = modified_code
                        st.session_state.modify_history.append({
                            "request": modification_request,
                            "response": response,
                            "old_code": current_code,
                            "new_code": modified_code,
                            "explanation": explanation
                        })
                    else:
                        st.error("Could not extract modified code from response")
            except Exception as e:
                st.error(f"Error modifying code: {str(e)}")
                st.error(traceback.format_exc())

    for idx, entry in enumerate(st.session_state.modify_history):
        st.markdown(f"### Modification #{idx + 1}")
        st.markdown(f"**Request:** {entry['request']}")
        st.markdown(f"**Explanation:** {entry['explanation']}")
        st.markdown("**Original Code:**")
        st.code(entry['old_code'], language='python')
        st.markdown("**Modified Code:**")
        st.code(entry['new_code'], language='python')

st.sidebar.markdown("---")
if st.sidebar.button("Reset All"):
    st.session_state.code_review_history = []
    st.session_state.debug_history = []
    st.session_state.modify_history = []
    st.session_state.modify_code = ""
    st.sidebar.success("All history and code have been reset")

#st.markdown("""
# #TODO

## Implement the following use cases
#and any other Python components or libraries of your choice, implement the following use cases on the "generate code" page of the application.  It is assumed and required that the application uses an LLM to assist behind-the-scenes.
#Using Streamlit,

#* Provide a feature to review code.  The use case is for a developer to provide some code, and to ask for a code review.


#* Provide a feature to debug code.  The use case is for a developer to provide some code, along with an optional error string, and to ask for help debugging the code, assuming that the error string was associated with execution of the code.


#* Provide a feature to modify or change the code using natural language conversationally.  The use case is for a developer to ask an LLM assistant to take some code, and some modification instructions.  The LLM assistant should provide modified code, and an explanation of the changes made.  Assuming the LLM is not perfect, the feature will allow the conversation to continue with more modification requests.

#* Provide a feature to reset the page, to allow all existing code and history to be cleared; this effectively starts a new conversation about possibly new code.
#""")




