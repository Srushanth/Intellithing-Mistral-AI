# Use an official Python runtime as a parent image
FROM python:3.11

# The maintainer of the Dockerfile
LABEL authors="Srush"

# The port on which the Gradio server will run
ARG GRADIO_SERVER_PORT=7860
# Set the environment variable in the container
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

# Set the working directory in the container to /workspace
WORKDIR /workspace

# Copy the requirements file into the container at /workspace
COPY ["requirements.txt", "./"]
# Copy the model file into the container at /workspace/model_gguf/
COPY ["./model_gguf/*", "./model_gguf/"]
# Copy the main Python script into the container at /workspace/src/
COPY ["./src/*", "./src/"]

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE ${GRADIO_SERVER_PORT}

# Run main.py when the container launches
CMD ["python", "./src/main.py"]
