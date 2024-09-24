## For the potential future
1. **Collaborative filtering:** can be introduced by asking other people to upload their imdb/letterboxd data. (reddit 
post, social media post, asking friends).
2. account creation, cookies. users can add to their IMDb/letterboxd watchlist through the website (integrate them 
somehow)
3. **Diversify** dataset: add directors, actors, country, language, etc.
4. accommodate users without imdb/letterboxd account, they can search a DB and rate films on the website, user profile
generated from their ratings

## Data Collection

You could use tmdb api directly, or use these python libraries:
 
* https://pypi.org/project/tmdb3/
* https://github.com/wagnerrp/pytmdb3/

this has crew list (includes director)
TMDb also has country, language, budget, poster. very useful. API is free. 50 requests/second rate limit.

afaik no publicly available dataset to download, API is done film-by-film, so would take a while to init a large 
dataset. from what I've seen, IDs are ints from 1 to X.

you can use /find API with tmdb and use the imdb id (tt...) to get the exact film. good to know 

afaik no way to import/change imdb date rated (shame smh)

exported letterboxd data is very limited (only title, year, rating), but could be useful in cross-referencing.

however, the only advantage of using letterboxd's data is the accurate date rated. otherwise it's not very helpful.

## Figuring out the user profile

What I don't like about year is that a film released in 1900 that is given a 10 has the same impact on the user profile 
vector as a 1900 film with a 1 rating.

## Recommender Systems eBook

**Novelty:** very important to recommend novel or unexpected films. Users are also interested in expanding their 
horizons. This is where my wildcard idea would work well: invert everything except imdbRating, (maybe fix numVotes to 0 
to encourage lesser-known films?)

**Diverse Results:** For example, if the user's highest genre is drama, don't recommend 20 drama films. Also throw in 
other recommendations from different genres that we know they also like (e.g. biographies could be a close second to 
drama, these should also be recommended).

**Taste evolution:** User's taste evolves over time. So perhaps have less weighting towards older ratings compared to 
newer ratings.

## Integrating Date Rated

* As mentioned in the previous section, people's taste in films change over time. Here is my idea to integrate this
numerically into my solution:
1. Relative:
  a. Normalise dateRated as a value between 1.0 and 0.8: 1.0 being the latest film you watched, 0.8 being the earliest.
  b. Scalar multiply this value to the film vector, similar to how we scalar multiply the film vector by myRating
2. Fixed:
  a. Range the scalar values between 0.5 and 1.0. Imdb was released in October 1990, so we can set that as 0.5 (base),
     and today's date as 1.0.
  b. scalar multiply this value by the vector, like described previously.

### Doing Relative dateRated Normalization

We want to do 0.8<x<1.0.
Normalize the value, *0.2 then +0.8

## Diversifying Results

A problem I'm having is that the same type of films are being recommended to the user, e.g. adventure comedy drama. RL
does help this somewhat, but I want to have the best starting state possible, and not just rely on RL.

### Ideas to diversify the recs

1. don't curve genres
2. balance quantity & mean rating of genres (see below)
3. **new** 30-days vector, recency. pick up on trends

vectors are unfavourably weighted towards film genres that have a high quantity.
For example, there is a large quantity of action films, and a low quantity of documentary films, but the mean rating of 
action films is lower than documentaries. The vector feature leans towards action films due to the higher quantity.

#### Ideas to solve the quantity > meanRating problem

**1** Completely disregard quantity
e.g. if you rated 2 documentary films a 10, then the documentary feature in the vector is a 1.0. This does not factor in
quantity whatsoever

What I don't like about this is that I feel like you should factor in quantity somehow. For example, if drama has a 
mean rating of 7.6 across 300 films, that should have significance over 10 biography films with a mean rating of 7.9.

**2** Have multiple user profiles

Perhaps create 23 user profiles (1 for each genre). Calculate weighted averages for these.

#### Ideal Recommendation Hierarchy

1. High mean rating, high quantity
2. High mean rating, low quantity

## Wildcards

### IDEA 1

Have a wildcard vector. Init to the inverse of User Profile: but keep imdbRating, numVotes, runtime fixed.
When a wildcard film is responded to, only the wildcard vector changes.
When a non-wildcard film is responded to, only the user profile vector changes.

### Vectorized Data Form
year_norm, imdbRating_norm, numVotes_norm, runtime_norm, action, adventure, animation, biography, comedy, crime, 
documentary, drama, family, fantasy, film-noir, history, horror, music, musical, mystery, news, romance, sci-fi, sport, 
thriller, war, western

content based filtering: "uses item features to recommend other items similar to what the user likes, based on their 
previous actions or explicit feedback"

### Similarity measures
1. Cosine similarity - cosine of the angle between 2 vectors
2. dot product
3. Euclidean distance

## CHAT GPT

Great choice! Content-based filtering can work well when you have user preferences and detailed information about items.
Here's a simplified step-by-step guide on how you could implement a content-based movie recommendation system using your
two datasets:

### 1. Data Preparation:

#### Movies You Like Dataset:
- This dataset should contain information about movies you've liked or interacted with.
- Include details like movie ID, title, genres, actors, directors, release year, etc.
- Create a user profile based on the features of the movies you liked.

#### IMDb Movies Dataset:
- This dataset should contain comprehensive information about all movies on IMDb.
- Extract relevant features like movie ID, title, genres, actors, directors, release year, etc.
- Create a vector representation for each movie based on these features.

### 2. Feature Extraction:

- Represent each movie in both datasets as a vector. You can use one-hot encoding for categorical features like genres 
and actors.
- Normalize numerical features such as release year.

### 3. User Profile Creation:

- Create a user profile vector based on the features of the movies you like.
- Combine the feature vectors of the movies you like, possibly with weighted averages based on your preferences.

### 4. Similarity Calculation:

- Use a similarity metric (e.g., cosine similarity) to measure the similarity between the user profile vector and the 
vectors of all movies in the IMDb dataset.
- Calculate the similarity scores for each movie.

### 5. Recommendation Generation:

- Rank the movies based on their similarity scores.
- Recommend the top N movies with the highest similarity scores that the user hasn't interacted with.

### 6. Integration with Web App:

- Implement the recommendation logic in your backend using your chosen programming language and framework.
- Expose an API endpoint that takes a user's liked movies as input and returns recommended movies.

### 7. Testing and Evaluation:

- Evaluate the system using metrics like precision, recall, or Mean Squared Error (MSE).
- Fine-tune your algorithm based on user feedback and evaluation results.

### Additional Considerations:

- **Weighting Features:** You might want to experiment with different weights for features based on their importance in 
user preferences.
- **Dynamic User Profiles:** Allow users to update their preferences over time to improve the accuracy of 
recommendations.
- **Scale and Efficiency:** Depending on the size of your IMDb dataset, consider optimizing your recommendation
- algorithm for efficiency.

Remember that this is a simplified guide, and you might need to adapt these steps based on the specific details and 
requirements of your project. Also, as you develop your system, it's essential to gather user feedback and continuously 
refine your recommendation algorithm for better accuracy.
