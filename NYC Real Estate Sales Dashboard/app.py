import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import numpy as np

# cleaning data
real_estate_data = pd.read_csv('nycdb_data.csv')
# fill all empty values with 0
real_estate_data.fillna(0, inplace=True)
neighborhoods = real_estate_data['neighborhood'].unique().tolist()
# extract quarter from date
real_estate_data['salequarter'] = real_estate_data['saledate'].apply(lambda x: pd.to_datetime(x)).dt.to_period('Q')

# create empty list
option = []

# iterate over players
for i in neighborhoods:
	value_labels = {'label':f'{i}', 'value':f'{i}'}
	option.append(value_labels)

# install semantics cdn
external_stylesheets = ['https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css']

# initialize app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Dash uses html tags
app.layout = html.Div(children=[
    html.A([
    		html.I(className="github icon")],
    	   	href='https://github.com/DCharles01', 
    	   	target="_blank", 
    	   	className="github"),
    html.A([
    		html.I(className="linkedin icon")],
    	   	href='https://www.linkedin.com/in/david-a-charles-iii-837844145/', 
    	   	target="_blank", 
    	   	className="linkedin"),
    dcc.Dropdown(
    	id='my-dropdown',
    	options=option,
    	value='ANNADALE'

    	),
    dcc.Graph(id='my-graph')
    ])

# Dash is built from flask
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def plotRealEstateData(selected_dropdown_value):
	df = pd.pivot_table(real_estate_data, values='saleprice', index=['neighborhood', 'salequarter'], aggfunc=[np.mean, np.sum, np.std])
	return {
		'data': [{
			'y': df.loc[selected_dropdown_value]['mean']['saleprice'],
			'x': [str(x) for x in df.loc[selected_dropdown_value].index.values]
		}],
		# format layout
		'layout':{
    		  'title': f'{selected_dropdown_value}\'s Sale Price by Quarter',
    		  'yaxis': {'title':'Sale Price'},
    		  'xaxis': {'title':'Quarters'}}
	}
if __name__ == '__main__':
    app.run_server(debug=True)