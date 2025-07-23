pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Cloning from Github Repo') {
            steps {
                script {
                    echo 'Cloning from Github Repo.....'
                    checkout scmGit(branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'mlops-github-token',
                            url: 'https://github.com/MaheshJakkala/MLOPs-Project.git'
                        ]])
                }
            }
        }

        stage('Install Python') {
            steps {
                script {
                    echo 'Installing Python...'
                    sh '''
                        sudo apt-get update
                        sudo apt-get install -y python3 python3-venv python3-pip
                        ln -s /usr/bin/python3 /usr/bin/python || true
                    '''
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setup Virtual Environment......'
                    sh """
                        python -m venv ${VENV_DIR}
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
    }
}
