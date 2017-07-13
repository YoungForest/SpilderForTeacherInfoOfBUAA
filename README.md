# 从官网爬取北航计算机学院老师基本信息

## 需求分析
从学院官网上，我们可以很轻松地获得各个老师的信息。但我们经常会遇到这样一个场景，需要获得研究特定方向的老师有哪些。所以我写了这个爬虫，
来获取北航计算机学院老师的信息，在各个老师的个人简介中有老师的研究方向；将其组织成二维表，存储到csv文件中。使用excel工具，搜索特定方向即可。

比如，搜索“大数据”，可以得到33位老师，满足了同学们通过方向找老师的需求。


## 使用方法
```bash
pip3 install requests BeautifulSoup4
python3 main.py
```

或者直接到release中下载已经爬好的表（注意时间，不过学院官网到是不怎么更新）。

## 仍存在的问题

### Windows下编码异常
在Windows下，爬取时会出现

	writerow(row)
	UnicodeEncodeError: 'gbk' codec can't encode character '\u2022' in position 510: illegal multibyte sequence
异常，但只会影响'樊文飞'和'张茂林'两位老师，其他老师信息没问题。

在Linux下不会出现该问题，因为其使用`UTF-8`编码，用`Excel`打开时要注意编码。
