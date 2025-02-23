# ***[FILM-REC](https://film-rec.onrender.com/)***

A film recommendation web app. Films are recommended based on user-submitted IMDB or Letterboxd data. I built the recommendation algorithm from scratch - no external ML libraries were used. This took me one year, and I was working on it as a side project, both for fun and learning.

Before starting the project, I was interested in ML and Data Science, so I wanted to work on a project related to this. I love films, so when it came to thinking about what kind of project to do, a recommendation web app was the clear answer.

## Recommendation Algorithm

I read the book *Recommender Systems: The Textbook by Charu C. Aggarwal* to learn about recommendation algorithms and what to consider. Collaborative filtering is...

## Project Architecture

## How to test locally

* Clone the repository and checkout to the `local-deployment` branch.
* Open 2 instances of the terminal. We will download dependencies and run both the frontend and the backend.
* In one terminal, run the following commands for the backend.
    ```sh
    $ cd backend/
    $ pip3 install -r requirements.txt
    $ python3 app.py
    ```
    * note: `pip` instead of `pip3` may work
    * or also `python` instead of `python3`
* In the other terminal, run the following commands for the frontend.
    ```sh
    $ cd frontend/
    $ npm install
    $ npm start
    ```
* npm should open the front page in localhost
    * If not, try go to [localhost:3000](http://localhost:3000)

## Acknowledgements
