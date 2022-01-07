# Machine Learning model microservice

## Run it

### Dependencies

Create virtual environment with pipenv.

```shell
pipenv install -r requirements.txt
pipenv shell
```

Or install dependencies globally.

```shell
pip install -r requirements.txt
```

### Starting service

```shell
python main.py
# or
uvicorn main:app --reload
```

This will start service at [127.0.0.1:8080](http://127.0.0.1:8080).

### Interactive API docs

Automatic interactive API documentation provided by swagger are available at [127.0.0.1:8080/docs](http://127.0.0.1:8080/docs).
