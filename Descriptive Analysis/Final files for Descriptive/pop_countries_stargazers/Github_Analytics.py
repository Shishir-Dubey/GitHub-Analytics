
##############################---------Forecasting ---------##################################### 
                  ###################---Github---#####################

class github_data:
    """docstring for ClassName"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
        

# ### ---------Retrieving Users information using pagination in json format ----------


   def user_list( users_range,ids_range,file_csv):
       
       github_id=input("Enter Your Github's user_id: ") 
       password=input("Enter Your Github's password ")
       
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
           
       return(user_info)
       
                
   
   # ### Replacing unused brackets from json and prettify it to make it usable......
   
   def pp_json(json_thing,sort=True, indents=4):
       if type(json_thing) is str:
           file_name =json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
       else:
           file_name =json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
       return file_name
   
   
   
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
           data=pp_json(data)
          
   
   
   
           outfile.write(data)
           #data = data.drop_duplicates()
       
       return (data)
   
   
   
   
   def repo_infos(user_id):
       for index in range(user_id,len(u_id)):
           usr_id=index
           print(usr_id)
           try:
               url = urlopen(data['repos_url'][index]).read().decode('utf8')
               #usr_id=index
               obj = json.loads(url)
               repo_list= (json.dumps(obj, indent=4, sort_keys=True))
               #repo_list=pd.read_json(repo_list)
               print(repo_list)           
               
               with open("repo.json", "a") as myfile:
                   myfile.write(repo_list)
           
           except urllib.error.HTTPError as error:
               
               time.sleep(3600)
               
               try:
                   repo_infos(usr_id)
                   
               except urllib.error.HTTPError as error:
                   print(error)
                   
   
  
  