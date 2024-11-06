#! /usr/bin/env python3
# coding: utf-8

import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

SRC_DIR = '/content/drive/MyDrive/CSE 419/Lab Assign-5/src'

THIS_DIR = os.path.dirname(os.path.realpath(SRC_DIR))
ROOT_DIR = os.path.dirname(os.path.realpath(THIS_DIR))

word_tokenize = word_tokenize
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()
