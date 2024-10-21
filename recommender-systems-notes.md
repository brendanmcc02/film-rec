# Recommender Systems Notes

# Chapter 1

## A Good Recommender System:

1. **Relevance:**
2. **Novelty:** A relative fresh or good rec. One possible implementation of this is to recommend lesser known films as opposed to popular/well-known ones.
3. **Diverse:** Not just recommending the same type of film
4. **Serendipity:** a genuinely unexpected and surprising rec - high risk/high reward. *For example: someone that likes Indian Food getting recommended Ethiopian food. The rec system sees patterns in 

* **Taste evolution:** User's taste evolves over time. So perhaps have less weighting towards older ratings compared to 
newer ratings.

After reading & understanding the different types of recommender systems, the ones that are relevant to my project:

* **Content-based Filtering:** Making recommendations based only on the films that the user has rated
* **Collaborative-based Filtering:** Making recommendations based off films that other users with similar taste also liked
    * realistially tough to implement as I won't really have access the large amounts of data beyond my own user data
    * I could gather ~5 from friends, but that's it
* **Hybrid:** Integrating both of the above into one Recommender System

**Context Awareness:** *The recommender system being aware of the various contexts (e.g. time of year, user's location). An example is a Recommender System pushing Christmas films when it hits December.*

* Time Sensitivity - when a new film comes out, could have a special weight/relevance for the recommender system

## Problems to be aware of

* **Cold-start** problem

## Types of Recommendations

* Top-k films
    * more relevant to my problem
* Predicting the rating that a user is likely to give it
    * less relevant

## Train & Test Data

In traditional ML, you would have a train-test split. In the case of collaborative filtering (which will have a very sparse matrix), the train data are all the cells with a value, and the test data is simply all the empty cells. That's essentially the translation.

# Chapter 2

He says that its common and recommended to pre-compute things in an 'offline' phase - do as less as you can on the fly.

## User-Based Neighbourhood Models
*aka: Collaborative-Based Filtering*

**Pearson Correlation Co-efficient:** A similarity metric between two linear variables. value is between -1 and 1:
* `-1`: Negative Correlation. When one of the variables increase, the other decreases.
* `0` : No correlation.
* `1` : Positive Correlation. When one of the variables increase, the other increases.

**Mean-centering:** getting the mean of a row of data and then subtracting the mean from each value in the row.
    * This is a clever way to get around the problem of different users rating things differently - for example, let's say you have one user that rates almost everything very highly: `>5`, another rates many things very negatively: `<5`. This can skew your calculations, so what you then do is mean-center the data, then begin your calculations to avoid bias.

In the case of collaborative filtering, Pearson is a better/more indicative similarity metric as opposed to cosine similarity. Section 2.3.1 explains it very well.

Lots of interesting stuff is mention in this section, while it was an interesting read, it still isn't incredibly relevant to my problem as I likely will only be using content-based filtering.

## Item-Based Neighbourhood Models

*aka Content-Based Filtering*
