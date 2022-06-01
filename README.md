# Lab 1: Microservices basics

## Requirements:
- flask
- requests
- hazelcast
```
pip3 install -r requirements.txt
```

## Usage:
Run the services with ports as arguments for loggers:
```
python3 src/facade_service.py
python3 src/messages_service.py 8081
python3 src/messages_service.py 8082
python3 src/logging_service.py 8083
python3 src/logging_service.py 8084
python3 src/logging_service.py 8085
```

Send POST/GET requests (i.e. using curl):

```
curl -X POST http://localhost:8080/facade -d "Your message"

curl -X GET http://localhost:8080/facade
```

## Results:

In file conclusion.pdf