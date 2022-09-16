# UDQL
## 引入
* 从CONLL到词节点的完整流程
	1. 载入conll文件为森林对象(不是树的集合)
	2. 解包森林对象为树对象们(树的列表)

## 功能与实现
	### 动词索引
		* 载入
			* 载入conll文件为森林对象
		* 解包
			* 解包森林对象为树对象们
		* 查看/返回/获得
			* 树对象的原始CONLL数据
				* 树对象.data_tree_raw
			* 树对象的所有单词
				* 树对象.get_all_forms()
