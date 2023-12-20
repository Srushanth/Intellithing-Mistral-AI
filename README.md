# Intellithing-Mistral-AI

1. docker build -t intellithing .
1. docker tag intellithing:latest 926015110176.dkr.ecr.eu-north-1.amazonaws.com/intellithing:latest
1. docker push 926015110176.dkr.ecr.eu-north-1.amazonaws.com/intellithing:latest
2. eksctl create cluster --name intellithing --region eu-north-1 --fargate
3. aws eks update-kubeconfig --name intellithing --region eu-north-1
4. eksctl create fargateprofile --cluster intellithing --region eu-north-1 --name intellithing-app --namespace intellithing
5. C:\GitHub\Intellithing-Mistral-AI\aws>kubectl apply -f full.yaml
6. kubectl get pods -n intellithing-namespace
7. kubectl get pods -n intellithing-namespace -w



- eksctl create cluster --name demo-cluster --region eu-north-1 --fargate
  - eksctl delete cluster --name demo-cluster --region eu-north-1
- aws eks update-kubeconfig --name demo-cluster --region eu-north-1
- eksctl create fargateprofile --cluster demo-cluster --region eu-north-1 --name alb-sample-app --namespace game-2048
- kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml
- kubectl get pods -n game-2048
- kubectl get svc -n game-2048
- kubectl get ingress -n game-2048
- eksctl utils associate-iam-oidc-provider --cluster demo-cluster --approve
- curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json
- aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document iam_policy.json
- eksctl create iamserviceaccount --cluster=demo-cluster --namespace=kube-system --name=aws-load-balancer-controller 
  --role-name AmazonEKSLoadBalancerControllerRole 
  --attach-policy-arn=arn:aws:iam::926015110176:policy/AWSLoadBalancerControllerIAMPolicy --approve 
  --override-existing-serviceaccounts
- helm repo add eks https://aws.github.io/eks-charts
- helm repo update eks
- helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=demo-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller --set region=eu-north-1 --set vpcId=vpc-078a05822c6741d31
- kubectl get deployment -n kube-system aws-load-balancer-controller
- kubectl get pods -n kube-system
- kubectl get deployment -n kube-system aws-load-balancer-controller
- kubectl get pods -n kube-system
- kubectl get ingress -n game-2048




## Model Download
curl -L https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q5_K_M.gguf --output mistral-7b-instruct-v0.1.Q5_K_M.gguf

## Authenticate for pushing the Docker image to AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin 926015110176.dkr.ecr.eu-north-1.amazonaws.com