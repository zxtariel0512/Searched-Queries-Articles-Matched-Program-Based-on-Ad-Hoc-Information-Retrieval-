#!/usr/bin/env python
# coding: utf-8

# In[124]:


import math

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',                           'onto','out','over','past','per','plus','since','till','to','under','until','up',                           'via','vs','with','that','can','cannot','could','may','might','must',                           'need','ought','shall','should','will','would','have','had','has','having','be',                           'is','am','are','was','were','being','been','get','gets','got','gotten',                           'getting','seem','seeming','seems','seemed',                           'enough', 'both', 'all', 'your' 'those', 'this', 'these',                            'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace',                            'anything', 'anytime' 'anywhere', 'everybody', 'everyday',                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',                           'you','your','yours','me','my','mine','I','we','us','much','and/or',                           '.','',',','''/;''',"'",'"'
                           ]

# analyze query file

q_file = open('cran.qry','r')
content = q_file.read()
q1 = content.split('.I')
q1.pop(0)
q_dict = {}

# process the raw data
for i in q1:
    curr = i.split('.W')
    # index
    idx = curr[0].strip('\n')
    idx = idx.strip(' ')
    # query
    query_raw = curr[1]
    query_line = query_raw.split('\n')
    query_line.pop(0)
    query = []
    for i in query_line:
        il = i.split(' ')
        for word in il:
            query.append(word)
    query.pop(len(query) - 1)
#     print(query)
    query_new = []
    for word in query:
#         print(word)
        word = word.strip(',')
        word = word.strip('?')
        word = word.strip('(')
        word = word.strip(')')
        if word not in closed_class_stop_words and word.isalpha():
            query_new.append(word)
    q_dict[idx] = query_new
# for keys, values in q_dict.items():
#     print(keys)
#     print(values)

# calculate TFIDF of query
q_tfidf = {}
for keys, values in q_dict.items():
    idx = keys
    query = values
    vector = []
    for curr_word in query:
        # get TF
        tf = 0
        for word in query:
            if word == curr_word:
                tf += 1
        # get IDF
        numQue = 0
        for keys, values in q_dict.items():
            if curr_word in values:
                numQue += 1
#         print(curr_word)
#         print(numQue)
        idf = math.log(len(q_dict) / numQue)
        vector.append(idf)
    q_tfidf[idx] = vector
# for keys, values in q_tfidf.items():
#     print(keys)
#     print(values)



# analyze article file

a_file = open('cran.all.1400','r')
cont = a_file.read()
articles_dict = {}
art_list = cont.split('.I')
# print(art_list)

art_list.pop(0)
# for i in art_list:
#     print(i)
for item in art_list:
    l1 = item.split('.T')
#     print(l1)
    # index
    idx = l1[0].strip('\n')
    idx = idx.strip(' ')
#     print(idx)
    # content
    l2 = l1[1].split('.W')
#     print(l2)
    art_raw = l2[1]
    art_lines = art_raw.split('\n')
    article_new = []
    for line in art_lines:
        line = line.replace('/', '')
        line = line.replace('-', ' ')
        word_list = line.split(' ')
        for word in word_list:
            word = word.strip(',')
            if word not in closed_class_stop_words and word.isalpha() and word != 'x':
                article_new.append(word)
    articles_dict[idx] = article_new
# for keys, values in articles_dict.items():
#     print(keys)
#     print(values)

# calculate TFIDF for the article
art_tfidf = {}
tfidf_word = {} # find the number of documents that contains certain word
for idx, art in articles_dict.items():
    non_repeat = [] # avoid repeated words in single article
    for word in art:
        if word in tfidf_word:
            if word not in non_repeat:
                tfidf_word[word] += 1
                non_repeat.append(word)
        else:
            tfidf_word[word] = 1
            non_repeat.append(word)
# print(tfidf_word)

# tfidf vector for each article
art_tfidf = {}
for idx, art in articles_dict.items():
    vector = []
    for word in art:
        tf = 0
        for curr_word in art:
            if word == curr_word:
                tf += 1
        idf = math.log(len(articles_dict) / tfidf_word[word])
        vector.append(tf * idf)
    art_tfidf[idx] = vector
#     print(idx)
#     print(vector)

# start cosine similarity
output = []
q_num = 1
for q_idx, q in q_tfidf.items():
    unsorted = []
    for a_idx, a in art_tfidf.items():
        curr = []
        curr.append(q_num)
        curr.append(a_idx)
        total = []
        for words in articles_dict[a_idx]:
            if words not in total:
                total.append(words)
        for words in q_dict[q_idx]:
            if words not in total:
                total.append(words)
        numerator = 0
        ai = 0
        qi = 0
        aii = 0
        qii = 0
        for t in total:
            if t in articles_dict[a_idx]:
                ai = a[articles_dict[a_idx].index(t)]
                aii += a[articles_dict[a_idx].index(t)] ** 2
            else:
                ai = 0
            if t in q_dict[q_idx]:
                qi = q[q_dict[q_idx].index(t)]
                qii += q[q_dict[q_idx].index(t)] ** 2
            else:
                qi = 0
            numerator += ai * qi
        denominator = math.sqrt(aii * qii)
        if denominator == 0:
            similarity = 0
        else:
            similarity = numerator / denominator
        g = float("{0:.3f}".format(similarity))
        curr.append(g)
#         print(similarity)
        unsorted.append(curr)
    q_num += 1
  
     
        
    # start to sort
    unsorted.sort(key = lambda unsorted: unsorted[2])
    unsorted.reverse()
    print(unsorted)
    output.append(unsorted)
    
test = open('output.txt', 'w')
for i in output:
    for j in i:
        test.write(str(j[0]) + ' ' + str(j[1]) + ' ' + str(j[2]))
        test.write('\n')

test.close()
q_file.close()
a_file.close()

# print(output)


        
            
    
    


# In[ ]:





# In[ ]:




