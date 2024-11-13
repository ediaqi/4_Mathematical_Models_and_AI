# Simulation Toolbox

The simulation tool was developed with [Streamlit](https://streamlit.io/) and [Docker](https://www.docker.com/).

[Streamlit](https://streamlit.io/) is a Python library designed for creating interactive web applications and dashboards with ease. It streamlines the process of turning data scripts into shareable web apps, making it an excellent choice for data scientists and developers. With Streamlit, you can quickly add interactive widgets and visualizations to your apps, simplifying the development of data-driven web applications.

[Docker](https://www.docker.com/) is a platform that simplifies the process of developing, packaging, and deploying applications inside containers, providing consistency across different environments. Containers encapsulate an application and its dependencies, enabling developers to create, test, and deploy applications in a predictable and isolated manner. Docker has become a cornerstone of modern application development, making it easier to build and deploy applications seamlessly across diverse computing environments.

## Tool Access

To access the tool, simply visit https://iaq-simulator.know-center.at/ in your web browser. No installation or downloads are required, and it is accessible from any device with an internet connection. The user interface is designed to be intuitive and user-friendly, featuring various input fields and sliders to answer the questions. The data given is treated with confidentiality and is not shared with third parties. Lastly, there is a “PREDICT” button for activating calculations and getting results for the PM2.5 and NO2 levels in the user's household. The current demo version works only for a specific area in Copenhagen, Denmark. An example of valid address to enter into the tool is Rådmandsgade 40, 2200, Denmark.

## Tool Overview
 
In the first section, called “Answer the following questions”, there are different subsections A - E where answers are required.
In subsection A a valid address must be entered. The calculations with “PREDICT” button will only work if a valid address is entered, otherwise an error message “Please input your valid address.” will be displayed. The address is not case sensitive.
 
Other questions in subsection A relate to the construction year, floor level and total household area. Answers can be manually entered or with the help of plus sign. The question mark sign shows required format for the construction year (YYYY), and that total area should be in square meters. 
In subsections B and C, the slider needs to be pulled to the right up to a wished number of days of use.
In subsection C, a checkbox needs to be checked if a carpet is present in the household, otherwise it should remain unchecked.
In subsection E, the slider needs to be pulled to the right up to a wished number of days of smoking.

In the second section called “Predict NO2 and PM2.5 concentration in your household” button “PREDICT” needs to be pressed to start the calculations. If a valid address is entered, the concentrations of NO2 and PM2.5 will be displayed.

## GitHub Repository Overview

The tool was developed within EDIAQI project using the code available here in this GitHub folder. If you use this code please consider citing EDIAQI project.

    .
    ├── .streamlit/           # Includes configuration file, config.toml, where the appearance of the app is customized
    ├── Pachage/              # Includes python scripts where all needed functions for run_app.py defined
    ├── Dependencies.txt      # Required packages for the application to run
    ├── Dockerfile            # Set of instructions for building a Docker image
    ├── No2_model             # Pretrained model for NO2 prediction
    ├── pm25_model            # Pretrained model for PM2.5 prediction
    ├── README.md             # Repository description
    └── run_appy.py           # Main streamlit file for execution

## Building the Simulation Toolbox

When located in this folder run the following lines to build the application:

> sudo docker build -t streamlit-app .

> sudo docker run -d -p 8501:8501 streamlit-app

