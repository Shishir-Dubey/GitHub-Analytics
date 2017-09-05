from GitHub_Extraction import *
def commits(rep_index):
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
                    token = "token1"
                    # print('SHishit')
                else:
                    token = "token2"
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
                            
def myscript(text):
    print (text)


a = commits(sys.argv[1])
print (a)


