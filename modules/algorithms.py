### Imports ###

#External
from flask import Flask, render_template, request, flash, redirect, url_for
from math import *
from random import *
import json, time, itertools

#Internal
from modules.toolbox import *



### Algorithms ###

### For Kruskals

def find_edges(coords): #takes coordinates and returns a sorted list of edges and total weight
	edges = []
	for m1, marker in enumerate(coords):
		for m2, other_marker in enumerate(coords):
			if marker != other_marker: #if the two nodes are different
				#adds edge to set
				edges.append((tuple(sorted([m1, m2])), edge_length(marker, other_marker)))
	return list(set(edges)) #removes any duplicates

def kruskals(coords):

	trees = []
	mst = [[] for i in range(len(coords))] #an adjacency matrix for the minimum spanning tree
	edges = sort_2d(find_edges(coords), 1, False) #a list of edges ascending by total weight
	
	for edge in edges: #each edge starting with the lowest total weight
		locations = [None, None]
		#testing which trees each node of the edge is contained within
		#by the nature of the algorithm each node can only appear in a single tree
		for i, tree in enumerate(trees):
			if edge[0][0] in tree: #if the first edge is in a given tree..
				locations[0] = i #store the index of the tree in locations[0]
			if edge[0][1] in tree: #if the second edge is in a given tree...
				locations[1] = i #store the index of the tree in locations[1]
		in_mst = True #assuming the edge will be in the mst until info otherwise
		#if neither node in is any tree
		if locations == [None, None]:
			trees.append(list(edge[0])) #create a new tree comprised of solely the edge
		#if either one of the nodes aren’t in any trees
		elif None in locations:
			new = locations.index(None) #find which of the nodes is 'new'
			tree = trees[locations[1-new]] #find the tree the 'old' node is contained within
			tree.append(edge[0][new]) #add the 'new' node into the corresponding tree
		#if the nodes are each contained within a different tree
		elif locations[0] != locations[1]:
			trees[locations[0]].extend(trees[locations[1]]) #combine the two trees
			del trees[locations[1]]
		#if both nodes are in the same tree
		else:
			in_mst = False #the edge is not a part of the mst
		if in_mst:
			mst = edge_append(mst, edge[0]) #adds the edge to the mst

		#the algorithm concludes when there is a single tree left containing every node
		if len(trees[0]) == len(coords):
			break

	print(f"MST found: {mst}")
	return mst #adjacency list

### For MST-DFS

def mst_dfs(coords):

	start = time.perf_counter()
	mst = kruskals(coords) #generates the mst using kruskals algorithm
	dfs_traversal = dfs(mst, mst[0][0]) #executes a dfs traversal
	t = time.perf_counter()-start #finds time taken
	
	return format(coords, shortcut(dfs_traversal), t, 'a mst-dfs algorithm') #formats output

### For Christofides

def find_odd(graph): #graph is an adjacency list
	odd_nodes = []
	for i, neighbours in enumerate(graph): #list of neighbours for each node
		if len(neighbours)%2==1: #if neighbours is of an odd length
			odd_nodes.append(i) #add it to odd_nodes
	return odd_nodes if odd_nodes else [0] #if there are no odd nodes the function defaults to 0

