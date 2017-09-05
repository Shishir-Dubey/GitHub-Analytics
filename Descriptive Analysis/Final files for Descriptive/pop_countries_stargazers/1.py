import plotly.plotly as py
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
#plotly.offline.init_notebook_mode()
print (__version__) # requires version >= 1.9.0

import pandas as pd
import plotly
#iplotly.tools.set_credentials_file(username='qwerty03', api_key='zalzm7bui9') 
plotly.offline.init_notebook_mode()

df = pd.read_csv('file1.csv')

df['text'] = df['city'] + '<br>Language-' +(df['language']).astype(str) + '<br>Stargazers-'+ (df['stargazers_count']).astype(str)+' numbers'
limits = [(0,2),(3,10),(11,20),(21,50),(50,300)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","green"]
Cnames = []
scale = 1

for i in range(len(limits)):

    lim = limits[i]

    df_sub = df[lim[0]:lim[1]]

    Cname = dict(

        type = 'scattergeo',

        locationmode = 'IS0-3',

        lon = df_sub['lon'],

        lat = df_sub['lat'],

        text = df_sub['text'],

        marker = dict(

            size = df_sub['stargazers_count']/scale,

            color = colors[i],

            line = dict(width=0.5, color='rgb(40,40,40)'),

            sizemode = 'area'

        ),

        name = '{0} - {1}'.format(lim[0],lim[1]) )

    Cnames.append(Cname)
    
    
    
layout = dict(
        title = 'Total number of stargazers',
        showlegend = True,
        geo = dict(
            scope='World',
            projection=dict( type='Distance Preserving' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=Cnames, layout=layout )
plot( fig, validate=False, filename='stargazers.html' )



