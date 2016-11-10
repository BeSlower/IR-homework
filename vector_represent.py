import os
import re
from nltk.stem.snowball import PorterStemmer  # load the stemmer module from NLTK
import nltk
import math


def clean_words(text, stem_flag):
    tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
    words = tokenizer.tokenize(text)

    # Convert to Lowercase
    # words = words.map(str.lower)
    cleanWords = [t.lower() for t in words]

    # Normalize (remove punctuation)
    # punc = string.punctuation
    # cleanWords = [t for t in cleanWords if t not in punc]
    cleanWords = [re.sub('[^0-9a-z]', "", x) for x in cleanWords]

    # Remove Empty Vectors
    cleanWords = [x for x in cleanWords if x != '']

    # Identify Digits & Convert to Num
    cleanWords = [re.sub("\d+", "NUM", x) for x in cleanWords]

    if stem_flag:
        # Stem Words
        cleanWords = [stemmer.stem(x) for x in cleanWords]  # call stemmer to stem the input

    return cleanWords


def term_frequency(word_, document_):
    count = 0
    for w in document_:
        if w == word_:
            count += 1
    return count


def document_frequency(word_, all_doc):
    count = 0
    for key_ in all_doc.keys():
        doc = all_doc[key_]
        for w in doc:
            if w == word_:
                count += 1
                break
    return count


def okapi_bm25_value(tf_, df_, doc_num_, doc_ave_length_, doc_length_, b, k):
    value = (k + 1) * float(tf_) / (float(tf_) + k * (1 - b + b * (float(doc_length_) / float(doc_ave_length_)))) \
            * math.log(float(doc_num_) / (float(df_)), 2)
    return value

stem_flag = False
retval = os.getcwd()
print ("Current Path: %s" % retval)

for corpus_idx in [1, 3, 4, 5, 2]:
    corpus_name = 'corpus'+str(corpus_idx)
    print('--------------------- Start Process %s ------------------------' % corpus_name)
    # initialize path
    corpus_path = retval + '/../corpus/' + corpus_name + '/'
    output_path = retval + '/../vector_model/' + corpus_name + '/'
    vocabulary_path = '/home/zhans/nltk_data/corpora/words/my_vocabulary'

    #nltk.corpus.words
    vocabulary_list = open(vocabulary_path, 'r').read().split()

    # set stemming or without stemming
    if stem_flag:
        stemmer = PorterStemmer()
        vocabulary_stem_list = [stemmer.stem(x) for x in vocabulary_list]
        vocabulary_list = list(set(vocabulary_stem_list))

    vocabulary_length = len(vocabulary_list)

    # clean the raw text and generate a clean word list for each document
    corpus_clean = {}
    print('--------------------- Clean document ------------------------')
    for document_name in os.listdir(corpus_path):
        document_path = corpus_path + document_name
        document = open(document_path, 'r').read()
        doc_clean_word = clean_words(document, stem_flag)
        # save the clean word of document into a dictionary
        corpus_clean[document_name] = doc_clean_word
    print("Clean document done!")
    print('--------- Initial values for vector representation ----------')
    # combine all documents
    total_doc = []
    # number of documents
    doc_num = 0

    for key in corpus_clean.keys():
        total_doc.extend(corpus_clean[key])
        doc_num += 1

    # average length on all documents
    doc_ave_length = len(total_doc) / doc_num

    print("Document num: %d" % doc_num)
    print("Total documents length: %d" % len(total_doc))
    print("Average document length: %d" % doc_ave_length)
    print("Vocabulary length: %d" % vocabulary_length)

    # represent each document based on vocabulary
    print('--------- Start to calculate vector representation ----------')
    doc_vector = {}
    for doc_idx, document_name in enumerate(os.listdir(corpus_path)):
        # initialize vector list for current document
        vector = {}
        print("--------- No.%d: %s" % (doc_idx+1, document_name))
        for idx, word in enumerate(vocabulary_list):
            # calculate term frequency
            TF = term_frequency(word, corpus_clean[document_name])
            if TF == 0:
                continue
            # calculate document frequency
            DF = document_frequency(word, corpus_clean)
            # calculate current document length
            doc_length = len(corpus_clean[document_name])
            # calculate Okapi BM25 score with default b (0.75) and k (1.2)
            bm25_value = okapi_bm25_value(TF, DF, doc_num, doc_ave_length, doc_length, b=0.75, k=1.2)
            # remove 0 for sparse coding
            if bm25_value == 0:
                continue
            vector[word] = bm25_value
            # calculate process completed ratio
            if (idx % 10) == 0:
                print("%.2f %% finished..." % float(100 * idx / vocabulary_length))

        # write the vector representation into txt file
        out = open(output_path + document_name, 'w')
        for key in vector.keys():
            out.write(key + '\t' + str(vector[key]) + '\n')
        out.close()
        print("done...")
        print("--------------------------------------")
        doc_vector[document_name] = vector

    print("--------- All Set ----------")
