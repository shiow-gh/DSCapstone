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
CCAFS_df=spacex_df[spacex_df['Launch Site']==("CCAFS LC-40")]
VAFB_df=spacex_df[spacex_df['Launch Site']==("VAFB SLC-4E")]
KSC_df=spacex_df[spacex_df['Launch Site']==("KSC LC-39A")]
CCAFS_SLC_df=spacex_df[spacex_df['Launch Site']==("CCAFS SLC-40")]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
html.Br(),
html.Div([ 
    html.Label("Select Sites"),
    dcc.Dropdown(id='site_dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                #searchable=True
                )
]),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                #html.Div(dcc.Graph(id='success-pie-chart')),
html.Br(),


html.Div(dcc.Graph(id='success_pie_chart')),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
html.Div([ 
    html.Label("Range Slider"),
    dcc.RangeSlider(id='payload_slider',
                min=0, max=10000, step=1000,
                #marks={0: '0',
                #       100: '100'},
                value=[min_payload, max_payload])
]),        
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                                ])
 # TASK 1: Add a dropdown list




# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success_pie_chart', component_property='figure'),
             Input(component_id='site_dropdown', component_property='value'))

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

def get_pie_chart(site_dropdown):
    #filtered_df = spacex_df
    All_success_df=spacex_df.groupby('Launch Site')['class'].sum().reset_index()
    if site_dropdown == 'ALL':
        fig = px.pie(All_success_df, values='class', 
        names='Launch Site', 
        title='Success Pie Chart for All Sites')
        #print ('All Sites Selected')
        return fig
    elif site_dropdown == 'CCAFS LC-40':
        Success_CCAFS=CCAFS_df.groupby('class')['class'].count()
        fig = px.pie(Success_CCAFS, values='class',
        names=[0,1],
        title='Pie chart for CCAFS LC-40 Success vs. Failure')
        return fig
    elif site_dropdown == 'VAFB SLC-4E':
        Success_VAFB=VAFB_df.groupby('class')['class'].count()
        fig = px.pie(Success_VAFB, values='class',
        names=[0,1],
        title='Pie chart for VAFB SLC-4E Success vs. Failure')
        return fig
    elif site_dropdown == 'KSC LC-39A':
        Success_KSC=KSC_df.groupby('class')['class'].count()
        fig = px.pie(Success_KSC, values='class',
        names=[0,1],
        title='Pie chart for KSC LC-39A Success vs. Failure')
        return fig
    else:
        Success_SLC=CCAFS_SLC_df.groupby('class')['class'].count()
        fig = px.pie(Success_SLC, values='class',
        names=[0,1],
        title='Pie chart for CCAFS SLC-40 Success vs. Failure')
        return fig   

#html.P("Payload range (Kg):"),
# TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)

@app.callback(
    Output(component_id='success_payload_scatter_chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
    Input(component_id='payload_slider', component_property='value')]
    )                
# TASK 4: Add a scatter chart to show the correlation between payload and launch success
#html.Div(dcc.Graph(id='success-payload-scatter-chart')),
def get_scatter_chart(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        fig = px.scatter(spacex_df,
        x='Payload Mass (kg)', 
        y='class', 
        color= 'Booster Version Category',
        title='Correlation between Payload and Success Scatter Chart')
        return fig
    elif site_dropdown == 'CCAFS LC-40':
        fig = px.scatter(CCAFS_df,
        x='Payload Mass (kg)', 
        y='class', 
        color= 'Booster Version Category',
        title='CCAFS LC-40 Correlation between Payload and Success Scatter Chart')
        return fig
    elif site_dropdown == 'VAFB SLC-4E':
        fig = px.scatter(VAFB_df,
        x='Payload Mass (kg)', 
        y='class', 
        color= 'Booster Version Category',
        title='VAFB SLC-4E Correlation between Payload and Success Scatter Chart')
        return fig
    elif site_dropdown == 'KSC LC-39A':
        fig = px.scatter(KSC_df,
        x='Payload Mass (kg)', 
        y='class', 
        color= 'Booster Version Category',
        title='KSC LC-39A Correlation between Payload and Success Scatter Chart')
        return fig
    else:
        fig = px.scatter(CCAFS_SLC_df,
        x='Payload Mass (kg)', 
        y='class', 
        color= 'Booster Version Category',
        title='CCAFS SLC-40 Correlation between Payload and Success Scatter Chart')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
