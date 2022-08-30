# Script extracting and processing data from a website

* Download content pages from https://www.cnas.org/articles-multimedia.The content/articles are on multiple pages;To get the content/article, we need to go the linked pages
(e.g.: clicking on "China and Russia’s Dangerous Convergence" to get to the content at the URL: "https://www.cnas.org/publications/commentary/china-and-russias-dangerous-convergence”)
* Perform the required text preparation, including the generation of bigrams
* Print on screen a sample (let’s say 5-6 articles from different pages
* Store the sample in a MongoDB database
* Perform sentiment analysis, wordcloud, LDA per each article, retrieving articles from the database. Print the results on the screen
* Create a requirements file with all the packages needed
* Use parameters (like on the number of sample articles or the location of files/db and URLs)
* Handle errors
* Skip all the non textual content (such as video and audio).

For the content download, we used "selenium" which is good choice; for sentiment "vader"; for wordcloud "wordcloud"; for LDA "gensim” libraries (including pyLDAvis for visualizatio
