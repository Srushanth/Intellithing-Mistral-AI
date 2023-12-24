# Project Setup 🚀
---
In this project, we will use VSCode, Anaconda, AWS CLI, AWS ECR, and AWS EKS to deploy a Mistral AI model from Hugging Face. Here are the steps to set up the project:
## Setup SSH in VSCode 🔑
---
To connect to the remote server using SSH, we need to add the following property to the `~.ssh/config` file on our local machine:
```properties
Host dev-gpu
    HostName ec2-16-16-76-171.eu-north-1.compute.amazonaws.com
    User ubuntu
    IdentityFile C:\Users\Srush\Downloads\dev-pem.pem
```
This will allow us to use the `dev-gpu` alias to access the server.

## Install Anaconda 🐍
---
To install Anaconda, a Python distribution that comes with many useful packages and tools, we need to run the following commands on the server:
```bash
curl -O https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
bash ./Anaconda3-2023.09-0-Linux-x86_64.sh
rm -f Anaconda3-2023.09-0-Linux-x86_64.sh
```
This will download, install, and remove the Anaconda installer script.

## Setup AWS CLI ☁️
---
To interact with AWS services from the command line, we need to install and configure the AWS CLI. We can do that by running the following commands on the server:
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws configure
```
This will download, unzip, install, and configure the AWS CLI. We will need to provide our AWS access key ID, secret access key, default region, and default output format.

### Login to AWS ECR 🐳
To push and pull Docker images from the AWS Elastic Container Registry (ECR), we need to login to the ECR service using the AWS CLI. We can do that by running the following command on the server:
```bash
aws --region <region> ecr get-login-password | docker login --username AWS --password-stdin <Account ID (12 digits)>.dkr.ecr.<region>.amazonaws.com
```
This will generate a login password and use it to authenticate with the ECR service. We will need to replace `<region>` and `<Account ID (12 digits)>` with our own values.

### Login to AWS EKS 🌐
To manage our Kubernetes cluster on the AWS Elastic Kubernetes Service (EKS), we need to login to the EKS service using the AWS CLI. We can do that by running the following command on the server:
```bash
aws eks --region <region> update-kubeconfig --name <cluster-name>
```
This will update our kubeconfig file with the EKS cluster information. We will need to replace `<region>` and `<cluster-name>` with our own values.

That’s it! We have successfully set up the project. We can now proceed to the next steps. 😊
