pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "sincere-blade-454507-s9"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo'){
            steps{
                echo 'Cloning Github repo to Jenkins ...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/kunjesh04/Hotel-Reservation-Prediction.git']])
            }
        }
        
        stage('Setting up venv'){
            steps{
                echo 'Setting virtual environment and installing dependencies ...'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
        
        stage('Building Docker img and pushing to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building Docker image and pushing to GCR ...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/hotel-res-pred:latest .

                        docker push gcr.io/${GCP_PROJECT}/hotel-res-pred:latest

                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploying to Google Cloud Run ...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy hotel-res-pred \
                            --image=gcr.io/${GCP_PROJECT}/hotel-res-pred:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated

                        '''
                    }
                }
            }
        }
    }
}