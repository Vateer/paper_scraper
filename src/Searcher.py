import requests
from bs4 import BeautifulSoup
import time,random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from src.Analyser import Analyser
from src.FileHandler import FileWriter
from src.Message import Message
from src.tool import *


class Searcher:
    def run(parser:dict):
        str2int = lambda x: int(x.lstrip().rstrip())
        base_url = r"https://dblp.uni-trier.de/search/publ/inc?q=stream:"
        message = Message(parser)
        file_writer = FileWriter(parser['parser']["output_file_path"])

        for aim in parser['parser']['aim'].split(","):
            message.print("Searching for {}".format(aim))
            aim_url = base_url+aim+":%20"
            file_writer.write_t1(aim.split("/")[1].upper())
            for key in parser['parser']['keyward'].split(','):
                aim_url+=key+"%20"
            year_range = parser['parser']['year']
            if year_range:
                if "-" in year_range:
                    year_range = year_range.split('-')
                    year_range = [str2int(year_range[0]),str2int(year_range[1])]
                else:
                    year_range = [str2int(year_range),str2int(year_range)]
            else:
                year_range = [0,0]
            for year in year_range:
                if year != 0:
                    year_url =aim_url + "year:"+str(year)+"%20"
                    file_writer.write_t2(str(year))
                    message.print("Searching for year {}".format(year))
                else:
                    year_url = aim_url
                b = 0
                url_ls = []
                while(True):
                    final_url = year_url + "&s=ydvspc&h=30&b={}".format(str(b))
                    b += 1
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(final_url, headers=headers, verify=False)
                    response.encoding = 'utf-8'
                    if response.status_code == 200:
                        print("search "+final_url)
                    else:
                        raise SystemError("网站无法连接")
                    bs1 = BeautifulSoup(response.text,'lxml')
                    res = bs1.select(".publ")
                    if res.__len__() == 0:
                        break
                    for publ_res in res:
                        href = publ_res.ul.find("li").find("div").a.get("href")
                        url_ls.append(href) #获取需要进去爬的论文网址
                not_handle = []
                for url in url_ls:
                    message.print("Searching for {}".format(url))
                    time.sleep(random.uniform(parser["system"]["delay"],parser["system"]["delay"]+2))
                    handle = True
                    cnt = 0
                    while handle:
                        try:
                            title, abstract = Analyser.run(url)
                            file_writer.write_with_structure(title=title, content=abstract)
                            handle = False
                        except:
                            print("网址 {} 的处理遇到了点问题".format(url))
                            if cnt < parser["system"]["retry"]:
                                print("正在重试第{}次".format(cnt+1))
                                cnt += 1
                            else:
                                not_handle.append(url)
                                handle = False
        file_writer.save()
        if not_handle.__len__():
            print("============不能结局的网址=============")
            for i in not_handle:
                print(i)
            
            