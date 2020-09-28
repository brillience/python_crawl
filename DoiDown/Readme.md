# 该工具使用Scrapy框架实现由DOI号 在 SCI-HUB网站上下载文献pdf文件到本地
# 所使用的数据库为Mysql，借助了https://github.com/tomleung1996/wos_crawler 该程序作为搜索相关文献的工具。
# 使用方法
- 安装mysql，创建wos_of_science数据库
- 使用wos_crawler爬取检索的内容到本地数据库
- 在spiders文件夹下的doi_down文件中修改mysql连接信息