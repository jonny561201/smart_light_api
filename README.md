# Tuya Smart Light API

### Developed to integrate with my home automation and control individual switches rather than smart lights
### Works with Tuya Devices (GHome, TREATLIFE, MOES, OHMAX, etc)

- a simple Python Flask API 
- manages the list of devices with an Postgres Db
- integrates with registered Tuya smart devices
  - currently only works with Outlet Device types
  - turn lights on/off
  - return status of existing device
  - organize devices into groups



### Development
- must have Docker Desktop or equivalent container tool
  - start docker ```docker compose up```
  - utilizes Postgres database
  - execute sql table migrations using Flyway
- install dependencies
  - ```pip install -r requirements.txt```
  - ```pip install -r requirements_test.txt```
- start app ```python app.py```
- create a settings.json file for config (example below)
  - "development": true,
  - "dbName": "smart_lights",
  - "dbPort": 5433,
  - "dbUser": "postgres",
  - "dbPass": "password"