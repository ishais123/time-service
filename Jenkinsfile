podTemplate(containers: [
     containerTemplate(name: 'build', image: 'ishais/jenkins:v1', ttyEnabled: true, command: 'sleep 100000000000'),
     containerTemplate(name: 'deploy', image: 'dtzar/helm-kubectl', ttyEnabled: true, command: 'sleep 100000000000')
  ],
  volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')] )
  {
    node(POD_LABEL) {
        git branch: 'main',
        credentialsId: 'jenkins-user-github',
        url: 'https://github.com/ishais123/time-service.git'
        container('build') {
            stage('build') {
                IMAGE = "ishais/time-service"
                GIT_TAG = sh(returnStdout: true, script: "git tag --contains | head -1").trim()
                LATEST_TAG = "latest"

                if ( GIT_TAG ){
                      withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh "./build.sh ${IMAGE} ${GIT_TAG} ${USERNAME} ${PASSWORD}"
                      }
                }
                else{
                      withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh "./build.sh ${IMAGE} ${LATEST_TAG} ${USERNAME} ${PASSWORD}"
                      }
                }
            }
        }
        container('deploy') {
            stage('deploy') {
                NAMESPACE = 'moon'
                RELEASE = 'moon-release'
                VALUES_FILE = 'values.yaml'

                dir('deployment/moon-chart') {
                    if ( GIT_TAG ){
                        sh "helm upgrade --install ${RELEASE} .  -f ${VALUES_FILE} --set time.image.tag=${GIT_TAG} -n ${NAMESPACE} --create-namespace"
                    }
                    else{
                        sh "helm upgrade --install ${RELEASE} .  -f ${VALUES_FILE} --set time.image.tag=${LATEST_TAG} -n ${NAMESPACE} --create-namespace"
                    }
                }
            }
            stage('test') {
                // Stage Variables
                NAMESPACE = 'moon'
                SVC_NAME = 'moon-release-time'
                SVC_HOSTNAME = sh(returnStdout: true, script: "kubectl get services -n ${NAMESPACE} ${SVC_NAME} --output jsonpath='{.status.loadBalancer.ingress[0].hostname}'").trim()
                SVC_PORT = '8082'
                SVC_ROUTE = 'api/v1/time'

                if ( SVC_HOSTNAME ){
                   sh "curl ${SVC_HOSTNAME}:${SVC_PORT}/${SVC_ROUTE}"
                }
                else{
                    sh "sleep 100"
                    sh "curl ${SVC_HOSTNAME}:${SVC_PORT}/${SVC_ROUTE}"
                }
            }
        }
    }
  }