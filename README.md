# Binman Kai
This application runs a flask server which collects the rubbish colleection details from the east dumbartonshire website 
and displays that information on a template. This should be able to be set to a schedule to collect that information 
automatically.

## Install
### Please note - Bootstrap Flask
I use bootstrap-flask to allow use of bootstrap5 with this project. This has a noted history of being a right pain and 
I appologise for that. Most IDEs will complain about the lack of the defunct flask-bootstrap and cause nonsense as a 
result.

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
Then open your browser to 
http://127.0.0.1:9090
It should initilise the instance and create an inital table