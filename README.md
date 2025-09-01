# Binman Kai
This application runs a flask server which collects the rubbish colleection details from the east dumbartonshire website 
and displays that information on a template. This should be able to be set to a schedule to collect that information 
automatically.

## Install - Docker

### Download the latest release
You can find it [here](https://github.com/camcleod99/binman_kai/releases)

### Unzip archive into a folder of your choseing and open terminal to it

### Build the docker installation
```bash
docker compose build
```

### Run the Docker Compose file
```bash
docker compose up -d
```

### Navigate to the webapp
In your browser of choice go to <localhost>:7777

***Note:*** This port number is decided by the configuration in the docker-compose file in line 6. Should 7777 be ocupied, simply set the first number to your desired port.

## Install - Python virtual enviroment

### Clone and CD into project
```bash
git clone https://github.com/camcleod99/binman_kai.git
```
### Install python .venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### install requirements
```bash
pip install -r requirments.txt
```
### install bootstrap-flask
```bash
pip install -U bootstrap-flask
```
## Run
```bash
source ./.venv/bin/activate && python3 ./main.py
```
### Navigate to the webapp
In your browser of choice go to <localhost>:9595
It should initilise the instance and create an inital table
