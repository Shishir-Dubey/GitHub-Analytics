####-Commit logs Extraction if commits stucks on any repository id" 

from GitHub_Extraction import *

#repos=pd.read_csv('users_repos_info.csv',index_col=None)
n=0

len=len(pd.read_csv('users_repos_info.csv',index_col=None))
for j in range(n+5,len,5):
		i=j-5
		print(i)
		print(j)
		d=commits_data_extraction(i,'users_repos_info.csv')
		del d
		gc.get_objects()
		gc.collect()

# commits_data_extraction(n,'users_repos_info.csv')
