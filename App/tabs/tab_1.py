import dash
from dash import dcc
from dash import html
import dash_daq as daq

from main import *


tab_1_layout = html.Div(style={'backgroundColor': font_colors['background']}, children=[
    html.Div([

        html.Div([
            html.H1('Static sensors'),
            dcc.Checklist(
                className='sensor-checklist',
                id="city-checklist",
                options=[{'label': 'Sensor '+str(i), 'value': i}
                         for i in available_line],
                value=[1],
                labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-left': '20px',
                            'margin-top': '20px'},
                inputStyle={"margin-right": "10px"}
            ),
            dcc.Checklist(
                className='all-sensor-checklist',
                id="all-checklist",
                options=[{"label": "All sensors", "value": "All"}],
                value=[],
                labelStyle={"display": "inline-block",
                            'margin-left': '20px', 'margin-top': '20px'},
                inputStyle={"margin-right": "10px"}
            ),
        ], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin-top': '17px'}),

        html.Div([
            html.H1('St Himark'),
            html.Div(className='himark-image', id="image")
        ], style={'width': '35%', 'float': 'left', 'display': 'inline-block', 'margin-top': '20px', 'margin-left': '70px'}),

        html.Div([
            html.Div([
                dcc.Slider(
                    className='disabled-slider',
                    id='radar-slider',
                    min=0,
                    max=200,
                    value=0,
                    marks={
                        0: {'label': '0', 'style': {'color': 'black'}},
                        200: {'label': '200', 'style': {'color': 'black'}}
                    },
                    vertical=True,
                    verticalHeight=400,
                ),
            ], style={'margin-top': '30px'}),

        ], style={'width': '5%', 'float': 'middle', 'display': 'inline-block', 'margin-top': '20px', 'margin-left': '40px'}),

        html.Div([
            html.H1("Static sensor: value per time",
                    style={'margin-top': '17px'}),
            dcc.Graph(id='indicator-graphic'),
            html.H1("Mobile sensor: value per time",
                    style={'margin-top': '30px'}),
            dcc.Dropdown(
                id='mobile-sensor-select',
                className='dropdown-mobile',
                options=[{'label': i, 'value': i} for i in available_mobile],
                value=1,
                placeholder="Select a mobile sensor to see his behaviour",
            ),
            dcc.RadioItems(
                id='map_or_chart',
                options=[{'label': i, 'value': i}
                         for i in ['Line chart', 'Image']],
                value='Line chart',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
            html.Div(id="image2")
        ], style={'width': '35%', 'float': 'right', 'display': 'block', 'margin-right': '10px'}),
    ]),

    html.Div([
        html.Div(className='time-info', id='output-container-range-slider'),
        dcc.Slider(id="time-slider",
                   min=0,
                   max=len(hour_range)-1,
                   value=0,
                   step=1,
                   marks={str(i): str("April " + str(hour_range[i])[8:10] + ", " + str(hour_range[i])[11:-3])
                          for i in range(0, len(hour_range), 24)},
                   included=False),
    ], style={'width': '60%', 'float': 'left', 'margin-left': '50px', 'margin-top': '50px'}),

    html.Div([
        html.H1('Machine Learning Classification'),
    ], style={'wdith': '100%', 'display': 'block', 'margin-top': '400px'}),

    html.Div([
        html.H2('Dimension :'),
    ], style={'wdith': '100%', 'display': 'block', 'margin-top': '20px'}),

    html.Div([
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i}
                     for i in ["Timestamp", "Long", "Lat", "Value"]],
            value="Timestamp",
            placeholder="Axis x",
        ),
    ], style={'width': '15%', 'display': 'inline-block', 'margin-left': '30px'}),

    html.Div([
        dcc.Dropdown(
            id='yaxis-column',
            options=[{'label': i, 'value': i}
                     for i in ["Timestamp", "Long", "Lat", "Value"]],
            value="Value",
            placeholder="Axis y",
        ),
    ], style={'width': '15%', 'margin-left': '30px', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='zaxis-column',
            options=[{'label': i, 'value': i}
                     for i in ["Timestamp", "Long", "Lat", "Value"]],
            value=None,
            placeholder="Axis z",
        ),
    ], style={'width': '15%', 'display': 'inline-block', 'margin-left': '30px'}),

    html.Div([
        html.H2('Cluster :'),
    ], style={'wdith': '100%', 'display': 'block', 'margin-top': '20px'}),

    html.Div([
        dcc.RadioItems(
            id='ml_cluster',
            options=[{'label': i, 'value': i}
                     for i in range(3, 9)],
            value=3,
            labelStyle={'display': 'inline-block',
                        'marginTop': '5px', 'margin': '30px'}
        )
    ]),

    html.Div([
        dcc.Graph(id='linear-graphic', style={'wdith': '50%'},)
    ])
])