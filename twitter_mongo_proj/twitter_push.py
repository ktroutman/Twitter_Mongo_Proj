import tweepy
import pymongo
from tm_connection import load_to_mongo
from config import cfg, client


#Create function for the API configration to use twitter
def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main(chunk_size,limit):
  api = get_api(cfg)
  # Create tweet and send it to twitter
  load_to_mongo(chunk_size,limit,client)
  streamed=list(client.twitter.collections.tweets_labeled.find({'interesting':1}).sort('$natural',pymongo.DESCENDING).limit(int(f'{limit}')))
  followers=[]
  #TO DO ON THE DBS LEVEL
  for t in streamed:
      followers.append(t['followers'])
  for t in streamed:
      if t['followers']==max(followers):
          tweet= 'By @'+t['username']+'\n\n'+t['text']
  status = api.update_status(status=tweet)
  

if __name__ == "__main__":
  main(3,10)