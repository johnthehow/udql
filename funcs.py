import matplotlib.pyplot as plt
from collections import Counter
def func_word_mdd(word,trees):
	''' 在tree组成的list(从forrester.all_trees获得)中计算一个词的平均依存距离'''
	worddd = []
	for tree in trees:
		wordnodes = tree.get_nodes_by_form(word)
		for wordnode in wordnodes:
			worddd.append(wordnode.get_depdistance())
	wordmdd = sum(worddd)/len(worddd)
	return wordmdd

def func_deprel_mdd(deprel,trees):
	'''获得一个依存关系的在所有句子中的平均依存距离'''
	depreldds = []
	for tree in trees:
		tree_node_dep_diss = []
		deprel_nodes = tree.get_nodes_by_deprel(deprel)
		if len(deprel_nodes) > 0:
			for node in deprel_nodes:
				dep_dis = abs(node.id-node.headid)
				tree_node_dep_diss.append(dep_dis)
			depreldds.append(sum(tree_node_dep_diss)/len(tree_node_dep_diss))
		else:
			pass
	avg_deprel_dep_dis = sum(depreldds)/len(depreldds)
	return avg_deprel_dep_dis

def func_pos_mdd(pos,trees):
	'''获得一种词性的平均依存距离'''
	posdds = []
	for tree in trees:
		tree_node_dep_diss = []
		pos_nodes = tree.get_nodes_by_upos(pos)
		if len(pos_nodes) > 0:
			for node in pos_nodes:
				dep_dis = abs(node.id-node.headid)
				tree_node_dep_diss.append(dep_dis)
			posdds.append(sum(tree_node_dep_diss)/len(tree_node_dep_diss))
		else:
			pass
	avg_pos_dep_dis = sum(posdds)/len(posdds)
	return avg_pos_dep_dis

def func_token_head_pos_dist(token,sentlen,trees,return_dist=True,return_raw_count=False,show_viz=False):
	'''获得一个词在指定句长的支配词位置分布'''
	token_selected_trees = []
	token_len_selected_trees = []
	token_head_pos = []
	for tree in trees:
		if token in [i.lower() for i in tree.get_all_forms()]:
			token_selected_trees.append(tree)
	for stree in token_selected_trees:
		if stree.stat_length == sentlen:
			token_len_selected_trees.append(stree)
	for tstree in token_len_selected_trees:
		matched_nodes = tstree.get_nodes_by_form(token)
		for node in matched_nodes:
			token_head_pos.append(node.headid)
	token_head_pos_dist = Counter(token_head_pos)
	for i in range(1,sentlen+1):
		if i not in token_head_pos_dist.keys():
			token_head_pos_dist[i]=0
	token_head_pos_dist = sorted(token_head_pos_dist.items())
	if show_viz == True:
		xs = [i[0] for i in token_head_pos_dist]
		ys = [i[1] for i in token_head_pos_dist]
		for i in range(1,sentlen+1):
			if i not in xs:
				if i==1:
					ys = [0]+ys
				else:
					try:
						ys[i-1]=0
					except:
						ys.append(0)
		print(xs)
		print([i for i in range(1,sentlen+1)])
		print(ys)
		plt.bar([i for i in range(1,sentlen+1)],ys,tick_label=[i for i in range(1,sentlen+1)],edgecolor='k')
		plt.show()
	if return_dist == True:
		return token_head_pos_dist
	elif return_raw_count == True:
		return token_head_pos

def vis_func_token_head_dist(token,sentlen,trees):
	res = dict(Counter(func_token_head_dist(token,sentlen,trees)))
	xs = [i[0] for i in sorted(res.items(), key = lambda kv: kv[0])]
	ys = [i[1] for i in sorted(res.items(), key = lambda kv: kv[0])]
	for i in range(1,sentlen+1):
		if i not in xs:
			if i==1:
				ys = [0]+ys
			else:
				try:
					ys[i-1]=0
				except:
					ys.append(0)
	print(xs)
	print([i for i in range(1,sentlen+1)])
	print(ys)
	plt.bar([i for i in range(1,sentlen+1)],ys,tick_label=[i for i in range(1,sentlen+1)],edgecolor='k')
	plt.show()


