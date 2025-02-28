# Recommender Systems Notes

*Notes I made while reading the **Recommender Systems: The Textbook by Charu C. Aggarwal**.*

# Chapter 1 - Introduction

## A Good Recommender System:

1. **Relevance:**
2. **Novelty:** A relative fresh or good rec. One possible implementation of this is to recommend lesser known films as opposed to popular/well-known ones.
3. **Diverse:** Not just recommending the same type of film
4. **Serendipity:** a genuinely unexpected and surprising rec - high risk/high reward. *For example: someone that likes Indian Food getting recommended Ethiopian food. The rec system sees patterns in their tastes that the user doesn't see.*

## Other Notes & Definitions

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

## Types of Recommendations

* Top-k films
    * more relevant to my problem
* Predicting the rating that a user is likely to give it
    * less relevant

## Train & Test Data

In traditional ML, you would have a train-test split. In the case of collaborative filtering (which will have a very sparse matrix), 
the train data are all the cells with a value, and the test data is simply all the empty cells. That's essentially the translation.

# Chapter 2 - Neighbourhood-Based Collaborative Filtering

* He says that its common and recommended to pre-compute things in an 'offline' phase - do as less as you can on the fly.
* The following 2 approaches make use of an user-item matrix, think of users as rows, items. (e.g. films) as columns.
* Neighbourhood-Based Collaborative Filtering can be thought of as a generalisation of KNN.

## User-Based Neighbourhood Models

**Pearson Correlation Co-efficient:** A similarity metric between two linear variables. value is between -1 and 1:
* `-1`: Negative Correlation. When one of the variables increase, the other decreases.
* `0` : No correlation.
* `1` : Positive Correlation. When one of the variables increase, the other increases.

**Mean-centering:** getting the mean of a row of data and then subtracting the mean from each value in the row.
    * This is a clever way to get around the problem of different users rating things differently - for example, let's say you have one user that rates almost everything very highly: `>5`, another rates many things very negatively: `<5`. This can skew your calculations, so what you then do is mean-center the data, then begin your calculations to avoid bias.

In the case of collaborative filtering, Pearson is a better/more indicative similarity metric as opposed to cosine similarity. Section 2.3.1 explains it very well.

Lots of interesting stuff is mention in this section, while it was an interesting read, it still isn't incredibly relevant to my problem as I likely will only be using content-based filtering.

## Item-Based Neighbourhood Models

At first, I had written down that this is basically content-based filtering, but I realised it's not - at least that's my understanding right now.

When measuring the similarity between 2 items (e.g. films), it uses an adjusted (ratings are mean-centered at 0) cosine similarity between 2 items.

The intuition behind the maths here, is that 2 items are deemed similar if **users rate the item similarly**. For example, if user A rates item `I` a 5/5 and user B rates item `I` a 1/5,
this will have a low cosine similarity.

So if you want to predict the rating of user `u`'s rating of an item `t`, you perform a weighted average calculation on the top-k films that are most similar (using adjusted cosine) to 
item `t` that the user `u` has rated. Bit of a mouthful. The formula speaks a thousand words: `Equation (2.15), Page 40`.

## Clustering

These calculations are infeasible and do not scale well at all - as a result, instead of calculating similarities to everything, you cluster your data and only compute similarities 
within that cluster. There is a great increase in efficency at the cost of slight decrease in accuracy.

* **Is it worth implementing this for my solution?**

* `<<` means much less than

## Regression Modeling for Neighbourhood Models

You can formulate the problem as a linear regression model.

Like in ML, you have a regularization parameter `λ>0` (lambda) that is a weight applied to the linear regression function that prevents overfitting.

## Determining Neighbourhoods as Graphs

Interesting subsection - user-item relations can be modelled using graphs: you have a bipartite graph where users and items are nodes, and edges exist between a user and an item if there is an 
observed rating between them. Neighbourhoods can then be determined by using the *Katz measure* - put simply: it is the length of walks between user `u` and `v` (weighted with parameter `β
<1`). Once a neighbourhood is determined, the previous neighbourhood models can be used.

# Chapter 3 - Model-Based Collaborative Filtering

In Chapter 2, neighbourhood-based collaborative filtering is known as an *instance-based 
learning method* - predictions are essentially made on the spot (however there is an *offline phase* 
to make computation more efficent). In this chapter, a model will be created using traditional ML 
methods. It is far more efficient in space complexity, less likely to overfit, and faster training speed.

