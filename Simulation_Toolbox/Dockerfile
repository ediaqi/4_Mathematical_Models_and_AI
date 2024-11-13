# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install needed packages
RUN pip3 install catboost==1.2 geopandas==0.13.2 numpy==1.23.5 osmnx==1.5.1 pandas==2.0.0 session-info==1.0.0 jupyter-client==8.3.0 jupyter-core==5.3.1 jupyterlab==4.0.3 streamlit==1.26.0 geopy==2.3.0

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "run_app.py"]