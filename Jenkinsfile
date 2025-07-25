// 




pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
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

        stage('Debug Info') {
            steps {
                sh 'pwd && ls -la'
                sh 'git rev-parse --show-toplevel || echo "Not a Git repo"'
            }
        }
    }
}
