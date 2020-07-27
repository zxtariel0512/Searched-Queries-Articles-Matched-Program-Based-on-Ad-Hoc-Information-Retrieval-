README

The program takes 2 input files:
* A query file consisting 255 queries.
* A article file consisting 1400 articles.

The prgram outputs 1 text file:
* Three columns text file representing the cosin similarity (i.e. the matching score) between each query and each article, sorted from high similarity score to low similarity score for each query.

The program opens input file inside (i.e. no need to enter input if use command line).

The program generates the output text file and analyzes 2 input files in following ways:
* Open and analyze query file
	- Tokenize the query, and store the index and its content
	- Remove all 'stopping words', numbers, and punctuations
	- Deal with special cases, such /***/ and **-**, by treating them as seperate words
	- Calculate TFIDF for each query, and store the TFIDF vectors via dictionary, in which keys denote query index and values denote the TFIDF vector
* Open and analyze article file
	- Tokenize the article, and store the index and its content only
	- Remove all 'stopping words', numbers, and punctuations
	- Deal with special cases, such /***/ and **-**, by treating them as seperate words
	- Calculate TFIDF for each article, and store the TFIDF vectors via dictionary, in which keys denote
* Calculate the cosine similarity
	- For each query
		-> For each article, calculate the score vector of current article and current query, which all have the same length of total number of distinct words that appear in current article and current query, with non-zero value (TFIDF) if appear in article (or query), and with zero value if not appear
		-> Get the cosine similarity by the formula

