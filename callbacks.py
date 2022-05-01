import plotly.graph_objs as go
import pandas as pd
from app import app
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash
import scipy.stats as stats
import researchpy as rp
import random
from sklearn.linear_model import LinearRegression
import pygsheets

#authorization
gc = pygsheets.authorize(service_file='clear-faculty-348813-1edaa94084f9.json')
## IMPORT  DATA


####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : '#18191b',
    'background-color' : '#18191b',
    'box-shadow' : '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top' : '10px'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : '#18191b',
    'background-color' : '#18191b',
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : '#18191b',
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

corporate_font_family = 'Dosis'

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

####################################################################################################

####################################################################################################
# 000 - DEFINE ADDITIONAL FUNCTIONS
####################################################################################################
def group_wavg(df, gr_by_cols, weight, value):
    """This function returns a df grouped by the gr_by_cols and calculate the weighted avg based
    on the entries in the weight and value lists"""
    # Calculate weight * value columns
    wcols = []
    cols = []
    for i in range(0,len(value),1):
        wcol = "w"+value[i]
        wcols.append(wcol)
        df[wcol] = df[weight[i]] * df[value[i]]
    # Group by summing the wcols and weight columns
    cols = weight
    for i in wcols:
        cols.append(i)
    df1 = df.groupby(gr_by_cols)[cols].agg('sum')
    df1.reset_index(inplace=True)
    # Divide wcols by weight and remove columns
    for i in range(0,len(value),1):
        df1[value[i]] = df1[wcols[i]] / df1[weight[i]]
        df1.drop(wcols[i], axis='columns', inplace=True)

    return df1

### DATA ####


# EXPLORE PAGE
####################################################################################################
####################################################################################################
####################################################################################################

@app.callback(
    Output("eplot", "figure"),
    Input('interval-component', 'n_intervals')
)

def display_graph(n):

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Focus2')
    #select the first sheet 
    wks = sh[0]
    data1 = wks.get_as_df()
    data1 = pd.DataFrame(data1)
    data1.columns =['Time', 'Values']

    #data1 = pd.read_csv("flatengagement_cal1.csv")

    # time_start = 50
    # data_array_1 = np.array(data1)

    Values = data1["Values"]
    Time = data1["Time"]

    #myline = np.linspace(2.5, 200, 100)
    fig = px.scatter(x=Time, y=Values, title='Engagement', trendline="lowess", trendline_options=dict(frac=0.1), trendline_color_override="#ec8785")
    fig.update_traces(mode = 'lines')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark", xaxis_title="Time",yaxis_title="Engagement Score",)
    fig.update_traces(opacity=0.5)
    return fig

    # model = LinearRegression()
    # model.fit(Time, Values.tip)

    # x_range = np.linspace(Time.min(), Time.max(), 100)
    # y_range = model.predict(x_range.reshape(-1, 1))

    # mymodel = np.poly1d(np.polyfit(Time,Values,5))
    # myline = np.linspace(2.5, 200, 100)

    # fig = px.line(x=Time, y=Values, title='Engagement')
    # fig2 = px.line(myline, mymodel)
    # fig3 = go.Figure(data=fig.data + fig2.data)
    # fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
    # fig3.update_traces(opacity=0.6)

    #return fig3

# def display_graph(xaxis_column_name, yaxis_column_name):
#     fig_go = go.Figure()
#     fig_go.add_trace(go.Histogram(x=dataset[xaxis_column_name], name=xaxis_column_name))
#     fig_go.add_trace(go.Histogram(x=dataset[yaxis_column_name], name=yaxis_column_name))
#     # Overlay both histograms
#     fig_go.update_layout(barmode='overlay', paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
#     # Reduce opacity to see both histograms
#     fig_go.update_traces(opacity=0.6)
#     return fig_go

# PRESENT PAGE
####################################################################################################
####################################################################################################
####################################################################################################

# ### Accidents over time
# @app.callback(
#     Output(component_id='areaplot', component_property='figure'),
#     [Input(component_id='severityChecklist', component_property='value'),
#         Input (component_id='country', component_property='value')
#     ])

