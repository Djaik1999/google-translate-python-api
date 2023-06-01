import os
import csv

import requests
from bs4 import BeautifulSoup

class GoogleTranslateAPI:
    def __init__(self, target_lang="ru", source_lang="en", timeout=5) -> None:
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.timeout = timeout

    def create_list(self, oneline_str, separator="; "):
        return oneline_str.split(separator)
    
    def _get_soup(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        response = requests.get(url, headers)
        return BeautifulSoup(response.text, "html.parser")
    
    def translate_one(self, word, target_lang=None, source_lang=None, timeout=None):
        """Translate one word"""
        if target_lang is None:
            target_lang = self.target_lang
        if source_lang is None:
            source_lang = self.source_lang
        if timeout is None:
            timeout = self.timeout

        url = f"https://translate.google.com/m?sl={source_lang}&tl={target_lang}&hl={target_lang}&q={word}"
        response_page = self._get_soup(url)
        try:
            result = response_page.find(class_="result-container").text
        except Exception as e:
            print(f"URL: {url}")
            raise e

        return result

    def translate_list(self, words_list):
        result_list = list()
        for word in words_list:
            translated_word = self.translate_one(word)
            result_list.append((word, translated_word, self.source_lang))
            print(f"{word} - {translated_word}")

        return result_list
    
    def result_to_csv(self, result_list, filename="result", path=""):
        
        if filename.endswith(".csv"):
            filename = filename[:-4]

        if os.path.exists(path):
            # Некорректно
            with open(f"{path}\\{filename}.csv", "w", encoding="utf-8") as fout:
                writer = csv.writer(fout)

                for row in result_list:
                    print(row)
                    writer.writerow(row)
