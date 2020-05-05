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
>|____bin  
| |____command.py  
| |____logSplit.py  
| |____sendEmail.py  
| |____scheJobHip.py  
| |____loggerPro.py  
| |____cmdThread.py  
|____config  
| |_______init__.py  
| |____configTask.py  
|____script  
| |____exploreSql.py  
| |____checkMaping.py  
| |____exploreMappingRealtion.py  
| |____table.txt  
|____README.md  
|____logs  
| |____hipdataload.log.cmd.2020-05-01  
| |____hipdataload.log  
| |____hipdataload.log.cmd.2020-05-03  
| |____hipdataload.log.cmd.2020-05-02  
|____mappings  
| |____tb_ml_dbm_users.json  
| |____tb_ml_dbm_dbsource.json  
|____sql  
| |____tb_ml_dbm_users.sql  
| |____tb_ml_dbm_dbsource.sql  
