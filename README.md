## 基于python3实现的任务批量自动化调度框架  

**功能说明：**
 1. 表映射，数据做ETL直接配置规则及字段实现mapping字段并进行解析后生成可执行HSQL
 2. 映射文件(json)格式及关键字段校验模块
 3. 配置config/configTask.py文件后，直接用DAG模式执行任务
 4.自动化定时执行 
 5. 日志切片模块，切割每日日志文件
 6. 任务监控模块，任务状况邮件提醒  

---

程序执行入口
`nohup python scheJobHip.py &`

**工程结构**
>.
|____bin  代码路径  
| |____command.py  
| |____propertiesUtiil.py  
| |____transforData.py  
| |____checkMaping.py  
| |____logSplit.py  
| |____scheJobHip.py  
| |____assemblyTask.py  
| |____cmdThread.py  
|____config  配置文件路基  
| |____config.perporties  
| |____configTask.py  
|____script  
|____README.md  
|____logs  日志文件路基  
| |____test.log  
| |____test.log.2020-04-26  
|____mappings  映射文件路径  
| |____tb_ml_test2.json  
| |____tb_ml_test.json  
|____sql  执行sql路径  
| |____t_ml_ttt.sql  
