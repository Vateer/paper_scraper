from src.Rule import Rule
# from Rule import Rule
import requests
from bs4 import BeautifulSoup
from src.tool import *


class Analyser():
    def judge(url:str):
        if "ieee.org" in url:
            return "ieee"
        elif "CVPR" in url:
            return "ieee"
        elif "ijcai." in url:
            return "ijcai"
        elif "doi.org" in url and "aaai." not in url:
            return "acm"
        elif "aaai." in url:
            return "aaai"
        elif "proceedings.mlr.press" in url:
            return "pmlr"
        else:
            return "unknown"
    def run(url:str) -> list:
        response = requests.get(url,'lxml',headers=headers)
        response.encoding = 'utf-8'
        res_ls:list
        title:str
        if Analyser.judge(url) == "ieee":
            title, res_ls = Rule.ieee_rule(response.text)
        elif Analyser.judge(url) == "acm":
            title, res_ls = Rule.acm_rule(response.text)
        elif Analyser.judge(url) == "aaai":
            title, res_ls = Rule.aaai_rule(response.text)
        elif Analyser.judge(url) == "pmlr":
            title, res_ls = Rule.pmlr_rule(response.text)
        elif Analyser.judge(url) == "ijcai":
            title, res_ls = Rule.ijcai_rule(response.text)
        else:
            return None
        return title, res_ls


# print(Analyser.run("https://doi.org/10.1109/CVPR52729.2023.02351"))
