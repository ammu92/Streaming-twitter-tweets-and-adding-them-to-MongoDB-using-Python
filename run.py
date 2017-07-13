import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import json
from pprint import pformat

"""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CREDENTIALS_PATH = "/Users/deepikaravi/pysource/twendsbot/twitter_credentials.txt"

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

my_db_data = []
public_tweets = api.home_timeline()
for i in range(0,5):
	user_dict = {}
	user_dict["hashtags"] = []
	user_dict["user"] = public_tweets[i].user.screen_name
	user_dict["location"] = public_tweets[i].user.location
	user_dict["tweet"] = public_tweets[i].text
	for tag in public_tweets[i].entities["hashtags"]:
		user_dict["hashtags"].append(tag["text"])
	my_db_data.append(user_dict)

#print (pformat(my_db_data))


# db connection and storage
db_client = MongoClient("deepika_mac", 27017)
db = db_client.tweetdb
#db.public_tweets_coll.insert(my_db_data)

loc_group = db.public_tweets_coll.aggregate(([{"$group" : {'_id':"$location"}}]))
#loc_docs = {}
for location in loc_group:
	print("\n********************************************************************************************************")
	print "location = " + str(location["_id"])
	print("********************************************************************************************************")
	loc_docs = db.public_tweets_coll.find({"location":location["_id"]})
	for doc in loc_docs:
		print pformat(doc)
	

"""
def init_tweets_api():
	CONSUMER_KEY = "Tjqzxt0gq7yjwZqzgM9i9RjDj"
	CONSUMER_SECRET = "2OkZKPBa8NOiB7fJsGfLubQJ6q63FTScUqajaWGgUcUKJ0CUJo"
	ACCESS_TOKEN = "4718427602-7aQJNIxOyiWkirbeGevAtnT9pryaRxWwPCMBfE6"
	ACCESS_TOKEN_SECRET = "xbM6QgASIrw95Eo0elZMcWJezLu150ljCSSb9AdfTX9MM"
	
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	return api

def init_mongodb():
	db_client = MongoClient("SAMSUNG-PC", 27017)
	db = db_client.twends
	return db

def get_new_tweets(api, db):
	my_db_data = []
	public_tweets = api.home_timeline()
	for public_tweet in public_tweets:
		user_dict = {}
		user_dict["hashtags"] = []
		user_dict["user"] = public_tweet.user.screen_name
		user_dict["location"] = public_tweet.user.location
		user_dict["tweet"] = public_tweet.text
		for tag in public_tweet.entities["hashtags"]:
			user_dict["hashtags"].append(tag["text"])
		my_db_data.append(user_dict)
	db.public_tweets_coll.insert(my_db_data)
	print "Successfully inserted tweets!"

	

def groupby_user(db):
	user_cursor = db.public_tweets_coll.aggregate(([{"$group" : {'_id':"$user"}}]))
	for user in user_cursor:
		print("\n********************************************************************************************************")
		print "User Name: " + str(user["_id"])
		print("********************************************************************************************************")
		docs = db.public_tweets_coll.find({"user":user["_id"]})
		for doc in docs:
			print "\n"
			print pformat(doc)
	

def countby_location(db):
	#loc_group = db.public_tweets_coll.aggregate(([{"$group" : {'_id':"$location"}}]))
	location_cursor = db.public_tweets_coll.aggregate(([{"$group" : {'_id':"$location", 'count':{'$sum':1}}}]))
	for location in location_cursor:
		try:
			print("\n********************************************************************************************************")
			print("Location: " + str(location["_id"]) + "\tNumTweets: " + str(location["count"]))
			print("********************************************************************************************************")
			#loc_docs = db.public_tweets_coll.find({"location":location["_id"]})
			#for doc in loc_docs:
			#	print pformat(doc)
		except UnicodeEncodeError:
			pass

def display_all(db):
	all_cursor = db.public_tweets_coll.find()
	print("\n********************************************************************************************************")
	for doc in all_cursor:
		print pformat(doc)
		print("\n********************************************************************************************************")
	




def main():
	api = init_tweets_api()
	db=init_mongodb()
	print "\n\nI am your TwendsBot!\nLet me help you find the trending tweets...\n"
	while(True):
		print "-"*40
		print "1. Find tweets by each user"
		print "2. Find the number of tweets by location"
		print "3. Display all tweets"
		print "4. Extract new tweets"
		print "-"*40
		choice = int(input("Enter choice::"))
		if choice == 1:
			groupby_user(db)
		elif choice == 2:
			countby_location(db)
		elif choice == 3:
			display_all(db)
		elif choice == 4:
			get_new_tweets(api, db)
		else:
			print "Invalid choice"

if __name__ == '__main__':
	main()
