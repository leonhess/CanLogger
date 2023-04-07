from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('C:/Users/leonh/Documents/GitHub/CanLogger/python/files/log_1.txt', sep=";")
#,sep=";",index_col="TIME"

print(df)
app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.ID.unique(), '628', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.ID==value]
    return px.line(dff, x='TIME', y='DLC')

if __name__ == '__main__':
    app.run_server(debug=True)

