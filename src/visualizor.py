import dash_core_components as dcc

class Visualizor:
    def create_choropleth_map(self, data):
        return dcc.Graph(id='choropleth-map')

    def create_bar_chart(self, data):
        return dcc.Graph(id='bar-chart')

    def create_wordcloud(self, data):
        return dcc.Graph(id='wordcloud')

    def create_line_chart(self, data):
        return dcc.Graph(id='line-chart')