pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'ravindra806'
        IMAGE_NAME = 'batch-job-d'
        TAG = "build-${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/myfirstgitravindra/batch-job-d'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG} .
                """
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'git-hub', passwordVariable: 'PWD', usernameVariable: 'USR')]) {
                    sh """
                    docker login -u $USR -p $PWD
                    docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh """
                kubectl --kubeconfig=/tmp/kubeconfig-jenkins.yaml delete job batch-job-d --ignore-not-found=true
                kubectl --kubeconfig=/tmp/kubeconfig-jenkins.yaml create job batch-job-d --image=${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}
                echo "Sucessfully deployed to Kubernetes!"
                kubectl --kubeconfig=/tmp/kubeconfig-jenkins.yaml get jobs
                kubectl --kubeconfig=/tmp/kubeconfig-jenkins.yaml get pods
                """
            }
        }
    }
}