import networkx as nx
import random
import math

def replace_in_context(new_nodes, old_nodes, new_graph, master):
	for node in old_nodes:
		new_graph.remove_node(node)
	for node in new_nodes:
		new_graph.add_node(node)
		for neighbor in master.neighbors(node):
			if neighbor in new_graph:
				new_graph.add_edge(node, neighbor)
	return new_graph

def mcmc_subgraph_sample (master, eg):
	#import pdb; pdb.set_trace()
	
	new_graph = eg.copy()
	new_num_edges = curr_num_edges = num_eg_edges = nx.number_of_edges (eg)	
	iterations = 2 * nx.number_of_nodes (eg)    # play around w/ this number
	step_size = 1								# play around w/ this number
	sample_set = set(master.nodes_iter()) - set(eg.nodes_iter())
	coeff = 1
	for i in range(iterations):
		new_nodes = random.sample(sample_set, step_size) 
		old_nodes = random.sample(new_graph.nodes(), step_size)
		new_graph = replace_in_context(new_nodes, old_nodes, new_graph, master)
		new_num_edges = nx.number_of_edges(new_graph)
		new_stat = abs(new_num_edges - num_eg_edges) 
		old_stat = abs(curr_num_edges - num_eg_edges) 
		rval = random.random()
		if (new_stat <= old_stat) or (rval < math.exp(coeff * (old_stat - new_stat))):
			# use new graph
			curr_num_edges = new_num_edges
			sample_set = (sample_set | set(new_nodes)) - set(old_nodes) 
		else:
			# swap back old graph
			new_graph = replace_in_context(old_nodes, new_nodes, new_graph, master)
		if new_stat > num_eg_edges:
			coeff *= 1
	return new_graph.nodes_iter()



