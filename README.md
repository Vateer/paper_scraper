# paper_scraper
## 总体介绍

一个用于爬取dblp上论文标题和摘要的爬虫。

原理：通过关键词在dblp上搜索，将搜索结果爬取下来，并可以通过gpt翻译。

代码比较简单，目前主要适配了IEEE，ACM，AAAI，PMLR平台的，其他没有的可以自己适配，主要修改src.Analyser和src.Rule即可。

## 使用方法

修改config.yaml，然后运行

```bash
python main
```

