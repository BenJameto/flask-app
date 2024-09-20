pipeline {
    agent any

    environment {
        FLASK_IMAGE = "benjameto/ejemplofeatures-flask-app"
        POSTGRES_IMAGE = "postgres:13"
        KUBERNETES_NAMESPACE = "flask-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Flask Docker Image') {
            steps {
                script {
                    docker.build("${FLASK_IMAGE}:${BUILD_NUMBER}", "-f Dockerfile.flask .")
                }
            }
        }

        stage('Push Flask Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("${FLASK_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${FLASK_IMAGE}:${BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh "kubectl config use-context minikube"
                    sh "kubectl apply -f k8s/manifests/postgres-manifest.yaml -n ${KUBERNETES_NAMESPACE}"
                    sh "kubectl apply -f k8s/manifests/flask-app-manifest.yaml -n ${KUBERNETES_NAMESPACE}"
                    sh "kubectl set image deployment/flask-app flask-app=${FLASK_IMAGE}:${BUILD_NUMBER} -n ${KUBERNETES_NAMESPACE}"
                }
            }
        }
    }
}