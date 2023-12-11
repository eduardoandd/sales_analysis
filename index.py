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


def month_filter(month):
    if month == 0:
        mask = df['Mês'].isin(df['Mês'].unique())
    
    else:
        mask = df['Mês'].isin([month])
        
    return mask


def team_filter(team):
    if team == 0:
        mask = df['Equipe'].isin(df['Equipe'].unique())
    else:
        mask= df['Equipe'].isin([team])
    
    return mask

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
                            html.Div(id='month_select',style={'text-align': 'center', 'margin-top':'10px'})
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
             ]),
             
             dbc.Row([
                 dbc.Col([
                     dbc.Card([
                         dbc.CardBody([
                             dcc.Graph(id='graph4', className='dbc', config=config_graph)
                         ])
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
#MESES
@app.callback(
    Output('graph1','figure'),
    Output('graph2','figure'),
    Output('month_select','children'),
    Input('radio-month','value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value'),
    
)
def row1(month,theme):
    template = template_theme1 if theme else template_theme2
    
    mask = month_filter(month)
    df_1 = df.loc[mask]
    
    #TOP VENDEDEDORES POR TIME
    df_1 = df_1.groupby(['Equipe', 'Consultor'], as_index=False)['Valor Pago'].sum().sort_values(ascending=False, by='Valor Pago')
    df_top_consultor_team= df_1.groupby('Equipe').head(1)
    
    fig_top_consultor_team = go.Figure(
        go.Pie(labels=df_top_consultor_team["Consultor"] + ' - ' + df_top_consultor_team['Equipe'] , values=df_top_consultor_team['Valor Pago'], hole=.6)
    )
    fig_top_consultor_team.update_layout(main_config, height=200, template=template,legend=dict(x=1, y=1, traceorder='normal', font=dict(size=10)))
    
    fig_consultor_faturamento = px.bar(df_top_consultor_team, x='Consultor', y='Valor Pago', color='Equipe')
    fig_consultor_faturamento.update_layout(main_config, height=200, template=template, showlegend=False)
    
    lista_mes = ['Ano todo', 'Janeiro', 'Fevereiro', 'Março', 'Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    
    select = html.H1(lista_mes[month])
    
    return fig_consultor_faturamento,fig_top_consultor_team,select
    
@app.callback(
    Output('graph3', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def graph3(team, theme):
    template= template_theme1 if theme else template_theme2
    
    mask = team_filter(team)
    df_team = df.loc[mask]
    
    df_chamada_dia=df_team.groupby('Dia', as_index=False)['Chamadas Realizadas'].sum()
    
    fig_chamada_dia= go.Figure(go.Scatter(
        x=df_chamada_dia['Dia'], y=df_chamada_dia['Chamadas Realizadas'], mode='lines', fill='tonexty'
    ))
    
    fig_chamada_dia.add_annotation(
        text='Chamadas Médias por dia do Mês',
        yref='paper',
        xref='paper',
        font=dict(
            size=17,
            color='gray'
        ),
        align= 'center', bgcolor='rgba(0,0,0,0.8)',
        x=0.05, y=0.85, showarrow=False)
    
    fig_chamada_dia.add_annotation(
        text=f'Média: {round(df_chamada_dia["Chamadas Realizadas"].mean(),2)}',
        xref='paper',
        yref='paper',
        font=dict(
            size=20,
            color='gray'
        ),
        align='center', bgcolor='rgba(0,0,0,0.8)',
        x=0.05, y=0.55, showarrow=False
    )
    
    fig_chamada_dia.update_layout(main_config, height=180, template=template)
    
    return fig_chamada_dia
       
@app.callback(
    Output('graph4', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def graph4(team, theme):
    
    template= template_theme1 if theme else template_theme2
    
    mask = team_filter(team)
    df_team = df.loc[mask]
    
    #MÊS
    df_chamada_mes = df_team.groupby('Mês', as_index=False)['Chamadas Realizadas'].sum()
    
    fig_chamada_mes= go.Figure(go.Scatter(
        x=df_chamada_mes['Mês'], y=df_chamada_mes['Chamadas Realizadas'], mode='lines', fill='tonexty'
    ))
    
    fig_chamada_mes.add_annotation(
        text='Chamadas Médias por mês',
        yref='paper',
        xref='paper',
        font=dict(
            size=17,
            color='gray'
        ),
        align= 'center', bgcolor='rgba(0,0,0,0.8)',
        x=0.05, y=0.85, showarrow=False)
    
    fig_chamada_mes.add_annotation(
        text=f'Média: {round(df_chamada_mes["Chamadas Realizadas"].mean(),2)}',
        xref='paper',
        yref='paper',
        font=dict(
            size=20,
            color='gray'
        ),
        align='center', bgcolor='rgba(0,0,0,0.8)',
        x=0.05, y=0.55, showarrow=False
    )
    
    fig_chamada_mes.update_layout(main_config, height=180, template=template)
    
    return fig_chamada_mes  
        
@app.callback(
    Output('graph5', 'figure'),
    Output('graph6', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)    
def graph5_and_graph6(month,theme):
    template = template_theme1 if theme else template_theme2
    #month=1
    
    mask = month_filter(month)
    df_5=df_6=df.loc[mask]
    
    df_top_consultant = df_5.groupby(['Consultor','Equipe'], as_index=False)['Valor Pago'].sum().sort_values(by='Valor Pago', ascending=False)
    fig_top_consultant= go.Figure(
        go.Indicator(
            mode='number+delta',
            title={'text':f'<span style="font-size:100%">{df_top_consultant["Consultor"].iloc[0]} - Top Consultante</span>'},
            value=df_top_consultant['Valor Pago'].iloc[0],
            number={'prefix':'R$'},
            delta = {'relative':True, 'valueformat': '.1%', 'reference':df_top_consultant['Valor Pago'].mean()}

        )
    )
    
    fig_top_consultant.update_layout(main_config,height=200, template=template)
    fig_top_consultant.update_layout({'margin': {'l':0,'r':0,'t':50,'b':0}})
    
    df_top_teams= df_6.groupby(['Equipe'],as_index=False)['Valor Pago'].sum().sort_values(by='Valor Pago',ascending=False)
    fig_top_team = go.Figure(
        go.Indicator(
            mode='number+delta',
            title={'text': f'<span style="font-size:100%">{df_top_teams["Equipe"].loc[0]} - Top Team'},
            value=df_top_teams["Valor Pago"].loc[0],
            number={'prefix':'R$'},
            delta = {'relative':True, 'valueformat': '.1%', 'reference':df_top_teams['Valor Pago'].mean()}
        )
    )
    
    fig_top_team.update_layout(main_config,height=200, template=template)
    fig_top_team.update_layout({'margin': {'l':0,'r':0,'t':50,'b':0}})
    
    return fig_top_consultant,fig_top_team
    
@app.callback(
    Output('graph7', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def graph7(theme):
    #theme='darkly'
    template = template_theme1 if theme else template_theme2
    
    df_equipe_mes = df.groupby(['Mês','Equipe'],as_index=False)['Valor Pago'].sum()
    df_equipe_mes_group = df.groupby('Mês',as_index=False)['Valor Pago'].sum()
    
    fig_equipe_mes = px.line(df_equipe_mes, y='Valor Pago', x='Mês', color='Equipe')
    fig_equipe_mes.add_trace(go.Scatter(y=df_equipe_mes_group['Valor Pago'], x=df_equipe_mes_group['Mês'], mode='lines+markers', fill='tonexty', name='Total de vendas'))
    
    fig_equipe_mes.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=190, template=template)
    fig_equipe_mes.update_layout({'legend': {'yanchor': 'top', 'y':0.99, 'font' : {'color':'white', 'size':10}}})
    
    return fig_equipe_mes
    
@app.callback(
    Output('graph8', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def graph8(month,theme):
    template = template_theme1 if theme else template_theme2
    month=8
    
    mask = month_filter(month)
    df_8=df.loc[mask]
    
    df_equipe_valor_pago= df_8.groupby('Equipe', as_index=False)['Valor Pago'].sum()
    
    fig_equipe_valor_pago= go.Figure(go.Bar(
        x=df_equipe_valor_pago['Valor Pago'],
        y=df_equipe_valor_pago['Equipe'],
        orientation='h',
        textposition='auto',
        text=df_equipe_valor_pago['Valor Pago'],
        insidetextfont=dict(family='Times', size=12)
    ))
    
    fig_equipe_valor_pago.update_layout(main_config, height=360, template=template)
    
    return fig_equipe_valor_pago
    
@app.callback(
    Output('graph9', 'figure'),
    Input('radio-month', 'value'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
)
def graph9(month,team,theme):
    template = template_theme1 if theme else template_theme2
    
    mask=month_filter(month)
    df_9= df.loc[mask]
    
    mask= team_filter(team)
    df_9= df_9.loc[mask]
    
    df_9=df_9.groupby('Meio de Propaganda', as_index=False)['Valor Pago'].sum()
    
    fig9=go.Figure()
    fig9.add_trace(go.Pie(labels=df_9['Meio de Propaganda'], values=df_9['Valor Pago'], hole=.7))
    
    fig9.update_layout(main_config, height=150, template=template, showlegend=False)
    
    return fig9

@app.callback(
    Output('graph10', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def graph10(team,theme):
    #team='Equipe 2'
    template = template_theme1 if theme else template_theme2
    
    mask = team_filter(team)
    df_10 = df.loc[mask]
    
    df10 = df_10.groupby(['Meio de Propaganda', 'Mês'], as_index=False)['Valor Pago'].sum()
    fig10=px.line(df10, y='Valor Pago', x='Mês', color='Meio de Propaganda')
    
    fig10.update_layout(main_config, height=200, template=template, showlegend=False)
    return fig10

def graph11(month,team, theme):
    template = template_theme1 if theme else template_theme2
    
    mask=month_filter(month)
    df_11= df.loc[mask]
    
    mask= team_filter(team)
    df_11 = df_11.loc[mask]
    
    fig11= go.Figure()
    fig11.add_trace(go.Indicator
                        (
                            mode='number',
                            title= {'text': f'<span style="font-size:100%">Valor Total</span><br><span style="font-size:70%"> Em Reais</span><br>'},
                            number={'prefix': 'R$'}
                        )
                    )
    
    fig11.update_layout(main_config, height=300, template=template)
    select = html.H1('Todas Equipes') if team == 0 else html.H1(team)
    
    return fig11,select



# Run server
if __name__ == '__main__':
    app.run_server(debug=False,port=8064)