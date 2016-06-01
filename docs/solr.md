
下载安装包 <http://apache.fayea.com/lucene/solr/5.5.1/solr-5.5.1.tgz>

- 解压solr-5.5.1.tgz
  - `tar zxvf solr-5.5.1.tgz`

- 启动Solr 并启动一个cloud的示例
  - `./bin/solr start -e cloud
  - 启动的时候  会提示
  ``` code
  NOTE: Please install lsof as this script needs it to determine if Solr is listening on port 89
  ```
  - 执行 `sudo apt-get install lsof` 这个工具还是挺有用的 建议安装上
  - 再次启动 目测是因为启动超过30s了 之后验证这个错误是可以忽略滴
  ``` code
  ERROR: Did not see Solr at http://localhost:8983/solr come online within 30
  ```
  - 查了下日志 './server/logs/\*.log' 好像不是这个问题 执行 ｀java -server -version｀ 出现以下问题 怀疑是内置jdk有问题
  ``` code
  Error occurred during initialization of VM
  Server VM is only supported on ARMv7+ VFP
  ```
  - 果真是jdk有问题 修改 `./bin/solr.in.sh` 增加
  ``` code
  SOLR_OPTS = '${SOLR_OPTS} -client'
  ```
  - 再次启动 `./bin/solr start -e cloud -V` 访问 http://yourip:8983/solr 成功
  ```
  Starting Solr using the following settings:
    JAVA            = java
    SOLR_SERVER_DIR = /usr/local/solr/server
    SOLR_HOME       = /usr/local/solr/server/solr
    SOLR_HOST       =
    SOLR_PORT       = 8983
    STOP_PORT       = 7983
    JAVA_MEM_OPTS   = -Xms128m -Xmx128m
    GC_TUNE         = -XX:NewRatio=3 -XX:SurvivorRatio=4 -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=8 -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:ConcGCThreads=4 -XX:ParallelGCThreads=4 -XX:+CMSScavengeBeforeRemark -XX:PretenureSizeThreshold=64m -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=50 -XX:CMSMaxAbortablePrecleanTime=6000 -XX:+CMSParallelRemarkEnabled -XX:+ParallelRefProcEnabled
    GC_LOG_OPTS     = -verbose:gc -XX:+PrintHeapAtGC -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintTenuringDistribution -XX:+PrintGCApplicationStoppedTime -Xloggc:/usr/local/solr/server/logs/solr_gc.log
    SOLR_TIMEZONE   = UTC
    SOLR_OPTS        = -Xss256k -client
  ```
