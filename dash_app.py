import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from flask import Flask
from flask_restful import Api, Resource, reqparse
import ast
import datetime
import argparse


dic_Name = {'Food-consumption': 'F_consumption', 'Water-consumption':'W_consumption', 'Weight':'weight', 'Growth':'growth'}


pigs = {}

MAX_LEN = 20
        

server = Flask(__name__)
app = dash.Dash(__name__, server=server)





app.layout = html.Div([

    html.Div(
        [
            html.H1('IOF2020 Pig Farming Dashboard'),
            html.Div([
            html.Img(src=app.get_asset_url('title.png'))
                ], style={'width': '10%'}),
            html.Div(
                [
                    html.P('This dashboard displays water consumption, food consumption, weight change, and growth of each pigs'),
                    html.P('To view graph corponding to each pig, first selct the type of graph from the first dropbox. Then add pig id on the second dropbox') 
                ]) 
        ]),
    

    html.Div([

            dcc.Dropdown(
                id='graph-type-dropdown',
                options=[
                    {'label': k, 'value': v}
                          for k,v in dic_Name.items()
                ],
                placeholder="Select a type of graph",
                #value=['F_consumption'],
                multi=True
            ),

            html.H1(''),


            dcc.Dropdown(
                id='pig-list-dropdown',
                options=[
                    {'label': pig, 'value': pig}
                          for pig in pigs.keys()
                ],
                placeholder="Select pigs id",
                #value=['pig'],
                multi=True
            ),


        ]),

        html.Button('Refresh', id='refresh_button'),


    html.Div(className='row', id='live-graph',),
    
    dcc.Interval(
        id='graph-update',
        interval=1*1000,
        n_intervals = 0
    ),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':5000})




@app.callback(Output('live-graph', 'children'),
              [Input('graph-type-dropdown', 'value'),
                Input('pig-list-dropdown', 'value'),
                Input('graph-update', 'n_intervals')])
def update_graph_scatter( graph_types, pig_list_id, interval):
    XX = []
    YY = [] 
    graph=[]

    if pig_list_id:
        if graph_types:
            for pig_id in pig_list_id:
                data= []
                title = '[ [' + str(pig_id) + '] -- '
                for graph_type in graph_types:
                    title += '[' + str(graph_type) + ']'
                    XX = list(pigs[pig_id][graph_type]['date']),
                    YY = list(pigs[pig_id][graph_type]['value']),
                    print('********** XX ', XX)
                    print('********** min max ', min(XX[0]),max(XX[0]))
                    data.append(
                        plotly.graph_objs.Scatter(
                            x=list(pigs[pig_id][graph_type]['date']),
                            y=list(pigs[pig_id][graph_type]['value']),
                            name= graph_type,
                            mode= 'lines+markers'
                            )
                        )
                graph.append(
                    dcc.Graph(
                        id=str(pig_id)+'live-graph', 
                        animate=True,
                        figure= {'data': data,'layout' : go.Layout(
                                            xaxis=dict(range=[min(XX[0]),max(XX[0])]),
                                            #yaxis=dict(range=[min(YY),max(YY)]),
                                            title=title+']')})
                    )
            children=[
                html.Div(
                graph 
                )
            ]

            return children

    children=[
        html.Div(
               graph 
            )
        ]

    

    return children



@app.callback(
    dash.dependencies.Output('pig-list-dropdown', 'options'),
    [dash.dependencies.Input('refresh_button', 'n_clicks')])
def update_output(n_clicks):
    options = [ {'label': pig, 'value': pig}
                          for pig in pigs.keys()
                ]
    return   options
    



api = Api(server)





class Pig(Resource):
    def get(self , pig_id):
        
        if pig_id in pigs:
            return str(pigs[pig_id]), 200
        
        return "{} not found.".format(pig_id), 404

    def post(self, pig_id):
        parser = reqparse.RequestParser()
        parser.add_argument("F_consumption")
        parser.add_argument("W_consumption")
        parser.add_argument("weight")
        parser.add_argument("growth")
        args = parser.parse_args()

        print(args)
        print(args['F_consumption'])

        if pig_id in pigs:
            val = args['F_consumption']
            if val is not None:
                val = ast.literal_eval(args['F_consumption']) 
                if val['value'] is not None:
                    if val['date'] is not None:
                        for i in range(len(val['value'])):
                            pigs[pig_id]['F_consumption']['date'].append(val['date'][i])
                            pigs[pig_id]['F_consumption']['value'].append(val['value'][i])
                    else:
                        for i in range(len(val[value])):
                            date_time = datetime.datetime.now()
                            pigs[pig_id]['F_consumption']['date'].append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                            pigs[pig_id]['F_consumption']['value'].append(val['value'][i])

            val = args['W_consumption']
            if val is not None:
                val = ast.literal_eval(args['W_consumption']) 
                if val['value'] is not None:
                    if val['date'] is not None:
                        for i in range(len(val['value'])):
                            pigs[pig_id]['W_consumption']['date'].append(val['date'][i])
                            pigs[pig_id]['W_consumption']['value'].append(val['value'][i])
                    else:
                        for i in range(len(val[value])):
                            date_time = datetime.datetime.now()
                            pigs[pig_id]['W_consumption']['date'].append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                            pigs[pig_id]['W_consumption']['value'].append(val['value'][i])

            val = args['weight']
            if val is not None:
                val = ast.literal_eval(args['weight']) 
                if val['value'] is not None:
                    if val['date'] is not None:
                        for i in range(len(val['value'])):
                            pigs[pig_id]['weight']['date'].append(val['date'][i])
                            pigs[pig_id]['weight']['value'].append(val['value'][i])
                    else:
                        for i in range(len(val[value])):
                            date_time = datetime.datetime.now()
                            pigs[pig_id]['weight']['date'].append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                            pigs[pig_id]['weight']['value'].append(val['value'][i])

            val = args['growth']
            if val is not None:
                val = ast.literal_eval(args['growth']) 
                if val['value'] is not None:
                    if val['date'] is not None:
                        for i in range(len(val['value'])):
                            pigs[pig_id]['growth']['date'].append(val['date'][i])
                            pigs[pig_id]['growth']['value'].append(val['value'][i])
                    else:
                        for i in range(len(val[value])):
                            date_time = datetime.datetime.now()
                            pigs[pig_id]['growth']['date'].append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                            pigs[pig_id]['growth']['value'].append(val['value'][i])


            return str(pigs[pig_id])+ ' exist', 200

        
        pig = {}
        val = args['F_consumption']
        if val is not None: 
            val = ast.literal_eval(args['F_consumption'])
            if val['date'] is not None:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date.append(val['date'][i])
                        value.append(val['value'][i])

                    F_consumption = {'date':date, 'value':value}
                    pig['F_consumption'] = F_consumption
            else:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date_time = datetime.datetime.now()
                        date.append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                        value.append(val['value'][i])

                    F_consumption = {'date':date, 'value':value}
                    pig['F_consumption'] = F_consumption

        val = args['W_consumption']
        if val is not None: 
            val = ast.literal_eval(args['W_consumption'])
            if val['date'] is not None:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date.append(val['date'][i])
                        value.append(val['value'][i])

                    W_consumption = {'date':date, 'value':value}
                    pig['W_consumption'] = W_consumption
            else:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date_time = datetime.datetime.now()
                        date.append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                        value.append(val['value'][i])

                    W_consumption = {'date':date, 'value':value}
                    pig['W_consumption'] = W_consumption

        val = args['weight']
        if val is not None: 
            val = ast.literal_eval(args['weight'])
            if val['date'] is not None:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date.append(val['date'][i])
                        value.append(val['value'][i])

                    weight = {'date':date, 'value':value}
                    pig['weight'] = weight
            else:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date_time = datetime.datetime.now()
                        date.append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                        value.append(val['value'][i])

                    weight = {'date':date, 'value':value}
                    pig['weight'] = weight

        val = args['growth']
        if val is not None: 
            val = ast.literal_eval(args['growth'])
            if val['date'] is not None:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date.append(val['date'][i])
                        value.append(val['value'][i])

                    growth = {'date':date, 'value':value}
                    pig['growth'] = growth
            else:
                if val['value'] is not None:
                    date = deque(maxlen=MAX_LEN)
                    value = deque(maxlen=MAX_LEN)
                    for i in range(len(val['value'])):
                        date_time = datetime.datetime.now()
                        date.append('{:02d}:{:02d}:{:02d}'.format(date_time.hour, date_time.minute, date_time.second))
                        value.append(val['value'][i])

                    growth = {'date':date, 'value':value}
                    pig['growth'] = growth
        pigs[pig_id] = pig
        return str(pigs[pig_id]) + ' Created' , 201

    def put(self, pig_id):
        return self.post(pig_id)

    def delete(self, pig_id):
        if pig_id in pigs:
            del pigs[pig_id]
            return "{} is deleted.".format(pig_id), 200
        
        return "{} not found.".format(pig_id), 404
      
api.add_resource(Pig, "/pig/<string:pig_id>")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IoF2020 Pig Farming Dashboard')
    parser.add_argument('--host', type=str, default= '127.0.0.1', 
        help='The host ip address where the dashboard runs' )
    parser.add_argument('--port', type=int, default= 8050, 
        help='The host port address where the dashboard runs' )

    args = parser.parse_args()

    app.run_server(debug=False, port=args.port, host=args.host)
    app.run_server(debug=False)


