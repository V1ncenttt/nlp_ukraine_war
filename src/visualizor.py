import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px

class Visualizor:
    def create_choropleth_map(self, data):
        """
        Create a choropleth map based on the provided data.

        Parameters:
        - data (tuple): A tuple containing three elements:
            - loc (list): List of location codes.
            - position (list): List of values corresponding to the locations.
            - countries (list): List of country names.

        Returns:
        - dcc.Graph: Dash component representing the choropleth map.
        """
        loc, position, countries = data

        # Create a Plotly figure for the choropleth map
        fig = go.Figure(
            data=go.Choropleth(
                locations=loc,  
                z=position,  
                locationmode="ISO-3", 
                colorscale="Reds",
                autocolorscale=False,
                text=[f"{country}: {value}" for country, value in zip(countries, position)], 
                marker_line_color="white",
                colorbar_title="Number of pro-russian tweets",
            )
        )

        # Update the layout of the figure for better presentation
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Reduce margins to use more space
            geo=dict(
                projection_scale=5,  # Adjust scale of the map
                center=dict(lat=0, lon=0),  # Adjust center
            )
        )

        # Return the choropleth map as a Dash Graph component
        return dcc.Graph(id='choropleth-map', figure=fig)


    def create_bar_chart(self, data):

        
        fig = px.bar(data, x='username', y='count')
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Reduce margins to use more space
        )
        return dcc.Graph(id='bar-chart', figure=fig)

    def create_wordcloud(self, wc):
        return dcc.Graph(id='wordcloud')

    def create_line_chart(self, data):
        return dcc.Graph(id='line-chart')