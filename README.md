# UDQL
## 引入
* 世界观
	1. 森林对象 (forrester)
	2. 树林列表(来自森林对象的方法) (list)
	3. 树对象 (udtree)
	4. 词节点对象 (udnode)
* 从CONLL到词节点的完整流程
	1. 载入conll文件为森林对象(不是树的集合)
	2. 解包森林对象为树林列表
	3. 从树林列表里根据序号挑一棵树
	4. 从一棵树中根据某个属性挑一个词节点对象

## 功能与实现
### 动词索引
* 载入
	* 载入conll文件为森林对象
		* 森林对象 = udql.forrester(CONLL文件位置)
* 解包
	* 解包森林对象为树林列表
		* 树林列表 = 森林对象.data_forrest
* 查看/返回/获得
	* 获得一个树对象
		* 树对象 = 树林列表[树序号]
	* 树对象的原始CONLL数据
		* 树对象.data_tree_raw
	* 树对象的所有单词
		* 树对象.get_all_forms()
	* 词节点对象列表
		* 通过词形
			* 树对象.get_nodes_by_form('词形')
		* 通过序号(从1开始)
			* 树对象.get_node_by_id(整数序号)
		* 通过词性
			* 树对象.get_nodes_by_upos('词性')
		* 通过依存关系
			* 树对象.get_node_by_deprel('依存关系')
	* 一个词节点对象的
		* 词形
			* 词节点对象.form
		* 词性(UD tagset)
			* 词节点对象.upos
		* 词性(非UD tagset)
			* 词节点对象.xpos
		* 依存关系
			* 词节点对象.deprel
		* 支配词节点对象
			* 词节点对象.get_head()
		* 从属词节点列表
			* 词节点对象.get_children()
		* 在句中的绝对位置(从0开始)
			* 词节点对象.id
	* 森林中的树数量
		* 森林对象.stat_forrest_size
	* 森林中的平均句长
		* 森林对象.stat_mean_sent_len
	* 森林的绝对平均依存距离(abs MDD)
		* 森林对象.index_forrest_mdd_abs
	* 森林的相对平均依存距离(rel MDD)
		* 森林对象.index_forrest_mdd_rel
	* 一个树对象的原始CONLL数据
		* 树对象.data_tree_raw
	* 一个树对象的绝对平均依存距离
		* 树对象.index_mdd_abs
	* 一个树对象的相对平均依存距离
		* 树对象.index_mdd_rel
	* 一个树对象的token数(句长)
		* 数对象.stat_length
