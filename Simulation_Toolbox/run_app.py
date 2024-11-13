# Import libraries
import pandas as pd
from datetime import datetime
from Pachage.geo1 import extrapoltion_one
from catboost import CatBoostRegressor
import streamlit as st

st.set_page_config(page_title="IAQ Simulator")

# Import pretrained models for NO2 and PM2.5
# NO2
from_file = CatBoostRegressor()
No2_model=from_file.load_model("No2_model")
# PM2.5
from_file = CatBoostRegressor()
pm25_model=from_file.load_model("pm25_model")


# Define time
time = datetime.today().isocalendar()
week_chem=time.week


# EDIAQI logo
sidebar_css = """
                <style>
                    #logo 
                    {
                        position: absolute;
                        bottom: 20px;
                    }
                </style>
              """
st.sidebar.markdown(sidebar_css, unsafe_allow_html=True)

logo_html = """
                <div id="logo">
                    <img src="https://ediaqi.eu/themes/custom/ediaqi01/images/ediaqi-logo-light.svg" alt="Logo">
                </div>
            """
st.sidebar.markdown(logo_html, unsafe_allow_html=True)


# EU and CC
sidebar_css = """
                <style>
                    [data-testid=stSidebar] [data-testid=stImage]
                    {
                        text-align: left;
                        display: block;
                        width: 30%;
                    }
                    .big-font
                    {
                        font-size:11px;
                    }
                </style>
              """
st.sidebar.markdown(sidebar_css, unsafe_allow_html=True)

st.sidebar.image("https://ediaqi.eu/themes/custom/ediaqi01/images/europe-flag.png")
st.sidebar.markdown('<p class="big-font">This project has received funding from the European Union’s Horizon Europe research and innovation programme under the grant agreement No. 101057497</p>', unsafe_allow_html=True)   
st.sidebar.image("https://ediaqi.eu/themes/custom/ediaqi01/images/cc-by.svg")


# Intro
st.write("Welcome to EDIAQI public simulation tool!")
st.write("Here, you have the opportunity to assess your indoor NO₂ and PM2.5 risk based on your location and additional household information.")


# Define questions
with st.container():
    st.header("1. Answer the following questions")
    # Household general information
    with st.container():
        st.subheader('A. Household general information')
        address = st.text_input("What is your address?", placeholder="address, postal code, country") # currently available 2200 Denmark, e.g. "rådmandsgade 40, 2200, denmark"
        construction_year = st.number_input("What is the year of construction of your household?", min_value=0, help="YYYY")
        floor_level = st.number_input("On which floor level are you located?", min_value=0)
        area = st.number_input("What is the total area of your household?", min_value=0, help='m' + '\u00B2')
    # Cooking
    with st.container():
        st.subheader('B. Cooking')
        #gasstove = st.selectbox("How many days a week do you use the gas stove?", options=list(range(8)))
        gasstove = st.slider("How many days a week do you use the gas stove?", min_value=0, max_value=7, step=1)
        cookerhood = st.slider("How many days a week do you use the cooker hood?", min_value=0, max_value=7, step=1)
    # Fireplace
    with st.container():
        st.subheader('C. Fireplace')
        fireplace = st.slider("How many days a week do you use the fireplace?", min_value=0, max_value=7, step=1)
    # Carpet
    with st.container():
        st.subheader('D. Carpet')
        #carpet = st.selectbox("Do you have a carpet?", [0,1], help="0 = NO, 1 = YES")
        st.write("Do you have a carpet?")
        carpet_yes = st.checkbox('YES')
        if carpet_yes:
            carpet = 1
        else:
            carpet = 0
    # Smoking
    with st.container():
        st.subheader('E. Smoking')
        smoking = st.slider("How many days a week do you smoke indoors?", min_value=0, max_value=7, step=1)


# From questions answers define features data frames for NO2 and PM2.5 prediction
dataframe_no2 = pd.DataFrame({"floor_level":[floor_level],"constrution_year":[construction_year],"area":[area],"passive_smoke":[smoking*52.1429],"carpet":[carpet],"cookerhood":[cookerhood*52.1429],"gasstove":[gasstove*52.1429],"fireplace":[fireplace*52.1429],"week_chem":[week_chem]})

dataframe_pm25 = pd.DataFrame({"floor_level":[floor_level],"constrution_year":[construction_year],"area":[area],"passive_smoke":[smoking*52.1429],"carpet":[carpet],"cookerhood":[cookerhood*52.1429],"gasstove":[gasstove*52.1429],"fireplace":[fireplace*52.1429],"week_pm":[week_chem]})


# Predict NO2 and PM2.5 concentration
with st.container():
    st.header("2. Predict NO\u2082 and PM2.5 concentration in your household")
    with st.container():
        if st.button("PREDICT"):
            #try:
            geo=extrapoltion_one(address,10**6)
            dataframe_no2 = pd.concat([geo, dataframe_no2], axis=1)
            dataframe_pm25 = pd.concat([geo, dataframe_pm25], axis=1)

            left_e, right_e = st.columns((2, 2))
            with left_e:
                with st.container():
                    st.subheader("NO\u2082")
                    st.subheader(f"{str(No2_model.predict(dataframe_no2)[0].round(1))} µg/m³")
            with right_e:
                with st.container():
                    st.subheader("PM2.5")
                    st.subheader(f"{str(pm25_model.predict(dataframe_pm25)[0].round(1))} µg/m³")
            #except:
            #    st.write("Please input your valid address.")

                    