pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: ''
            }
        }

        stage('Instalar dependências') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Executar testes') {
            steps {
                sh './venv/bin/pytest tests/'
            }
        }

        stage('Gerar relatório de testes') {
            steps {
                sh './venv/bin/pytest tests/ --junitxml=tests/results.xml
                '
            }
        }

    }

    post {
        always {
            junit 'tests/results.xml'
        }
    }
}