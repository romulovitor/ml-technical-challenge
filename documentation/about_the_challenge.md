# We could have done it better
  
We could implement a CI / CD process to store as access keys to the database, in case this project was for a production environment. Thus avoiding the exposure of the credentials of access to the database.
Another point is related to the scalability of the scraping process, as it was developed, only vertical scaling is possible. Context precedents can be an issue.
To make the project complete, we could also create an SDK to make it easier to use considering making it available to other developers.
Could have put more validation points using python's exception handling

# Why I adopted technologies

I used MongoDB because it is a very common and easy-to-scale database, if necessary you just need to create new nodes.
Docker-compose was used to orchestrate the mongo and API services, thus allowing better control between images and communication between containers.
  
# Attention points

The "apparitions" prediction process was a bit confusing because when we do the scraping we already collect the total of "apparitions" so I don't see the need to make the prediction. However, even so, I will do the calculation, so as entities it has a new field to store the prediction.
About the feature vector, I chose to save the vector with the features of each link, to avoid unnecessary reprocessing to scrape the pages, as it is a costly operation in terms of processing. For each feature it is necessary to perform a search on the page, being an O (n) operation, determined by the features.

Another point is related to the model, every time a new prediction is requested, the model performs the entire process of data collection and preparation, thus bringing better control over the process and providing random records for the prediction. A negative point in this approach is related to computational processing. It is important to note that this can be adjusted