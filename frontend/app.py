from dash import Dash, html, dash, Output, Input
import pandas as pd
import requests
from furl import furl


def get_recommendation_movies(movieId):
    req = requests.get('http://127.0.0.1:8000/get_recommendation/' + movieId)
    json_data = req.json()
    print(json_data)
    dataframe = pd.DataFrame(json_data)
    return generate_table(dataframe)


def get_user_recommendation(userId):
    req = requests.get('http://127.0.0.1:8000/user_recommendation/' + userId)
    json_data = req.json()
    print(json_data)
    dataframe = pd.DataFrame(json_data)
    return generate_table(dataframe)


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def make_layout():
    return html.Div([
        dash.dcc.Location(id="url", refresh=False),
        html.H4(children='Movie recommendation'),
        html.Div(id='content'),
        html.H4(children='SVD recommendation'),
        html.Div(id='content2'),
    ])


app = Dash(__name__)
app.layout = make_layout


@app.callback(Output('content', 'children'),
              [Input('url', 'href')])
def _content(href: str):
    f = furl(href)
    movieId = f.args['movieId']

    return get_recommendation_movies(movieId)


@app.callback(Output('content2', 'children'),
              [Input('url', 'href')])
def _content2(href: str):
    f = furl(href)
    userId = f.args['userId']

    return get_user_recommendation(userId)


if __name__ == '__main__':
    app.run_server(debug=True)
