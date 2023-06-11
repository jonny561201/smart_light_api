#!/usr/bin/env bash

YELLOW='\033[1;33m'
WHITE='\033[0m'
RED='\033[0;31m'

SMART_LIGHT_SERVICE_FILE=smartLight.service


function cloneServiceFiles {
    if [[ -d "/home/pi/smart_light_api" ]]; then
        echo -e "${YELLOW}---------------Service Folder Exists---------------${WHITE}"
        cd /home/pi/smart_light_api
        git pull
    else
        echo -e "${YELLOW}---------------Cloning Service---------------${WHITE}"
        cd /home/pi/
        git clone https://github.com/jonny561201/smart_light_api.git /home/pi/smart_light_api
    fi
}

function startVirtualEnv {
    if [[ ! -d "/home/pi/smart_light_api/venv" ]]; then
      echo -e "${YELLOW}----------Creating VirtualEnv----------${WHITE}"
      pushd "/home/pi/smart_light_api"
      pip3 install virtualenv
      python3 -m virtualenv venv
      popd
    fi
      echo -e "${YELLOW}---------------starting VirtualEnv---------------${WHITE}"
      source ./venv/bin/activate
}

function installDependencies {
    echo -e "${YELLOW}---------------Installing Dependencies---------------${WHITE}"
    pip3 install -Ur requirements.txt
}

function stopService {
    echo -e "${YELLOW}---------------Stopping Service---------------${WHITE}"
    sudo systemctl stop ${SMART_LIGHT_SERVICE_FILE}
    sudo rm /lib/systemd/system/${SMART_LIGHT_SERVICE_FILE}
}

function copyServiceFile {
    echo  -e "${YELLOW}---------------Creating SystemD---------------${WHITE}"
    sudo chmod 666 ${SMART_LIGHT_SERVICE_FILE}
    sudo yes | sudo cp ./deployment/${SMART_LIGHT_SERVICE_FILE} /lib/systemd/system/${SMART_LIGHT_SERVICE_FILE}
}

function configureSystemD {
    echo  -e "${YELLOW}---------------Configuring SystemD---------------${WHITE}"
    sudo systemctl daemon-reload
    sudo systemctl enable ${SMART_LIGHT_SERVICE_FILE}
}

function migrateDatabase {
    echo  -e "${YELLOW}---------------Migrating Database---------------${WHITE}"
    python3 -m yoyo apply -b --database postgresql://${DB_USER}:${DB_PASS}@localhost:${DB_PORT}/${DB_NAME} ./sql/migration/
}

function restartDevice {
    echo  -e "${YELLOW}---------------Rebooting Device---------------${WHITE}"
    sudo reboot
}

function createEnvironmentVariableFile {
    if [[ ! -f "/home/pi/smart_light_api/serviceEnvVariables" ]]; then
        echo -e "${YELLOW}---------------Creating Environment Variable File---------------${WHITE}"
        createFile
    else
        echo -e "${YELLOW}---------------Environment Variable File Already Exists---------------${WHITE}"
        echo 'Would you like to recreate serviceEnvVariables file? (y/n)'
        read USER_RESPONSE
        if [[ ${USER_RESPONSE} == "y" ]]; then
            createFile
        fi
    fi
    echo -e "${YELLOW}---------------Exporting Environment Variables---------------${WHITE}"
    set -o allexport; source ./serviceEnvVariables; set +o allexport
}

function createFile {
    echo -e "Enter Database Username:${WHITE}"
    read SQL_USER
    echo -e "Enter Database Password:${WHITE}"
    read SQL_PASS
    echo -e "Enter Database Name:${WHITE}"
    read SQL_DB
    echo -e "Enter Database Port:${WHITE}"
    read SQL_PORT
    echo -e "Enter Smart Light API Key:${WHITE}"
    read LIGHT_API_USER

    echo "DB_USER=${SQL_USER}" >> serviceEnvVariables
    echo "DB_PASS=${SQL_PASS}" >> serviceEnvVariables
    echo "DB_NAME=${SQL_DB}" >> serviceEnvVariables
    echo "DB_PORT=${SQL_PORT}" >> serviceEnvVariables
    echo "API_KEY=${LIGHT_API_KEY}" >> serviceEnvVariables
}


stopService
cloneServiceFiles
startVirtualEnv
installDependencies
createEnvironmentVariableFile
migrateDatabase
copyServiceFile
configureSystemD
restartDevice