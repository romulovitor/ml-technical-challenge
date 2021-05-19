#Readme

- extract data from pages
- count the number of references (“appearances”) that we find of
a link from other sources.
- crawl the different links from a base set and persist,
- how many different references(appearances)
- The maximum level, N, of depth of the crawler
is defined at the beginning of the process:
- In addition, this information can be enriched for each link with the information that it deems
necessary to store.
  
- vector with at least 10 numerical characteristics
- This vector must be saved in a new storage instance (table,
document, file, etc):
  
Finally, a REST API will be built such that it uses the defined storage and allows obtaining
the vector of features associated with a link:

● If the link is in the database, answer the precalculated vector.

● If the link is not found in the database, the values corresponding to the vector must
be calculated, inserted into the database and then returned. This vector will not have
the number of external references calculated.

--------------
To do this, we will use the information that is already crawled in the previous section,
generating a 70-30 random sample. With the largest sample, a random forest of 100 trees of
depth 10 will be trained, without feature bagging and with the value of appearances as the
target. The performance of this model won’t be evaluated in the scope of this exercise
(meaning the model doesn’t need to be good predicting “appearances”).

The functionality is added to the REST API predicting the “appearances” of a link:

● If the number of “appearances” is already calculated, return it.

● If the number of “appearances” is not calculated, this information must be sent to the
model so that it can be screened (if necessary, reuse the previous functionality of
computing the vector online). Then, this information will be updated in the storage
and it will be returned to the user.