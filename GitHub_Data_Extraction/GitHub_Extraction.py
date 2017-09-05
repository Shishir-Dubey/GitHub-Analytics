
##############################--------Github Data Extraction ---------##################################### 
                 
######------Importing all the necessary Packages-----########

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
import subprocess
import os
import gc
from time import sleep
import codecs
import time
import requests
import getpass
import itertools
from urllib.request import urlopen, Request
from urllib.error import HTTPError , URLError
from GitHub_Extraction import *


i=0
n=0
j=0

###-----Function pp_json to beautify the Json response into a file.----##### 

def pp_json(json_thing,sort=True, indents=4):
       if type(json_thing) is str:
           file_name =json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
       else:
           file_name =json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
       return file_name

     

######-------Function to remove the constraints from the Json file and make it working Json -------#####
def cleaned_data(file_in,file_out):
        
       with open(file_in, 'r',encoding='utf-8') as infile,open(file_out, 'w') as outfile:
           data = infile.read()
       # data = data.replace("-", "")
           data = data.replace('][',',')
           data = data.replace('][][][',',')
           data = data.replace('][][][][',',')
           data = data.replace('][][',',')
           data = data.replace(']\n[',',')
           data = data.replace(',,',',')
           data = data.replace(',,,,',',')
           data = data.replace(',,,',',')
           data = data.replace(',,',',')
           #data = data.replace('][',',')
           # data = data.replace('][][',',')
           data =pp_json(data)
          
           outfile.write(data)
           #data = data.drop_duplicates()
       
       return (data)

#####-----Module for extracting Random GitHub Users Data--------#######

class user_data_extraction(): 


     def __init__(self,  users_range,ids_range,file_csv):

       # github_id=input("Enter Your Github's user_id: ") 
       # password=input("Enter Your Github's password ")
       
       github_id="user_id" 
       password="password"
       gh = login(github_id, password)
       user_info=[]
       try:
           for i in range(users_range):
               j=randrange(ids_range)
               #i =100*i
               j=j*100
               u_id= j
               access = gh.user_with_id(u_id)
               
               #print(j+1)
               #userid_index= index
               user_info.append({'user_id':access.id, 'name': access.name, 'login':access.login,
                                 'bio':access.bio,'created_at':access.created_at,'company':access.company,
                                'disk_usage':access.disk_usage,'following_count':access.following_count,
                                'followers_count':access.followers_count,'last_modified':access.last_modified,
                                'owned_private_repos':access.owned_private_repos,'public_repos_count':access.public_repos_count,
                                'location':access.location,'total_private_gists':access.total_private_gists,
                                'total_private_repos':access.total_private_repos,'repos_url':access.repos_url})
                 
               #print(user_info)
       except urllib.error.HTTPError as error:
           
           time.sleep(1600)
           
           #for i in range(userid_index,len(u_id)):
           user_info.append({'user_id':access.id, 'name': access.name, 'login':access.login,
                               'bio':access.bio,'created_at':access.created_at,'company':access.company,
                               'disk_usage':access.disk_usage,'following_count':access.following_count,
                               'followers_count':access.followers_count,'last_modified':access.last_modified,
                               'owned_private_repos':access.owned_private_repos,'public_repos_count':access.public_repos_count,
                               'location':access.location,'total_private_gists':access.total_private_gists,
                               'total_private_repos':access.total_private_repos,'repos_url':access.repos_url})
           print (error)
                   
       #           
      
       
       
       user_info=pd.DataFrame(user_info)
       user_info=user_info.drop_duplicates()
       user_info.to_csv(file_csv,index= None)
       self.data=pd.read_csv(file_csv)
       #return(user_info)
       #self.data=user_info 
       print (self.data)   

       for index,values in self.data.iterrows():
         print(index)




    ## def data(self):
      #  return self.data
        
           
                
#####-----Module for extracting GitHub Users repositories Data--------#######

