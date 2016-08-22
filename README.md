# Welcome to the Movies database.

This is a Django powered website that has a focus on movie ratings and reviews.

## Installation

To get the site up and running locally:

1. Clone the repo
2. pip install -r requirements.txt
3. Have a postgres server with an empty movies database
4. Navigate to the movieratings directory
5. ./manage.py migrate
6. Wait while all the data is imported. (Sometimes takes up to 30 minutes)

## Usage

Simply register an account and start rating some movies. After you have rated several movies, you can use the Recommend Movies feature to receive movie suggestions based off your previous ratings. Please note that this feature is in the early stages and can take up to 5 minutes to run.

## Credit

Movie Lens for the data set located [here](http://grouplens.org/datasets/movielens/)

## Future

* Improve speed on average score calculations
* Improve the Movie Recommender speed
* Cache results from Movie Recommender and update the cache periodically
