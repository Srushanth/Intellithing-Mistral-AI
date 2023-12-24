# Introduction 🚀
---
## Overview 📝
---
This project aims to deploy a [Mistral AI model](https://huggingface.co/mistralai) from [Hugging Face](https://huggingface.co/docs/transformers/main/model_doc/mistral) in an [Amazon Elastic Kubernetes Service (EKS)](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html) environment, create an API for it, and use the API in a [Gradio](https://www.gradio.app/) interface to test the model interactively. The project also requires the solution to have minimal standby servers and scale automatically as the requests or load increases. The project was assigned on *__11-Dec-2023__*.

The *__Mistral AI model__* is a *__large language model with 7 billion parameters__* that can generate text for various tasks. The EKS environment is a managed service that simplifies the deployment and management of Kubernetes clusters on AWS. The Gradio interface is a web-based GUI that allows users to interact with the model easily. The project uses various AWS services and tools, such as `VSCode`, `AWS CLI`, `EKS`, `ECS`, `EC2`, `VPC`, `IAM`, `K9S`, `eksctl`, and `Terraform` to create and configure the resources needed for the project.

## Project Structure 🗂
---
```
.
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── aws
│   ├── 2048-pod.yaml
│   ├── del-LoadBalancer.yaml
│   ├── del-deployment.yaml
│   ├── deployment.yaml
│   ├── full.yaml
│   ├── iam_policy.json
│   ├── mygame-svc.yaml
│   ├── sample.yml
│   └── service.yaml
├── data
│   └── raw
│       └── Aurelien-Geron-Hands-On-Machine-Learning-with-Scikit-Learn-Keras-and-Tensorflow_-Concepts-Tools-and-Techniques-to-Build-Intelligent-Systems-OReilly-Media-2019.pdf
├── docs
│   ├── Introduction.md
│   └── index.md
├── mkdocs.yml
├── model_gguf
│   └── mistral-7b-instruct-v0.1.Q5_K_M.gguf
├── notebooks
│   ├── 1.download-model.ipynb
│   ├── 1.gguf_model.ipynb
│   ├── 1.guff-gradio.ipynb
│   ├── 1.init.ipynb
│   ├── gptq.ipynb
│   ├── streamer.ipynb
│   └── test.ipynb
├── requirements.txt
├── simple-bank
│   ├── deployment.yaml
│   └── service.yaml
└── src
    ├── __init__.py
    ├── flagged
    ├── main-stream.py
    ├── main.py
    └── streamer.py
```

## Clone and manage the repository 🛠
---
1. Clone the repository to your local machine by running `git clone https://github.com/Srushanth/Intellithing-Mistral-AI`. 🖥
1. Create a new branch for your feature or bug fix by running `git checkout -b <branch_name>`. 🌿
1. Make your changes to the code and test them locally. 🧪
1. Commit your changes to the branch by running `git add .` and `git commit -m "<commit_message>"`. 
    * **Note:** Use a meaningful and descriptive commit message that explains why you made the changes. 💬
1. Push your branch to the remote repository by running `git push origin <branch_name>`. 🚀
1. Create a pull request to merge your branch to the master branch. 
    * **Note:** Use a clear and concise title and description for your pull request and assign a reviewer to approve it. 🙋‍♂️
1. Wait for the reviewer to review your code and provide feedback. If there are any issues or suggestions, make the necessary changes and push them to the branch. 🔄
1. Once the reviewer approves your pull request, merge it to the master branch. 🎉

