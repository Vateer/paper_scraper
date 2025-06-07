from abc import ABC, abstractmethod
import docx
import openai
from dashscope import Generation
from src.FileHandler import FileWriter
from src.Message import Message
from tqdm import tqdm
import requests
from openai import OpenAI

class BaseTranslator(ABC):
    def __init__(self, config: dict):
        self.config = config
    
    @abstractmethod
    def translate(self, inp: str) -> str:
        pass
    
    def run(self):
        config = self.config
        file_writer = FileWriter(config['translate']["output_file_path"])
        doc = docx.Document(config['translate']["translate_file"])
        progress_bar = tqdm(doc.paragraphs, desc='Processing', ncols=80)

        for para in progress_bar:
            if para.style.name.startswith("Heading"):
                heading_level = int(para.style.name[-1])
                if heading_level > 2:
                    file_writer.write(para.text, level = heading_level)
                    file_writer.write(self.translate(para.text), level = heading_level)
                    # file_writer.write(self.translate(para.text))
                else:
                    eval("file_writer.write_t{}".format(heading_level))(para.text)
            else:
                if para.text:
                    file_writer.write(para.text)
                    file_writer.write(self.translate(para.text))
                else:
                    file_writer.write('')
            progress_bar.update(1)
        file_writer.save()

class OpenAITranslator(BaseTranslator):
    def __init__(self, config: dict):
        super().__init__(config)
        if config['translate']['openai_host']:
            openai.api_base = config['translate']['openai_host']
        openai.api_key = config['translate']['openai_key']

    def translate(self, inp: str) -> str:
        prompt = "你是一位专业的翻译，请将下面的文本翻译成优雅的简体中文，同时准确保持其原意："
        msg = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": inp},
        ]
        chat_completion = openai.ChatCompletion.create(
            model=self.config['translate']['model'],
            messages=msg,
            temperature=0.1
        )
        return chat_completion.choices[0].message.content



class DeepseekTranslator(BaseTranslator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = OpenAI(
            api_key=config['translate']['deepseek_key'],
            base_url=config['translate']['deepseek_host']
        )
        
    def translate(self, inp: str) -> str:
        prompt = "你是一位专业的翻译，请将下面的文本翻译成优雅的简体中文，同时准确保持其原意："
        response = self.client.chat.completions.create(
            model=self.config['translate']['deepseek_model'],
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": inp}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content

class QwenTranslator(BaseTranslator):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = OpenAI(
            api_key=config['translate']['qwen_key'],
            base_url=config['translate']['qwen_host']
        )
        
    def translate(self, inp: str) -> str:
        prompt = "你是一位专业的翻译，请将下面的文本翻译成优雅的简体中文，同时准确保持其原意："
        response = self.client.chat.completions.create(
            model=self.config['translate']['qwen_model'],
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": inp}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content

class Translator:
    def __init__(self, config: dict):
        self.config = config
        self.translator = self._create_translator()
    
    def _create_translator(self) -> BaseTranslator:
        translators = {
            'openai': OpenAITranslator,
            'deepseek': DeepseekTranslator,
            'qwen': QwenTranslator
        }
        
        translator_type = self.config['translate']['translate_mode'].lower()
        translator_class = translators.get(translator_type)
        if not translator_class:
            raise ValueError(f"Unsupported translator type: {translator_type}")
        
        return translator_class(self.config)
    
    def run(self):
        return self.translator.run()
                    
                    


        
        
    























