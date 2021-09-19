# SITE AUTOPUPPETEER

## INSTALLATION ON WINDOWS

```
    python3 -m pip install --upgrade pip
    python3 -m venv .env
    .\.env\Scripts\activate.bat
    pip install -r requirements.txt
    python manage.py runserver
```


#### if you have problem see
- https://www.python.org/downloads/
- https://docs.python.org/3/library/venv.html
- https://docs.python.org/3/using/windows.html
- https://docs.python.org/3/using/unix.html


### INSTALLATION ON DOCKER

edit docker-compose.yml to change the exposed port
```
docker-compose -f docker-compose.yml up -d
```

### Google Spreedsheet
if you want to use googlesheet Datas
- create a Google project with Google sheet api
- create an Auth2 with url http://localhost/ if local or your url
- rename and store your Auth2 credentials.json  in this path AAPyppeteer/util/credentials.json
- the first time you run a project with a Google spreadsheet a pop-up will open to access the application
- login in 


### TODO
- add Data to  Documenation  and Exemple

## Download
See the [releases page](https://github.com/gquesnot/Site_AutoPyppeteer/releases) 
