# src/app.py

import streamlit as st
import os
from content_check import check_content
from translator import Translator
from text_to_speech import text_to_speech
from content_creator import rag_workflow


# Generate unique categories from mistakes
def gen_category_list(list_highlight):
    return {mistake_type for highlight in list_highlight for mistake_type in highlight["mistake_type"]}


# Generate tooltip HTML content
def create_tooltip(text, mistake_types):
    mistake_types_str = ", ".join(mistake_types)
    return f'<span class="tooltip">{text}<span class="tooltiptext">{mistake_types_str}</span></span>'


# Apply mistake highlighting and suggestions
def apply_highlighting(input_content, list_highlight, is_fix=False):
    processed_content = input_content
    for item in list_highlight:
        mistake = item["mistake"]
        suggestion = item["suggestion"]
        mistake_types = item["mistake_type"]
        replacement = suggestion if is_fix else mistake

        # Replace mistakes with tooltips
        tooltip_content = f'<mistake-type1-fix>{create_tooltip(replacement, mistake_types)}</mistake-type1-fix>' if is_fix else f'<mistake-type1>{create_tooltip(mistake, mistake_types)}</mistake-type1>'

        processed_content = processed_content.replace(mistake, tooltip_content)
        processed_content = processed_content.replace(mistake.replace("'", '"').replace('"s ', "'s "), tooltip_content)

    return f'<div class="div-style-textarea"><p>{processed_content}</p></div>'


# Generate markdown content with both original and fixed highlights
def gen_markdown_content(input_content, list_highlight):
    original_content = apply_highlighting(input_content, list_highlight, is_fix=False)
    fixed_content = apply_highlighting(input_content, list_highlight, is_fix=True)

    # Escape special characters
    original_content = original_content.replace('$', '\$')
    fixed_content = fixed_content.replace('$', '\$')

    return original_content, fixed_content


# Define page functions
def page_home():
    st.title("Government Hackathon Project [Rename the Project)")
    st.write(
        "Welcome to the Government Hackathon Project. Use the navigation bar to explore different functionalities.[Some explanation/ picture/ diagram]")

def page_content_creator():
    st.title("AI Content Creator")
    st.write(
        "Add some banner/pic & explain sth incld functionality & link to the requirement")
    pdf_input = st.file_uploader("Upload PDF file", type=('pdf'))
    objective = st.text_input("Objective")
    ai_gen_button = st.button("Generate Content by AI")
    if ai_gen_button :
        with st.spinner('Processing...'):
            generated_content = rag_workflow(pdf_input, objective)
            st.markdown(generated_content, unsafe_allow_html=True)
            st.download_button(
                label="Save the content",
                data=generated_content,
                # file_name="sample.txt",
                mime="text/plain"
            )


