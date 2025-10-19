"""
EmailPreprocessor class - required for loading the trained model
This file must exist before importing the model
"""

import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class EmailPreprocessor(BaseEstimator, TransformerMixin):
    """
    Custom transformer for preprocessing email text
    MUST match the class definition from your training notebook
    """
    def __init__(self,
                 strip_headers=True,
                 lowercase=True,
                 replace_urls=True,
                 replace_numbers=True,
                 remove_punctuation=True,
                 do_stemming=False):
        self.strip_headers = strip_headers
        self.lowercase = lowercase
        self.replace_urls = replace_urls
        self.replace_numbers = replace_numbers
        self.remove_punctuation = remove_punctuation
        self.do_stemming = do_stemming
        if self.do_stemming:
            from nltk.stem import SnowballStemmer
            self.stemmer = SnowballStemmer("english")

    def _strip_headers(self, text):
        """Remove email headers (everything before first blank line)"""
        parts = re.split(r'\r?\n\r?\n', text, maxsplit=1)
        return parts[1] if len(parts) > 1 else text

    def _replace_urls(self, text):
        """Replace URLs with URL token"""
        return re.sub(r'https?://\S+|www\.\S+', ' URL ', text)

    def _replace_numbers(self, text):
        """Replace numbers with NUMBER token"""
        return re.sub(r'\b\d+(?:[.,]\d+)?\b', ' NUMBER ', text)

    def _remove_punct(self, text):
        """Remove punctuation"""
        return re.sub(r'[^\w\s]', ' ', text)

    def _stem(self, text):
        """Apply stemming to words"""
        tokens = text.split()
        tokens = [self.stemmer.stem(t) for t in tokens]
        return " ".join(tokens)

    def transform(self, X, y=None):
        """
        Transform email texts
        
        Args:
            X: array-like of email texts
            y: ignored
            
        Returns:
            np.array: transformed texts
        """
        out = []
        for text in X:
            if self.strip_headers:
                text = self._strip_headers(text)
            if self.lowercase:
                text = text.lower()
            if self.replace_urls:
                text = self._replace_urls(text)
            if self.replace_numbers:
                text = self._replace_numbers(text)
            if self.remove_punctuation:
                text = self._remove_punct(text)
            if self.do_stemming:
                text = self._stem(text)
            # Collapse whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            out.append(text)
        return np.array(out)
    
    def fit(self, X, y=None):
        """Fit method (does nothing, required by sklearn)"""
        return self