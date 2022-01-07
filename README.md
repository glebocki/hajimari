<h1>Hajimari<sub><sub><sup>&nbsp;(<i>Japanese</i>: origin; beginning.)</sup></sub></sub></h1><br>


---

Configurable environment for API deployment for machine learning models.

## Run it:

### Running with [Pipenv](https://pipenv.pypa.io/en/latest/)

First create a virtual environment and install dependencies with `pipenv`.

```shell
pipenv install -r requirements.txt
pipenv shell
```

### Installing dependencies globally

```shell
pip install -r requirements.txt
```

### Starting App

You can start Hajimari Generator service directly

```shell
cd hajimari
python main.py
```

Or run the live server with:

``` shell
cd hajimari
uvicorn main:app --reload
```

Navigate to [127.0.0.1:8000](http://127.0.0.1:8000)

Automatic interactive API documentation (provided by Swagger UI) avaliable at [/docs](http://127.0.0.1:8000/docs)

## Testing

```shell
pytest
```

## Generated package contents

Service generates a `.zip` package with a microservice capable of running provided machine learning model.

```text
example_ml_service
├── README.md
├── main.py
├── model.h5
└── requirements.txt
```