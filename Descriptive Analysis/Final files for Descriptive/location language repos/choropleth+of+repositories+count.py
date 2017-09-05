import plotly.plotly as py
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *

print (__version__) # requires version >= 1.9.0

import pandas as pd
import plotly
#plotly.tools.set_credentials_file(username='qwerty03', api_key='zalzm7bui9')# if wanted to use in an online mode.
plotly.offline.init_notebook_mode()



df = pd.read_csv('Location_Languages_repos.csv')

data = [ dict(
        type = 'choropleth',
        locations = df['iso3'],
        z = df['Repositories_Count'].sort_values(ascending=True),
        text = df['language'],
        colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
        autocolorscale = True,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = True,
            tickprefix = '',
            title = 'repositories count'),
      ) ]

layout = dict(
    title = 'Which countries has highest repositories count',
    geo = dict(
        showframe = False	,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
plot( fig, validate=False, filename='Location_Languages_repos(count).html' )# Prefix 'i'in plot function if wanted to use in jupyter notebook.


# In[ ]:




# In[ ]:



