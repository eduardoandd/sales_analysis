import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


#INGESTÃO E TRATAMENTO DE DADOS
df = pd.read_csv('dataset_asimov.csv')

month_name = {'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6, 'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12}

df['Mês']=df['Mês'].map(month_name)
df['Valor Pago']= df['Valor Pago'].str.lstrip('R$ ').astype(int)

#VENDAS POR EQUIPE
df1= df.groupby('Equipe',as_index=False)['Valor Pago'].sum()

fig1 = go.Figure(go.Bar(
    x=df1['Valor Pago'],
    y=df1['Equipe'],
    orientation='h',
    textposition='auto',
    text=df1['Valor Pago'],
    insidetextfont=dict(family='Times',size=12)
))

#CHAMADAS REALIZADAS POR DIA DO MÊS
df2=df.groupby('Dia', as_index=False)['Chamadas Realizadas'].sum()

fig2 = go.Figure(
    go.Scatter(
        x=df2['Dia'],y=df2['Chamadas Realizadas'],
        mode='lines',
        fill='tonexty'
    )
)

fig2.add_annotation(
    text='Chamadas médias por dia no mês',
    xref='paper',yref='paper',
    font=dict(
        size=10,
        color='blue'
    ),
    align='center', bgcolor="rgba(200, 200, 200, 0.8)",x=1.0,y=0.85,showarrow=False
)

fig2.add_annotation(
    text=f'Méda : {round(df["Chamadas Realizadas"].mean(),2)}',
    xref='paper',yref='paper',
    font=dict(
        size=10,
        color='blue'
    ),
    align='center', bgcolor="rgba(200, 200, 200, 0.8)",x=0.80,y=0.79,showarrow=False

)


#CHAMADAS MÉDIAS POR MÊS
df4 = df.groupby('Mês', as_index=False)['Chamadas Realizadas'].sum()
df4

fig4 = go.Figure(
    go.Scatter(
        x=df4['Mês'],y=df4['Chamadas Realizadas'], mode='lines',fill='tonexty'
    )
)

fig4.add_annotation(
    text='Chamadas médias por mês',
    xref='paper',yref='paper',
    font=dict(
        size=10,
        color='blue'
    ),
    align='center', bgcolor="rgba(200, 200, 200, 0.8)",x=0.05,y=0.85,showarrow=False
)
fig4.add_annotation(
    text=f'Média: {round(df["Chamadas Realizadas"].mean(),2)}',
    xref='paper',yref='paper',
    font=dict(
        size=10,
        color='blue'
    ),
    align='center', bgcolor="rgba(200, 200, 200, 0.8)",x=0.05,y=0.79,showarrow=False
)


#VALORES PAGOS POR MÊS POR MEIO DA PROPAGANDA
df5 = df.groupby(['Meio de Propaganda','Mês'],as_index=False)['Valor Pago'].sum()

fig = px.line(df5, x='Mês',y='Valor Pago',color='Meio de Propaganda')

#VALORES PAGOS TOTAIS POR MEIO DA PROPAGANDA
df6= df.groupby('Meio de Propaganda', as_index=False)['Valor Pago'].sum()

fig6=go.Figure(
    go.Pie(labels=df6['Meio de Propaganda'], values=df6['Valor Pago'], hole=.7)
)

df.columns
#VENDAS DE CADA EQUIPE POR MÊS + TOTAL
df_teams = df.groupby(['Equipe','Mês'], as_index=False)['Valor Pago'].sum()
df_amount_paid=df.groupby('Mês',as_index=False)['Valor Pago'].sum()

fig_teams=px.line(df_teams, x='Mês',y='Valor Pago', color='Equipe')
fig_teams.add_trace(go.Scatter(x=df_amount_paid['Mês'],y=df_amount_paid['Valor Pago'],fill='tonexty', opacity=0.1, name='Total de Vendas'))
fig_teams_pie=go.Figure(
    go.Pie(labels=df_teams['Equipe'],values=df_teams['Valor Pago'])
)

# EFICIÊNCIA DE VENDAS
df_sales_efi = df.groupby(['Status de Pagamento'], as_index=False)['Chamadas Realizadas'].sum()

fig_sales_efi = go.Figure(
    go.Pie(labels=df_sales_efi['Status de Pagamento'],values=df_sales_efi['Chamadas Realizadas'], hole=0.6)
)

#MELHORES CONSULTORES
df_top_consultant = df.groupby(['Consultor','Equipe'], as_index=False)['Valor Pago'].sum().sort_values(by='Valor Pago', ascending=False)

fig_top_consultant= go.Figure(
    go.Indicator(
        mode='number+delta',
        title={'text':f'<span style="font-size:150%">{df_top_consultant["Consultor"].iloc[0]} - Top Consultant</span>'},
        value=df_top_consultant['Valor Pago'].iloc[0],
        number={'prefix':'R$'},
        delta = {'relative':True, 'valueformat': '.1%', 'reference':df_top_consultant['Valor Pago'].mean()}
                 
    )
)

#Melhor Equipe

df_top_teams= df.groupby(['Equipe'],as_index=False)['Valor Pago'].sum().sort_values(by='Valor Pago',ascending=False)

fig_top_team = go.Figure(
    go.Indicator(
        mode='number+delta',
        title={'text': f'<span style="font-size:150%">{df_top_teams["Equipe"].loc[0]} - Top Team'},
        value=df_top_teams["Valor Pago"].loc[0],
        number={'prefix':'R$'},
        delta = {'relative':True, 'valueformat': '.1%', 'reference':df_top_teams['Valor Pago'].mean()}
    )
)

#GANHOS TOTAIS

df_total_earnings=df['Valor Pago'].sum()

fig_total_earnings = go.Figure(
    go.Indicator(
        mode='number',
        title={'text': f'<span style="font-size:150%">Valor total arrecadado'},
        value=df_total_earnings,
        number={'prefix':'R$'},
    )   
)

#MELHOR VENDEDOR DE CADA EQUIPE

df_top_saller_team = df.groupby(['Equipe','Consultor'],as_index=False)['Valor Pago'].sum().sort_values(by='Valor Pago',ascending=False)

df_tst_group = df_top_saller_team.groupby('Equipe',as_index=False).head(1)

fig_top_saller_team = go.Figure(
    go.Pie(
        labels=df_tst_group["Consultor"] + ' - ' + df_tst_group['Equipe'],
        values=df_tst_group['Valor Pago'],
        hole=.6
    )
)

#TOP MELHORES VENDEDORES
df_top_sallers= df.groupby(['Consultor','Equipe'],as_index=False)['Valor Pago'].sum().sort_values(by='Valor Pago', ascending=False).head(5)

fig_top_sallers = px.bar(df_top_sallers,x='Consultor',y='Valor Pago', color='Equipe')

fig_top_sallers.update_xaxes(categoryorder='total descending')