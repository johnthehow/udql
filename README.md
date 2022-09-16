# UDQL
## 引入
* 世界观
	1. 森林对象
	2. 树林列表(来自森林对象的方法)
	3. 树对象
	4. 词节点对象
* 从CONLL到词节点的完整流程
	1. 载入conll文件为森林对象(不是树的集合)
	2. 解包森林对象为树对象们(树的列表)

## 功能与实现
### 动词索引
* 载入
	* 载入conll文件为森林对象
		* 森林对象 = udql.forrester(CONLL文件位置)
* 解包
	* 解包森林对象为树林列表
		* 树林对象 = 森林对象.data_forrest
* 查看/返回/获得
	* 树对象的原始CONLL数据
		* 树对象.data_tree_raw
	* 树对象的所有单词
		* 树对象.get_all_forms()
	* 一个词,作为node对象
		* 通过词形
			* 树对象.get_nodes_by_form('词形')
		* 通过序号
			* 树对象.get_node_by_id(整数序号)
		* 通过词性
			* 树对象.get_nodes_by_upos('词性')
		* 通过依存关系
			* 树对象.get_node_by_deprel('依存关系')
