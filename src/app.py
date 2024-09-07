# src/app.py

import streamlit as st
import requests
import json
import os

import content_check


def gen_category_list(list_highlight):
    myset = set()
    for i in list_highlight:
        for j in i["mistake_type"]:
            myset.add(j)
    return myset

def gen_markdown_content(input_data_content, list_highlight):
    prep_data = input_data_content
    prep_data2 = input_data_content

    for i in list_highlight:
        # print(i["mistake"])

        mistake_types = ", ".join(i["mistake_type"])

        prep_data = prep_data.replace(i["mistake"], f'<mistake-type1><span class="tooltip">' + i["mistake"] + f'<span class="tooltiptext">'+mistake_types+'</span></span>' + "</mistake-type1>") 
        prep_data = prep_data.replace(i["mistake"].replace("'",'"').replace('"s ',"'s "), f'<mistake-type1><span class="tooltip">' + i["mistake"] + f'<span class="tooltiptext">'+mistake_types+'</span></span>' +  "</mistake-type1>") 

        prep_data2 = prep_data2.replace(i["mistake"], f'<mistake-type1-fix><span class="tooltip">' + i["suggestion"] + f'<span class="tooltiptext">'+mistake_types+'</span></span>' + "</mistake-type1-fix>") 
        prep_data2 = prep_data2.replace(i["mistake"].replace("'",'"').replace('"s ',"'s "), f'<mistake-type1-fix><span class="tooltip">' + i["suggestion"] + f'<span class="tooltiptext">'+mistake_types+'</span></span>' + "</mistake-type1-fix>") 
        pass

    output_data  = f'<div class="div-style-textarea"><p>' + prep_data + f'</p></div>'
    output_data2 = f'<div class="div-style-textarea"><p>' + prep_data2 + f'</p></div>'

    return output_data, output_data2

def main():


    # Specify the directory you want to list
    directory = './src/openai_response/'

    # # List files in the directory
    # files = os.listdir(directory)

    # # Print the files
    # for file in files:
    #     print(file)




    # with open(directory +'test_res1.json') as f:
    #     raw_json = json.load(f)

    with open(directory +'prompt.txt') as f:
        raw_prompt = f.read()

    with open(directory +'input.txt') as f:
        raw_input_example = f.read()


    raw_json = check_content(raw_input_example)



    input_example, input_example2 = gen_markdown_content(raw_input_example, raw_json)
    list_category = gen_category_list(raw_json)
    # Initialize


    # Start writing
    st.title("Government Hackathon Project")
    st.write("This Streamlit app interacts with the FastAPI backend to make predictions.")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    # page = st.sidebar.radio("Choose a page", ["Home", "Rewrite Content"])
    page = st.sidebar.radio("Choose a page", [ "Rewrite Content"])

    # if page == "Home":
    #     st.write("Welcome to the home page!")
    #     st.write("Use the navigation menu to make predictions.")

    if page == "Rewrite Content":
        st.header("Rewrite Content")

        # # System input
        # input_prompt = st.text_area('Enter the system prompt:', key = "raw_prompt", value = raw_prompt, height=500)

        # User input
        # st.write("Enter the data for prediction:")
        # input_data = st.text_input("Input Data")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Original Content")
            st.markdown(input_example, unsafe_allow_html=True)

            # st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">text</p>', unsafe_allow_html=True)
            # original_text = st.text_area("Original Content", key = "original_text", value = raw_input_example, height=500)


        with col2:
            st.write("Rewrite Content")
            st.markdown(input_example2, unsafe_allow_html=True)
            # rewrite_text = st.text_area("Rewrite Content", key = "rewrite_text", value = raw_input_example, height=500, label_visibility="collapsed")
        
        # with col3:
        #     st.write("Feedback")


        #     # Insert containers separated into tabs:
        #     tab1 = st.tabs(list_category)
        #     # with tab1:
        #     #     st.header("A cat")
        #     # tab2.write("this is tab 2")


        # Predict button
        if st.button("Predict"):
            if input_data:
                try:
                    # Send data to FastAPI backend
                    response = requests.post("http://localhost:8000/predict/", json={"input_data": input_data})
                    response.raise_for_status()
                    prediction = response.json().get("prediction")
                    st.write(f"Prediction result: {prediction}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter some input data.")


        st.dataframe(raw_json, use_container_width=True)
        # st.json(raw_json)

        


if __name__ == "__main__":

    st.set_page_config(layout="wide")
    st.markdown("""
            <style>
                mistake-type1 {
                    background-color: yellow;
                    color: black;
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 1rem;
                }
                mistake-type1-fix {
                    background-color: blue;
                    color: black;
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 1rem;
                }

                .div-style-textarea {
                    background-color:rgb(38, 39, 48);
                    color:rgb(250, 250, 250);
                    border-radius:2%; 
                    padding:1rem;
                    line-height:1.4;
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 1rem;
                }


                .tooltip {
                  position: relative;
                  /*display: inline-block; not necessary*/
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
                  /* Position the tooltip */
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
            """,unsafe_allow_html=True)

    main()
