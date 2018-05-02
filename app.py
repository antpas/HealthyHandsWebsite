import paramiko
import pandas as pd
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import csv
import re
import os
import math
import json
from os import path

app = Flask(__name__)

def sshDownload():
    # # Open a transport
    # host = "10.0.0.9"
    # port = 22
    # transport = paramiko.Transport((host, port))

    # # Auth
    # username = "pi"
    # password = "raspberry"
    # transport.connect(username = username, password = password)
    # sftp = paramiko.SFTPClient.from_transport(transport)

    # # Download
    # filepath = '/pi/Documents/Data/OutputData.csv'
    # localpath = 'C:/Users/antth/Desktop/HealthyHandsDashboard/'
    # sftp.get(filepath, localpath)

    # # Close
    # sftp.close()
    # transport.close()
    return 0


@app.route("/")
def chart():
    sshDownload()
    dates = []
    waterUsed = []
    soapEvents = []
    waterEvents = []
    soapUseTime = []
    with open('OutputData.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader, None)  # skip the headers
        for row in csvReader:
            dates.append(row[0])
            waterUsed.append(row[1])
            if row[3] == "":
                soapTemp = ""
            elif row[3] == "0":
                soapTemp = 0
            else:
                soapTemp = 1
            soapEvents.append(soapTemp)

            if row[0] == "":
                waterTemp = ""
            else:
                waterTemp = 1
            waterEvents.append(waterTemp)

            if row[4] == "":
                continue
            else:
                soapUseTime.append(float(row[5]) - float(row[4]))

    soapEvents = list(filter(None, soapEvents))
    waterEvents = list(filter(None, waterEvents))
    soapUseTime = list(filter(None, soapUseTime))
    soapTimes = [0,0,0,0,0,0]
    for s in soapUseTime:
        if s <= 5:
            soapTimes[0] = soapTimes[0] + 1
        elif s > 5 and s <= 10:
            soapTimes[1] = soapTimes[0] + 1    
        elif s > 10 and s <= 20:
            soapTimes[2] = soapTimes[0] + 1
        elif s > 20 and s <= 40:
            soapTimes[3] = soapTimes[0] + 1
        elif s > 40 and s <= 60:
            soapTimes[4] = soapTimes[0] + 1
        elif s > 60:
            soapTimes[5] = soapTimes[0] + 1

    numSoap = len(soapEvents)
    numWater = len(waterEvents)
    dates = list(filter(None, dates))
    dates = dates[-10:]
    waterUsed = list(filter(None, waterUsed))
    waterUsed = list(map(float, waterUsed))
    return render_template('index.html', waterUsed=waterUsed, dates= dates, numSoap=numSoap, numWater=numWater, soapTimes=soapTimes)

if __name__ == "__main__":
    extra_dirs = ['C:/Users/antth/Desktop/HealthyHandsDashboard',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.run(extra_files=extra_files, debug=True)           
                        