*I will not be reading the rest of the chapter as it relates to **collaborative filtering**, and 
in my problem I want to focus on **content-based filtering.***

# Chapter 4 - Content-Based Recommender Systems

## Limitations of Content-Based filtering

* **Cold-start problem** for new users
* Less likely to give novel, diverse or serendipitous recommendations

This chapter will concern itself more so with unstructured domains (as opposed to structured). 
It says the methods can be easily translated to structured domains (which I understand is my 
film data problem).

## Nearest Neighbour Classification

This method will compute the predicted rating of an unseen film by averaging the ratings of the unseen's films k-nearest neighbours that the user has seen. You can additionally apply weights to 
the ratings, e.g. 'closer' films get more weight, 'further' ones get less weight. After doing all 
these calculations on all unseen films, for a top-k recommendation system you would rank the films 
and return the top-k films.

## Bayes Classifier

Pretty interesting, the book has a great explanation. Essentially, based on past ratings, you calculate 
conditional probabilities to inform you of the predicted rating for an unseen film.

If I actually do intend to use this, there are some important notes regarding Laplacian smoothing, 
which is very useful for cold starts for example. This also prevents overfitting.

This method will be return a predicted rating on each unseen film, and they are then sorted and the 
top-k films are returned based off these.

## Rule-Based Classifiers

Quite an interesting and intuitive concept. Some definitions to get started:

* **Support:** the fraction of rows satisfying both antecendent & consequent.
* **Confidence:** the fraction of rows satisfying from the consequent from the rows 
already known to satisfy the antecendent.

## Interpretation

An advantage of content-based filtering is that you can make a clear interpretation to the 
user why the item was recommended - e.g. "because you like 1980s Romantic Comedies...". It is 
mentioned this is easier to do with Bayes and Rule-Based classifiers, but still possible (yet 
more difficult) with regression-based ones (I would classify my vector approach as something 
very similar to linear regression).
 
## Disadvantages of Content-Based Filtering

* The only recommendations to the user are based on what they have seen already - the result is lack of novelty and serendipity
    * *How can I work around this without the use of collaborate filtering?*

## Reflections

Ok, I'm a little bit disappointed because this chapter was supposed to be 'the big one'. The classifiers discussed were a bit underwhelming, and I did not see a huge advantage to them compared to my vector method. In fact, my vector method is basically (i.e. very similar to) linear regression, which was discussed in this chapter (I didn't talk about it because there wasn't anything too novel to write about).

# Chapter 7 - Evaluating Recommender Systems

Offline methods are by far the more commonly used evaluation methods from a research and practice persepective.

**Coverage:** The size of the proportion of items the recommender system can recommend. For example, a recommender system that only recommends films from 2024 has small coverage because it will not recommend films outside of 2024 - a large portion of films will never get recommended.

Think about how to work with the cold start problem - obviously with 0 films you can make generic 
recommendations, but what about 5 films? 10 films? Where do you draw theline?

There is talk about **trust** - the user's trust in the recommender system. He mentions that when 
a recommender system gives a logical reason for the recommendation, the user is more likely to gain 
their trust in the recommender system.

Further to this point about trust - do your best to get the most optimal, inital recommendations. 
Don't just rely on reinforcement learning to get your system from awful recommendations to good ones.
The user may get fed up and not be interested in helping your system through their input.

## Measuring Novelty

* Pick a datetime `t_0`
* Remove all films from the training data that were rated after `t_0`
* Remove some films that were rated before `t_0`
* If your system recommends one of the test films before `t_0`, your metric should be penalised.
* If your system recommends one of the test films after `t_0`, your metric should be rewarded.

## Cross-Validation
* A problem with dividing train-test-validate data is that you will have inherent selection bias - 
you are evaluating off films that the user has chosen to watch. Good to keep in mind.

## Evaluating top-k Recommender Systems

* For this, you need to extract some test data before training my model. These items should be ranked 
by their rating, and this ordered list can be assumed to be our ground truth.
* You then use your recommender system to rank the unseen items and then compare how the predicted 
ordering performed to the ground-truth ordering. 
* Can use the *Kendall Rank Correlation Co-efficient.*

## Limitations & Challenges of Evalution

* Users taste evolves over time, so when you do train-validate-test splits, there may be implicit 
biases
    * *You may have to consider temporal train-test splits*
    * While this will likely result in different distributions between training and test data, it is more realistic
* As mentioned already, by extracting out test data from the user, that already has inherent bias 
as the user has **chosen** to watch that film
