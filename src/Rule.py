from bs4 import BeautifulSoup
class Rule:
    #返回标题，内容
    def ieee_rule(html:str):
        bs1 = BeautifulSoup(html,'lxml')
        title = bs1.select_one('title').text.split("|")[0]
        content = [bs1.select_one('meta[property="twitter:description"]')['content']]
        return title, content #?
    def acm_rule(html:str):
        bs1 = BeautifulSoup(html,'lxml')
        total_abstract = bs1.select(".abstractSection.abstractInFull")[0]
        title = bs1.select(".citation__title")[0]
        res = []
        for ab in total_abstract.find_all('p'):
            res.append(ab.text)
        return title.text, res
    def aaai_rule(html:str):
        bs1 = BeautifulSoup(html,'lxml')
        title = bs1.select(".page_title")[0].text.replace("\n","").replace("\t","")
        content = bs1.select(".abstract")[0].text.replace("\nAbstract\n","").rsplit("\n")[0].lstrip("\t")
        return title, [content]
    def pmlr_rule(html:str):
        bs1 = BeautifulSoup(html,'lxml')
        title = bs1.select(".post-content")[0].select("h1")[0].text
        content = bs1.select(".abstract")[0].text.lstrip("\n").lstrip(" ").lstrip("\n").rstrip(" ").rstrip("\n").rstrip(" ")
        return title, [content]
    def ijcai_rule(html:str):
        bs1 = BeautifulSoup(html,'lxml')
        title = bs1.select(".container-fluid")[0].select("h1")[0].text.replace("\t","").lstrip("\n").lstrip(" ").lstrip("\n").rstrip("\n").rstrip(" ").rstrip("\n")
        content = bs1.select(".container-fluid")[0].select(".col-md-12")[0].text.replace("\t","").lstrip("\n").lstrip(" ").lstrip("\n").rstrip("\n").rstrip(" ").rstrip("\n")
        return title, [content]