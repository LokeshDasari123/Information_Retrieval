#! /usr/bin/env python3
# coding: utf-8

import os
import argparse
from definitions import ps
from classes.reuters import Reuters
from classes.spimi import SPIMI
from classes.query import Query, AndQuery, OrQuery
from classes.compression_table import CompressionTable
from classes.bm25 import BM25

def stem_index(index):
    """
    Convert all index keys to lowercase and combine postings to make queries more consistent.
    :param index: Dictionary containing terms and postings.
    :return: Index with all keys stemmed and postings combined.
    """
    new_index = {}
    for k, v in index.items():
        stemmed_key = ps.stem(k)
        if stemmed_key not in new_index:
            new_index[stemmed_key] = index[k]
        else:
            new_index[stemmed_key] += index[k]
    return new_index

parser = argparse.ArgumentParser(description="Configure Reuters parser and set document limit per block.")

parser.add_argument("-d", "--docs", type=int, help="Documents per block", default=500)
parser.add_argument("-r", "--reuters", type=int, help="Number of Reuters files to parse, choice from 1 to 22", choices=range(1, 23), default=22)
parser.add_argument("-rs", "--remove-stopwords", action="store_true", help="Remove stopwords", default=False)
parser.add_argument("-s", "--stem", action="store_true", help="Stem terms", default=False)
parser.add_argument("-c", "--case-folding", action="store_true", help="Use case folding", default=False)
parser.add_argument("-rn", "--remove-numbers", action="store_true", help="Remove numbers", default=False)
parser.add_argument("-a", "--all", action="store_true", help="Use all compression techniques", default=False)
parser.add_argument("-p", "--path", type=str, help="Path to the dataset directory", default='/content/drive/MyDrive/CSE 419/Lab Assign-4/1000_documents')

args = parser.parse_args()

if __name__ == '__main__':
    if args.all:
        args.remove_stopwords = True
        args.stem = True
        args.case_folding = True
        args.remove_numbers = True

    # Initialize Reuters and process tokens
    reuters = Reuters(
        dataset_directory=args.path,  # Use the path argument from command line
        number_of_files=args.reuters,
        docs_per_block=args.docs,
        remove_stopwords=args.remove_stopwords,
        stem=args.stem,
        case_folding=args.case_folding,
        remove_numbers=args.remove_numbers
    )

    # Tokenize documents and create SPIMI index
    tokens = reuters.get_tokens()
    spimi = SPIMI(reuters=reuters)
    index = spimi.construct_index()

    # Handle compressed index
    if args.remove_stopwords or args.stem or args.case_folding or args.remove_numbers:
        print("Your index has already been compressed, will use that as unfiltered.")

    table = CompressionTable(index)
    print(table.generate_table())
    print()

    # Stem index if needed
    if not args.stem:
        index = stem_index(index)

    # Conduct queries
    while True:
        user_input = input("Would you like to conduct an AND query or an OR query? Hit enter for no. [and/or] ")
        if user_input == "":
            break
        elif user_input.lower() in ["and", "or"]:
            and_query = AndQuery(index)
            or_query = OrQuery(index)
            user_query = Query.ask_user()
            if user_input.lower() == "and":
                and_query.execute(user_query)
                and_query.print_results()
            elif user_input.lower() == "or":
                or_query.execute(user_query)
                or_query.print_results()

    # Experiment with BM25 ranking function
    bm25 = BM25(reuters=reuters, index=index, n=reuters.number_of_documents)
    while True:
        choices = {"y": True, "n": False}
        user_input = input("Would you like to experiment with the Okapi BM25 ranking function? [y/n] ")
        if user_input.lower() not in choices:
            pass
        elif choices[user_input.lower()]:
            user_query = Query.ask_user()
            bm25.compute_bm25(user_query)
        elif not choices[user_input.lower()]:
            break
