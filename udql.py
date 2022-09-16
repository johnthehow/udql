print('''
>>> [thehow.udql]
UDQL: Universal Dependencies for Quantitative Linguistics
Universal Denpendencies计量语言学处理工具包

功能:
1. 将conllu格式的UD树库实例化为Forrest对象>Tree对象>Node对象结构
2. 计算Absolute MDD绝对平均依存距离
3. 计算Relative MDD相对平均依存距离

未来计划:
* 加入复杂网络相关指标
* 加入变量间关系自动匹配功能
	* 线性关系
		* 实现
			* 线性相关系数
			* 线性回归
	* 非线性关系
		* 函数关系
			* 实现
				* 分布拟合
				* 非线性回归
				* 神经网络

已知问题:
1. udnode的代码提示中客串了udtree的属性和方法

使用手册:
1. class forrester
	属性
		stat_forrest_size	统计: 树库中包含的树数量
		stat_forrest_mean_sent_len	统计: 树库中的平均句长
		index_forrest_mdd_abs	指标: 树库绝对mdd
		index_forrest_mdd_rel	指标: 树库相对mdd
		data_forrest		统计: 森林对象(本类的主要功能)	
	方法
		get_forrest_mdd_abs()	方法: 计算树库的绝对MDD
		get_forrest_mdd_rel()	方法: 计算树库的相对MDD
		get_worder_free()	方法: 计算树库的语序自由度
		get_morph_rich(measure)	方法: 计算树库的形态丰富度

2. class udtree
	属性
		data_tree_raw	数据: 一棵树的原始数据(tab切分过的)
		index_mdd_abs	指标: 一棵树的绝对MDD
		index_mdd_rel	指标: 一棵树的相对MDD
		stat_length	指标: 一棵树的token数(长度)
	方法
		get_all_forms()	方法: 显示一棵树的文本内容
		get_all_nodes()	方法: 返回一棵树的所有token作为udnode对象
		get_form_by_id(id)	方法: 根据id显示一个token的文本内容
		get_node_by_id(id)	方法: 返回一个token通过id, 作为udnode对象
		get_form_by_deprel(deprel)	方法: 返回一课树满足依存关系deprel的form
		get_node_by_deprel(deprel)	方法: 返回一棵树满足依存关系deprel的udnode对象
		get_mdd_abs	方法: 返回一棵树的绝对MDD
		get_mdd_rel	方法: 返回一棵树的相对MDD

3. class udnode
	属性
		id	id
		deprel	依存关系: 该词是其支配词的什么
		headid	支配词id
		form	该词的形式
		lemma	该词的词典形
		upos	该词的UD词性标签
		xpos	该词的非UD词性标签
		feats	该词的其他标注属性
	方法
		get_head()	获得该词的支配词(作为udnode)
		get_children()	获得该词的从属词(作为[udnode])
		get_children_by_deprel()	获得该词的满足deprel依存关系的从属词
	''')