class repositories_infos_extraction(user_data_extraction):
    
    """docstring for repositories_infos_extraction
    
        user_data_extraction = List of Users id to extract the information of respective users.
        file_name= "Name of the file in which repositories data has to be stored."
    
    """
    
    def __init__(self,user_data_extraction, file_name):
        u_id =list(user_data_extraction.data['user_id'])
        u_id= pd.DataFrame(u_id)
        #print("shishir"+str(u_id))
        user_id =0
        
        for index in range(user_id,len(u_id)):
            
            usr_id=index
            
            #print(usr_id)
            
            try:
                url = urlopen(user_data_extraction.data['repos_url'][index]).read().decode('utf8')
                #usr_id=index
                obj = json.loads(url)
                repo_list= (json.dumps(obj, indent=4, sort_keys=True))
                #repo_list=pd.read_json(repo_list)
                print(repo_list)
                
                with open('user_data_backup.json', "a") as myfile:
                        myfile.write(repo_list)
                        myfile.flush()
                        myfile.close()
                  
           
            except urllib.error.HTTPError as error:
                
                    time.sleep(3600)
               
                    try:
                        repo_infos(usr_id)
                    
                    except urllib.error.HTTPError as error:
                    
                        print(error)
        cleaned_data('file.json','file2.json')
        len(pd.read_json('file2.json'))
        repos=pd.read_json('file2.json')
        repos=repos.replace({'{/sha}':'' }, regex=True)
        len(repos)
        s= []
        # In[345]:
        repo_owner=pd.DataFrame(repos['owner'])
        for i in range(0,len(repo_owner)):
            s.append((repo_owner['owner'][i]))
        s= pd.DataFrame(s)
        len(s)
        repos['owners_id']=pd.Series(s['id'])
        repos.set_index('owners_id')
        #repos=repos.sort('owners_id')
        repos.to_csv('user\'s_repos_info.csv',index=False)



    
########- Module for extracting Github repositories commits Logs------#########

class commits_data_extraction():
    __slots__ = ['lenrepos', 'index','rep_index','file_name','i','n','url','obj','repos']    
    def __init__(self,rep_index):
        global i,n,j
        sys.stdout.flush()        
        lenrepos=len(pd.read_csv('users_repos_info.csv',index_col=None))
        rep_index=int(rep_index)
        for index in range(rep_index,lenrepos):
            # rep_ind=index
            if n==index:
                index=index+1
            repos=pd.read_csv('users_repos_info.csv',index_col=None)
            #print(rep_ind)

            #print(repos['id'][index],repos['owners_id'][index])
            #print(repos['commits_url'][index])
            try:

                if i%2 == 0:
                    token = "Token1"
                    # print('SHishir')
                else:
                    token = "Token2"
                    # print('GV')                
                url = repos['commits_url'][index]

                # print(token)    
                url = Request(url)
                url.add_header('Authorization', 'token %s' % token)
                url = urlopen(url).read().decode('utf8')
                #print(url.read())
                #url = urlopen(repos['commits_url'][index]).read().decode('utf8')
                #print(repos['commits_url'][index])
                obj = json.loads(url)
                commits_list= (json.dumps(obj, indent=4, sort_keys=True))
                #repo_list=pd.read_json(repo_list)
                #print(commits_list)

                with open("commits_{0}_{1}".format(repos['id'][index],repos['owners_id'][index]), "w") as myfile:
                    myfile.write(commits_list,)
                    myfile.flush()
                    myfile.close()
                del repos,myfile, url, obj, commits_list
                gc.collect()
                gc.get_objects()
                print(index)
                print(' Done')
                j=j+1
                if j==20 :
                    os.kill(os.getpid(), 9)
                                      

            except HTTPError as e:
                if(e.code == 403):
                    print("Rate Limit Exceeded, will continue after sometime.Waiting.....")
                    print(index)
                    n=index
                    time.sleep(600)
                    i =+1
                    print(e.code)
                    commits(index)
                elif(e.code == 409):
                    print("EXCEPTION OCCURED at "+ repos['commits_url'][index] + "Skipping to next id")
                    print(index)
                    index = index + 1
                    print(e.code)
                    commits(index) 
        # sys.exit()
        print("Finished with row {} ,GOOD BYE".format(index))
        print('')
        os.kill(os.getpid(), 9)                                       
                            
