# COMP479
Projects for COMP 479: Information Retrieval And Web Search

* Project #1 - Used NLTK library, and BeautifulSoup to parse Reuters collection into documents, articles, tokens, stems. Removed stopwords indexed in indexer. Used two methods to create the indexer: 
	1. Pipelining from block 1 to block 6
	2. Feeding input one block at a time.

* Project #2 - Created a unfiltered index, a single term querying processor and a compressed index. 
	* The tokens needed to be sorted and the duplicate terms needs to be merged. This resulted in have a merged posting list that has to be sorted again.
	* The query are passed as parameter and used to look up the term in the index.
	* As for the creating a compressed index, numbers were removed, it was case-folded and the stopwords were removed.