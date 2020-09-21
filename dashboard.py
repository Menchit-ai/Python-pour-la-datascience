# filename = 'dash-01.py'

#
# Imports
#

import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

#
# Data
#

year = 2002

gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)

#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    #@app.callback(
    #Output(component_id='graph1', component_property='figure'), # (1)
    #[Input(component_id='year-dropdown', component_property='value')] # (2)
    #)
    #Output et Input marche pas
    def update_figure(input_value): # (3)
        return px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)


    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Life expectancy vs GDP per capita ({year})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Label('Year'),
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=[
                                    {'label': '1952', 'value': 1952},
                                    {'label': '1957', 'value': 1957},
                                    {'label': '1962', 'value': 1962},
                                    {'label': '1967', 'value': 1967},
                                    {'label': '1972', 'value': 1972},
                                    {'label': '1977', 'value': 1977},
                                    {'label': '1982', 'value': 1982},
                                    {'label': '1987', 'value': 1987},
                                    {'label': '1992', 'value': 1992},
                                    {'label': '1997', 'value': 1997},
                                    {'label': '2002', 'value': 2002},
                                    {'label': '2007', 'value': 2007},
                                ],
                                value=2007,
                            ),

                            html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {year}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''), # (7)

    ]
    )

    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)