class forrester:
	def __init__(self,filename):
		# 原理: 将conllu文件遇到空行就截断成一棵树
		self.__filename = filename
		with open(self.__filename,mode='r',encoding='utf-8') as self.__udfile:
			self.__udlines = self.__udfile.readlines()
		assert self.__udlines != [], print("空的udlines")
		# 删除树库中的注释行
		self.__udlines = [line for line in self.__udlines if not line.startswith('#')]
		# 最后一行若不为空行, 添加入空行, 用于截断步骤识别
		if self.__udlines[-1] != ['\n']:
			self.__udlines.append('\n')
		self.__rawlines = [line for line in self.__udlines if not line.startswith('\n')]
		self.__rawlines = [line.split(sep='\t') for line in self.__rawlines]
		# 容器变量
		self.__tree_segs = []
		self.__tree_seg = []
		# 将由行组成的树库按照空行切段作为树
		for line in self.__udlines:
			if not line.startswith('\n'):
				self.__tree_seg.append(line)
			else:
				self.__tree_segs += [self.__tree_seg]
				self.__tree_seg = []
		assert self.__tree_segs != [], print("空的__tree_segs")
		# 将每棵树中的每一行, 按照\t切段
		self.__cut_tree_segs = [[line.split(sep='\t') for line in tree] for tree in self.__tree_segs]
		# 删除行开头有形如'1-2','7.1'形式的id的, 不影响UD所包含的信息
		self.__cut_tree_segs = [[tkline for tkline in tree if tkline[0].find('-') == -1] for tree in self.__cut_tree_segs]
		self.__cut_tree_segs = [[tkline for tkline in tree if tkline[0].find('.') == -1] for tree in self.__cut_tree_segs]
		# 将每个行列表形式的树实例化为对象树, 依赖udtree类
		self.data_forrest = [udtree(line) for line in self.__cut_tree_segs]
		# 如果森林末尾有空树, 删除这个空树
		if self.data_forrest[-1].get_all_forms() == []:
			self.data_forrest = self.data_forrest[:-1]
		# 描述统计: 树库中的树数量
		self.stat_forrest_size = len(self.data_forrest)
		# 描述统计: 树库中的平均句长
		self.stat_forrest_mean_sent_len = self.__get_mean_sent_len()
		# 指标MDD_ABS
		self.index_forrest_mdd_abs = self.get_forrest_mdd_abs()
		# 指标MDD_REL
		self.index_forrest_mdd_rel = self.get_forrest_mdd_rel()
		self.__udfile.close()
	def __get_mean_sent_len(self):
		forrest = self.data_forrest
		sent_lens = [tree.stat_length for tree in forrest]
		msl = sum(sent_lens)/len(sent_lens)
		return msl
	def get_forrest_mdd_abs(self):
		# 绝对MDD
		forrest = self.data_forrest
		dds = []
		for tree in forrest:
			dds.append(tree.get_mdd_abs())
		mdd_abs = sum(dds)/len(dds)
		return mdd_abs
	def get_forrest_mdd_rel(self):
		# 相对MDD, 绝对MDD除去句长的影响
		forrest = self.data_forrest
		dds = []
		sent_lens = []
		for tree in forrest:
			dds.append(tree.get_mdd_abs())
			sent_lens.append(tree.stat_length)
		mdd = sum(dds)/len(dds)
		msl = sum(sent_lens)/len(sent_lens)
		mdd_rel = mdd/msl
		return mdd_rel
	def get_worder_free(self):
		import scipy
		from scipy import spatial
		forrest = self.data_forrest
		match_tree = []
		svo,sov,vso,vos,osv,ovs = [],[],[],[],[],[]
		for tree in forrest:
			nsubjs = [nsubj for nsubj in tree.get_node_by_deprel('nsubj')]
			if len(nsubjs) != 0:
				for nsubj in nsubjs:
					fin_verb = nsubj.get_head()
					objs = fin_verb.get_children_by_deprel('obj')
					if len(objs) != 0 and fin_verb.upos == 'VERB':
						match_tree.append(tree)
						nsubj_id = nsubj.id
						fin_verb_id = fin_verb.id
						obj_id = objs[0].id
						if nsubj_id<fin_verb_id<obj_id:
							svo.append(tree)
						# SOV
						elif nsubj_id<obj_id<fin_verb_id:
							sov.append(tree)
						# VSO
						elif fin_verb_id<nsubj_id<obj_id:
							vso.append(tree)
						# VOS
						elif fin_verb_id<obj_id<nsubj_id:
							vos.append(tree)
						# OSV
						elif obj_id<nsubj_id<fin_verb_id:
							osv.append(tree)
						# OVS
						elif obj_id<fin_verb_id<nsubj_id:
							ovs.append(tree)
		wodist = [len(svo),len(sov),len(vso),len(vos),len(osv),len(ovs)]
		wodist_norm = [i/sum(wodist) for i in wodist]
		absfreewo = [1/6]*6
		wofreedom = 1-scipy.spatial.distance.cosine(absfreewo,wodist_norm)
		res = {'wodist':wodist,'wofree':wofreedom}
		return res
	def get_morph_rich(self,measure):
		from lexical_diversity import lex_div as lexdiv
		conll_lines = self.__rawlines
		raws = [line[1] for line in conll_lines]
		lemmas = [line[2] for line in conll_lines]
		raw_txt = ' '.join(raws)
		lem_txt = ' '.join(lemmas)
		raw_txt_tok = lexdiv.tokenize(raw_txt)
		lem_txt_tok = lexdiv.tokenize(lem_txt)
		if measure == 'MATTR':
			winlen = 500
			raw_txt_morph_rich = lexdiv.mattr(raw_txt_tok,winlen)
			lem_txt_morph_rich = lexdiv.mattr(lem_txt_tok,winlen)
		elif measure == 'MSTTR':
			winlen = 500
			raw_txt_morph_rich = lexdiv.msttr(raw_txt_tok,winlen)
			lem_txt_morph_rich = lexdiv.msttr(lem_txt_tok,winlen)
		elif measure == 'HDD':
			raw_txt_morph_rich = lexdiv.hdd(raw_txt_tok)
			lem_txt_morph_rich = lexdiv.hdd(lem_txt_tok)
		elif measure == 'MTLD':
			raw_txt_morph_rich = lexdiv.mtld(raw_txt_tok)
			lem_txt_morph_rich = lexdiv.mtld(lem_txt_tok)
		elif measure == 'MTLDMABID':
			raw_txt_morph_rich = lexdiv.mtld_ma_bid(raw_txt_tok)
			lem_txt_morph_rich = lexdiv.mtld_ma_bid(lem_txt_tok)
		mamr = raw_txt_morph_rich - lem_txt_morph_rich
		return mamr

