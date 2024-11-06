import os
from bs4 import BeautifulSoup
from definitions import ROOT_DIR, word_tokenize, stopwords, ps

class Reuters:

    def __init__(self, dataset_directory='dataset', number_of_files=22, docs_per_block=500,
                 remove_stopwords=False, stem=False, case_folding=False, remove_numbers=False):
        """
        Initiate the Reuters objects which will contain the reuters files.
        :param dataset_directory: Path to the dataset directory containing subfolders with text files.
        :param number_of_files: Number of text files that will be parsed (not used here as we are processing all files).
        :param docs_per_block: Number of documents per generated block.
        :param remove_stopwords: Will we include stopwords?
        :param stem: Will we stem the terms?
        :param case_folding: Will we lower terms to their lowercase variant?
        :param remove_numbers: Will we remove terms that are just numbers?
        """
        self.dataset_directory = dataset_directory

        self.docs_per_block = docs_per_block
        self.number_of_documents = 0
        self.number_of_tokens = 0

        self.remove_stopwords = remove_stopwords
        self.stem = stem
        self.case_folding = case_folding
        self.remove_numbers = remove_numbers

        self.will_compress = self.remove_stopwords or self.stem or self.case_folding or self.remove_numbers

        self.list_of_lists_of_tokens = []

        # Dictionary with key -> doc ID and value -> length of that document in words
        self.document_lengths = {}
        self.average_document_length = 0

    def get_tokens(self):
        """
        Find all tokens in the text files under subfolders.
        For each file:
            - Read the content and tokenize the text.
            - Create tuples of (term, document ID) for each term in the document.

        :return: List of lists of tokens (tuples of (term, document ID)).
        """
        tokens = []
        current_document = 0
        print("Parsing text files...")

        for subdir, _, files in os.walk(self.dataset_directory):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        terms = word_tokenize(content)
                        if self.will_compress:
                            terms = self.compress(terms)
                        document_id = current_document
                        token_pairs = [(term, document_id) for term in terms]
                        tokens.extend(token_pairs)
                        self.number_of_documents += 1

                        self.document_lengths[document_id] = len(token_pairs)
                        current_document += 1
                        if current_document == self.docs_per_block:
                            self.number_of_tokens += len(tokens)
                            self.list_of_lists_of_tokens.append(tokens)
                            tokens = []
                            current_document = 0

        if tokens:
            self.number_of_tokens += len(tokens)
            self.list_of_lists_of_tokens.append(tokens)

        self.average_document_length = self.number_of_tokens / self.number_of_documents
        print("Found %s documents and %s tokens. %d block file(s) will be generated.\n"
              % ("{:,}".format(self.number_of_documents), "{:,}".format(self.number_of_tokens), len(self.list_of_lists_of_tokens)))

        return self.list_of_lists_of_tokens

    def compress(self, terms):
        """
        Compress terms list by removing stopwords, stemming, case folding, or removing numbers.
        :param terms: List of terms to be compressed.
        :return: Compressed list of terms.
        """
        if self.remove_stopwords:
            terms = [term for term in terms if term.lower() not in stopwords]
        if self.stem:
            terms = [ps.stem(term) for term in terms]
        if self.case_folding:
            terms = [term.casefold() for term in terms]
        if self.remove_numbers:
            terms = [term for term in terms if not term.replace(",", "").replace(".", "").isdigit()]

        return terms
