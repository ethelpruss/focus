import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash
from datetime import datetime as dt
from app import app
import dash_bootstrap_components as dbc



####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################
## DATA



#######################  Css formatting
corporate_colors = {
    'dark-blue-grey' : '#394867',
    'medium-blue-grey' : '#394867',
    'superdark-green' : '#14274E',
    'dark-green' : '#394867',
    'medium-green' : '#394867',
    'light-green' : '#F1F6F9',
    'pink-red' : '#f1d18a',
    'dark-pink-red' : '#f1d18a',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : '#F1F6F9'
}

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['superdark-green'],
    'background-color' : corporate_colors['superdark-green'],
    'padding-top' : '10px'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    }

navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
    }

recapdiv = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'rgb(251, 251, 252, 0.1)',
    'margin-left' : '15px',
    'margin-right' : '15px',
    'margin-top' : '15px',
    'margin-bottom' : '15px',
    'padding-top' : '5px',
    'padding-bottom' : '5px',
    'background-color' : 'rgb(251, 251, 252, 0.1)'
    }

recapdiv_text = {
    'text-align' : 'left',
    'font-weight' : '350',
    'color' : corporate_colors['white'],
    'font-size' : '1.5rem',
    'letter-spacing' : '0.04em'
    }

####################### Corporate chart formatting

corporate_title = {
    'font' : {
        'size' : 16,
        'color' : corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid' : False,
    'linecolor' : corporate_colors['light-grey'],
    'color' : corporate_colors['light-grey'],
    'tickangle' : 315,
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_yaxis = {
    'showgrid' : True,
    'color' : corporate_colors['light-grey'],
    'gridwidth' : 0.5,
    'gridcolor' : corporate_colors['dark-green'],
    'linecolor' : corporate_colors['light-grey'],
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Century Gothic'

corporate_legend = {
    'orientation' : 'h',
    'yanchor' : 'bottom',
    'y' : 1.01,
    'xanchor' : 'right',
    'x' : 1.05,
	'font' : {'size' : 9, 'color' : corporate_colors['light-grey']}
} # Legend will be on the top right, above the graph, horizontally

corporate_margins = {'l' : 5, 'r' : 5, 't' : 45, 'b' : 15}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font = {'family' : corporate_font_family},
    title = corporate_title,
    title_x = 0.5, # Align chart title to center
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis = corporate_xaxis,
    yaxis = corporate_yaxis,
    height = 270,
    legend = corporate_legend,
    margin = corporate_margins
    )


#####################
# Header with logo
def get_header():

    header = html.Div([

        html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.Img(
            src = app.get_asset_url('banner.png'),
            height = '300 px',
            width = '1000 px')
            ],
            className='col-8',
            style = {'padding-top' : '1%'}
        ),

        html.Div([

            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '1%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' :'#18191b'}
        )

    return header

#####################
# Nav bar
def get_navbar(p = 'explore'):

    navbar_explore = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Explore',
                        style = navbarcurrentpage),
                href='/apps/explore'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Analyze'),
                href='/apps/analyze'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Present'),
                href='/apps/present'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : '#18191b'}
    )

    navbar_analyze = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Explore'),
                href='/apps/explore'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Analyze',
                        style = navbarcurrentpage),
                href='/apps/analyze'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Present'),
                href='/apps/present'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : corporate_colors['dark-green']}
    )

    navbar_present = html.Div([

        html.Div([], className = 'col-3'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Explore'),
                href='/apps/explore'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Analyze'),
                href='/apps/analyze'
                )
        ],
        className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children = 'Present',
                        style = navbarcurrentpage),
                href='/apps/present'
                )
        ],
        className='col-2'),

        html.Div([], className = 'col-3')

    ],
    className = 'row',
    style = {'background-color' : '#18191b'}
    )

    if p == 'explore':
        return navbar_explore
    elif p == 'analyze':
        return navbar_analyze
    else:
        return navbar_present

#####################
# Empty row

def get_emptyrow(h='45px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow


####################################################################################################
# 003 - PRESENT
####################################################################################################
present = html.Div()


####################################################################################################
# 001 - EXPLORE
####################################################################################################
# violin_input = html.Div([
#     dbc.Label('Select the visualization'),
#     dbc.RadioItems(
#     id='dist-marginal',
#     options=[{'label': x, 'value': x}
#             for x in ['boxplot', 'violin plot']],
#     value='violin plot')
# ])

start = html.Div([
        dbc.Switch(
            id="switch",
            label="Toggle to start",
            value=False,
            )  
    ]
)

timer =    html.Div([ dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0)])

explore = html.Div(
    [   
        get_header(),
        get_navbar('explore'),
        #First row (empty)
        dbc.Container([
        #Second row (options)
        dbc.Row([
                timer
        ]),
        dbc.Row(html.H4("Track your engagement", style={'paddingTop': '20px', 'paddingBottom': '40px'})),
        dbc.Row([
            dbc.Col(),
            dbc.Col(),
        ]),

        dbc.Row([
            #First column
            dbc.Col(html.Div( dcc.Graph(id="eplot"))),
        ]),

        ], className = 'container-fluid rounded p-3 my-3 bg-secondary text-white'),
    ])

####################################################################################################
# 002 - ANALYZE
####################################################################################################

#### INPUT

#### FIRST ROW, FIRST COLUMN ############

analyze = html.Div()
