# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                               dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'site1'},
                    {'label': 'VAFB SLC-4E', 'value': 'site2'},
                    {'label': 'KSC LC-39A', 'value': 'site3'},
                    {'label': 'CCAFS SLC-40', 'value': 'site4'},
                ],
                value='ALL',
                placeholder="place holder here",
                searchable=True
                ),
                html.Br(),
                

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       2500: '2500',
                       5000: '5000',
                       7500: '7500'},
                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),])

                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total success lunches by site')
        return fig
    else:
        if entered_site == 'site1':
            filtered_df = spacex_df[spacex_df["Launch Site"]=="CCAFS LC-40"]
            f=filtered_df.groupby("class").count().reset_index()
            fig = px.pie(f, values='Launch Site',
            names='class', 
            title='Total success lunches in CCAFS LC-40 sr')
            return fig
        if entered_site == 'site2':
            filtered_df = spacex_df[spacex_df["Launch Site"]=="VAFB SLC-4E"]
            f=filtered_df.groupby("class").count().reset_index()
            fig = px.pie(f, values='Launch Site',
            names='class', 
            title='Total success lunches in VAFB SLC-4E sr')
            return fig
        if entered_site == 'site3':
            filtered_df = spacex_df[spacex_df["Launch Site"]=="KSC LC-39A"]
            f=filtered_df.groupby("class").count().reset_index()
            fig = px.pie(f, values='Launch Site',
            names='class', 
            title='Total success lunches in KSC LC-39A sr')
            return fig
        if entered_site == 'site4':
            filtered_df = spacex_df[spacex_df["Launch Site"]=="CCAFS SLC-40"]
            f=filtered_df.groupby("class").count().reset_index()
            fig = px.pie(f, values='Launch Site',
            names='class', 
            title='Total success lunches in CCAFS SLC-40 sr')
            return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")])
def payload_slider(entered_site2,MM):
    dff = spacex_df[(spacex_df["Payload Mass (kg)"]>=MM[0])&(spacex_df["Payload Mass (kg)"]<=MM[1])]
    if entered_site2 == 'ALL':
        fig2 = px.scatter(dff, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return fig2
    else:
        if entered_site2 == 'site1':
            filtered_df = dff[dff["Launch Site"]=="CCAFS LC-40"]
            fig2 = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
            return fig2
        if entered_site2 == 'site2':
            filtered_df = dff[dff["Launch Site"]=="VAFB SLC-4E"]
            fig2 = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
            return fig2
        if entered_site2 == 'site3':
            filtered_df = dff[dff["Launch Site"]=="KSC LC-39A"]
            fig2 = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
            return fig2
        if entered_site2 == 'site4':
            filtered_df = dff[dff["Launch Site"]=="CCAFS SLC-40"]
            fig2 = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
            return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
