*My digital scribbles and ideas.*

# Main Takeaways from the Recommender Systems textbook
* Recall the aspects of a good recommender system - think about novelty, diversity and serendipity
  * **Diversity** - I'm thinking of implementing clustering as opposed to just one user profile
  * **Novelty** - Still need to explore this, atm I'm thinking of a wildcard profile
  * **Serendipity** - Can be challenging without collaborative filtering, but there might be some workarounds. still 
  need to explore.
* Use some tools to evaluate the recommender system
* A possible efficiency implementation is to instead of performing user profile dot products with **every film**, you 
cluster the films and only perform cosine sim comparisons on individual films within clusters with relatively high 
cosine similarity
* Think about how to overcome the **cold start problem**, i.e. when users have 0 films and they check the site.
  * Additionally, what if the user only has 5 films rated? or 10? where do you draw the line between fully relying on 
    their data, or filling in the gaps?
* Think about ways to add **interpretation**, e.g. *"because you liked 1980s rom-coms..."*. This adds a layer of
sophistication to your recommender system and increases users trust in the recommendations

# For the potential future
1. **Collaborative filtering:** can be introduced by asking other people to upload their imdb/letterboxd data. (reddit 
post, social media post, asking friends).
2. account creation, cookies. users can add to their IMDb/letterboxd watchlist through the website (integrate them 
somehow)
3. ~~accommodate users without imdb/letterboxd account, they can search a DB and rate films on the website, user profile
generated from their ratings~~
