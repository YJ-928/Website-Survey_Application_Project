"""
Translation utility for converting English text to Telugu at runtime
"""
import json
import os
from pathlib import Path
from typing import Optional


class TranslationService:
    """Service to handle runtime translations from English to Telugu"""
    
    _instance = None
    _translations = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationService, cls).__new__(cls)
            cls._instance._load_translations()
        return cls._instance
    
    def _load_translations(self):
        """Load Telugu translations from JSON file"""
        if self._translations is not None:
            return
        
        # Get the path to translations file (go up to django root, then into data folder)
        base_dir = Path(__file__).resolve().parent.parent.parent
        translations_path = base_dir / 'data' / 'translations_te.json'
        
        try:
            with open(translations_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Flatten the nested structure for easier lookup
            self._translations = {}
            for category, translations in data.items():
                self._translations.update(translations)
                
        except FileNotFoundError:
            print(f"Warning: Translation file not found at {translations_path}")
            self._translations = {}
        except json.JSONDecodeError as e:
            print(f"Warning: Error parsing translation file: {e}")
            self._translations = {}
    
    def translate(self, text: str, language: str = 'en') -> str:
        """
        Translate text from English to specified language
        
        Args:
            text: The English text to translate
            language: Target language code ('en' or 'te')
        
        Returns:
            Translated text if language is 'te' and translation exists,
            otherwise returns original text
        """
        if not text or language == 'en':
            return text
        
        if language == 'te':
            # Return Telugu translation if exists, otherwise fallback to English
            return self._translations.get(text, text)
        
        return text
    
    def get_all_translations(self) -> dict:
        """Return all translations for debugging purposes"""
        return self._translations.copy()


# Singleton instance
translation_service = TranslationService()


def translate(text: str, language: str = 'en') -> str:
    """
    Convenience function to translate text
    
    Args:
        text: English text to translate
        language: Target language code ('en' or 'te')
    
    Returns:
        Translated text
    """
    return translation_service.translate(text, language)
