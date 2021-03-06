# short.ly
Flask URL shortening service with simple API and sqlite database backend.

![Main page](.imgs/shortly.png)
![Example URL](.imgs/shortly-example.png)

## Run

### Local
```shell script
# install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# optional configuration
export SHORTLY_DB_PATH=/tmp/db.sqlite

# run
export FLASK_APP="shortly"
flask init-db
flask run
# OR
gunicorn -b 127.0.0.1:5000 "shortly:create_app()"
```

## TODO
* [ ] add mysql support (already partially implemented)
* [ ] add pytest test suite for flask (test index page and API)