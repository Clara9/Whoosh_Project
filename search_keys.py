import os.path
import string
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import fields
from whoosh.qparser import QueryParser
import spacy
import string

class Search:
    def __init__(self):
        return
    
    def search(self, keyword):
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
            
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored = True))

        ix = index.create_in("indexdir", schema)

        with open('./data/sample.txt') as f:
            texts = list(f)
        with open('./data/sample-title.txt') as f2:
            titles = list(f2)
        
        writer = ix.writer()
        for i in range(len(titles)):
            writer.add_document(title = titles[i], content = texts[i])
        writer.commit()

        searcher = ix.searcher()
        query = QueryParser("content", ix.schema).parse(keyword)
        results = searcher.search(query, terms=True, limit = 20)

        for r in results:
            print(r['title'])
            print(r['content'])
            # print (r, r.score)
        # Was this results object created with terms=True?
#         if results.has_matched_terms():
#             # What terms matched in the results?
#             print(results.matched_terms())

        # What terms matched in each hit?
        print ("matched terms")
        print("Number of matched result is " + str(len(results)))

    #         for hit in results:
    #             print(hit.matched_terms())
        return self.return_tuples(results)
    
    def find_definition(self, df):
        nlp = spacy.load('en')
        arr = []
        with open('./data/sample.txt') as f:
            texts = list(f)[:1000]
        for text in texts:
            # print(text)
            doc = nlp(text)
            sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
            for tok in sub_toks:
                tmp = str(tok).lower()
                if df in tmp and text not in arr:
                    arr.append(text)
        return arr
        
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
        results = search_word(keyword)

    # if __name__ == "__main__":
    #     main('loops')
# s = Search()
# s.find_definition('input')