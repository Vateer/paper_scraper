import yaml 
from src.Searcher import Searcher
from src.Translator import Translator
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)

config_file_path = './config.yaml'
config = load_config(config_file_path)

if config['engine']['mode'] == 'parser':
    Searcher.run(config)
elif config['engine']['mode'] == 'translate':
    translator = Translator(config)
    translator.run()
print("done!")
