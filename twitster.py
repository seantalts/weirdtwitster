# vim: set fileencoding=UTF-8
import calendar
import time
import twython
import rfc822
from credentials import CREDENTIALS

NUM_RETWEETS_REQUIRED = 34

def time_in_seconds(twitter_time):
    return calendar.timegm(rfc822.parsedate(twitter_time))


class Retweeter(object):
    """Examines the timeline of a user and finds popular tweets to retweet.
    """
    def __init__(self, **credentials):
        self.api = twython.Twython(**credentials)

    def is_popular(self, status):
        return status['retweet_count'] > NUM_RETWEETS_REQUIRED

    def should_examine(self, status):
        return not status['retweeted'] and not status['favorited']

    def examine_tweets(self, cutoff_age=None):
        cutoff = time.time() - (cutoff_age or 60 * 60 * 5)
        last_time = time.time()
        max_id = None
        while last_time > cutoff:
            print "max_id %s" % max_id
            for status in self.api.get_home_timeline(max_id=max_id, trim_user=0, count=200):
                if self.should_examine(status) and self.is_popular(status):
                    print "this one made the cut:", status
                    try:
                        self.api.retweet(id=unicode(status['id']))
                        print "Successful retweet."
                    except twython.exceptions.Twython as e:
                        print "Whoa. tweet from: ", status['user']['screen_name'], " original user: ", status['retweeted_status']['user']['screen_name']
                    except twython.TwythonError as e:
                        if e.error_code == 403 and (
                                'error occurred processing your request.' in e.msg):
                            print "must have already retweeted this tweet"
                        else:
                            raise
                    time.sleep(0.1)

            max_id = status['id']
            last_time = time_in_seconds(status['created_at'])
            time.sleep(0.1)


class TweetDownloader(object):
    """Downloads all the tweets of a user's friends
    """
    def __init__(self, **credentials):
        self.api = twython.Twython(**credentials)

    def download_tweets(self):
        pass

if __name__ == "__main__":
    r = Retweeter(**CREDENTIALS)
    r.examine_tweets()
