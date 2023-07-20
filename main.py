from flask import Flask, redirect, url_for, request, render_template, jsonify
import threading
from datetime import *
import time

app = Flask(__name__)       # app is the name of our flask module

averageTemp = 27            
activeNodes = 0             # The number of active nodes in our system
lastCalc = datetime.now() - timedelta(minutes = 10) # Since there are no previous calculations, set the time of lastCalc to 10 minutes ago. 

nodes = [{"last": datetime.now() - timedelta(minutes = 1), "temp":27} for i in range(40)] # This list conatins all the sensor data
recentTemp = nodes

@app.route('/app/<int:id>')
def user(id):
    global lastCalc, averageTemp, nodes, activeNodes
    nodeTemp = float(nodes[id]["temp"]) if (datetime.now()-nodes[id]["last"]) < timedelta(seconds=5) else float(0)
    return jsonify({"avg" : float(averageTemp), "sensor" : nodeTemp, "active" : activeNodes})    # return a JSON response

@app.route('/esp/<int:id>/<float:temp>')
def esp(id, temp):
    global lastCalc, averageTemp, nodes, activeNodes
    nodes[id]["temp"] = temp  # store the node temperature
    nodes[id]["last"] = datetime.now()
    nodeTemp = float(nodes[id]["temp"]) if (datetime.now()-nodes[id]["last"]) < timedelta(seconds=5) else float(0)
    return jsonify({"avg" : float(averageTemp), "sensor" : nodeTemp, "active" : activeNodes})    # return a JSON response

@app.route('/web/')
def web():
    return render_template("index.html")

def averageCalc():
    while(True):
        global recentTemp, lastCalc, averageTemp, nodes, activeNodes
        recentTemp = [nodes[i]["temp"] for i in range(40) if (datetime.now()-nodes[i]["last"]) < timedelta(seconds=5)] # Put all the node temperatures, whose data was less than 5 seconds old in an array
        activeNodes = len(recentTemp)   # Calculate number of nodes which sent data within the last 5 seconds
        averageTemp = float(sum(recentTemp)/len(recentTemp)) if len(recentTemp) != 0 else float(0) # Calculate the average only if array has some elements
        time.sleep(0.25)   # perform the calculation of averaging every 250 milliseconds 

if __name__=='__main__':
    averageCalcThread = threading.Thread(target=averageCalc)
    averageCalcThread.start()                                   # Run the averaging calculation on a diffrent thread
    app.run(host = '0.0.0.0', port=8080, debug=True)
