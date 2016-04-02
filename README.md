The code runs using python version 3.4.3

The algorithm uses a heap structure with a hash table to 
keep track of the unique hashtag pairs. The timestamp
a particular hashtag pair came in is used as the priority
key for the heap. 

The average case running time is O(t + m * log(N)) 
where t is the number of tweets, m is the total number 
of hashtag pairs that are obtained from all tweets, 
and N is the maximum number of unique hashtag pairs 
that can be found in tweets that are within a 
60 second window plus one extra tweet.

If hash table lookups are assumed to be constant time
then the above analysis can be strengthened to worst 
case running time.


All tests are made using random input; the output
is produced using a naive version of the algorithm
where after every tweet the graph is reconstructed
and hashtag pairs that fall out of the 60 second 
window are deleted.
