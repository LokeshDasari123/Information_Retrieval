#! /usr/bin/env python3
# coding: utf-8

import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Update the ROOT_DIR to point to the correct directory if necessary
SRC_DIR = '/content/drive/MyDrive/CSE 419/Lab Assign-5/src_2'

THIS_DIR = os.path.dirname(os.path.realpath(SRC_DIR))
ROOT_DIR = os.path.dirname(os.path.realpath(THIS_DIR))

# Initialize NLTK components
word_tokenize = word_tokenize
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()