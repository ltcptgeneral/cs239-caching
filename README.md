# CS239 Cache System
This repo is for our final project in CS239 in UCLA. The goal is to test caching strategies in a microservice environment to assess and analyze their pros and cons.

## Motivation
This project was inspired by the fact that there have not been many papers discussing the utility and optimization of caching in microservices. MuCache, one of the papers addressing the topic, proposed a caching system for microservices but only utilized a simple Key-Value caching strategy that wasn't explored any further.
Thus, we want to follow up on MuCache and see how much impact different caching strategies would have on microservices in terms of latency, memory usage, and cache hits.

## Methodology
To test caching strategies on microservices, we decided to build a micro service system mimicking interactions between microservices to easily implement and test different caching strategies. The idea is that the caching between two services will be the same for any other pair of services. Thus, we can scale down our targeted environment.
We designed our own cache and microservice system and will use different metrics to test our caching strategies.


## How to run

### Set Up Virtual Environment
macOS/Linux

```python3 -m venv venv && source venv/bin/activate```

Windows (CMD)

```python -m venv venv && venv\Scripts\activate```

Windows (PowerShell)

```python -m venv venv && venv\Scripts\Activate.ps1```

### Install Dependencies

```pip install -r requirements.txt```

### Edit config.yaml to set the caching strategy:

``` 
    cache_strategy: "Baseline"  # Change to "Prefetch" or "Tiered"
    cache_limit: 10
    l2_cache_limit: 100
```

### Run Microservice

```python run.py```

### Test API Endpoints

Fetch a User Profile

```curl -X GET "http://127.0.0.1:8000/user/1"```

Update a User Profile

```
curl -X POST "http://127.0.0.1:8000/update_user/?user_id=2&name=Bob&followers=200&bio=TechEnthusiast&posts=AIIsAwesome"


```

### Stop the server and deactive virtual env

macOS/Linux

```deactivate```

Windows

```venv\Scripts\deactivate.bat```