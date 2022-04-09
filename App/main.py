from datetime import time
from re import X
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from tabs import tab_1
from common import *
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from sklearn.cluster import KMeans


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True


app.layout = html.Div([
    dcc.Tabs(id="main-tab"),
    html.Div(id='tabs-content')
])


# Main callback
@app.callback(Output('tabs-content', 'children'),
              [Input('main-tab', 'value')])
def render_content(tab):
    return tab_1.tab_1_layout


# Tab callbacks

# Main St Himark image
@app.callback(
    Output("image", "children"),
    Input("city-checklist", "value"),
    Input("radar-slider", "value"),
    Input("time-slider", "value"))
def update_map(cities_selected, radar_value, time_value):
    fig = px.imshow(map_black, color_continuous_scale="gray")
    for idx, line in enumerate(cities_selected):
        a = ssl[ssl['Sensor-id'] == line]
        x, y = resize(a.Long, a.Lat)
        time_df = df3[df3['Timestamp'] == hour_range[time_value]]
        time_df.dropna(subset=["Long"], inplace=True)
        # Show mobile sensors positions
        for index, row in time_df.iterrows():
            a, b = resize(row.Long, row.Lat)
            if point_in_circle(a, b, x, y, radar_value):
                fig.add_shape(
                    type='circle',
                    x0=int(a-4), x1=int(a+4), y0=int(b+4), y1=int(b-4),
                    xref='x', yref='y',
                    line_color=radar_color(row.Value, 60))
                fig.add_trace(go.Scatter(
                    x=[a, a],
                    y=[b-15, b-15],
                    hovertemplate='<extra></extra>',
                    text=[row['Sensor-id']],
                    mode="text",
                    hoverinfo='all',
                    showlegend=False,
                ))
        fig.add_shape(type="circle",
                      xref="x", yref="y",
                      fillcolor="#edf2f4",
                      x0=int(x-radar_value), x1=int(x+radar_value), y0=int(y+radar_value), y1=int(y-radar_value),
                      line_color='white',
                      opacity=0.4)
    # Add static radar position
    for idx, line in enumerate(cities_selected):
        a = ssl[ssl['Sensor-id'] == line]
        x, y = resize(a.Long, a.Lat)
        fig.add_shape(
            type='rect',
            x0=int(x-5), x1=int(x+5), y0=int(y+5), y1=int(y-5),
            xref='x', yref='y',
            line_color=colors[idx],
            fillcolor=colors[idx])
    fig.update_xaxes(visible=False, showticklabels=False, side='top')
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_layout(coloraxis_showscale=False, transition_duration=500,
                      paper_bgcolor=font_colors['background'], plot_bgcolor=font_colors['background'],
                      xaxis={
                          'showgrid': False
                      },
                      yaxis={
                          'showgrid': False
                      },
                      margin=dict(t=0, b=0, l=0, r=0),
                      hovermode=False)
    for i in range(len(radar_colors)):
        fig.add_trace(go.Scatter(
            x=[0, 300],
            y=[557, 557],
            text=["0", "> 200"],
            mode="text",
            showlegend=False,
        )),
        fig.add_shape(type='rect',
                      xref="x",
                      yref="y",
                      x0=i*25,
                      x1=25+i*25,
                      y0=587,
                      y1=597,
                      line=dict(
                          color=radar_colors[i],
                          width=3,
                      ),
                      fillcolor=radar_colors[i])
    return dcc.Graph(figure=fig)


# Line graph with static sensors value trought time
@app.callback(
    Output("city-checklist", "value"),
    Output("all-checklist", "value"),
    Output('indicator-graphic', 'figure'),
    Input("city-checklist", "value"),
    Input("all-checklist", "value"))
