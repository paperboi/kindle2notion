from enum import Enum


class Locale(Enum):
    # Enum containing languages
    ENGLISH = "en"
    SPANISH = "es"

    def __str__(self):
        return self.value


class Word(Enum):
    # For each word, we have to handle different languages
    NOTE = {
        Locale.ENGLISH: "note",
        Locale.SPANISH: "nota"
    }
    LOCATION = {
        Locale.ENGLISH: "location",
        Locale.SPANISH: "posición",
    }
    PAGE = {
        Locale.ENGLISH: "page",
        Locale.SPANISH: "página",
    }
    DATE_ADDED = {
        Locale.ENGLISH: "added on",
        Locale.SPANISH: "añadido el",
    }
    # Date formats also depend on language
    DATE_FORMAT = {
        Locale.ENGLISH: "%A, %d %B %Y %I:%M:%S %p",
        Locale.SPANISH: "%A, %d %B %Y %H:%M:%S",
    }

    def __str__(self, language=Locale.ENGLISH):
        return self.value[language]
