#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "3002464001-re5dQQ06KcxtD5HPS7aNhFoRw33pSJje0BNupnk"
access_token_secret = "5bW0IiTa8ygutXTT2Ukl6vfjBoAhPF0EYitqY79k4nLZT"
consumer_key = "rcLD3eYXnPTEP6lmJOaGbhAO1"
consumer_secret = "8UqweEJOzlMzi4xmDcsGtS0TEvQ6IvHPq9gzRGywP777zbtkT6"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby', 'icecream', 'nutella'])