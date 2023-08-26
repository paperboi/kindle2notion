from typing import List

from kindle2notion.languages.enums import Word, Locale


class WordDetector:

    def __init__(self, languages: List[Locale]):
        self.languages = languages
        self.language_words = {lang: set() for lang in languages}

        for word in Word:
            for lang in word.value:
                self.language_words[lang].add(word.value[lang])

    def detect(self, text):
        scores = {lang: 0 for lang in self.languages}
        for lang, words in self.language_words.items():
            scores[lang] = sum([len(word) for word in words if self.has_word(text, word)])
        return max(scores, key=scores.get)

    def has_word(self, text, word):
        return word.lower() in text.lower()

