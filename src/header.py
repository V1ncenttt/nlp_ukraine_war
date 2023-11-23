import dash_html_components as html
import dash
banner_style = {
    "backgroundColor": "white",
    "padding": "10px",
    "textAlign": "center",
    "display": "flex",
    "color": "black",
    "fontSize": "24px",
    "fontFamily": "Open Sans, sans-serif",
    "font-weight": "700",
}

class Header:
        def create_header(self):
            """
            Create the header section for the Dash application.

            Returns:
            - html.Div: Dash HTML component representing the header.
            """
            header_div = html.Div([
                html.Img(src=dash.get_asset_url("ukr_flag.png"),
                        style={'height': '50px', 'border-radius': '10px', 'marginRight': '10px'}),
                html.Div("Ukrainian War: a global opinion analysis using Twitter data",
                        style={'fontSize': '24px', 'padding-top': '10px'})
            ], style=banner_style)

            return header_div
