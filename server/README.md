# Server

Server is an Express node appliction that persists biometric data sent by the VideoBiometrics **collector** application. 
Additionally **server** hosts the **webclient** application that graphically displays biometric data. 

Note that as proof-of-concept application, **server** is missing features that would be required in production such as authentication and encryption

## Pre-requisites
1) Node. **Server** is Node application and requires Node version 10.16.0, (or later). It is recommended that the node version manager
**nvm** is used.
2) MySql. **Server** uses a MySql database to persist the biometric data
3) A schema in the database, named **video_biometrics**

## Installation steps
1) Copy the config_sample.json file to config.json and complete the database credentials 

    `VideoBiometrics/server/config $ cp config_sample.json config.json`
2) Edit the 'username', 'password', 'database' and 'host' in all configurations
3) Install the dependencies

    `VideoBiometrics/server $ yarn install`
4) Create a folder 'public_react' that will contain the **webclient** application

    `VideoBiometrics/server $ mkdir public_react`
5) Complete building the webclient application then copy the build folder to the public_react folder

    `VideoBiometrics/server/public_react $ cp ../../webclient/build build`
6) To run on port 80
    
    `VideoBiometrics/server $ sudo PORT=80 node bin/www`


