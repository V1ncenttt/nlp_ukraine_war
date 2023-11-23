import dash_core_components as dcc

class DropdownCreator:
    def create_date_dropdown(self):
        return dcc.Dropdown(
            id='date-dropdown',
            options=[{'label': date, 'value': date} for date in get_all_dates()],
            value=get_default_date()
        )

    def create_option_dropdown(self, id):
        return dcc.Dropdown(
            id=id,
            options=[{'label': 'Option 1', 'value': 'option1'}, {'label': 'Option 2', 'value': 'option2'}],
            value='option1'
        )

    def create_country_dropdown(self):
        return dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in get_all_countries()],
            value=get_default_country()
        )