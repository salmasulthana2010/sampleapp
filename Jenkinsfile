pipeline {
    agent any

    parameters {
        choice(name: 'BRANCH', choices: ['dev', 'qa'], description: 'Choose a branch to deploy')
    }

    environment {
        REPO_URL = 'https://github.com/YOUR-USERNAME/sample-deploy-project.git'  // 🔁 CHANGE this
        TARGET_SERVER = 'ec2-user@<your-ec2-public-ip>'                           // 🔁 CHANGE this
        SSH_KEY = '/var/lib/jenkins/.ssh/id_rsa'                                  // Jenkins key to SSH
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${params.BRANCH}", url: "${env.REPO_URL}"
            }
        }

        stage('Build') {
            steps {
                echo "Building from branch ${params.BRANCH}"
                sh 'ls -l'
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo "Deploying to EC2: ${TARGET_SERVER}"
                sh """
                    chmod 600 ${SSH_KEY}
                    scp -i ${SSH_KEY} -o StrictHostKeyChecking=no -r index.html deploy.sh ${TARGET_SERVER}:/home/ec2-user/${params.BRANCH}_site/
                    ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${TARGET_SERVER} "bash /home/ec2-user/${params.BRANCH}_site/deploy.sh ${params.BRANCH}"
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment to ${params.BRANCH} succeeded!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
