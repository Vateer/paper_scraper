import docx
import openai
from src.FileHandler import FileWriter
from src.Message import Message
from tqdm import tqdm

class Translator():
    def __init__(self, parser:dict):
        if parser['translate']['openai_host']:
            openai.api_base = parser['translate']['openai_host']
        openai.api_key = parser['translate']['openai_key']
        self.parser = parser

    def translate(self, inp:str):
        prompt = "You are a professional translator, and I will provide you with various languages from academic conferences. Your task is to accurately convey the meaning of these languages and translate them into elegant Simplified Chinese."
        msg = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Code summarization aims to generate brief natural language descriptions for source codes."},
            {"role": "assistant", "content": "代码概述旨在为源代码生成简洁的自然语言描述。"},
            {"role": "user", "content": inp},
        ]
        chat_completion = openai.ChatCompletion.create(model=self.parser['translate']['model'], messages=msg,temperature=0.1)
        return chat_completion.choices[0].message.content

    def run(self):
        parser = self.parser
        file_writer = FileWriter(parser['translate']["output_file_path"])
        doc = docx.Document(parser['translate']["translate_file"])
        progress_bar = tqdm(doc.paragraphs, desc='Processing', ncols=80)

        # for para in doc.paragraphs:
        for para in progress_bar:
            if para.style.name.startswith("Heading"):
                heading_level = int(para.style.name[-1])
                if heading_level > 2:
                    file_writer.write(para.text, level = heading_level)
                    file_writer.write(self.translate(para.text), level = heading_level)
                else:
                    eval("file_writer.write_t{}".format(heading_level))(para.text)
            else:
                if para.text:
                    file_writer.write(para.text)
                    file_writer.write(self.translate(para.text))
                else:
                    file_writer.write('')
            # progress_bar.set_postfix({'content': para.text})
            progress_bar.update(1)
        file_writer.save()
                    
                    


        
        
    























