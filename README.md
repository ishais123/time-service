# Moon Helm-Chart CI/CD 

Build & Deploy Moon Helm-Chart over EKS cluster using Jenkins CI/CD Pipeline   

## Clone Repository
git clone https://github.com/ishais123/time-service.git

## Requirements

| Name | Version |
|------|-------------|
| <a name="eksctl"></a> [kubectl](kubectl) | 1.19.7 
| <a name="eksctl"></a> [eksctl](eksctl) | 0.40.0 
| <a name="AWS CLI"></a> [AWSCLI](AWSCLI) | 2 
| <a name="Helm"></a> [Helm](Helm) | 3.4.2 
| <a name="git"></a> [git](git) | 2.23.0

## EKS setup
```bash
// Use default aws profile by default, you can change it with --profile flag
// You can modify cluster configuration in deployment/eksctl.yaml file

eksctl create cluster -f deployment/eksctl.yaml 
aws eks  update-kubeconfig --name <cluster-name> --region <aws-region>
```
## Jenkins setup
```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update

kubectl create namespace jenkins
kubectl apply -f deployment/jenkins/jenkins-volume.yaml -n jenkins
kubectl apply -f deployment/jenkins/jenkins-sa.yaml -n jenkins
helm install jenkins -n jenkins -f values.yaml jenkins/jenkins
```
## Build locally
```bash
docker build -t ishais/time-service:local .
docker login -u=<docker hub username> -p=<docker hub password>
docker push  ishais/time-service:local
```
## Deploy locally
```bash
// You can customize the values.yaml file as you want

cd deployment/moon-chart
helm upgrade --install <release-name> .  -f values.yaml -n <namespace> --create-namespace
```
## Jenkins Pipeline
```bash
// Get Jenkins admin password 

printf $(kubectl get secret --namespace jenkins jenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode);echo

// Kubernetes plugin required

// You have to configure 2 Credentials: 
1) jenkins-user-github - github username & password
2) docker-hub-cred - docker-hub username & password

// In each pipelime you define you need to mark 2 checkbox under build trigger:
1) GitHub hook trigger for GITScm polling
2) Poll SCM

// You must configure Github repository setting (URL, creds, Jenkinsfile location) in the pipeline configuration

// There is github webhook in repo which trigger the pipeline each push event
```
## Push Changes 
```bash
// Use tag to push new changes

git init .
git remote add origin <repo URL>
git add .
git commit -a -m "first commit by me"
git pull origin main
git tag <tag value>
git push -f origin main --tags <tag value>

// It will trigger the Pipeline using webhook

```


## License