# def updateAreaPlot(severity, country):
#     if country == 'United Kingdom (UK)':
#         df = pd.read_csv('data/GBseverity.csv')
#     elif country == 'England':
#         data = pd.read_csv('data/wide_bycountry.csv')
#         df = data.loc[data['Country'] == 'England']
#     elif country == 'Scotland':
#         data = pd.read_csv('data/wide_bycountry.csv')
#         df = data.loc[data['Country'] == 'Scotland']
#     else:
#         data = pd.read_csv('data/wide_bycountry.csv')
#         df = data.loc[data['Country'] == 'Wales']

#     severity = list(severity)
#     cols = [col for col in df.columns if col in severity]
#     cols.append('Accident year')
#     filtered_df = df[cols]
#     print(filtered_df)
#     name = "Accidents by severity in " + str(country)
#     fig = px.area(filtered_df, x=filtered_df['Accident year'], y=filtered_df.columns, color_discrete_map={
#                     "Fatal": 'rgb(178,34,34)',
#                     "Serious": 'rgb(249,139,96)',
#                     "Slight": 'rgb(255,224,132)'},
#                     title = name)
#     fig.update_layout(template="plotly_dark",
#     paper_bgcolor='rgba(0,0,0,0)',
#     plot_bgcolor='rgba(0,0,0,0)',
#     xaxis_title="Year",
#     yaxis_title="Amount of accidents",)
#     fig.update_xaxes(rangeslider_visible=True)
#     fig.update_layout(yaxis_range=[0,210000])
        
#     return fig


# @app.callback(
# Output(component_id='severitypie', component_property='figure'),
# [Input (component_id='country', component_property='value')
# ])

# def severitypie(country):
#     if country == 'England':
#         data = pd.read_csv('data/wide_bycountry.csv')
#         df = data.loc[data['Country'] == 'England']
#     elif country == 'Scotland':
#         data = pd.read_csv('data/wide_bycountry.csv')
#         df = data.loc[data['Country'] == 'Scotland']
#     else:
#         data = pd.read_csv('data/wide_bycountry.csv')
#         df = data.loc[data['Country'] == 'Wales']

#     total_fatal = df['Fatal'].sum()
#     total_serious= df['Serious'].sum()
#     total_slight= df['Slight'].sum()

#     labels = ['Fatal','Serious','Slight']
#     values = [total_fatal, total_serious, total_slight]
#     colors = ['rgba(178,34,34,0.9)', 'rgba(249,139,96,0.8)', 'rgba(255,224,132,0.7)']

#     # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     fig.update_traces(textposition='inside', textinfo='percent+label',  marker=dict(colors=colors))


#     fig.update_layout(
#     paper_bgcolor='rgba(0,0,0,0)',
#     plot_bgcolor='rgba(0,0,0,0)',
#     template="plotly_dark",
#     showlegend=False,
#     margin=dict(l=0, r=0, t=0, b=0))
#     return fig

# @app.callback(
# Output(component_id='countrypie', component_property='figure'),
# [Input(component_id='severityChecklist', component_property='value')])

# def countrypie(severity):
#     data = pd.read_csv('data/wide_bycountry.csv')
#     England = data.loc[data['Country'] == 'England']
#     Wales = data.loc[data['Country'] == 'Wales']
#     Scotland = data.loc[data['Country'] == 'Scotland']

#     total_England = 0
#     total_Scotland = 0
#     total_Wales = 0

#     for value in list(severity):
#         total_England += England[value].sum()
#         total_Scotland += Scotland[value].sum()
#         total_Wales += Wales[value].sum()

#     labels = ['England','Scotland','Wales']
#     values = [total_England, total_Scotland, total_Wales]
#     colors = ['#F1F1F1', '#92a8d1', '#c94c4c']


#     # Use `hole` to create a donut-like pie chart
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#     fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(colors=colors))

#     fig.update_layout(
#     paper_bgcolor='rgba(0,0,0,0)',
#     plot_bgcolor='rgba(0,0,0,0)',
#     template="plotly_dark",
#     showlegend=False,
#     margin=dict(l=0, r=0, t=0, b=0))

#     return fig



#### ANALYZE PAGE
