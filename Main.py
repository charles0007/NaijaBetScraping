import ScrapingTools as syn
from NaijaBetScraping import NaijaBetScrape
from stem import Signal
from stem.control import Controller
import threading
import time 

startDate=""
endDate=""
stake_no=3
match_no=1
max_time=70
last_stake=1 
for i in range(last_stake):
    time.sleep(20)
    t1=threading.Thread(target=NaijaBetScrape,args=(max_time,i+1),name = "Thread-{}".format(i + 1))
    t1.start()





