#!/usr/bin/python
import re
from datetime import datetime
import requests
import json

qUrl = "" #for queueing and exiting
sUrl = "" #for ending service
auth = "" #auth token

headers = {}
headers["Authorization"] = auth
headers["Content-Type"] = "application/json"

lastseen=0
globalseen=0

def tmstmp(date):
    
    dt_obj = datetime.strptime(date, "%d/%m/%y %H:%M:%S.%f")
    tmstmp = datetime.timestamp(dt_obj)
    return tmstmp


def readnext(filename,lastseen,globalseen):

  with open(filename) as fil:
      fil.seek(lastseen)
      if (lastseen>=globalseen):
          globalseen=lastseen
          for line in fil:
              events(line)

          return fil.tell()


def sendToDb(dict):

    if dict["result"] == "push" or dict["result"] == "pull":
        print("test")
        res = requests.post(qUrl,headers=headers,data=json.dumps(dict))
        print(json.dumps(dict))
        print(res.status_code,res.reason)

    if dict["result"].startswith("0") or dict["result"].startswith("AP"):
        print("test")
        res = requests.post(sUrl,headers=headers,data=json.dumps(dict))
        print(json.dumps(dict))
        print(res.status_code,res.reason)
    
    return


def push(date,name,size):

    queueing = {
        "result": "push",
        "data": { "size": -1, "service": '' },
        "name": "service",
        "source": "francesco_test",
        "timestamp": -1
    }

    timestamp = tmstmp(date)

    queueing["data"]["size"] = size
    queueing["data"]["service"] = name
    queueing["timestamp"] = timestamp

    sendToDb(queueing)

    return

def exit(date,name):

    exiting = {
        "result": 'pull',
        "data": { "service": ''},
        "name": 'queue',
        "source": 'francesco_test',
        "timestamp": 0
    }

    timestamp = tmstmp(date)

    exiting["data"]["service"] = name
    exiting["timestamp"] = timestamp

    sendToDb(exiting)
 
    return

def end(date,name,processTime,queueTimeP,queueTime,result):

    ending = {
    "result": '',
    "data": {
             "service": 'machinedata_insert',
             "processtime": 0,
             "queuetime": 0 },
    "name": '',
    "source": 'francesco_test',
    "timestamp": 0
}   

    timestamp = tmstmp(date)
    print(type(queueTime))

    ending["data"]["service"] = name 
    
    ending["name"] = name
    ending["timestamp"] = timestamp
    ending["result"] = result
    
    if(queueTime!=None):
        queueTime=int(queueTime)
        ending["data"]["queuetime"] = queueTime

    if(processTime!=None):
        processTime=int(processTime)
        queueTimeP=int(queueTimeP)
        ending["data"]["processtime"] = processTime
        ending["data"]["queuetime"] = queueTimeP

    print(ending)

    sendToDb(ending)

    return

def events(line):
    queueReg = re.match('^(\d{2}\\/\d{2}\\/\d{2}\s\d{2}:\d{2}:\d{2}\.\d)\s\[.*?\]\[Enqueued service (\w+) for processing \(size=(\d+)\).*\]$',line)
    exitReg = re.match('^(\d{2}\/\d{2}\/\d{2}\s\d{2}:\d{2}:\d{2}\.\d)\s\[.*?\]\[<-- REQUEST NAME: (\w+) - PARAMS:.*\]$',line)
    endReg = re.match('^(\d{2}\/\d{2}\/\d{2}\s\d{2}:\d{2}:\d{2}\.\d)\s(?:ServiceProcessor:\s\[.*?\]\s|\[.*\]\[)-->\sANSWER\sTO:\s(\w+)\sTIME\(ms\)(?:\s\[process\s-\selapsed\]:\s(\d+)\s-\s(\d+)|:\s(\d+))\sRESULT:\s(?:(\w+)(.*$|.*\]))$',line)
    
    if queueReg:
        push(queueReg.group(1),queueReg.group(2),int(queueReg.group(3)))
    if exitReg:
        exit(exitReg.group(1),exitReg.group(2))
    if endReg:
        end(endReg.group(1),endReg.group(2),endReg.group(3),endReg.group(4),endReg.group(5),endReg.group(6))

    return


if __name__ == "__main__":
    while True:
        lastseen = readnext("follow.txt",lastseen,globalseen)
   