def page_rewrite_content():
    st.title("AI Content Editor")
    st.write(
        "Add some banner/pic & explain sth incld functionality & link to the requirement")
    # Define the folder path
    folder_path = 'raw_data'

    # List all text files in the folder
    text_files = [''] + [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Create a dropdown menu with a default empty string option
    st.write('Select a text file:')
    selected_file = st.selectbox('content_editor_box', text_files,label_visibility = 'collapsed')

    # Check if a valid file is selected
    if selected_file:
        # Ensure it's not the empty string
        file_path = os.path.join(folder_path, selected_file)
        with open(file_path, 'r') as file:
            file_content = file.read()

    st.write('Edit Content')
    text_input = st.text_area('content_editor_text',file_content if selected_file else '', height=200,label_visibility = 'collapsed')
    if st.button("Rewrite Content by AI"):
        with st.spinner('Processing...'):
            llm_output = check_content(text_input)
            col1, col2 = st.columns(2)
            col1.write("Original Content")
            col2.write("Rewritten Content")
            original_text, fixed_text = gen_markdown_content(text_input, llm_output)
            col1.markdown(original_text, unsafe_allow_html=True)
            col2.markdown(fixed_text, unsafe_allow_html=True)
            st.dataframe(llm_output, use_container_width=True)
            st.download_button(
                label="Save the content",
                data=fixed_text,
                # file_name="sample.txt",
                mime="text/plain"
            )



def page_translator():
    st.title("AI Content Translator")
    st.write(
        "Add some banner/pic & explain sth incld functionality & link to the requirement")
    # Define the folder path
    folder_path = 'raw_data'

    # List all text files in the folder
    text_files = [''] + [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Create a dropdown menu with a default empty string option
    st.write('Select a text file:')
    selected_file = st.selectbox('translator_box:', text_files,label_visibility ='collapsed')

    # Check if a valid file is selected
    if selected_file:
        # Ensure it's not the empty string
        file_path = os.path.join(folder_path, selected_file)
        with open(file_path, 'r') as file:
            file_content = file.read()

    st.write('Edit Content')
    text_input = st.text_area('translator_text',file_content if selected_file else '', height=200,label_visibility ='collapsed')
    trans_obj = Translator()
    st.write('Language')
    select_lang = st.selectbox('Language', trans_obj.language_list, label_visibility ='collapsed')
    translate_button = st.button("Translate Content")
    if translate_button:
        with st.spinner('Processing...'):
            trans_text = trans_obj.translate_content(content=text_input, translated_language=select_lang)
            st.markdown(trans_text, unsafe_allow_html=True)
            st.download_button(
                label="Save the translation",
                data=trans_text,
                # file_name="sample.txt",
                mime="text/plain"
            )

def page_reader():
    st.write(
        "Add some banner/pic & explain sth incld functionality & link to the requirement")
    st.title("AI Content Reader")
    # Define the folder path
    folder_path = 'raw_data'

    # List all text files in the folder
    text_files = [''] + [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Create a dropdown menu with a default empty string option
    st.write('Select text file:')
    selected_file = st.selectbox('reader_box', text_files, label_visibility = 'collapsed')

    # Check if a valid file is selected
    if selected_file:
        # Ensure it's not the empty string
        file_path = os.path.join(folder_path, selected_file)
        with open(file_path, 'r') as file:
            file_content = file.read()

    st.write('Edit Content')
    text_input = st.text_area('reader_text',file_content if selected_file else '', height=200,label_visibility ='collapsed')
    tts_button =st.button("Text to Speech")
    if tts_button:
        with st.spinner('Processing...'):
            text_to_speech(text_input,play=False)
            st.audio('output.mp3', format="audio/wav", start_time=0)



# Main function to handle page routing
def main():
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
            mistake-type1, mistake-type1-fix {
                font-family: "Source Sans Pro", sans-serif;
                font-size: 1rem;
                color: black;
            }
            mistake-type1 {
                background-color: yellow;
            }
            mistake-type1-fix {
                background-color: blue;
            }
            .div-style-textarea {
                background-color: rgb(38, 39, 48);
                color: rgb(250, 250, 250);
                border-radius: 2%;
                padding: 1rem;
                line-height: 1.4;
                font-family: "Source Sans Pro", sans-serif;
                font-size: 1rem;
            }
            .tooltip {
                position: relative;
                border-bottom: 1px dotted black;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 120px;
                background-color: black;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px 0;
                position: absolute;
                z-index: 1;
                bottom: 100%;
                left: 50%;
                margin-left: -60px;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
            }
        </style>
    """, unsafe_allow_html=True)
    # st.markdown("""
    #     <style>
    #     .stButton>button {
    #         background-color: #4CAF50;
    #         color: white;
    #         padding: 10px 24px;
    #         border-radius: 8px;
    #     }
    #     .stTextArea textarea {
    #         background-color: #F0F0F0;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)

    # Set OpenAI API Key from secrets
    os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]

    # Create a sidebar for page navigation
    # page = st.sidebar.selectbox("Choose a page", ["Home","AI Content Creator","AI Content Editor", "AI Content Translator","AI Content Reader"])
    home, content_creator_tab, content_editor_tab, content_translator_tab, content_reader_tab = st.tabs(
        ["Home","AI Content Creator","AI Content Editor", "AI Content Translator","AI Content Reader"])

    # Render the selected page
    # if page == "Home":
    #     page_home()
    # elif page == "AI Content Creator":
    #     page_content_creator()
    # elif page == "AI Content Editor":
    #     page_rewrite_content()
    # elif page == "AI Content Translator":
    #     page_translator()
    # elif page == "AI Content Reader":
    #     page_reader()

    # Render the selected page
    with home:
        page_home()
    with content_creator_tab:
        page_content_creator()
    with content_editor_tab:
        page_rewrite_content()
    with content_translator_tab:
        page_translator()
    with content_reader_tab:
        page_reader()


if __name__ == "__main__":
    main()