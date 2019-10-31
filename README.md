# NaijaBetScraping
#Python programme for scraping live football data from NaijaBet using selenium

#Python 3.6.6

#Dependencies
pip install threading
pip install time


#Example

from NaijaBetScraping import NaijaBetScrape

import threading

import time 

# VARIABLES
max_time=70 # maximum time to for scraping(using the football time) 

sleep_time=20 # maximum sleep time when running thread

#program using thread 

for i in range(last_stake):

    time.sleep(sleep_time)
    
    t1=threading.Thread(target=NaijaBetScrape,args=(max_time,i+1),name = "Thread-{}".format(i + 1))
    
    t1.start()
    
#the program is been run in a thread
    
    







