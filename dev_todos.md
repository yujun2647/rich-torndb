# 功能优化
* 创建表doc，筛选去掉 IF NOT EXISTS 检测 [完成]
* 字段添加，使用 after 

# 开始测试功能
## 编写测试，测试是否成功插入，然后删除数据/ 或者一开始插入时，user_id 使用随机数 [完成]

## 把 join table 功能带过来2 [完成]

# 重写 __subclass__, 解决单元测试时，Base 子类 混乱问题 [已处理，放弃，这样弄得更乱]
    * mock_tables/mock_rich_torndb.py
    * 每个测试方法前后，将 MockBase 的 subclasses 清空
    