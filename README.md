# 爬取本地歌单上的歌曲，下载指定歌曲


实现通过文本中的歌名搜索指定歌曲的功能，下载至本地

Constructions:

       python main.py -h 获取帮助

       python main.py -k 歌曲名
    
       python main.py -t 包含歌曲名的文本路径

文本格式如下：
![歌曲名称列表](/src/txt.png)  

也可以搜索下载某首歌
运行结果：

![运行过程](/src/running.png) 

下载结束：

![下载结果](/src/down.png)  

下载失败的歌曲会记录在当前文件夹下的failsongs中。
