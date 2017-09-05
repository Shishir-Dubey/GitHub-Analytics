import subprocess
import os
from time import sleep
import codecs
import time
import sys
import pandas as pd
from random import randrange
import io
import json
import urllib
import requests
import numpy as np
import github3
from github3 import login
from pandas.io.json import json_normalize
import itertools
from urllib.request import urlopen, Request
from urllib.error import HTTPError , URLError
from github3.exceptions import AuthenticationFailed
import getpass
import pymongo
from pymongo import MongoClient
import re

class User_Data_Extraction(): 
    
    """ This module is for the extraction of GitHub users in Random"""
    def __init__(self,users_range=0,random_fashion=True,
                 seq_start=0,start_range=0,end_range=None):
        #ids_range = kwargs.get('iruds_range',)
        #start_range = kwargs.get('start_range',0)
        #end_range = kwargs.get('end_range',None)      
        try:
            	self.github_id = input("Enter Your Github's user_id: ") 
            	self.password = getpass.getpass("Github's password:")
            	self.gh = login(self.github_id, self.password)


            	self.user_id_list=[]
            	self.connection = MongoClient()

            	print("Here is the list of Databases:\n",self.connection.database_names())

            	self.db_name=input("Please enter the existing database name or new database name to which the collections are to be stored :\t")
            	self.db_name=(self.db_name)
            	print(self.db_name)
            	
            	#self.db = self.connection[(db_name)]
            	self.drop_db=input("Do you want to drop the Database if exists: \t 1)Yes 2) No\n")

            	if(self.drop_db in ['YES','yes','Yes']):
            		self.connection.drop_database("{0}".format(self.db_name))
            		self.db = self.connection[(self.db_name)]

            	else:
            		print("Database using is %s" %self.db_name)
            		self.db = self.connection[(self.db_name)]


            	self.col_name=input("Please enter the collection name to which records are to be stored::\t")
            	self.col_name=self.col_name
            	print(self.col_name)


            	
            	self.drop_coll=input("Do you want to drop the collection if exists: \t 1)Yes 2) No\n") 
            	
            	if(self.drop_coll in ['YES','yes','Yes']):
            		self.db[self.col_name].drop()
            		self.collection = self.db[self.col_name]

            	else:
            		self.collection = self.db[self.col_name]
            		#self.collection = self.collection({'_id':False})
            	self.counter = 0
            	self.counter_range=users_range
            
            	#counter_range=users_range-counter
            	#print(counter_range)
            	for nb_users in range(users_range):
                    while(self.counter != users_range):
                        
                        if (random_fashion == True):
                            user_id = randrange(start_range,end_range)
                            if(user_id in self.user_id_list):
                                user_id = randrange(start_range,end_range)
                            
                        else:
                            user_id=seq_start
                            seq_start+=1
                            if user_id in self.user_id_list:
                                user_id=+1
                        print(user_id) 

                        self.push_count=0
                        self.pull_count=0
                        self.issues_count=0
                        self.issue_comments_count=0
                        self.watchers_count=0
                        self.forks_count=0
                        self.creation_count=0
                        self.forks_count=0
                        self.creation_count=0
                        self.commit_comments_count=0
                        self.downloads_count=0
                        self.repository_changes_count=0
                        self.user_id_list.append(user_id)
                        self.access = self.gh.user_with_id(user_id)
                        self.access_id_null=False
                        
                        try:
                            self.access_id_null=self.access.is_null()
                        except (AttributeError) as e :
                            print('Not_null_Moving to next Id')
                            pass
                        #print(self.access)
                                                   
                        while(self.access_id_null !=False):
                            print('found Null...again extracting new id')
                            if (random_fashion == True):
                                user_id = randrange(start_range,end_range)
                                if(user_id in self.user_id_list):
                                    user_id = randrange(start_range,end_range)
                            else:
                                user_id=seq_start
                                seq_start+=1
                                print(seq_start)
                                if user_id in self.user_id_list:
                                    user_id=+1
                            self.user_id_list.append(user_id)    
                            self.access = self.gh.user_with_id(user_id)
                            try:
                                self.access_id_null=self.access.is_null()
                            except (AttributeError) as e :
                                self.access_id_null=False
                            
                        self.ctime = self.access.created_at.ctime().split()
                        self.last_modified=self.access.last_modified.split()
                        self.last_mod_time_split=(self.last_modified[4])
                        #print(self.last_mod_time_split)
                        self.last_mod_time_split=re.split(':',(self.last_mod_time_split))
                        #print(self.ctime)
                        #print(list(self.access.events()))
                        #print(self.last_mod_time_split)
                        self.events = (list(self.access.events()))
                        #print("list:",self.events)
                        self.events= pd.DataFrame(self.events)
                        #print(self.events)
                        self.events=self.events.astype(str)
                        #print(self.events)
                        
                        try:
                            for i in (self.events[0]):
                                if (i == '<Event [Push]>'):
                                    self.push_count+=1
                                elif i== '<Event [PullRequest]>':
                                    self.pull_count+=1
                                elif i =='<Event [Issues]>':
                                    self.issues_count+=1
                                elif i=='<Event [IssueComment]>':
                                    self.issue_comments_count+=1
                                elif i=='<Event [Watch]>':
                                    self.watchers_count+=1
                                elif i=='<Event [Fork]>':
                                    self.forks_count+=1
                                elif i=='<Event [Create]>':
                                    self.creation_count+=1
                                elif i=='<Event [CommitCommentEvent]>':
                                    self.commit_comments_count+=1
                                elif i=='<Event [DownloadEvent]>':
                                    self.downloads_count+=1	
                                elif i=='<Event [RepositoryEvent]>':
                                    self.repository_changes_count+=1
                        except KeyError:
                            pass
                                
                        print({'push_count':self.push_count,'pull_count':self.pull_count,'issues_count':self.issues_count,
                        		  'issue_comment_count':self.issue_comments_count,'watchers_count':self.watchers_count,
                        		  'forks_count':self.forks_count,'creation_count':self.creation_count,'commits_count': self.commit_comments_count,
                                  'downloads_count':self.downloads_count,'repository_changes_count':self.repository_changes_count})
                        

                        print(self.last_modified[5])
                        #print(j+1)
                        #userid_index= indexif
                        user_info = {
                                    
                                    'user_id':self.access.id, 'name': self.access.name, 'login':self.access.login,'bio':self.access.bio,
                                    'created_at':self.access.created_at,'created_at_weekday':self.ctime[0],'created_at_day':self.ctime[2],
                                    'created_at_month':self.ctime[1],'created_at_year':self.ctime[4],'created_at_hour':self.access.created_at.hour,
                                    'created_at_minutes':self.access.created_at.minute,'created_at_seconds':self.access.created_at.second,
                                    'creation_tz':self.access.created_at.tzname(),'creation_time_iso':self.access.created_at.isoformat(),
                                    'created_at_time':self.ctime[3],'company':self.access.company,'disk_usage':self.access.disk_usage,
                                    'following_count':self.access.following_count,'followers_count':self.access.followers_count,
                                    'last_modified':self.access.last_modified,'last_modified_at_weekday':self.last_modified[0],
                                    'last_modified_at_day':self.last_modified[1],'last_modified_at_month':self.last_modified[2],
                                    'last_modified_at_year':self.last_modified[3],'last_modified_at_hour':self.last_mod_time_split[0],
                                    'last_modified_at_minutes':self.last_mod_time_split[1],'last_modified_at_seconds':self.last_mod_time_split[2],
                                    'last_modified_time':self.last_modified[4],'last_modified_tz':self.last_modified[5],
                                    'owned_private_repos':self.access.owned_private_repos,'public_repos_count':self.access.public_repos_count,
                                    'location':self.access.location,'public_gists':self.access.public_gists,'total_private_gists':self.access.total_private_gists,
                                    'total_private_repos':self.access.total_private_repos,'push_count':self.push_count,'pull_count':self.pull_count,
                                    'watchers_count':self.watchers_count,'forks_count':self.forks_count,'creation_count':self.creation_count,
                                    'issues_count':self.issues_count,'commits_count': self.commit_comments_count,'downloads_count':self.downloads_count,
                                    'repository_changes_count':self.repository_changes_count,'issue_comments_count':self.issue_comments_count,
                                    'repos_url':self.access.repos_url,'etag':self.access.etag,'hireable':self.access.hireable }
                        try:
                                    
                            self.collection.insert_one(user_info)
                            self.counter_range=users_range-self.counter
                            #print(self.counter_range)
                            self.counter+= 1
                            #print(self.counter_range)
                        except pymongo.errors.InvalidDocument as error:
                            self.counter-=1
                            #print(self.counter_range,error)
                            continue
                    
                    #print(user_info)
                    
        except (HTTPError,AuthenticationFailed,github3.exceptions.ForbiddenError) as error:
        	print("No. of users_information collected:",self.counter)
        	self.collected=users_range-self.counter
        	print("No of users_remaining:",self.collected)
        	if(error.code == 403):
        		print (error)
        		print("%s:Rate Limit Exceeded, will continue after sometime.Waiting.....",error)
        		time.sleep(60)
        		User_Data_Extraction(users_range=self.counter_range,seq_start=seq_start,
                                 start_range=start_range,end_range=end_range,
                                 random_fashion=True)
        	elif(error.code == 409):
        		print(error)

        	elif(error.code == 401):
        		print(error,"\n \n Please enter credentials again to coninue..\n\n")
        		User_Data_Extraction(users_range=self.counter_range,seq_start=seq_start,
                                 start_range=start_range,end_range=end_range,
                                 random_fashion=True)

        print (self.counter)

        self.collection.ensure_index(input("Index field for the collection:"),unique=True)
        print("Data Extracted successfully.")
    
        