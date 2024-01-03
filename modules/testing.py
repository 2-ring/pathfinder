### Imports ###

#External
from random import *

#Internal
from modules.algorithms import *



### For Testing ###

#Generates random collections of n coordinates
def random_coords(n):
	return [{'lat': uniform(-90, 90), 'long': uniform(-180, 180)} for c in range(n)]

#Enables calling a function multiple times
def multi_call(coords, method, n, test_data):
	data = []
	for x in range(n):
		result = call_method(coords, method, test_data)
		data.append(result)
		print(f'Call {x+1}: {result}')
	return data

#Compares seeded and pure genetic algorithm
def compare_ga(num_coords, num_tests):

	#Starts timer
	start = time.perf_counter()
	
	#Compiling data
	coords = random_coords(num_coords)
	pure = multi_call(coords, 'pure', num_tests, True)
	seeded = multi_call(coords, 'seeded', num_tests, True)

	#Analysing data
	average_stats = [] #average times and gens
	for i in [0 , 1]:
		for type in [pure, seeded]:
			average_stats.append(sum([float(type[x][i][1-i]) for x in range(num_tests)])/num_tests)
	
	return average_stats, time.perf_counter()-start #returns findings and time taken