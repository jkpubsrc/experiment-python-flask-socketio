#!/usr/bin/python3



import os
import time
import queue
import eventlet
import threading

from flask import Flask, render_template, request, send_from_directory, Response, send_file
from flask_socketio import SocketIO






statusQueue = eventlet.Queue()

app = Flask(__name__, static_url_path="")
socketio = SocketIO(app, engineio_logger=True, async_mode='threading')
#socketio = SocketIO(app, engineio_logger=True, async_mode="eventlet")

def ack():
    print("< Message sent was received!")
#

def emitStatus():
	print("Beginning to emit ...")
	while True:
		msg = statusQueue.get()
		print("> Sending status packet: " + str(msg))
		socketio.emit("clientstatus", msg, callback=ack, broadcast=True)
		statusQueue.task_done()
		print("> Sending status packet done.")
	print("Terminated.")
#

socketio.start_background_task(emitStatus)


def threadRunnable():
	stateID = 0
	while True:
		msg = {
			"stateID": stateID,
		}

		print(">", end="", flush=True)
		#print("Adding status packet to queue: " + str(msg))

		statusQueue.put(msg)

		time.sleep(2)
		stateID += 1
#
thread = threading.Thread(target = threadRunnable)
thread.start()









@app.route("/<path>", methods=["GET", "POST"])
def sendData1(path):
	# print(path)
	return send_from_directory('wwwroot', path)
#



@app.route("/", methods=["GET", "POST"])
def sendIndex():
    return send_file("wwwroot/index.html", mimetype="text/html")
#



@socketio.on("myws")
def handle_myEvent(message):
	print("< Message received: " + str(message))
#







if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)















