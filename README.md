<h1>Hajimari<sub><sub><sup>&nbsp;(<i>Japanese</i>: origin; beginning.)</sup></sub></sub></h1><br>

_Everything have to start somewhere._

---

Configurable environment for API deployment for machine learning models.

## Run it:

```shell
pip install -r requirements.txt
```

``` shell
cd hajimari
uvicorn main:app --reload
```

Docs avaliable at [/docs](http://127.0.0.1:8000/docs)

## Testing

```shell
pytest
```

## Generated package contents

Service generates a `.zip` package with a microservice capable of running provided model.

```text
example_ml_service
├── README.md
├── main.py
├── model.h5
├── requirements.txt
└── run.sh
```