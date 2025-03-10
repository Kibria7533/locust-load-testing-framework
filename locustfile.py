import random
from locust import HttpUser, TaskSet, task, between 
from random import randint
import json
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19 (LocustIO)",
    "Android 4.0.3;AppleWebKit/534.30;Build/IML74K;GT-I9220 Build/IML74K (LocustIO)",
    "KWC-S4000/ UP.Browser/7.2.6.1.794 (GUI) MMP/2.0 (LocustIO)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) (LocustIO)",
    "Googlebot-Image/1.0 (LocustIO)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0 (LocustIO)",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52 (LocustIO)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
]

token = "Bearer Token"


def file_upload(l):
    attach = open('/mnt/locust/file.pdf', 'rb')
    l.headers = {
        "User-Agent":USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)],
        "Authorization": token
    }
    r = l.client.post("/api/v1/path/", data={
        'docType': '1',
        'category': 'DEFAULT',
        'pathId': 'DEFAULT',
         }, files={'file': attach})

def file_get(l):
  
    l.headers = {
            "User-Agent":USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)],
            "Authorization": token
        }
    l.client.headers = l.headers
    res=l.client.get("/api/v1/path/")
    print(res)


def index(l):
    random_number = random.randint(1, 15)
    l.headers = {
            "User-Agent":USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)],
            "Authorization": token
        }
    l.client.headers = l.headers
    res=l.client.get("/api/v1/path/")
    print(res)

def voterareas(l):
    random_number = random.randint(1, 15)
    l.headers = {
            "User-Agent":USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)],
            "Authorization": token
        }
    l.client.headers = l.headers
    res=l.client.get("/api/v1/path/")
    print(res)

def candidatedetails(l):
    random_number = random.randint(1, 15)
    l.headers = {
            "User-Agent":USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)],
            "Authorization": token
        }
    l.client.headers = l.headers
    res=l.client.get("/api/v1/path/")
    print(res)

def vcenter(l):
    random_number = random.randint(1, 15)
    l.headers = {
            "User-Agent":USER_AGENTS[random.randint(0,len(USER_AGENTS)-1)],
            "Authorization": token
        }
    l.client.headers = l.headers
    
    #l.client.get("/api/v1/path/"+ str(random_number))
    
    l.client.get("/api/v1/path/"+ str(random_number))

def stats(l):
    random_number = random.randint(1, 15)
    l.client.get("/api/v1/path/")

class UserTasks(TaskSet):
    # one can specify tasks like this
    #tasks = [index, vcenter, stats, bartasheets, candidatedetails, voterareas]
    tasks = [file_upload, file_get]

class WebsiteUser(HttpUser):
    host = "http://localhost:8090"
    tasks = [UserTasks]