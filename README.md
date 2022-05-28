# Lab 1: Microservices basics

## Requirements:
- flask
- requests
```
pip install -r requirements.txt
```

## Usage:
Run the services:
```
python3 src/facade_service.py
python3 src/logging_service.py
python3 src/messages_service.py
```

Send POST/GET requests (i.e. using curl):

```
curl -X POST http://localhost:8080/facade -d "Your message"

curl -X GET http://localhost:8080/facade
```

## Results:

In file conclusion.pdf