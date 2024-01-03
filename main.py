### Imports ###

#External

from flask import Flask, render_template, request, flash, redirect, url_for
from math import *
from random import *
import json, time, itertools

#Internal

from modules.algorithms import *



### Website ###

#Initializing webapp
app = Flask(__name__)

#Calls algorithm functions
def call_method(coords, method, test_data):
	if method == 'bruteforce':
		data = bruteforce(coords)
	elif method == 'pure' or method == 'seeded':
		data = genetic_algorithm(coords, method)
		if not test_data: #allows for testing of the genetic algorithm
			data = data[0]
	elif method == 'mst-dfs':
		data = mst_dfs(coords)
	elif method == 'christofides':
		data = only_christofides(coords)
	else:
		return 422 #unprocessable content response status code
	return data

#Website pages

#Webpage where a new set of coordinates can be inputted
@app.route('/')
def main():
	return render_template('input.html')

#Where the coordinates the user inputted are sent once submitted
@app.route('/post', methods=['POST'])
def receive_input():
	if request.method == 'POST':
		
		json = request.json #parsing received data as json
		method, markers = json['method'], json['markers']

		
		#global so that they can be accessed by output() which calls the algorithms
		global data 
		global finished #prevents output() from returning the template before the algorithm has terminated
		
		finished = False #by default the algorithm has not been completed yet
		data = call_method(markers, method, False) #call_method() calls the relevant algorithm function
		finished = True #once the previous line has be executed the algorithm is finished and output() can return the template

		return '', 200 #success status response

#displays a gif while the algorithm computes
@app.route('/loading')
def loading():
	return render_template('loading.html')

#displays the solution to the user
@app.route('/output')
def output():
	start = time.perf_counter() #records the time at which the algorithm starts running
	while time.perf_counter()-start < 5: #this will time the connection out after 249s - 1s before the browser will time out
		if finished == True: #once the algorithm has concluded
			return render_template('output.html', data=data) #passes data to output template to be displayed to user
	return render_template('error.html') #if the connection times out or an error occurs

#Runs webapp
app.run(host='0.0.0.0', port=8080)

