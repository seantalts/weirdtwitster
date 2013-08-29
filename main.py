import webapp2
import twitster

class RetweetPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello, webapp2 asdfjlsakdfj World!')
      cutoff = self.request.params.get('cutoff', None)
      r = twitster.Retweeter(**twitster.CREDENTIALS)
      r.examine_tweets(cutoff_age=cutoff)

app = webapp2.WSGIApplication([('/find_more_retweets', RetweetPage)],
                              debug=True)
