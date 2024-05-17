import os
import yaml
import locale

class Translator:
    def __init__(self, lang='en-us'):
        self.lang = lang
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        lang_file = f"{self.lang}.yaml"
        if os.path.exists(lang_file):
            with open(lang_file, 'r', encoding='utf-8') as file:
                self.translations = yaml.safe_load(file)
        else:
            raise FileNotFoundError(f"Translation file '{lang_file}' not found.")

    def translate(self, key):
        return self.translations.get(key, key)

def get_system_language():
    # 获取系统语言设置
    system_lang, _ = locale.getdefaultlocale()
    return system_lang

# 获取系统语言并设置翻译器
system_lang = get_system_language()

# 映射系统语言到yml文件的名称
lang_mapping = {
    'zh_CN': 'zh-cn',
    'en_US': 'en-us',
}

# 设置默认语言为英文
lang = lang_mapping.get(system_lang, 'en-us')

translator = Translator(lang)

# 使用翻译器
# print(translator.translate('你好'))  # 根据系统语言输出相应的问候语
