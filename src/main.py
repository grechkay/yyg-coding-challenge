import json
import os
import heapq as hq
import datetime
from itertools import combinations
import avecount
import logging
import tweetheap


if __name__ == '__main__':
    #The idea of the algorithm is to read each tweet line by line, maintaining a priority queue 
    #which uses the created_at value as its priority. 

    #Every time a tweet comes in, unique hashtags are extracted the timespamp of the tweet is obtained.
    #If the timestamp is the latest that has come in then its value is saved, otherwise it is ignored.

    #For each combination of two hashtags, the two hashtags are pushed along with the timestamp onto a 
    #priority queue and an edge is added in the graph. If the edge already exists in the priority 
    #queue, then instead of adding it, the timestamp of the existing element is changed.

    #Then the oldest elements from the priority are
    #deleted from the queue until an element is reached which occured within the last 60 seconds; 
    #subsequently all the expired edges (and vertices) are removed from the graph.

    #The graph class does no error checking and assumes perfect input.

    #The average case runtime is O(t + m*log(N)) where m is the total number of hashtag pairs that need to be processed
    #and N is the maximum number of unique hashtag pairs that occur within a minute window plus one extra tweet,
    #and t is the total number of tweets.

    f = '%a %b %d %H:%M:%S %z %Y'   # This is the pattern to transform the "created_at" field into a datetime object
   


    tweet_window = tweetheap.TweetHeap() #Priority queue for the tweets.

    latest_tweet = 0 #Keeping track of the latest timestamp.

    ave_count_graph = avecount.AveCountGraph() #Creating the graph object.
    
    
    basedir = os.curdir
    outfile = open(basedir + '/tweet_output/output.txt','w')
    
    logging.basicConfig(filename=basedir + '/src/logfile.log',level=logging.DEBUG, filemode = 'w')
   
    with open(basedir + '/tweet_input/tweets.txt','r') as input_file:
        for line in input_file:
            try: # Try to read the JSON line
                tweet_json = json.loads(line)
            except: #If can't then skip the tweet and log the line.
                logging.error(line)
                continue
            if 'limit' in tweet_json: # logging rate limit messages and continuing to the next tweet
                logging.info(line)    
                continue
            try:
                # attempting to get the hashtags out of the json object
                # if it fails then this is due to a malformed tweet and the tweet will be skipped.
                hashtags = [ t['text'] for t in tweet_json['entities']['hashtags']  ]
            except:
                logging.error(line)
                continue
            hashtags = set(hashtags) # Making the set of hashtags unique
            try:
                # attempting to get the time the tweet was created at
                # if it fails then this is due to a malformed tweet and the tweet will be skipped
                created_at = tweet_json['created_at'] 
            except:
                logging.error(line)
                continue
            tweet_dt = datetime.datetime.strptime(created_at,f) #Converting the time to a datetime object
            tweet_ts = int(tweet_dt.timestamp()) #Converting the datetime object into a timestamp
            latest_tweet = max(tweet_ts,latest_tweet) #Keeping track of when the latest tweet came in
            window_floor = latest_tweet - 60 #Keeping track of the minimum timestamp a tweet must have to be included in the graph.


            if tweet_ts > window_floor:
                # If the timestamp of the current tweet is bigger than the current floor then
                # each combination of two unique hashtags is pushed onto the priority queue
                # with the priority being their timestamp.

                # If the set of hashtags is new then it is added to the priority queue,
                # otherwise the timestamp of the existing element is simply changed.
                # Subsequently the new edges are added to the graph data structure.
                for elem in combinations(hashtags,2):
                    elem = frozenset(elem)
                    if elem not in tweet_window.edgehash: # O(1) average
                        ave_count_graph.add_edge(*elem)   # O(1) average
                    tweet_window.push((tweet_ts,elem))    # O(log(N)) worst case. In this case N is the number of unique hashtag pairs in the heap including 
                                                          # the ones derived from the current tweet; this includes all the hashtag pairs that fall into 
                                                          # the minute window of the timestamp of the latest tweet (as of the previous tweet).
                    
            while True:
                # Tweets that fall outside the 60 second window are popped off the priority queue one at a time. Their corresponding
                # edges in the graph structure are subsequently removed.

                # Since the edges that are to be removed are always added first, there is no danger of removing edges that don't exist.
                if len(tweet_window.heap) == 0:
                    break
                most_distant = hq.nsmallest(1,tweet_window.heap)[0]     # O(1) worst case
                if most_distant[0] > window_floor:                      
                    break
                else:
                    elem = tweet_window.pop()                           # O(log(N)) worst case. N here is less than or equal to the N from the push routine.
                    ave_count_graph.remove_edge(*elem[1])               # O(1) average

            ave = ave_count_graph.get_ave() * 100 // 1 / 100.0 # Truncating to 2 decimal points
            k = "{:.2f}".format(ave) # Formatting to 2 decimal point.
            outfile.write(k)
            outfile.write('\n')
       
