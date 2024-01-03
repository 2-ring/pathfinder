### Imports ###

#External
from flask import Flask, render_template, request, flash, redirect, url_for
from math import *
from random import *
import time, re

### Utility functions ###

#Recursive function that finds all the permutations of the terms in a list
def permutation(lst): #takes any array as input

	#Base case
	if len(lst) < 2:
		if lst:
			return [lst]
		return []

	#The list of permutations
	l = []

	#For each index in the argument
	for i in range(len(lst)):

		 m = lst[i]
		 #All terms except m
		 remLst = lst[:i] + lst[i+1:]

		 #Finds all permutations with m at the start
		 for p in permutation(remLst):
				 l.append([m] + p)		 
	return l #Passes the permutations up the stack frame

#Finds distance between two coordinates accounting for the curvature of the earth
def edge_length(c1, c2): #Coordinates are given as a dictionary
	#Extracts lat and lon values from dictionaries
	lat1, lon1 = c1.values()
	lat2, lon2 = c2.values()
	p = pi/180 #Constant to covert between deg and rad
	#Standard formula
	a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
	return 12742 * asin(sqrt(a)) #Returns as a float

#Adds an edge to an adjacency matrix
def edge_append(graph, nodes):
	for i, node in enumerate(nodes):
		graph[node].append(nodes[1-i])
	return graph

#Removes an edge from a graph
def edge_remove(graph, edge): #graph is an adjacency matrix, edge is a list of two nodes
	for i, node in enumerate(edge):
		graph[node].remove(edge[1-i])
	return graph

#Recursive depth first search function
def dfs(graph, start): #graph is an adjacency matrix, start is the root node for the traversal
	stack, path = [start], []

	while stack:
		vertex = stack.pop()
		if vertex in path:
			continue
		path.append(vertex)
		for neighbour in graph[vertex]:
			stack.append(neighbour)

	return path

#Sorts a two dimensional array by the value of a given index of each term
def sort_2d(lst, sort_by, descending): #lst is a 2d array, sort_by an index and descending is a bool
	return sorted(lst, key=lambda x: x[sort_by], reverse=descending) #returns a 2d array

#Used for christofides and mst-dfs
def shortcut(path):
	shortcutted = [] #nodes that have previously appeared in the path
	for node in path:
		if node not in shortcutted: #if the node has been encountered before
			shortcutted.append(node) #mark the node as encountered
	return shortcutted+[path[0]] #makes the path a cycle by adding the first node to the end

#finds the total distance of a path
def path_dist(coords, path):
	dist = 0 #total distance
	prev = path[0]
	#adds the distance of each hop to the total
	# +path[0] triple checks the path is a cycle - if it already is it will be redundant
	for node in path[1:]+[path[0]]: 
		dist += edge_length(coords[prev], coords[node])
		prev = node
	return dist #returns float

#substitutes each coordinate index for the corrosponding actual coordinate
def order_markers(markers, solution):
	return [markers[x] for x in solution]