class udtree:
	def __init__(self,tree_data):
		self.stat_length = len(tree_data)
		self.data_tree_raw = tree_data
		# self.index_mdd_abs = self.get_mdd_abs()
		# self.index_mdd_rel = self.get_mdd_rel()
	def get_raw_line_by_id(self,id):
		line_raw = self.data_tree_raw[id-1]
		return line_raw
	def get_raw_lines_by_form(self,form):
		form = form.lower()
		lines_raw = [line_raw for line_raw in self.data_tree_raw if line_raw[1].lower()==form]
		return lines_raw
	def get_all_forms(self):
		token_forms = [line[1] for line in self.data_tree_raw]
		return token_forms
	def get_form_by_deprel(self,deprel):
		res_deprel = [line[1] for line in self.data_tree_raw if line[7]==deprel]
		return res_deprel
	def get_node_by_deprel(self,deprel):
		id_list = [int(line[0]) for line in self.data_tree_raw if line[7]==deprel]
		nodelist = [self.get_node_by_id(nid) for nid in id_list]
		return nodelist
	def get_form_by_upos(self,upos):
		res_upos = [line[1] for line in self.data_tree_raw if line[3]==upos]
		return res_upos
	def get_nodes_by_upos(self,upos):
		id_list = [int(line[0]) for line in self.data_tree_raw if line[3]==upos]
		nodelist = [self.get_node_by_id(nid) for nid in id_list]
		return nodelist
	def get_form_by_id(self,id):
		res_id = [line[1] for line in self.data_tree_raw if line[0]==str(id)]
		return res_id
	def get_node_by_id(self,id):
		node = udnode(self.get_raw_line_by_id(id),self.data_tree_raw)
		return node
	def get_nodes_by_form(self,form):
		form = form.lower()
		nodes = [udnode(line_raw,self.data_tree_raw) for line_raw in self.get_raw_lines_by_form(form)]
		return nodes
	def get_all_nodes(self):
		id_list = [int(line[0]) for line in self.data_tree_raw]
		nodelist = [self.get_node_by_id(nid) for nid in id_list]
		return nodelist
	def get_mdd_abs(self):
		nodelist = self.get_all_nodes()
		ddlist = [abs(node.id-node.headid) for node in nodelist if node.headid != 0]
		mdd_abs = sum(ddlist)/len(nodelist)
		return mdd_abs
	def get_mdd_rel(self):
		nodelist = self.get_all_nodes()
		ddlist = [abs(node.id-node.headid) for node in nodelist if node.headid != 0]
		mdd_abs = sum(ddlist)/len(nodelist)
		mdd_rel = mdd_abs/self.stat_length
		return mdd_rel
	def get_word_mdd_abs(self,form):
		form = form.lower()
		nodelist = self.get_nodes_by_form(form)
		ddlist = [abs(node.id-node.headid) for node in nodelist if node.headid != 0]
		mdd_abs = sum(ddlist)/len(nodelist)
		return mdd_abs
	def get_word_mdd_rel(self,form):
		form = form.lower()
		nodelist = self.get_nodes_by_form(form)
		ddlist = [abs(node.id-node.headid)/self.stat_length for node in nodelist if node.headid != 0]
		mdd_rel = sum(ddlist)/len(nodelist)
		return mdd_rel



