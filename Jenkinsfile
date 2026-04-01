pipeline {
    agent any
    environment {
        // Global environment variable
        GitPush = 'true'
    }
    triggers {
        // Run daily at 1:00 AM Github server time
        cron('H 0 * * *') 
    }
    options {
        // Required to clean before the default SCM checkout
        skipDefaultCheckout(true) 
    }
    stages {
        stage('Clean') {
            steps {
                cleanWs() // Clean the workspace
            }
        }
        stage('Git Checkout') {
            steps {
                // The pipeline automatically checks out code if configured as Pipeline script from SCM'
                git branch: 'main', url: 'https://github.com/luckxander/shop'
            }
        }
        stage('Update HTML') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    // Execute the Python script and print real time output to console
                    bat 'python -u C:\\Python\\shop\\main.py'
                }
            }
        }
        stage('Run Python Script') {
            steps {
                // Automatically aborts after 1 minute
                timeout(time: 1, unit: 'MINUTES') {
                    // Execute the Python script and print real time output to console
                    bat 'python -u C:\\Python\\shop\\main.py'
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    // ... (perform local changes and commit as shown above) ...
                    bat 'echo "Modified at $(date)" >> version.txt'
                    bat 'git config user.name "luckxander"'
                    bat 'git config user.email "lusenabh@gmail.com"'
                    bat 'git add .'
                    bat 'git commit -m "Automatic commit from pipeline [ci skip]"'
                    // Use the dedicated gitPush step
                    // 'scm' refers to the SCM configuration used in the initial checkout
                    gitPush(gitScm: scm, targetBranch: 'main', targetRepo: 'origin')
                }                            
            }

        }
    }
    post {
        always {
            script {
                if (currentBuild.result == 'SUCCESS') {
                    echo 'Build successful! It will send an email'
                    emailext (
                                subject: "Success: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                                body: "Build successful! View the details at: https://luckxander.github.io/shop/",
                                to: "lusenabh@gmail.com",
                                recipientProviders: [
                                    culprits(), 
                                    requestor()
                                ]
                    )
                } 
                else if (currentBuild.result == 'FAILURE') {
                    echo 'Build failure! It will send an email'
                    emailext (
                                subject: "Build Failed: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                                body: "Build failed. Check the console output here: https://luckxander.github.io/shop/",
                                to: "lusenabh@gmail.com",
                                recipientProviders: [
                                    culprits(), 
                                    requestor()
                                ]
                    )
                } 
                else {
                    echo "Build finished with an unusual result: ${currentBuild.result}. It will send "
                    emailext (
                                subject: "Unusual build result: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                                body: "Build finished with an unusual result. Check the console output here: https://luckxander.github.io/shop/",
                                to: "lusenabh@gmail.com",
                                recipientProviders: [
                                    culprits(), 
                                    requestor()
                                ]
                    )                    
                }
            }
        }
    }
}