#takes an array of node indices (and coords) and outputs all perfect matching solutions
def min_perfect_matching(coords, nodes): 
	#finding all pairs
	n = len(nodes)
	min_solution = [inf, ()]
	pairs = []
	
	for i in range(n): #n^2 time complexity
		for j in range(n):
			
			if i != j: #if the indices are not the same
				pair = sorted([nodes[i], nodes[j]]) #sorted to avoid duplicates
				if pair not in pairs:
					pairs.append(pair)

	matching = list(itertools.combinations(pairs, n//2)) #find all matching solutions given the list of all pairs
	#finds all perfect matching pairs via bruteforce
	#if i had extra time this could perhaps be more efficient
	perfect_matching = [] 
	for solution in matching:
		perfect = True
		original_len = len(solution)*2
		if original_len==len(list(set([j for sub in pairs for j in sub]))):
			total_dist = 0
			for nodes in solution:
				total_dist += edge_length(coords[nodes[0]], coords[nodes[1]])
			if total_dist < min_solution[0]:
				min_solution = [total_dist, solution]
	
	return min_solution[1]

def christofides(coords):
	s = time.perf_counter() #records when the algorithm was started
	graph = kruskals(coords) #finding minimum spanning tree
	odd_nodes = find_odd(graph) #finding all odd nodes
	#finding the minimum spanning perfect matching solution of the odd nodes as a bipartite graph
	perfect_pair = min_perfect_matching(coords, odd_nodes) 
	#a graph is perfect matching when all nodes are split into pairs with no overlap

	#adding all edges from the perfect matching solution to the graph adjacency matrix
	for nodes in perfect_pair:
		graph = edge_append(graph, nodes)	 

	#finding the amount of edges in the graph
	#doesn't call find_edges() for efficiency
	length = 0
	for x in graph: #first counts total length of the adjacency matrix
		for n in x:
			length += 1
	num_edges = int(length/2) #then divides it by two to find the number of edges
	
	start = find_odd(graph)[0] #finding any odd node to start fleurys at (if there is one)
	#if there isn't one it will default to the first node

	t = time.perf_counter()-s #calculates time taken
	cycle = fleurys(start, graph, num_edges, [start]) #fleurys finds the cycle in the graph
	path = shortcut(cycle) #shortcutting unnecessary sections of the cycle
	return [path, t] #path is an array and t is a float

#function exists so that christofides can be used as part of another algorithm
def only_christofides(coords): 
	result = christofides(coords)
	return format(coords, result[0], result[1], 'christofides algorithm') #formats output to be sent to the client
	
#For Fleury's

def fleury_valid(u, v, graph, num_edges): #checks the next edge doesn't disconnect any sections of the graph

	if len(graph[u]) == 1: #if it is the last edge it has to be valid
		return True
	else:
		with_edge = len(dfs(graph, u)) #counts the number of nodes when the graph contains the edge
		
		graph_copy = [row[:] for row in graph]
		edge_remove(graph_copy, [u, v])
		
		without_edge = len(dfs(graph_copy, u)) #and the number of nodes without the edge contained
		
		return False if with_edge > without_edge else True #if with_edge is greater than the edge is a 'bridge'

def fleurys(start, graph, num_edges, path): #recursively finds eulerian cycle
	for neighbour in graph[start]: #try's all connected nodes to see if they are valid next edges
		if fleury_valid(start, neighbour, graph, num_edges): #checks the next edge doesn't disconnect any sections of the graph
			path.append(neighbour) #if the edge is valid add it to the path
			edge_remove(graph, [start, neighbour]) #the edge has been 'used' so remove it from the original graph
			fleurys(neighbour, graph, num_edges, path)
	return path


	
### For Bruteforce

def bruteforce(coords):
	start = time.perf_counter() #records when the algorithm was started
	nodes = list(range(len(coords))) #creates a list [1, 2, 3..n]
	perms = permutation(nodes[1:]) #find all possible permutations of this list

	#finds the length of each permutation
	shortest = [inf, []] #total weight, path
	for p in perms:
		p = [0]+p+[0] #makes permutation a cycle
		p_dist =  path_dist(coords, p) #finds distance of permutation
		
		#if the total distance of the newest path is shorter than the previous shortest
		if p_dist < shortest[0]:
			shortest = [p_dist, p] #assign the shortest as the new path

	t = time.perf_counter()-start
	return format(coords, shortest[1], t, 'bruteforce', shortest[0])

### For GA


#Takes a list of chromosomes and returns a 2d array of chromosomes and total weight
def find_fitness(coords, chrms):
	
	if len(chrms) == 1: #making the function compatible with only one chromosome
		chrms = [chrms]
	#adding the fitness (1/path weight) to each chromosome
	with_fitness = [[1/path_dist(coords, c+[c[0]]), c] for c in chrms] 

	#returning 2d array in descending order of fitness
	return sort_2d(with_fitness, 0, True) 

#this is used to generate an initial population as well as avoiding local maximums through generations
def random_chromosomes(coords, n): 
	return [sample(list(range(len(coords))), len(coords)) for x in range(n)]

#removes each term of an array (elements) from another list (c)
def multi_remove(elements, c): 
	lst = c.copy()
	for x in elements:
		lst.remove(x)
	return lst

#takes an array of indices (ints) as input
def scramble_mutation(c):
	
	sub, start_i = subsection(c)[:2] #gets random subsection
	shuffle(sub) #shuffles it (randomises order)
	
	c = multi_remove(sub, c)
	for node in sub[::-1]: #and replaces it in the same place but shuffled
		c.insert(start_i, node)
		
	return c #then returns the mutated chromosome

#Takes a chromosome without fitness and returns a random subsection
def subsection(path): 

	last = len(path)-1 #max subsection length
	#This could be optimized significantly
	if last > 1:
		min = 2 #min subsection length
	else:
		min = 1
		
	sub_len = randint(min, last) #length of the subsection
	start_i = randint(0, last-sub_len) #starting index of the subsection

	#allows for 'looping' around the path
	if start_i > len(path)-sub_len: #if subsection exceeds end
		sub = path[start_i:] + path[:sub_len-len(sub)]
	else:
		sub = path[start_i:start_i+sub_len]
	
	return sub, start_i, sub_len, last

#picking two chromosomes to cross (tournament selection)
def selection(population):
	
	fitness_weighting = 0.1

	#getting a random sample of chromosomes - size of dependant on fitness_weighting
	smple = sample(population, round(len(population)*fitness_weighting)) 
	#x is the fittest chromosome in the sample y is a random chromosome from the population
	return smple[0][1], choice(population)[1] 

def reproduce(population):

	#the probability that a single chromosome will mutate
	mutation_rate = 0.2
	
	#selecting parents
	x, y = selection(population)

	#crossing parents
	child = cross(x,y)
	
	#mutating and returning
	return scramble_mutation(child) if random() < mutation_rate else child

def cross(x, y): #order crossover

	#getting a random subsection of the y chromosome
	sub, start_i, sub_len, last = subsection(y) 

	#creating a partly empty chromosome with only the subsection in the same place it was
	child = [None]*start_i+sub+[None]*(last-start_i-sub_len+1)
	#filling the empty spaces in the child chromosome with the remaining nodes - from the x chromosome in order
	for node in multi_remove(sub, x): 
		child[child.index(None)] = node
		
	return child #returns new chromosome without fitness
	
def genetic_algorithm(coords, method):

	start = time.perf_counter()

	#parameters
	k = len(coords)*50 #population size
	#the quantity of the fittest chromosomes that are maintained between generations
	maintain_rate = round(k/100) if k/100>3 else 3
	#the amount of new random chromosomes that are introduced each generation
	generational_randomness = 1 #this can cause issues with random_chromosomes()
	#once max_gens is reached the algorithm will terminate no matter what
	max_gens = round(k/2)
	#the amount of generations without improvement before termination
	generation_threshold = round(max_gens/5)

	#generating initial population
	population = random_chromosomes(coords, k)
	if method == 'seeded':
		population[-1] = christofides(coords)[0][:-1]
	population = find_fitness(coords, population)

	#generation counters
	generation = 0
	no_improvement = 0
	#defining termination conditions
	while generation < max_gens and no_improvement < generation_threshold:
		
		new_generation = []
		generation += 1
		fittest = population[0]
		print(f'=== Generation: {generation} == Fittest: {fittest[1]} ===')

		#preserving fittest chromosomes from the previous generation
		new_generation.extend([c[1] for c in population[:maintain_rate]])
		#adding completly random chromosomes to the new generation
		new_generation.extend(random_chromosomes(coords, generational_randomness))
		#reproducing until population size is reached
		for x in range(k-maintain_rate-generational_randomness):
				new_generation.append(reproduce(population))

		#finding the fitness of the new generation
		new_generation = find_fitness(coords, new_generation)
		#if no improvement was seen increment the counter
		if population[0] == new_generation[0]:
			no_improvement += 1
		#else:
		#	no_improvement = 0
		#overriding the previous generation
		population = new_generation

	#preparing for the results to be sent to the client	
	t = time.perf_counter()-start
	algorithm_name = f'a {method} genetic algorithm'
	return format(coords, fittest[1]+[fittest[1][0]], t, algorithm_name), [generation]

### Formatting ###

#prepares the result of the algorithms to be sent to the client
def format(coords, path, t, algorithm_name, dist=None):

	#logs final solution
	print(f'Solution using {algorithm_name}: {path}')

	#if the distance wasn't calculated during the algorithm it is calculated here
	if not dist:
		dist = path_dist(coords, path)

	#avoids rerunning bruteforce
	if algorithm_name == 'bruteforce':
		time_comparison = ''
		distance_comparison = 'which, by definition, is optimal'

	#comparing the results to bruteforce, if possible
	elif len(coords) < 10:
		bruteforce_results =  bruteforce(coords)

		#creates a sentence comparing algorithm run time to bruteforce
		if bruteforce_results[1] < t:
			time_comparison = f', ~{sig_fig(t/bruteforce_results[1], 2)}x slower than'
		elif bruteforce_results[1] > t:
			time_comparison = f', ~{str(sig_fig(bruteforce_results[1]/t, 2)).strip(".0")}x faster than'
		else:
			time_comparison = ', taking the same amount of time as'
		time_comparison += f' bruteforce (taking {bruteforce_results[1]}s)'

		#creates a sentence comparing total path weight to bruteforce
		distance_error = abs(dist-bruteforce_results[4])
		if distance_error == 0:
			distance_comparison = 'which is the optimal solution'
		else:
			distance_comparison = f'which has an error of {sig_fig(distance_error, 2)}km'

	#if the problem has too many nodes to feasibly run bruteforce for comparison
	else:
		time_comparison = ', can not be compared because bruteforce was unfeasible due to the quantity of nodes'
		distance_comparison = 'it cannot be determined if this solution is optimal'

	data = None
	return [order_markers(coords, path), sig_fig(t, 2), algorithm_name, time_comparison, dist, distance_comparison]

#rounds value to n significant figures
def sig_fig(value, n):	
	return float('{:g}'.format(float('{:.{p}g}'.format(value, p=n))))