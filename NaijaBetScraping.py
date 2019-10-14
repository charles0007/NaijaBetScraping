# data_gathering
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
import pandas as pd
import numpy as np
import csv
import math
import random 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from boltons import iterutils
import socket
import socks
from stem import Signal
from stem.control import Controller
from pandas.plotting import andrews_curves
import matplotlib as plt
import ScrapingTools as syn

csv_titles=[]
# SELECT MATCH FOR THE DAY
def NaijaBetScrape(max_time,match_no):
	chromeOptions = webdriver.ChromeOptions()
	url="https://www.naijabet.com/live/"
	# , 'disk-cache-size': 4096 dnt use for dynamic pages
	prefs = {'profile.managed_default_content_settings.images':2}
	chromeOptions.add_experimental_option("prefs", prefs)
	# driver = webdriver.Chrome(chrome_options=chromeOptions)
	driver=webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/chromedriver/chromedriver.exe",options=chromeOptions)
	driver.get(url)
	#login
	try:
		login_element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, "b-usermenu__form")))
		
		#loginbox > fieldset > a #password
	finally:
		soup=BeautifulSoup(driver.page_source,"lxml")
		fieldset=soup.select("#loginbox > fieldset")
		

	i_loop=2
	while 1:
		driver.get("https://www.naijabet.com/live")
		try:
			login_element = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, "b-menu__link")))
			i_loop+=1
		finally:
			soup=BeautifulSoup(driver.page_source,"lxml")
		
			doubles=soup.select("#menu___allsports > li.all-tabs.tab-all.b-menu__item.m-menu__item_first.g-shadow_1_1_6.sport_block_18.sport_block > ul")
			if len(doubles)==0:
    				doubles=soup.select("#menu___allsports > li.b-menu__item.m-menu__item_first.g-shadow_1_1_6.sport_block_18.sport_block > ul")
			tring=""
			ddiv=""
	
			for double in doubles:
	    			tring=tring+str(double.encode('utf-8'))
	    			
			
			odd_id=[]
			ty=1
			no_result=False
			odds=[]
			odds_value=[]
			nth=1
			match_nth=0
			title_arr=[]
			data_collection = {}
					# prev_data_collection = {}
			match_odd_id=[]
			match_id_arr=[]
			it=0
			loop=0
			try:
				loop_num=0
				for dt in BeautifulSoup(tring,"lxml").find_all(class_="b-menu__link"):
					loop_num=loop_num+1	
					if loop_num!=match_no:
						continue
					# # if loop_num>5:
					# # 	break
					try:
						score_scope_id=dt.get("id")
						# print("success")
						teams=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[1]").text
						score=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[2]").text
						scope=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[3]").text
						# start_time=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[4]").text
						# print(scope.split("'")[0])
						try:
							team1=str(teams).split("-")[0].strip()
							team2=str(teams).split("-")[1].strip()
						except:
							team1=str(teams).split("vs")[0].strip()
							team2=str(teams).split("vs")[1].strip()
						scope=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[3]").text
						team_time=scope.split("'")[0]
						score=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[2]").text
						team1_score=str(score).split(":")[0].strip()
						team2_score=str(score).split(":")[1].strip()

						driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']").click()
						time.sleep(20)
						trings=""
						# //*[@id="content"]/div/div[1]/div[loop]/div[1]/h1 #left
						for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div > div.b-message.m-message_no_result"):
									no_result=True
						if no_result and int(team_time)>max_time:
								no_result=False
								if len(data_collection)>10:
									writeCsv(data_collection,team1,team2)
									driver.quit()
									print("quit1")
									break
									print("brhghgeak")
						elif no_result and int(team_time)<max_time and len(data_collection)>10:
    							continue
						for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div.events_contein.g-clearfix > div.live_left"):
								trings=trings+str(tring_b4.encode('utf-8'))
								# print(trings)
						while 1:
							# print("another--")
							nth=1					
							while 1:
														
								try:
									title=""
									
									for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div.events_contein.g-clearfix > div.live_left > div:nth-of-type("+str(nth)+") > div.b-title.b-title__bg.title_contein_box.drop_title > h1"):
										title_arr.append(tring_b4.text)
										
										title=tring_b4.text
										# print(tring_b4.text)
									if title=="":
										break
									trings=""
									for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div > div.live_left > div:nth-of-type("+str(nth)+")"):
											trings=trings+str(tring_b4.encode('utf-8'))
									# for d in BeautifulSoup(trings,"lxml").find_all(class_="cell_bord_l"):
									# 		if d.a.get('id')=="None" or d.a.get('id')=="" or d.a.get('id')==None:
									# 		continue
									# 	# print(str(d.a.get('id')))
									# 	str_id=d.a.get('id');
										
									for d in BeautifulSoup(trings,"lxml").find_all(class_="b-link"):
										not_available=False
										# for market_disabed in BeautifulSoup(d,"lxml").find_all(class_="market_disabed"):
										# 	not_available=True
										# 	print("not_available")
										if d.get('id')=="None" or d.get('id')=="" or d.get('id')==None or not_available==True:# or d.get('id') in match_id_arr:
											continue
										str_id=d.get('id');	
										match_id_arr.append(str_id)
										if title=="Match Odds" or title=="Number of goals" or title=="Away team number of goals" or title=="Home team number of goals" or title=="Next Goal":  
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]").text 
										elif title=="Asian Handicap":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[4]").text +"  "+driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[3]").text 
										elif title=="Over/Under":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b").text 
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[4]/span").text +"  "+driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[3]").text  
										elif title=="Correct Score" or title=="Double Chance" or title=="Half Time/Full Time":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]").text 
										elif title=="Over/Under home team" or title=="Over/Under away team":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span[2]/span").text +"  "+driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span[1]").text
										elif title=="Odd/Even" or title=="Both teams to score" or title=="Home team to score" or title=="Away team to score": 
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span").text
										elif title=="Three-way handicap": 
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span/span").text #//*[@id="content"]/div/div[2]/div[6]/div[2]/table/tbody/tr[3]/td[1]/span/p
										else:
											odds_name=""
											odds_value_=0

											# try:
											# 	odds_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											# except:
											# 	odds_=0
											# odds_value_=0
											# odds_goal=""
											# try:
											# 	odds_goal=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]").text
											# except:
											# 	odds_goal=""
											# try:
											# 	odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span[1]").text	
											# 	# print("first try")
											# except:
											# 	# print("first except")
											# 	try:
											# 		odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[3]").text
											# 		# print("second try")
											# 	except:
											# 		odds_value_=0
												# print("second except")	
												
										# str_id:title,
										
										prev_data_collection={}
										scope=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[3]").text
										team_time=scope.split("'")[0]
										score=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[2]").text
										team1_score=str(score).split(":")[0].strip()
										team2_score=str(score).split(":")[1].strip()
										prev_data_collection={"title":title,"odd_id":str_id,"odds_name":odds_name,"odds_value":odds_value_,"team1_goal":team1_score,"team2_goal":team2_score,"team_time":team_time}#add titile to dict, goal,time
										# data_collection.update(prev_data_collection)
										# print("loop- "+str(it))
										data_collection[it]=prev_data_collection
										
										# print(data_collection[it])
										it=it+1
										odds.append(driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']").text)# click odds
										odds_value.append(driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text) #odd value
										

									nth=nth+1
									break
								except KeyboardInterrupt:
									driver.quit()
									break
								except ConnectionRefusedError:
									driver.quit()
									break
								except ConnectionAbortedError:
									driver.quit()
									break
								except ConnectionError:
									driver.quit()
									break
								except Exception as ex:
									print("continue111--"+str(ex).split('(')[0].strip())
									if str(ex).split('(')[0].strip()=="HTTPConnectionPool":
										writeCsv(data_collection,team1,team2)
										# driver.quit()
										exit(0)
										break
									continue
							nth=2
							while 1:
													
								try:
									
									title=""
									
									for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div > div.bet_right.live_right.widget_margin_fix > div:nth-of-type("+str(nth)+") > div.b-title.b-title__bg.title_contein_box.drop_title > h1"):
										title_arr.append(tring_b4.text)
										title=tring_b4.text
										
									if title=="":
										for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div.events_contein.g-clearfix > div.bet_right.live_right > div:nth-of-type("+str(nth)+") > div.b-title.b-title__bg.title_contein_box.drop_title > h1"):
    											title_arr.append(tring_b4.text)
    											title=tring_b4.text
										if title=="":
											break
									
									trings=""
									for tring_b4 in BeautifulSoup(driver.page_source,"lxml").select("#content > div > div.live_right > div:nth-of-type("+str(nth)+")"):
											trings=trings+str(tring_b4.encode('utf-8'))
									# for d in BeautifulSoup(trings,"lxml").find_all(class_="cell_bord_l"):
									# 		if d.a.get('id')=="None" or d.a.get('id')=="" or d.a.get('id')==None:
									# 		continue
									# 	# print(str(d.a.get('id')))
									# 	str_id=d.a.get('id');	
									
									for d in BeautifulSoup(trings,"lxml").find_all(class_="b-link"):
										if d.get('id')=="None" or d.get('id')=="" or d.get('id')==None:# or d.get('id') in match_id_arr:
											continue
										str_id=d.get('id');	
										match_id_arr.append(str_id)
										if title=="Match Odds" or title=="Number of goals" or title=="Away team number of goals" or title=="Home team number of goals" or title=="Next Goal":  
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]").text 
										elif title=="Asian Handicap":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[4]").text +"  "+driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[3]").text 
										elif title=="Over/Under":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b").text 
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[4]/span").text +"  "+driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[3]").text  
										elif title=="Correct Score" or title=="Double Chance" or title=="Half Time/Full Time":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]").text 
										elif title=="Over/Under home team" or title=="Over/Under away team":
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text 
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span[2]/span").text +"  "+driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span[1]").text
										elif title=="Odd/Even" or title=="Both teams to score" or title=="Home team to score": 
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span").text
										elif title=="Three-way handicap": 
											odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											odds_name=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span/span").text
										else:
											odds_name=""
											odds_value_=0

											# try:
											# 	odds_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text
											# except:
											# 	odds_=0
											# odds_goal=""
											# try:
											# 	odds_goal=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]").text
											# except:
											# 	odds_goal=""
											# odds_value_=0
											# try:
											# 	odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[2]/span[1]").text	
											# except:
											# 	try:
											# 		odds_value_=driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/span[3]").text
											# 	except:
											# 		odds_value_=0		
										# str_id:title,	
										
										prev_data_collection={}
										time.sleep(1)
										scope=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[3]").text
										team_time=scope.split("'")[0]
										score=driver.find_element_by_xpath("//*[@id='"+score_scope_id+"']/div/span[2]").text
										team1_score=str(score).split(":")[0].strip()
										team2_score=str(score).split(":")[1].strip()
										prev_data_collection={"title":title,"odd_id":str_id,"odds_name":odds_name,"odds_value":odds_value_,"team1_goal":team1_score,"team2_goal":team2_score,"team_time":team_time}#add titile to dict, goal,time
										# print("loop- "+str(it))
										data_collection[it]=prev_data_collection
										
										# print(data_collection[it])
										it=it+1
										odds.append(driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']").text)# click odds
										odds_value.append(driver.find_element_by_xpath("//*[@id='"+d.get("id")+"']/b[1]").text) #odd value
										

									nth=nth+1
									break
								except KeyboardInterrupt:
									driver.quit()
									break
								except ConnectionRefusedError:
									driver.quit()
									break
								except ConnectionAbortedError:
									driver.quit()
									break
								except ConnectionError:
									driver.quit()
									break
								except Exception as ex:
									print("continue2222: "+ str(ex).split('(')[0].strip())
									# writeCsv(data_collection,team1,team2)
									# driver.quit()
									if str(ex).split('(')[0].strip()=="HTTPConnectionPool":
										writeCsv(data_collection,team1,team2)
										# driver.quit()
										exit(0)
										break
									
							odd_arr=[]
							#  and title==""
							if int(team_time)>=max_time:
								writeCsv(data_collection,team1,team2)
								print("quit-generally")								
								break

							# else:
								# print("it:-"+str(it))
								# print("team_time - "+str(team_time))
								# print("data_collection- "+str(len(data_collection)))
								# continue
						break
						# loop+=1
						# if loop>=5:
						# 	break
					except KeyboardInterrupt:
						driver.quit()
						break
					except ConnectionRefusedError:
						driver.quit()
						break
					except ConnectionAbortedError:
						driver.quit()
						break
					except ConnectionError:
						driver.quit()
						break	
					except Exception as ex:
						print("Execp- "+ str(ex).split('(')[0].strip())
						if len(data_collection)>1:
							writeCsv(data_collection,team1,team2)
						# driver.quit()
						print("quit3")
						if str(ex).split('(')[0].strip()=="HTTPConnectionPool":
							writeCsv(data_collection,team1,team2)
							# driver.quit()
							exit(0)
							break
						continue
					
			except Exception as ex:
				print("last ex- "+str(ex))
				writeCsv(data_collection,team1,team2)
				driver.quit()
				print("quit4")
				break
		
		for csv_title in csv_titles:
			syn.get2UniqueRows(syn.csvToDictListDesc(csv_title,True),csv_title)
			syn.getUniqueRowsByOdds(syn.csvToDictListDesc(csv_title,False),csv_title)
		syn.getSimilarData2(csv_titles)
		
		# csv_titles.clear()
		driver.quit()
		break
		# if int(team_time)>=85:
    	# 		break	


def writeCsv(data_collection,team1,team2):
	csv_file =team1+"__"+team2+".csv"
	csv_titles.append(csv_file)
	csv_columns = ['title','odd_id','odds_name','odds_value','team1_goal','team2_goal','team_time']
	try:
		with open("1teams/"+csv_file, 'w',encoding='utf-8',newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			i=0
			for data in data_collection:
				# print(data_collection[data])
				writer.writerow(data_collection[data])
		data_collection.clear()
	except IOError as ex:
		print("I/O error"+str(ex)) 

