# src/app.py

import streamlit as st
import requests
import os

from content_check import check_content


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

    output_data = output_data.replace('$', '\$')
    output_data2 = output_data2.replace('$', '\$')
    return output_data, output_data2

def main():


    # Specify the directory you want to list
    directory = './openai_response/'

    # # List files in the directory
    # files = os.listdir(directory)

    # # Print the files
    # for file in files:
    #     print(file)




    # with open(directory +'test_res1.json') as f:
    #     raw_json = json.load(f)

    # with open(directory +'prompt.txt') as f:
    #     raw_prompt = f.read()
    #
    # with open(directory +'input.txt') as f:
    #     raw_input_example = f.read()


    # raw_json = check_content(raw_input_example)



    # input_example, input_example2 = gen_markdown_content(raw_input_example, raw_json)
    # list_category = gen_category_list(raw_json)
    # Initialize


    # Start writing
    st.title("Government Hackathon Project")

    # User input
    text_input = st.text_area('Input Example')
    text_input = '''
Energy consumption
Energy consumption measures the amount of energy used in the Australian economy. It includes 
energy consumed in energy conversion activities (such as electricity generation and petroleum 
refining), but nets off derived or secondary fuels produced domestically (such as electricity and refined 
oil products) to avoid double counting of energy. It is equivalent to total primary energy supply. It is 
equal to domestic production plus imports minus exports (and changes in stocks). Further detail is 
provided in Department of Climate Change, Energy, the Environment and Water (2023) Guide to the 
Australian Energy Statistics.
Energy consumption fell 0.1 per cent in 2021–22 to 5,762 petajoules, the third successive year of 
decline and down 7 per cent from the all-time peak of 6,188 petajoules reached in 2018-19. The drop 
in energy consumption from three years ago, 426 petajoules, is the same amount of energy obtained 
from filling a 55-litre tank of petrol 227 million times.
In 2021–22, the Australian economy grew 3.6 per cent to $2.2 trillion. Population grew 1.2 per cent to 
reach 26.0 million people.
    '''

    button = st.button("Rewrite Content")
    button = True
    if button:

        # st.markdown(input_example, unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        llm_output = check_content(text_input)
        col1.write("Original Content")
        col2.write("Rewrite Content")



        original_text, fixed_text = gen_markdown_content(text_input, llm_output)
        col1.markdown(original_text, unsafe_allow_html=True)
        col2.markdown(fixed_text, unsafe_allow_html=True)

        st.dataframe(llm_output, use_container_width=True)
            # st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">text</p>', unsafe_allow_html=True)
            # original_text = st.text_area("Original Content", key = "original_text", value = raw_input_example, height=500)


            # rewrite_text = st.text_area("Rewrite Content", key = "rewrite_text", value = raw_input_example, height=500, label_visibility="collapsed")
        
        # with col3:
        #     st.write("Feedback")


        #     # Insert containers separated into tabs:
        #     tab1 = st.tabs(list_category)
        #     # with tab1:
        #     #     st.header("A cat")
        #     # tab2.write("this is tab 2")


        # Predict button
        # if st.button("Predict"):
        #     if input_data:
        #         try:
        #             # Send data to FastAPI backend
        #             response = requests.post("http://localhost:8000/predict/", json={"input_data": input_data})
        #             response.raise_for_status()
        #             prediction = response.json().get("prediction")
        #             st.write(f"Prediction result: {prediction}")
        #         except requests.exceptions.RequestException as e:
        #             st.error(f"An error occurred: {e}")
        #     else:
        #         st.warning("Please enter some input data.")



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
    os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
    main()
