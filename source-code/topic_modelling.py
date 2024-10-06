doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."
doc6 = "Good morning Ma'am. May I come in? I am nervous today about my interview."
doc7 = "hi Jody! Let's go out for coffee today?"

# compile documents
doc_complete = [doc1, doc2, doc3, doc4, doc5]
doctemp = [doc6,doc7]

def topic(doc_complete):

    import nltk
    #nltk.download("stopwords")
    #nltk.download("wordnet")
    
    from nltk.corpus import stopwords
    from nltk.stem.wordnet import WordNetLemmatizer
    import string
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized
    
    doc_clean = [clean(doc).split() for doc in doc_complete] 
    
    # Importing Gensim
    import gensim
    from gensim import corpora
    
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)      
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
    
    for idx, topic in ldamodel.show_topics(formatted=False, num_words= 10):
        print('Topic: {} \nWords: \n {}'.format(idx, '|'.join([w[0] for w in topic])))
    
    print("\n")
    
    print(ldamodel.print_topics(num_topics=3, num_words=10))
    
    
topic(doc_complete)
#print(ldamodel[doc_complete[0],doc_complete[1]])

#---------------------------

#---------------------------
import pyLDAvis
#import pyLDAvis.gensim
#from pyLDAvis import gensim
import pyLDAvis.gensim_models as gensimvis

pyLDAvis.enable_notebook()
#vis = gensimvis.prepare(ldamodel, doc_complete, dictionary)
#print(vis)


#----------------
