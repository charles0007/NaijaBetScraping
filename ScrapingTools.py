import pandas as pd
import numpy as np
import csv
import math
import random
import socket
import socks
from stem import Signal
from stem.control import Controller

 
# def writeCsv(data_collection,team1,team2):
#     	csv_file =team1+"__"+team2+".csv"
# 	csv_titles.append(csv_file)
# 	csv_columns = ['title','odd_id','odds_name','odds_value','team1_goal','team2_goal','team_time']
# 	try:
# 		with open("1teams/"+csv_file, 'w',encoding='utf-8',newline='') as csvfile:
# 			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
# 			writer.writeheader()
# 			i=0
# 			for data in data_collection:
# 				# print(data_collection[data])
# 				writer.writerow(data_collection[data])
# 		data_collection.clear()
# 	except IOError as ex:
# 		print("I/O error"+str(ex)) 

def writeCsv2UniqueSet(data_collection,csv_file,col):
	# csv_file = team1+"__"+team2+".csv"
	if col is not None:
		csv_columns=col
	else:
		csv_columns = ['title','odd_id','odds_name','odds_value','team1_goal','team2_goal','team_time']
	try:
		with open(csv_file, 'w',encoding='utf-8',newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			i=0
			for data in data_collection:
				# print(data_collection[data])
				writer.writerow(data)
		# data_collection.clear()
	except IOError as ex:
		print("I/O error"+str(ex)) 

def csvToDict(filename):
	df={}
	# , header=None, index_col=0, squeeze=True
	df=pd.read_csv(filename)#.to_dict()
	return df


def eliminateDuplicate(data_collection):
	# data_collection.sort_values("title", inplace = True)
	data_collection.drop_duplicates(subset ="odd_id", keep = False, inplace = True)
	data_collection.to_csv('Updated_Czech Republic U21__Iceland U21.csv')
	# print(data_collection) 
	return data_collection

def sortCsv(filename):
	df={}
	df=pd.read_csv('1teams/'+filename)
	df.sort_index(axis=0, inplace = True,ascending=False)
	df.to_csv('2sortResult/'+filename)
	return df

def csvToDictListDesc(csv_path,sort):
	if sort:
		sortCsv(csv_path)
	mylist = []
	mydict = {}

# read the csv and write to a dictionary
	with open('2sortResult/'+csv_path, 'r') as csv_file:
	    reader = csv.reader(csv_file)
	    for column in reader:
	    	title=column[1]
	    	str_id=column[2]
	    	odds_name=column[3]
	    	odds_value_=column[4]
	    	
	    	team1_score=column[5]
	    	team2_score=column[6]
	    	team_time=column[7]
	    	mydict = {"title":title,"odd_id":str_id,"odds_name":odds_name,"odds_value":odds_value_,"team1_goal":team1_score,"team2_goal":team2_score,"team_time":team_time}
	    	mylist.append(mydict)
	return mylist				

def csvToDictListLowOdds(csv_path):
	mylist = []
	mydict = {}
# read the csv and write to a dictionary
	try:
		with open('4LowOdds/'+csv_path, 'r') as csv_file:
			reader = csv.reader(csv_file)
			for column in reader:
				title=column[0]
				str_id=column[1]
				odds_name=column[2]
				odds_value_=column[3]
				
				team1_score=column[4]
				team2_score=column[5]
				team_time=column[6]
				mydict = {"title":title,"odd_id":str_id,"odds_name":odds_name,"odds_value":odds_value_,"team1_goal":team1_score,"team2_goal":team2_score,"team_time":team_time}
				mylist.append(mydict)
	except:
		pass
	return mylist

def finalDataToDictList(csv_path):
	mylist = []
	mydict = {}

# read the csv and write to a dictionary
	with open(csv_path, 'r') as csv_file:
	    reader = csv.reader(csv_file)
	    for column in reader:
	    	title=column[0]
	    	odds_name=column[1]
	    	team_time=column[2]
	    	apperance=column[3]	    	
	    	mydict = {"title":title,"odds_name":odds_name,"team_time":team_time,"apperance":apperance}
	    	mylist.append(mydict)
	return mylist				

def csvToDictList(csv_path):
	mylist = []
	mydict = {}

# read the csv and write to a dictionary
	with open(csv_path, 'r') as csv_file:
	    reader = csv.reader(csv_file)
	    for column in reader:
	    	title=column[0]
	    	str_id=column[1]
	    	odds_name=column[2]
	    	odds_value_=column[3]
	    	
	    	team1_score=column[4]
	    	team2_score=column[5]
	    	team_time=column[6]	    	
	    	mydict = {"title":title,"odd_id":str_id,"odds_name":odds_name,"odds_value":odds_value_,"team1_goal":team1_score,"team2_goal":team2_score,"team_time":team_time}
	    	mylist.append(mydict)
	return mylist

def csvToDictListResult(from_path,csv_path):
	mylist = []
	mydict = {}
	match_odds_count=0
	team1=csv_path.split("__")[0].lower()
	team2=csv_path.split("__")[1].lower().split(".")[0]
# read the csv and write to a dictionary
	with open(from_path+csv_path, 'r') as csv_file:
	    reader = csv.reader(csv_file)
	    for column in reader:
    		if column[0].strip()=="title":
    			continue
	    	title=column[0]
	    	str_id=column[1]
	    	odds_name=column[2].strip()
	    	odds_value_=column[3]	    	
	    	team1_score=column[4]
	    	team2_score=column[5]
	    	team_time=column[6]
	    	result="undefined"
	    	str_title=title.strip()
	    	score1=int(team1_score)
	    	score2=int(team2_score)
	    	if str_title=="Both teams to score" or str_title=="Home team to score":
	    		if odds_name.strip()=="No goal" and (int(team1_score)==0 and int(team2_score)==0):
    	    			result="win"
	    		elif odds_name.strip()=="Goal" and (int(team1_score)>0 and int(team2_score)>0):
	    			result="win"
	    		else:
	    			result="loss"					
	    	elif str_title=="Match Odds":
	    		if int(team1_score)>int(team2_score) and odds_name.strip().lower()==team1:
	    			result="win"
	    		elif int(team1_score)==int(team2_score) and odds_name.strip().lower()=="draw":
	    			result="win"
	    		elif int(team2_score)>int(team1_score) and odds_name.strip().lower()==team2:
	    			match_odds_count=0
	    			result="win"
	    		else:
	    			result="loss"
	    		match_odds_count=match_odds_count+1
	    	elif str_title=="Number of goals" or str_title=="Away team number of goals" or str_title=="Home team number of goals":
	    		odd_goal=odds_name.split("or")[0]
	    		less_or_more=""
	    		try:
	    			less_or_more=odds_name.split("or")[1].strip()
	    		except:
	    			less_or_more=""
	    		if int(team1_score)+int(team2_score)==int(odd_goal) and less_or_more=="":
	    			result="win"
	    		elif int(team1_score)+int(team2_score)>=int(odd_goal) and less_or_more=="more":
	    			result="win"
	    		elif int(team1_score)+int(team2_score)<=int(odd_goal) and less_or_more=="less":
	    			result="win"
	    		else:
	    			result="loss"	    
	    	elif str_title=="Over/Under" or str_title=="Over/Under home team" or str_title=="Over/Under away team":
	    		over_under=odds_name.strip().split(" ")[0].strip().lower()
	    		over_under_point=odds_name.strip().split(" ")[-1].strip()
	    		# print(odds_name.strip()+"again")
	    		# try:
	    		# 	one=int(over_under_point.split(".")[0])
	    		# except:
	    		# 	print(odds_name.strip().split(" "))
	    		one=int(over_under_point.split(".")[0])
	    		two=int(over_under_point.split(".")[-1])
	    		if over_under=="over":
	    			if score1+score2>=one+1 and two==5:
	    				result="win"
	    			elif score1+score2>one+1 and two==75:
	    				result="win"
	    			elif score1+score2==one+1 and two==75:
	    				result="half"
	    			else:
	    				result="loss"
	    		elif over_under=="under":
	    			if score1+score2<=one:
	    				result="win"
	    			else:
	    				result="loss" 
	    	elif str_title=="Correct Score":
	    		if score1==int(odds_name.strip().split("-")[0]) and score2==int(odds_name.strip().split("-")[1]):
	    			result="win"
	    		else:
	    			result="loss"
	    	elif str_title=="Double Chance":
	    		if odds_name=="X2" and ((score1==score2) or score2>score1):
	    			result="win"
	    		elif odds_name=="1X" and ((score1==score2) or score1>score2):
	    			result="win"
	    		elif odds_name=="12" and ((score1>score2) or score2>score1):
	    			result="win"
	    		else:
	    			result="loss" 
	    	elif str_title=="Odd/Even":
	    		if odds_name=="Even" and (score1+score2)==0:
	    			result="win"
	    		elif odds_name=="Even":
	    			if(score1+score2)%2==0:
	    				result="win"
	    		elif odds_name=="Odd" and (score1+score2)%2>0:
	    			result="win"
	    		else:
	    			result="loss"
	    	mydict = {"title":title,"odd_id":str_id,"odds_name":odds_name,"odds_value":odds_value_,"team1_goal":team1_score,"team2_goal":team2_score,"team_time":team_time,"result":result}
	    	mylist.append(mydict) 
	return mylist				


def getUniqueRowsByOdds(mylist,csv_title):
	new_data=[]
	new_dict={}
	i=0
	# new_data.append(mylist[1])
	for data in mylist:
		count=0
		rty=False
		exist=False
		exist_c=0
		for n_d in new_data:
			if n_d['odd_id'] == data['odd_id']:
    				exist=True
    				break
		for n_d in new_data:
    			if data['odd_id']== n_d['odd_id'] and (data['odds_value'] !=n_d['odds_value']):
        				count=count+1
        				break
        # 				rty=True
		if  not exist or(count>0):
			new_data.append(data)

		# print(rty)
	writeCsv2UniqueSet(new_data,'UniqueSetByOdds/'+csv_title)
	# getUniqueByTime(new_data,csv_title)
	# print(new_data)

def teams_result(mylist,folder,csv_title):
	new_data=[]
	new_dict={}
	i=0
	col=['title','odd_id','odds_name','odds_value','team1_goal','team2_goal','team_time','result']
	
	# new_data.append(mylist[1])
	for data in mylist:
		count=0
		rty=False
		exist=False
		exist_c=0
		for n_d in new_data:
			if n_d['odd_id'] == data['odd_id']:
    				exist=True
    				break
		for n_d in new_data:
    			if data['odd_id']== n_d['odd_id'] and (data['odds_name'] !=n_d['odds_name']):
        				count=count+1
        				break
        # 				rty=True
		if  not exist or(count>0):
			new_data.append(data)

	writeCsv2UniqueSet(new_data,'1teams_result/'+folder+'/'+csv_title,col)


def get2UniqueRows(mylist,csv_title):
	new_data=[]
	new_dict={}
	i=0
	# new_data.append(mylist[1])
	for data in mylist:
		count=0
		rty=False
		exist=False
		exist_c=0
		for n_d in new_data:
			if n_d['odd_id'] == data['odd_id']:
    				exist=True
    				exist_c=exist_c+1

		for n_d in new_data:
    			if data['odd_id']== n_d['odd_id'] and (data['odds_value'] !=n_d['odds_value'] or data['team1_goal'] !=n_d['team1_goal'] or data['team2_goal'] !=n_d['team2_goal']):
        				count=count+1
	
        # 				rty=True
		if  not exist or(count>0 and exist_c==1):
			new_data.append(data)

		# print(rty)
	getUniqueByTime(new_data,csv_title)
	


def getUniqueByTime(mylist,csv_title):
	new_data=[]
	new_dict={}
	i=0
	# new_data.append(mylist[1])
	for data in mylist:
		count=0
		rty=False
		exist=False
		exist_c=0
		for n_d in new_data:
			if n_d['odd_id'] == data['odd_id']:
    				exist=True
    				exist_c=exist_c+1

		for n_d in new_data:
    			if data['odd_id']== n_d['odd_id'] and (data['team_time'] !=n_d['team_time']):
        				count=count+1
	
        # 				rty=True
		if  not exist:
			new_data.append(data)
	writeCsv2UniqueSet(new_data,'3UniqueDataByTime/'+csv_title)
	lowOdds(new_data,csv_title)



def lowOdds(mylist,csv_title):
	new_data=[]
	new_dict={}
	i=0
	# new_data.append(mylist[1])
	for data in mylist:
		count=0
		rty=False
		low_odd=False
		try:
			if  float(data['odds_value'])<2.0:
    				new_data.append(data)
		except:
			continue
	writeCsv2UniqueSet(new_data,'4LowOdds/'+csv_title)

# np.array_equal(np.array([1, 2]), np.array([1, 2]))

def getSimilarData(csv_titles):
	new_data=[]
	new_dict={}
	title_arr=[]
	time_arr=[]
	odd_id_arr=[]
	row_data=[]
	for i in range(99):
		for csv_title in csv_titles:
			mylist=csvToDictListLowOdds(csv_title)
			i=0
			for data in mylist:
				count=0
				rty=False
				exist=False
				exist_c=0
				title=data['title']
				team_time=data['team_time']
				str_id=data['odd_id']
				odds_value_=data['odds_value']
				mydict = [title,str_id,odds_value_,team_time]
				if mydict in new_data:
					break				
				new_data.append(mydict)
		print(new_data)
		if np.array_equal(new_data):
    			row_data.append(new_data[0])
	writeCsv2UniqueSet(row_data,'SimilarData/'+'csv_title.csv')

def getSimilarData2(csv_titles):
	myDict={}
	new_data=[]
	arr_len=[]
	array_n=0
	csv_files=[]
	mylist=[]
	for csv_title in csv_titles:
		try:
			# myDict=csvToDictListLowOdds(csv_title)#pd.read_csv('4LowOdds/'+csv_title,usecols=["title","team_time"])
			myDict=pd.read_csv('4LowOdds/'+csv_title,usecols=["title","odds_name","team_time"])
			new_data.append(np.array(myDict))
			arr_len.append(len(myDict))
			csv_files.append(csv_title)
		except:
			continue
	new_data.clear()	
	print(arr_len)
	print(csv_titles)
	highest_len_csv=list(np.array(arr_len)).index(np.array(arr_len).max())
	# try:
	myDict=np.array(pd.read_csv('4LowOdds/'+csv_files[highest_len_csv],usecols=["title","odds_name","team_time"]))
	for csv_dic in myDict:
		count=0
				
		for csv_title in csv_files:
			newDict=np.array(pd.read_csv('4LowOdds/'+csv_title,usecols=["title","odds_name","team_time"]))
			if csv_dic in newDict:

				count=count+1		
		if count>0:
			resultDict = {"title":csv_dic[0],"odds_name":csv_dic[1],"team_time":csv_dic[2],"apperance":count}
			mylist.append(resultDict)
	# except:
	# 	pass
	csv_columns = ['title','odds_name','team_time','apperance']
	try:
		with open('SimilarData/final_data.csv', 'w',encoding='utf-8',newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			i=0
			for data in mylist:
				print(data)
				writer.writerow(data)
		# data_collection.clear()
	except IOError as ex:
		print("I/O error"+str(ex)) 


def changeIp(controller):
	controller.signal(Signal.NEWNYM)
	socks.set_default_proxy(socks.SOCKS5,"localhost",9150)
	socks.socket=socks.socksocket