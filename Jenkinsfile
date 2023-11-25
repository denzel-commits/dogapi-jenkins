pipeline{
    agent {
        node{
            label 'docker-agent-python311'
        }
    }
    environment{
        PYTHONPATH = "${WORKSPACE}"
    }
    stages{
        stage("Build"){
            steps{
                echo "Building..."
                sh 'pip install -r requirements.txt'
            }
        }
        stage("Test"){
            steps{
                echo "Testing..."
                sh 'python -m pytest -n=2 --tb=line'
            }
        }
    }
    post{
        always{
                allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'target/allure-results']]
                ])
        }
    }
}
