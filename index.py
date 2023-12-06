from dash import html,dcc,Input,Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import dash

FONT_AWESOME=["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__,external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally=True
server=app.server

# ========================= Styles ========================= #
tab_card = {'height': '100%'}

main_config = {
    'hovermode': 'x unified',
    'legend': {
        "yanchor":"top",
        "y":0.9,
        "xanchor":"left",
        "x":0.1,
        "title": {"text":None},
        "font": {"color":"white"},
        "bgcolor": "rgba(0,0,0,0.5)"
    },
    "margin": {"l":10,"r":10,"t":10,"b":10}
}

#DESABILITA OS BOTOES DO PLOTLY
config_graph={"displayModeBar":False, "showTips":False}

template_theme1='flatly'
template_theme2='darkly'
url_theme1=dbc.themes.FLATLY
url_theme2=dbc.themes.DARKLY


# ========================= Ingesão de dados ========================= #
df = pd.read_csv('dataset_asimov.csv')
df_cru = df.copy()

month_name = {'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12}

df['Mês']=df['Mês'].map(month_name)
df['Valor Pago']= df['Valor Pago'].str.lstrip('R$ ').astype(int)



#CRIANDO OPÇÕES DE FILTRO MÊS E EQUIPE
options_month = [{'label': 'Ano todo', 'value': 0}]
options_team = [{'label': 'Todas as Equipes', 'value':0}]

[options_month.append({'label':i, 'value':j}) for i,j in zip(df_cru['Mês'].drop_duplicates(),df['Mês'].drop_duplicates())]
options_month = sorted(options_month, key=lambda x: x['value'])


[options_team.append({'label':i, 'value':int(i[-1])}) for i in df['Equipe'].drop_duplicates()]
options_team = sorted(options_team, key=lambda x: x['value'])




# ========================= Layout ========================= #

app.layout = dbc.Container(children=[
    
    #Row 1
     dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([  
                            html.Legend("Sales Analytics")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Asimov Academy")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://asimov.academy/", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Top Consultores por Equipe')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, md=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id='radio-month',
                                options=options_month,
                                inline=True,
                                labelCheckedClassName='text-success',
                                inputCheckedClassName='border border-success bg-success',
                            ),
                            html.Div(id='teste',style={'text-align': 'center', 'margin-top':'10px'})
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
        
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
     
     #ROW 2
     dbc.Row([
         
         #COLUNA 1
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     dbc.Card([
                         dbc.CardBody([
                             dcc.Graph(id='graph3', className='dbc', config=config_graph)
                         ])
                     ], style=tab_card)
                 ])
             ],className='g-2 my-auto', style={'margin-top': '7px'}),
             
             dbc.Row([
                 dbc.Col([
                     dbc.Card([
                        dcc.Graph(id='graph4', className='dbc', config=config_graph)
                     ], style=tab_card)
                 ])
             ], className='g2 my-auto', style={'margin-top': '7px'})
         ], sm=12,lg=5),
         
         #COLUNA 2
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     dbc.Card([
                         dbc.CardBody([
                             dcc.Graph(id='graph5', className='dbc', config=config_graph)
                         ])
                     ], style=tab_card)
                 ], sm=6),
                 
                 dbc.Col([
                     dbc.Card([
                         dbc.CardBody([
                             dcc.Graph(id='graph6', className='dbc', config=config_graph)
                         ])
                     ], style=tab_card)
                 ],sm=6)
             ], className='g-2'),
             
             dbc.Row([
                 dbc.Col([
                     dbc.Card([
                         dcc.Graph(id='graph7', className='dbc', config=config_graph)
                     ], style=tab_card)
                 ])
             ], className='g2 my-auto', style={'margin-top': '7px'})
         ], sm=12, lg=4),
         
         #COLUNA 3
         dbc.Col([
             dbc.Card([
                 dcc.Graph(id='graph8', className='dbc', config=config_graph)
             ], style=tab_card)
         ], sm=12,lg=3)
     ], className='g2 my-auto', style={'margin-top': '7px'}),
     
     #ROW 3
     dbc.Row([
         dbc.Col([
             dbc.Card([
                 dbc.CardBody([
                     html.H4('Distribuição de Propaganda'),
                     dcc.Graph(id='graph9', className='dbc',config=config_graph)
                 ])
             ], style=tab_card)
         ], sm=12, lg=2),
         
         dbc.Col([
             dbc.Card([
                 dbc.CardBody([
                     html.H4('Valores de propaganda convertidas por mês'),
                     dcc.Graph(id='graph10', className='dbc',config=config_graph)
                 ])
             ], style=tab_card)
         ], sm=12, lg=5),
         
         dbc.Col([
             dbc.Card([
                 dbc.CardBody([
                     dcc.Graph(id='graph11', className='dbc', config=config_graph)
                 ])
             ], style=tab_card)
         ], sm=12, lg=3),
         
         dbc.Col([
             dbc.Card([
                 dbc.CardBody([
                     html.H5('Escolha a Equipe'),
                     dbc.RadioItems(
                         id='radio-team',
                         options=options_team,
                         value=0,
                         inline=True,
                         labelCheckedClassName='text-warning',
                         inputCheckedClassName='border border-warning bg-warning'
                     ),
                     html.Div(id='team-select',style={'text-align': 'center', 'margin-top':'10px'}, className='dbc')
                 ])
             ], style=tab_card)
         ], sm=12, lg=2)
     ], className='g2 my-auto', style={'margin-top': '7px'})
     
     
], fluid=True, style={'height': '100vh'})

# ========================= Callbacks ========================= #
@app.callback(
    Output('teste','children'),
    Input('radio-month','value')
)
def update_div_teste(selected_month):
    if selected_month == 1:
        return 'Janeiro'
    elif selected_month == 2:
        return 'Fevereiro'
    elif selected_month == 3:
        return 'Março'
    elif selected_month == 4:
        return 'Abril'
    elif selected_month == 5:
        return 'Maio'
    elif selected_month == 6:
        return 'Junho'
    elif selected_month == 7:
        return 'Julho'
    elif selected_month == 8:
        return 'Agosto'
    elif selected_month == 9:
        return 'Setembro'
    elif selected_month == 10:
        return 'Outubro'
    elif selected_month == 11:
        return 'Novembro'
    elif selected_month == 12:
        return 'Dezembro'
    elif selected_month == 0:
        return 'Ano todo'
    else:
        return ''


# Run server
if __name__ == '__main__':
    app.run_server(debug=True,port=8059)