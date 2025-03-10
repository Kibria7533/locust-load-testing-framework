# Locust API Load Testing Framework

## Overview
This repository contains a **Locust-based stress testing framework** designed to test the performance of APIs and microservices. It simulates high-traffic scenarios by generating concurrent user requests and analyzing response times, failures, and scalability.

## Features
- **Automated API load testing with Locust**
- **Custom user agent simulation**
- **Authentication with bearer tokens**
- **File uploads and API data retrieval**
- **Supports assertions for response validation**
- **Docker and Docker Compose integration**

---

## Installation

### Install Locust using pip
```bash
pip3 install locust
```

### Basic Locust Test
Create a simple Locust script to test an endpoint:

```python
from locust import HttpUser, task

class User(HttpUser):
    @task
    def main_page(self):
        self.client.get("/")
```

Run Locust in **headless mode**:
```bash
locust --headless -u 1 -r 1 -H https://www.example.com
```
Where:
- `-u` specifies the number of users
- `-r` defines the spawn rate
- `-H` sets the host URL

---

## Advanced Locust Script
The following script simulates a **real user journey**:
1. Enter the website
2. Log in
3. Add a product to the cart
4. View the cart

```python
from locust import HttpUser, SequentialTaskSet, task, between

class User(HttpUser):    
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = between(1, 5)

        @task
        def main_page(self):
            self.client.get("/")
            self.client.get("https://api.demoblaze.com/entries")

        @task
        def login(self):
            response = self.client.post("https://api.demoblaze.com/login", json={"username": "aaaa", "password": "YWFhYQ=="})
            global token
            token = response.json().get("Auth_token")
            self.client.post("https://api.demoblaze.com/check", json={"token": token})

        @task
        def click_product(self):
            self.client.get("/prod.html?idp_=1")
            self.client.post("https://api.demoblaze.com/view", json={"id": "1"})

        @task
        def add_to_cart(self):
            self.client.post("https://api.demoblaze.com/addtocart", json={"id": "1234", "cookie": token, "prod_id": 1, "flag": 'true'})

        @task
        def view_cart(self):
            with self.client.post("https://api.demoblaze.com/viewcart", catch_response=True, json={"cookie": token, "flag": 'true'}) as response:
                if '"prod_id":1' not in response.text:
                    response.failure("Assert failure: Response does not contain expected prod_id")
```

---

## Running Locust with Docker

### Dockerfile
```dockerfile
FROM locustio/locust

COPY requirements.txt /tmp/custom-requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r /tmp/custom-requirements.txt

COPY locustfile.py /mnt/locust/locustfile.py
```

### Docker Compose Configuration
```yaml
version: '3'

services:
  master:
    build: .
    ports:
     - "8090:8089"
    command: -f /mnt/locust/locustfile.py --master -H http://master:8089
  
  worker:
    build: .
    command: -f /mnt/locust/locustfile.py --worker --master-host master
```

To start the load testing cluster:
```bash
docker-compose up --scale worker=5
```
This will run Locust with 1 **master node** and 5 **worker nodes**.

---

## Assertions with Locust
You can use assertions to validate API responses:

```python
def assert_contains(response, text):
    with response as r:
        if text not in r.text:
            r.failure(f"Expected response to contain {text}")

assert_contains(self.client.post("https://api.demoblaze.com/viewcart", json={"cookie": token, "flag": 'true'}), '"prod_id":1')
```

---

## Conclusion
This **Locust API Load Testing Framework** provides an efficient way to stress test APIs, measure response times, and detect performance bottlenecks. Whether you are testing login authentication, file uploads, or complex API workflows, this framework is **scalable**, **customizable**, and **Docker-ready**.

Happy load testing! 🚀

