import dash_core_components as dcc
import dash_html_components as html
import dash
from app import app
from app import server 
from layouts import explore, analyze, present
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/explore':
         return explore
    elif pathname == '/apps/analyze':
         return analyze
    elif pathname == '/apps/present':
         return present
    else:
        return explore # This is the "home page"

if __name__ == '__main__':
    app.run_server(debug=False)
