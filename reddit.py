'''
Created on Jul 7, 2018

@author: john
'''
import praw

class RedditManager():
    
    def __init__(self, cId, cSecret, userAgent, username, password):
        userAgent = "TroyCalendarBot"
        
        self.reddit = praw.Reddit(client_id=cId, 
                                  client_secret=cSecret, 
                                  user_agent=userAgent, 
                                  username=username, 
                                  password=password)
    
    
    def post(self, subreddit, title, data):
        return self.reddit.subreddit(subreddit).submit(title=title, selftext=data)
    
    def crosspost(self, post, sub):
        post.crosspost(sub)