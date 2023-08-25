from typing import List

from kindle2notion.parsing.enums import Word, Locale


class WordDetector:

    def __init__(self, languages: List[Locale]):
        self.languages = languages
        self.language_words = {lang: set() for lang in languages}

        for word in Word:
            for lang in word.value:
                self.language_words[lang].add(word.value[lang])

    def detect(self, text):
        text_words = set(text.split())
        scores = {lang: 0 for lang in self.languages}

        for lang, words in self.language_words.items():
            matches = text_words & words
            scores[lang] += len(matches)

        return max(scores, key=scores.get)
