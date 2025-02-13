# CS239 Cache System
This repo is for our final project in CS239 in UCLA. The goal is to test caching strategies in a microservice environment to assess and analyze their pros and cons.

## Motivation
This project was inspired by the fact that there have not been many papers discussing the utility and optimization of caching in microservices. MuCache, one of the papers addressing the topic, proposed a caching system for microservices but only utilized a simple Key-Value caching strategy that wasn't explored any further.
Thus, we want to follow up on MuCache and see how much impact different caching strategies would have on microservices in terms of latency, memory usage, and cache hits.

## Methodology
To test caching strategies on microservices, we decided to build a micro service system mimicking interactions between microservices to easily implement and test different caching strategies. The idea is that the caching between two services will be the same for any other pair of services. Thus, we can scale down our targeted environment.
We designed our own cache and microservice system and will use different metrics to test our caching strategies.
