// 




pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        DOCKERHUB_CREDENTIAL_ID = 'mlops-dockerhub'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'maheshjakkala/prediction-mlops-app'
    }

    stages {
        // stage('Cloning Github Repo') {
        //     steps {
        //         script {
        //             echo 'Cloning Github Repo......'
        //             checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'mlops-github-token', url: 'https://github.com/MaheshJakkala/MLOPs-Project.git']])
        //         }
        //     }
        // }
        stage('Fix Git Safe Directory') {
            steps {
                sh 'git config --global --add safe.directory /var/jenkins_home/workspace/MLOPs'
            }
        }
        stage('Check Python Version and ensurepip') {
            steps {
                sh '''
                    echo "=== Python Version ==="
                    python3 --version || echo "python3 not found"

                    echo "=== Python Location ==="
                    which python3 || echo "python3 not found"

                    echo "=== ensurepip Check ==="
                    python3 -m ensurepip --version || echo "ensurepip not available"
                '''
            }
        }


        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setup Virtual Environment......'
                    sh """
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    """
                }
            }
        }

        stage('Linting Code') {
            steps {
                script {
                    echo 'Linting Code.....'
                    sh """
                        . ${VENV_DIR}/bin/activate
                        pylint application.py main.py --output=pylint-report.txt --exit-zero || echo 'pylint stage completed'
                        flake8 application.py main.py --ignore=E501,E302 --output-file=flake8-report.txt || echo 'flake8 stage completed'
                        black application.py main.py || echo 'Black stage Completed'
                    """
                }
            }
        }

        stage('Trivy Scanning') {
            steps {
                script {
                    echo 'Trivy Scanning.......'
                    sh "trivy fs ./ --format table -o trivy-fd-report.html"                
                }
            }
        }
        stage('Building Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image.......'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")              
                }
            }
        }
        stage('Scanning Docker Image') {
            steps {
                script {
                    echo 'Docker Image Scanning.......'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-scan-report.html"             
                }
            }
        }

        stage('Pushing Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image.......'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}" , "${DOCKERHUB_CREDENTIAL_ID}"){
                        dockerImage.push('latest')
                    }
            }
        }
        

        // stage('Debug Info') {
        //     steps {
        //         sh 'pwd && ls -la'
        //         sh 'git rev-parse --show-toplevel || echo "Not a Git repo"'
        //     }
        // }
    }
}
