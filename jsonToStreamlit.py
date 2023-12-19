import sys
sys.path.append('c:/Users/jerry/OneDrive/Desktop/codeWork/GamesDictionary')
import pandas as pd
import streamlit as st
from editJson.ReadJson import transformJson 
import json
from io import StringIO

uploadedGamesDictJson = st.file_uploader("Choose a Games dictionary JSON")


def on_click_callback():
    # Actions to perform when the button is clicked
    st.write("Button clicked!")

# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_excel().encode('utf-8')
# df =convert_df(df)

# st.download_button(
#     label="Download data as CSV",
#     data=df,
#     file_name='GamesFictionary.csv',
#     mime='text/csv/xlsx',
#     on_click=on_click_callback
# )



if uploadedGamesDictJson is not None:
    try:
        file_contents = uploadedGamesDictJson.getvalue()
        string_contents = file_contents.decode('utf-8')
        json_data = json.loads(string_contents)
        df = transformJson(json_data)

        @st.cache_data 
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv(index=False).encode('utf-8')
        df =convert_df(df)
        
        st.download_button(
            label="Download data as CSV",
            data=df,
            file_name='GamesDictionary.csv',
            mime='text/csv',
            on_click=on_click_callback
        )



        if df is not None:
            st.write(df)
        else:
            st.write("No data found in the uploaded file")
    except Exception as e:
            st.write(f"An error occurred: {e}")

else:
    st.write("Please upload a file.")


# with open(r'C:\Users\jerry\OneDrive\Desktop\codeWork\GamesDictionary\2024GamesReleases.json', 'r', encoding='utf-8') as gamesJson:
#     GamesDictionary = json.load(gamesJson)


# transformJson(GamesDictionary)