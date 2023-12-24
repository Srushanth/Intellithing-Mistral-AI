# Use an official Python runtime as a parent image
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

# The maintainer of the Dockerfile
LABEL authors="Srush"

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
EXPOSE 8080

# Run main.py when the container launches
CMD ["python", "./src/streamer.py"]
