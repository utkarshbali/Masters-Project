def replace_in_context(new_nodes, old_nodes, new_graph, master):
	for node in old_nodes:
		new_graph.remove(node)
	for node in new_nodes:
		new_graph.add(node)
		for neigbor in master[node].neighbors():
			new_graph.add(node, neighbor)
	return new_graph

def mcmc_subgraph_sample (master, eg):
	new_graph = eg.copy()
	new_num_edges = curr_num_edges = num_eg_edges = nx.number_of_edges (eg)	
	iterations = 2 * nx.number_of_nodes (eg)    # play around w/ this number
	step_size = 1								# play around w/ this number
	sample_set = set(master.nodes) - set(eg.nodes)

	for i in range(iterations):
		new_nodes = random.sample(sample_set, step_size) 
		old_nodes = random.sample(new_graph.nodes, step_size)
		new_graph = replace_in_context(new_nodes, old_nodes, new_graph, master)
		new_num_edges = nx.number_of_edges(eg)
		new_stat = math.abs(new_num_edges - num_eg_edges) 
		old_stat = math.abs(curr_num_edges - num_eg_edges) 
		if new_stat <= old_stat | random.random() > math.exp(old_stat- new_stat):
			# use new graph
			curr_num_edges = new_num_edges
			sample_set = (sample_set | set(new_nodes)) - set(old_nodes) 
		else:
			# swap back old graph
			new_graph = replace_in_context(old_nodes, new_nodes, new_graph, master)

	return new_graph.nodes



