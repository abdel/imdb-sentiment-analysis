class Config(object):
    SITE_NAME = 'Sentiment Analysis for Movie Reviews'
    SITE_SLUG_NAME = 'imdb-sentiment-analysis'
    TAGLINES = ['Sentiment Analysis using Deep Learning']
    SITE_DESCRIPTION = 'Sentiment analysis for movie reviews'
    SITE_KEYWORDS = 'sentiment analysis, imdb, movie, review, nlp, deep learning'
    ADMINS = ['abdelm.is@gmail.com']

class DevelopmentConfig(Config):
    DOMAIN = 'localhost=5000'
    ASSET_DOMAIN = 'localhost=5000'

class ProductionConfig(Config):
    DOMAIN = 'imdb-sentiment-analysis.herokuapp.com'
    ASSET_DOMAIN = 'imdb-sentiment-analysis.herokuapp.com'