def update_line_graph(cities_selected, all_selected):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "city-checklist" or input_id == "slider":
        all_selected = ["All"] if set(
            cities_selected) == set(available_line) else []
    elif input_id == "all-checklist":
        cities_selected = available_line if all_selected else []
    new_df = pd.DataFrame(columns=['Timestamp', 'Sensor-id', 'Value'])
    for line in cities_selected:
        new_df = new_df.append(df[df['Sensor-id'] == line])
    fig = px.line(new_df, x="Timestamp", y="Value",
                  color='Sensor-id', color_discrete_sequence=colors, width=425, height=230)
    fig.update_xaxes(visible=True, showticklabels=True)
    fig.update_yaxes(visible=True, showticklabels=True)
    fig.update_layout(yaxis_range=[min(df.Value)-5, max(df.Value)+5],
                      paper_bgcolor=font_colors['background'], plot_bgcolor=font_colors['background'],
                      xaxis={
        'showgrid': False
    },
        yaxis={
        'showgrid': True
    }),
    fig.update_layout(transition_duration=500, margin=dict(t=0, b=0, l=0, r=0))
    fig.update_layout(hovermode="x", hoverlabel_align='right')
    return cities_selected, all_selected, fig


# Line chart or St Himark for mobile sensor data
@app.callback(
    Output("image2", "children"),
    Input("mobile-sensor-select", "value"),
    Input("map_or_chart", "value"))
def update_map2(sensor_id, map_line):
    mobile_data = df3[df3['Sensor-id'] == sensor_id]
    mobile_data.dropna(subset=["Long"], inplace=True)
    # Show line chart with mobile sensor value
    if map_line == 'Line chart':
        fig = px.line(mobile_data, x="Timestamp", y="Value",
                      color='Sensor-id', width=425, height=230)
        fig.update_xaxes(visible=True, showticklabels=True)
        fig.update_yaxes(visible=True, showticklabels=True)
        fig.update_layout(
            paper_bgcolor=font_colors['background'], plot_bgcolor=font_colors['background'],
            xaxis={
                'showgrid': False
            },
            yaxis={
                'showgrid': True
            }),
        fig.update_layout(transition_duration=500,
                          margin=dict(t=0, b=0, l=0, r=0))
        fig.update_layout(hovermode="x", hoverlabel_align='right')
    else:
        fig = px.imshow(map_white, color_continuous_scale="gray")
        if sensor_id:
            for index, row in mobile_data.iterrows():
                x, y = resize(row.Long, row.Lat)
                fig.add_shape(
                    type='circle',
                    x0=int(x-4), x1=int(x+4), y0=int(y+4), y1=int(y-4),
                    xref='x', yref='y',
                    line_color=radar_color(row.Value, 60))
        fig.update_xaxes(visible=False, showticklabels=False, side='top')
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_layout(coloraxis_showscale=False, transition_duration=500,
                          paper_bgcolor=font_colors['background'], plot_bgcolor=font_colors['background'],
                          xaxis={
                              'showgrid': False
                          },
                          yaxis={
                              'showgrid': False
                          },
                          margin=dict(t=0, b=0, l=0, r=0))
        fig.update_layout(width=335, height=290, hovermode=False)
    return dcc.Graph(figure=fig)


# Time label on time slider
@app.callback(
    Output('output-container-range-slider', 'children'),
    Input('time-slider', 'value'))
def update_output(value):
    date = str(hour_range[value])
    return "April ", date[8:10], ", ", date[11:-3]


# Machine learning cluster graphic
@app.callback(
    Output('linear-graphic', "figure"),
    Input("xaxis-column", "value"),
    Input("yaxis-column", "value"),
    Input("zaxis-column", "value"),
    Input("ml_cluster", "value"))
def update_linear_graph(xaxis, yaxis, zaxis, cluster):
    new_df = df3.copy()
    new_df = new_df.drop(['Sensor-id'], axis=1)
    new_df = new_df.drop(['User-id'], axis=1)
    new_df = new_df.dropna()
    X = new_df.iloc[:, 1:4].values
    kmeans = KMeans(n_clusters=cluster, init="k-means++",
                    max_iter=500, n_init=10, random_state=123)
    identified_clusters = kmeans.fit_predict(X)
    data_with_clusters = new_df.copy()
    data_with_clusters['Cluster'] = identified_clusters
    if xaxis and yaxis and zaxis:
        fig = px.scatter_3d(data_with_clusters, x=xaxis, y=yaxis, z=zaxis,
                            color='Cluster', opacity=0.8, size='Value', size_max=30)
    else:
        if xaxis or yaxis:
            fig = px.scatter(data_with_clusters, x=xaxis, y=yaxis,
                             color='Cluster', opacity=0.8, size='Value', size_max=30)
        else:
            fig = px.scatter()
    fig.update_layout(
        paper_bgcolor=font_colors['background'], plot_bgcolor=font_colors['background'])
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
