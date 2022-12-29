pipeline {
  agent any
  stages {
    
    stage("Pull") {
      steps {
        echo 'Pulling form GitHub'
      }
    }
    
    stage("Building") {
      steps {
        echo 'Building Image'
      }
    }
    
    stage("Push") {
      steps {
        echo 'Pushing Image to ECR'
      }
    }
  }
}
    