class udnode(udtree):
	def __init__(self,node_data,tree_data):
		super().__init__(tree_data)
		self.id = int(node_data[0])
		self.form = node_data[1]
		self.lemma = node_data[2]
		self.upos = node_data[3]
		self.xpos = node_data[4]
		self.feats = node_data[5]
		self.headid = int(node_data[6])
		self.deprel = node_data[7]
	def get_head(self):
		if int(self.headid) == 0:
			self.head = self
		else:
			self.head = self.get_node_by_id(int(self.headid))
		return self.head
	def get_children(self):
		children_id = [int(line[0]) for line in self.data_tree_raw if int(line[6]) == self.id]
		children = [self.get_node_by_id(childid) for childid in children_id]
		return children
	def get_children_by_deprel(self,deprel):
		children = self.get_children()
		res_children = [child for child in children if child.deprel == deprel]
		return res_children
	def get_depdistance(self):
		depdistance = abs(self.id-self.headid)
		return depdistance

def get_word_mdd(word,trees):
	''' 在tree组成的list(从forrester.data_forrest获得)中计算一个词的平均依存距离'''
	worddd = []
	for tree in trees:
		wordnodes = tree.get_nodes_by_form(word)
		for wordnode in wordnodes:
			worddd.append(wordnode.get_depdistance())
	wordmdd = sum(worddd)/len(worddd)
	return wordmdd

def get_deprel_mdd(deprel,trees):
	'''获得一个依存关系的在所有句子中的平均依存距离'''
	depreldds = []
	for tree in trees:
		tree_node_dep_diss = []
		deprel_nodes = tree.get_node_by_deprel(deprel)
		if len(deprel_nodes) > 0:
			for node in deprel_nodes:
				dep_dis = abs(node.id-node.headid)
				tree_node_dep_diss.append(dep_dis)
			depreldds.append(sum(tree_node_dep_diss)/len(tree_node_dep_diss))
		else:
			pass
	avg_deprel_dep_dis = sum(depreldds)/len(depreldds)
	return avg_deprel_dep_dis

def get_pos_mdd(pos,trees):
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

if __name__ == "__main__":
	import os
	cwd = os.getcwd()
	treebankpath = cwd +'\\'+'treebanks\\'
	respath = cwd + '\\' + 'res\\res.txt'
	os.chdir(treebankpath)
	filelist = os.listdir()
	print('''
Measures Available:
1. MATTR
2. MSTTR
3. HDD
4. MTLD
5. MTLD_MA_BID (MTLDMABID)
		''')
	morph_rich_measure = input('Input Morphological Richness Measure:')
	with open(respath,mode='a+',encoding='utf-8') as res_file:
		print('Result file created at: ' + str(respath))
		res_file.write('filename')
		res_file.write('\t')
		res_file.write('mdd_abs')
		res_file.write('\t')
		res_file.write('mdd_rel')
		res_file.write('\t')
		res_file.write('worder_free')
		res_file.write('\t')
		res_file.write('morph_rich')
		res_file.write('\n')
	for file in filelist:
		forrest_obj = forrester(file)
		mdd_abs = forrest_obj.get_forrest_mdd_abs()
		mdd_rel = forrest_obj.get_forrest_mdd_rel()
		worder_freedom = forrest_obj.get_worder_free()['wofree']
		morph_rich = forrest_obj.get_morph_rich(morph_rich_measure)
		print(file)
		print('MDD_ABS: ' + str(mdd_abs))
		print('MDD_REL: ' + str(mdd_rel))
		print('WODER_FREE: ' + str(worder_freedom))
		print('MORPH_RICH: ' + str(morph_rich))
		with open(respath,mode='a+',encoding='utf-8') as res_file:
			res_file.write(file)
			res_file.write('\t')
			res_file.write(str(mdd_abs))
			res_file.write('\t')
			res_file.write(str(mdd_rel))
			res_file.write('\t')
			res_file.write(str(worder_freedom))
			res_file.write('\t')
			res_file.write(str(morph_rich))
			res_file.write('\n')
	os.system('pause')
