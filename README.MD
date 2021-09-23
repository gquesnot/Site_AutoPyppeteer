# SITE AUTOPUPPETEER


## INSTALLATION ON WINDOWS

```
    python3 -m pip install --upgrade pip
    python3 -m venv .env2
    .\.env2\Scripts\activate.bat
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

### Auth
- username: admin
- password: password


### Google Spreedsheet
See [installation](https://github.com/gquesnot/Site_AutoPyppeteer/blob/master/INSTALL_GOOGLE_API/INSTALL.MD)


### TODO
- add Data to  Documenation  and Exemple

## Download
See the [releases page](https://github.com/gquesnot/Site_AutoPyppeteer/releases)
