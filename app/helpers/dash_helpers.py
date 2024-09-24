# Data Visualisation Packages
# Import Dash HTML and core components
# Experimental example for Dash + Matplotlib
from dash import Dash, html, dcc
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def create_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dash/')
    
    img = create_line_chart_matplotlib()

    dash_app.layout = html.Div([
        html.Link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/5.2.3/css/bootstrap.min.css'),
        
        html.Div(className='container mt-4', children=[
            html.H1('Hello Dash', className='text-center mb-4'),

            # Dash Line Chart
            html.Div(className='row mb-4', children=[
                html.Div(className='col', children=[
                    html.H2('Line Chart using Dash', className='text-center'),
                    dcc.Graph(
                        id='dash-line-chart',
                        figure={
                            'data': [
                                {'x': np.linspace(0, 10, 100), 'y': np.sin(np.linspace(0, 10, 100)), 'type': 'line', 'name': 'Sine'},
                                {'x': np.linspace(0, 10, 100), 'y': np.cos(np.linspace(0, 10, 100)), 'type': 'line', 'name': 'Cosine'}
                            ],
                            'layout': {
                                'title': 'Line Chart with Dash',
                                'xaxis': {'title': 'X-axis'},
                                'yaxis': {'title': 'Y-axis'},
                            }
                        }
                    )
                ])
            ]),
            
            # Bootstrap JS
            html.Script(src='https://code.jquery.com/jquery-3.6.0.min.js'),
            html.Script(src='https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js'),
            html.Script(src='https://stackpath.bootstrapcdn.com/bootstrap/5.2.3/js/bootstrap.min.js'),
        ])
    ])

    return dash_app

def create_dash_app_2(flask_app):
    dash_app_2 = Dash(__name__, server=flask_app, url_base_pathname='/dash2/')

    img = create_line_chart_matplotlib()

    dash_app_2.layout = html.Div([
        html.Link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/5.2.3/css/bootstrap.min.css'),
        
        html.Div(className='container mt-4', children=[
            html.H1('Hello Dash with Matplotlib', className='text-center mb-4'),

            # Matplotlib Line Chart
            html.Div(className='row', children=[
                html.Div(className='col', children=[
                    html.H2('Line Chart using Matplotlib', className='text-center'),
                    html.Img(src=img, style={'width': '100%', 'height': 'auto'})
                ])
            ]),

            # Bootstrap JS
            html.Script(src='https://code.jquery.com/jquery-3.6.0.min.js'),
            html.Script(src='https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js'),
            html.Script(src='https://stackpath.bootstrapcdn.com/bootstrap/5.2.3/js/bootstrap.min.js'),
        ])
    ])

    return dash_app_2

def create_line_chart_matplotlib():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure()
    plt.plot(x, y, label='Sine Wave', color='blue')
    plt.title('Sine Wave Line Chart')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"
