import os.path
import string
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import fields
from whoosh.qparser import QueryParser
from nltk.tokenize import sent_tokenize
import spacy
import string
import nltk

class Search:
    def __init__(self):
        nltk.data.path.append('./nltk_data/')

    def search_terms(self, keyword, definition, flag):
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")

        schema = Schema(title=TEXT(stored=True), content=TEXT(stored = True), \
            subjective=KEYWORD(stored=True, lowercase=True, scorable=True))

        ix = index.create_in("indexdir", schema)

        with open('./data/sample.txt') as f:
            texts = list(f)

        with open('./data/sample-title.txt') as f2:
            titles = list(f2)

        with open('./data/subs.txt') as f3:
            subs = list(f3)

        writer = ix.writer()
        for i in range(len(titles)):
            writer.add_document(title = titles[i], content = texts[i][1:-2], subjective = subs[i])
        writer.commit()

        s = ix.searcher()

        if flag:
            query = QueryParser("content", ix.schema).parse(keyword)
        else:
            query = QueryParser("subjective", ix.schema).parse(definition)
        results = s.search(query, terms=True, limit = 20)

        return results

    def find_subjectives(self):
        nlp = spacy.load('en')
        with open('./data/sample.txt') as f:
            texts = list(f)[:3000]
        res = []
        for text in texts:
            arr = []
            sentences = sent_tokenize(text)
            for sentence in sentences:
                doc = nlp(sentence)
                sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj")]
                arr.append(sub_toks)
            res.append(arr)
        return res

    def write_to_sub(self, arr):
        with open('./data/subs.txt', 'w') as f2:
            for arr in res:
                f2.write(str(arr).lower() + '\n')

    def return_tuples(self, input):
        arr = []
        for value in input:
            tmp = value['content']
            if value['content'][0] == '"':
                tmp = value['content'][1:]
            arr.append([value['title'][:-2], tmp[:-2], value.score])
        return arr

    def print_score(self, results):
        found = results.scored_length()
        print(found)
        print(results.has_exact_length())
        if results.has_exact_length():
            print("Scored", found, "of exactly", len(results), "documents")

    def main(self, keyword):
        write_data(self)

    # if __name__ == "__main__":
    #     main('loops')
# s = Search()
# res = s.find_subjectives()
# s.write_to_sub(res)

