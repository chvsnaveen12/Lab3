from flask import Flask, redirect, url_for, request, render_template, jsonify, render_template 
from datetime import *

app = Flask(__name__)       # app is the name of our flask module

averageTemp = 27            
activeNodes = 0             # The number of active nodes in our system
lastCalc = datetime.now() - timedelta(minutes = 10) # Since there are no previous calculations, set the time of lastCalc to 10 minutes ago. 

nodes = [{"last": datetime.now() - timedelta(minutes = 1), "temp":27} for i in range(40)] # This list conatins all the sensor data

@app.route('/app/<int:id>')
def user(id):
    global lastCalc, averageTemp, nodes, activeNodes
    if (datetime.now() - lastCalc) > timedelta(seconds = 1):    # If it has been more than 1 second since our last calculation, perform the calculation 
        recentTemp = [nodes[i]["temp"] for i in range(40) if (datetime.now()-nodes[i]["last"]) < timedelta(seconds=5)]  # Make a list of all the sensor temperature, which was less than 5 seconds old
        activeNodes = len(recentTemp)
        averageTemp = float(sum(recentTemp)/len(recentTemp)) if len(recentTemp) != 0 else float(0) # Calculate the average only if array has some elements 
        nodeTemp = float(nodes[id]["temp"]) if (datetime.now()-nodes[id]["last"]) < timedelta(seconds=5) else float(0) # The temperature of the specific node 
        lastCalc = datetime.now()
        return jsonify({"avg" : float(averageTemp), "sensor" : nodeTemp, "active" : activeNodes, "calc" : "n"})    # return a JSON response
    else:
        nodeTemp = float(nodes[id]["temp"]) if (datetime.now()-nodes[id]["last"]) < timedelta(seconds=5) else float(0)
        return jsonify({"avg" : float(averageTemp), "sensor" : nodeTemp, "active" : activeNodes, "calc" : "n"})

@app.route('/esp/<int:id>/<float:temp>')
def esp(id, temp):
    global lastCalc, averageTemp, nodes, activeNodes
    nodes[id]["temp"] = temp  # store the node temperature
    nodes[id]["last"] = datetime.now()
    if (datetime.now() - lastCalc) > timedelta(seconds = 1):
        recentTemp = [nodes[i]["temp"] for i in range(40) if (datetime.now()-nodes[i]["last"]) < timedelta(seconds=5)]
        activeNodes = len(recentTemp)
        averageTemp = float(sum(recentTemp)/len(recentTemp)) if len(recentTemp) != 0 else float(0)
        nodeTemp = float(nodes[id]["temp"]) if (datetime.now()-nodes[id]["last"]) < timedelta(seconds=5) else float(0)
        lastCalc = datetime.now()
        return jsonify({"avg" : float(averageTemp), "sensor" : nodeTemp, "active" : activeNodes, "calc" : "n"})
    else:
        nodeTemp = float(nodes[id]["temp"]) if (datetime.now()-nodes[id]["last"]) < timedelta(seconds=5) else float(0)
        return jsonify({"avg" : float(averageTemp), "sensor" : nodeTemp, "active" : activeNodes, "calc" : "n"})

@app.route('/web/')
def web():
    return render_template("index.html")
    

if __name__=='__main__':
    app.run(host = '0.0.0.0', port=8080, debug=True)
