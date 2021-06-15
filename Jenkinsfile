podTemplate(containers: [
     containerTemplate(name: 'deploy', image: 'dtzar/helm-kubectl', ttyEnabled: true, command: 'sleep 100000000000'),
     containerTemplate(name: 'build', image: 'docker', ttyEnabled: true, command: 'sleep 100000000000')
  ],
  volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')] )
  {
    node(POD_LABEL) {
        git branch: 'main',
        credentialsId: 'jenkins-user-github',
        url: 'https://github.com/ishais123/moon.git'
        container('build') {
            stage('build') {
                sh "ls -la"

                GIT_TAG = sh(returnStdout: true, script: "git tag --contains | head -1").trim()

                if ( GIT_TAG ){
                    dir('time-service') {

                      sh "docker build --network host -t ishais/time-service:${GIT_TAG} ."
                      withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh "docker login -u='${USERNAME}' -p='${PASSWORD}'"
                        sh "docker push ishais/time-service:${GIT_TAG}"
                      }
                    }
                }
                else{
                    dir('time-service') {
                      sh "docker build --network host -t ishais/time-service:latest ."
                      withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh "docker login -u='${USERNAME}' -p='${PASSWORD}'"
                        sh "docker push ishais/time-service:latest"
                      }
                    }
                }
                sh "docker images"
            }
        }
        container('deploy') {
            stage('deploy') {
                sh "kubectl get nodes"
            }
        }
    }
  }