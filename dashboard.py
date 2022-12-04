import dash
from dash import State
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import mysql.connector
import pyodbc
import time
import os

import pandas as pd
import json

import smtplib
import email.message
import time

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

try:
    server = 'healthsystem.database.windows.net'
    database = 'healthsystem'
    username = 'grupo01sis'
    password = '#GfHealthSystem01'
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server +
                          ';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD=' + password)
    conn.autocommit = True
    cursor = conn.cursor()
    print("Conexão com o Banco de Dados SQL Server Azure efetuada com sucesso.")
except:
    print("\U0001F916 Estou tentando me conectar ao banco de dados MySQL.", "\n--------")

    conn = mysql.connector.connect(
        host='172.17.0.2',
        user='root',
        password='root',
        port=3305
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("Consegui! Conexão com o Banco de Dados MySQL efetuada com sucesso.")

# =====================================================================

dir_path = os.path.dirname(os.path.realpath(__file__))

if(os.path.exists(dir_path + '/' + 'df_bar.csv') and os.path.isfile(dir_path + '/' + 'df_bar.csv')): 
  os.remove(dir_path + '/' + 'df_bar.csv') 
  print("df_bar excluido!") 
else: 
  print("df_bar não encontrado!")
  
if(os.path.exists(dir_path + '/' + 'df_states.csv') and os.path.isfile(dir_path + '/' + 'df_states.csv')): 
  os.remove(dir_path + '/' + 'df_states.csv') 
  print("df_states excluido!") 
else: 
  print("df_states não encontrado!")

df = pd.read_sql("SELECT nomeRegiao as 'Regiao', sigla as 'UF', nomeEstado as 'Estado', nomeCidade as 'Cidade', round(avg(valor), 2) as 'vidaSaudavel', momento as 'Data' FROM GustavoRegiao JOIN GustavoCidade on idRegiao = fkRegiao JOIN GustavoEstado on idEstado = fkEstado JOIN GustavoEquipamento on idCidade = fkCidade JOIN GustavoLeitura on idEquipamento = fkEquipamento GROUP BY nomeRegiao, sigla, nomeEstado, nomeCidade, momento;", con=conn)
df_states = df[~df["Estado"].isna()]
df_states.to_csv(dir_path + '/' + 'df_states.csv')

print(df_states)

time.sleep(2)

df_states = pd.read_csv(dir_path + '/' + r"df_states.csv")

brazil_states = json.load(open(dir_path + '/' + 'geojson/brazil_geo.json'))

cursor.execute(
    f"SELECT TOP 1 FORMAT(momento, 'yyyy-MM-dd') FROM GustavoLeitura ORDER BY momento DESC;")
rowAtual = cursor.fetchone()
dataAtual = str(''.join(map(str, rowAtual)))

df_states_ = df_states[df_states["Data"] == f"{dataAtual}"]

print(df_states_)

df_bar = pd.read_sql(
    "SELECT round(avg(valor), 2) as 'Média Do Dia', momento as 'Data' FROM GustavoLeitura GROUP BY momento;", con=conn)
df_bar.to_csv(dir_path + '/' + 'df_bar.csv')

print(df_bar)

time.sleep(2)

df_bar = pd.read_csv(dir_path + '/' + r'df_bar.csv')

# =====================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

avg_lifeExp = df_states_['vidaSaudavel'].sum(
) / df_states_['vidaSaudavel'].count()

fig = px.choropleth_mapbox(df_states_, locations="UF",
                           geojson=brazil_states, center={
                               "lat": -16.95, "lon": -47.78},
                           zoom=4, color="vidaSaudavel", color_continuous_scale=px.colors.diverging.BrBG, color_continuous_midpoint=avg_lifeExp, opacity=0.4,
                           hover_data={
                               "UF": True, "Estado": True, "Cidade": True, "vidaSaudavel": True, "Data": True}
                           )
fig.update_layout(
    paper_bgcolor="#242424",
    mapbox_style="stamen-terrain",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,)

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_bar["Data"], y=df_bar["Média Do Dia"], marker=dict(color=df_bar["Média Do Dia"],
                                                                              colorscale='viridis')))

fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
)

modal_1 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Informações sobre a Dashboard")),
        dbc.ModalBody(" Esta Dashboard foi elaborada para proporcionar o monitoramento de equipamentos multiparametricos utilizando apenas Python e Kotlin, proporcionando para o gestor uma visão analítica (Macro) e uma visão sintética (Micro) de cada Unidade Federativa com hardware distribuido pelo País."),
        dbc.ModalBody(" Tecnologias utilizadas no projeto:"),
        html.Div([
            html.Img(src=app.get_asset_url("wordcloud.png"), height=250, width="100%", style={
                    "border-radius": "20px"}
            )], style={"padding": "15px", "Display": "Flex", "align-items":"center", "width":"100%"}
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Abrir Previsão",
                id="open-toggle-modal-2",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="toggle-modal-1",
    centered=True,
    is_open=False,
)

modal_2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Previsão de Custos - Cost & Growth Forecast")),
        dbc.ModalBody(" A Previsão de custos é uma estratégia muito importante usada pela HealthSystem para que seja possível saber como será a situação do negócio futuramente, portanto, tem a função de garantir um processo organizado, e que estimula o aprendizado, para realizar ajustes no orçamento caso necessário."),
        dbc.ModalBody(" Grafico de projeção:"),
        html.Div([
            html.Img(src=app.get_asset_url("billing.png"), height=300, width="100%", style={
                    "border-radius": "20px"}
            )], style={"padding": "15px", "Display": "Flex", "align-items":"center", "width":"100%"}
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Retornar para informações",
                id="open-toggle-modal-1",
                className="ms-auto",
                n_clicks=0,
            )
        ),
    ],
    id="toggle-modal-2",
    centered=True,
    is_open=False,
)

# =====================================================================

app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([
                    html.Div([
                        html.Img(id="logo", src=app.get_asset_url(
                            "healthsystem-logo-white.png"), height=50),
                        html.H5(
                            children="Monitoramento operacional Analitico & Sintetico"),
                        dbc.Button("BRASIL", color="primary",
                                   id="location-button", size="lg", style={
                    "margin-right": "10px"}),
                        dbc.Button(
                            "Saber mais", id="open-toggle-modal", n_clicks=0, style={
                    "margin-right": "10px"}),
                        modal_1,
                        modal_2,
                    ], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
                html.P("Informe a data na qual deseja obter informações:", style={
                    "margin-top": "40px"}),
                html.Div(
                        className="div-for-dropdown",
                        id="div-test",
                        children=[
                            dcc.DatePickerSingle(
                                id="date-picker",
                                min_date_allowed=df_states.groupby(
                                    "Estado")["Data"].min().max(),
                                max_date_allowed=df_states.groupby(
                                    "Estado")["Data"].max().min(),
                                initial_visible_month=df_states.groupby(
                                    "Estado")["Data"].min().max(),
                                date=df_states.groupby("Estado")[
                                    "Data"].max().min(),
                                display_format="MMMM D, YYYY",
                                style={"border": "0px solid black"},
                            )
                        ],
                    ),

                dbc.Row([
                        dbc.Col([dbc.Card([
                                dbc.CardBody([
                                    html.Span(
                                        "Equipamentos Identificados", className="card-text"),
                                    html.H3(
                                        style={"color": "#adfc92"}, id="equipamentos-identificados-text"),
                                    html.Span("Equipamentos Estáveis",
                                              className="card-text"),
                                    html.H5(style={"color": "#adfc92"},
                                            id="equipamentos-estaveis-text"),
                                ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                                                       "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                                       "color": "#FFFFFF"})], md=6),
                        dbc.Col([dbc.Card([
                                dbc.CardBody([
                                    html.Span("Equipamentos em Alerta",
                                              className="card-text"),
                                    html.H3(style={"color": "yellow"},
                                            id="anomalia-preocupante-text"),
                                    html.Span("Equipamentos Críticos",
                                              className="card-text"),
                                    html.H5(style={"color": "red"},
                                            id="anomalia-critica-text"),
                                ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                                                       "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                                                       "color": "#FFFFFF"})], md=6),
                        ]),

                html.Div([
                    html.P("Grafico de Analise Macro do Brasil:",
                           style={"margin-top": "25px"}),
                    dcc.Graph(id="bar-graph", figure=fig2, style={
                        "background-color": "#242424",
                        "height": "250px"
                    }),
                    dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="circle",),
                    time.sleep(1)
                ], id="teste")
            ], md=5, style={
                "padding": "25px",
                "background-color": "#242424"
            }),
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig,
                                            style={'height': '100vh', 'margin-right': '10px'})],
                    ),
                ], md=7),
        ], className="g-0")
    ], fluid=True,
)

# =====================================================================

@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("toggle-modal-1", "is_open"),
    [
        Input("open-toggle-modal", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
        Input("open-toggle-modal-2", "n_clicks"),
    ],
    [State("toggle-modal-1", "is_open")],
)
def toggle_modal_1(n0, n1, n2, is_open):
    if n0 or n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("toggle-modal-2", "is_open"),
    [
        Input("open-toggle-modal-2", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
    ],
    [State("toggle-modal-2", "is_open")],
)
def toggle_modal_2(n2, n1, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [
        Output("equipamentos-identificados-text", "children"),
        Output("equipamentos-estaveis-text", "children"),
        Output("anomalia-preocupante-text", "children"),
        Output("anomalia-critica-text", "children"),
    ], [Input("date-picker", "date"), Input("location-button", "children")]
)
def display_status(date, location):
    if location == "BRASIL":
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE momento = '{date}';")
        rowIdenti = cursor.fetchone()
        identificados_novos = int(''.join(map(str, rowIdenti)))
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE mediaValor > 40 and mediaValor < 60 and momento = '{date}';")
        rowEst = cursor.fetchone()
        estaveis_novos = int(''.join(map(str, rowEst)))
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE ((mediaValor > 10 and mediaValor < 40) or (mediaValor > 60 and mediaValor < 90)) and momento = '{date}';")
        rowPrep = cursor.fetchone()
        preocupantes_novos = int(''.join(map(str, rowPrep)))
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE (mediaValor < 10 or mediaValor > 90) and momento = '{date}';")
        rowCrit = cursor.fetchone()
        criticos_novos = int(''.join(map(str, rowCrit)))
        print("Leitura da Região:", location, "Equipamentos identificados:", identificados_novos, "Equipamentos estaveis:",
              estaveis_novos, "Equipamentos Preocupantes:", preocupantes_novos, "Equipamentos Criticos:", criticos_novos)
    else:
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, fkEstado, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento, fkEstado) as ResultTable JOIN GustavoEstado on idEstado = fkEstado WHERE momento = '{date}' and sigla = '{location}';")
        rowIdenti = cursor.fetchone()
        identificados_novos = int(''.join(map(str, rowIdenti)))
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, fkEstado, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento, fkEstado) as ResultTable JOIN GustavoEstado on idEstado = fkEstado WHERE mediaValor > 40 and mediaValor < 60 and momento = '{date}' and sigla = '{location}';")
        rowEst = cursor.fetchone()
        estaveis_novos = int(''.join(map(str, rowEst)))
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, fkEstado, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento, fkEstado) as ResultTable JOIN GustavoEstado on idEstado = fkEstado WHERE ((mediaValor > 10 and mediaValor < 40) or (mediaValor > 60 and mediaValor < 90))  and momento = '{date}' and sigla = '{location}';")
        rowPrep = cursor.fetchone()
        preocupantes_novos = int(''.join(map(str, rowPrep)))
        time.sleep(1)
        cursor.execute(
            f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, fkEstado, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento, fkEstado) as ResultTable JOIN GustavoEstado on idEstado = fkEstado WHERE (mediaValor < 10 or mediaValor > 90) and momento = '{date}' and sigla = '{location}';")
        rowCrit = cursor.fetchone()
        criticos_novos = int(''.join(map(str, rowCrit)))
        print("Leitura do Estado:", location, "Equipamentos identificados:", identificados_novos, "Equipamentos estaveis:",
              estaveis_novos, "Equipamentos Preocupantes:", preocupantes_novos, "Equipamentos Criticos:", criticos_novos)
    return (
        identificados_novos,
        estaveis_novos,
        preocupantes_novos,
        criticos_novos,
    )


@app.callback(
    Output("choropleth-map", "figure"),
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df_states[df_states["Data"] == date]

    avg_lifeExp = df_data_on_states['vidaSaudavel'].sum(
    ) / df_data_on_states['vidaSaudavel'].count()

    fig = px.choropleth_mapbox(df_states_, locations="UF",
                               geojson=brazil_states, center={
                                   "lat": -16.95, "lon": -47.78},
                               zoom=4, color="vidaSaudavel", color_continuous_scale=px.colors.diverging.BrBG, color_continuous_midpoint=avg_lifeExp, opacity=0.4,
                               hover_data={
                                   "UF": True, "Estado": True, "Cidade": True, "vidaSaudavel": True, "Data": True}
                               )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="stamen-terrain", autosize=True,
                      margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"),
     Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)

    else:
        return "BRASIL"


def enviar_notificacao():
    time.sleep(1)
    cursor.execute(
    f"SELECT TOP 1 FORMAT(momento, 'yyyy-MM-dd') FROM GustavoLeitura ORDER BY momento DESC;")
    rowAtual = cursor.fetchone()
    date = str(''.join(map(str, rowAtual)))
    time.sleep(1)
    cursor.execute(f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE momento = '{date}';")
    rowIdenti = cursor.fetchone()
    identificados_novos = int(''.join(map(str, rowIdenti)))
    time.sleep(1)
    cursor.execute(f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE mediaValor > 40 and mediaValor < 60 and momento = '{date}';")
    rowEst = cursor.fetchone()
    estaveis_novos = int(''.join(map(str, rowEst)))
    time.sleep(1)
    cursor.execute(f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE ((mediaValor > 10 and mediaValor < 40) or (mediaValor > 60 and mediaValor < 90)) and momento = '{date}';")
    rowPrep = cursor.fetchone()
    preocupantes_novos = int(''.join(map(str, rowPrep)))
    time.sleep(1)
    cursor.execute(f"SELECT count(fkEquipamento) as EquipamentosPorDia FROM (SELECT fkEquipamento, avg(valor) as mediaValor, momento FROM GustavoLeitura GROUP BY momento, fkEquipamento) as ResultTable WHERE (mediaValor < 10 or mediaValor > 90) and momento = '{date}';")
    rowCrit = cursor.fetchone()
    criticos_novos = int(''.join(map(str, rowCrit)))
    
    corpo = f"""
    <div style="display: flex; flex-direction: column; justify-content: space-around; align-items: center; width: 100%">
        <div>
            <img src="https://dormed.vteximg.com.br/arquivos/ids/158742-1000-1000/Monitor-Multiparametro-com-Tela-15---ECG---SpO2---Resp---PNI--RD15---R-D-Mediq.png?v=637091751694200000" width="150" height="100">
            <h1>Relatorio de Indicadores - <span style="color: green;">HealthSystem</span> - {date}</h1>
        </div>
        <div>
            <h4>Os relatórios e indicadores operacionais da HealthSystem têm por finalidade expor informações sobre a empresa, de modo a auxiliar o gestor na elaboração de estratégias e tomada de decisões.</h4>
        </div>
        <h2>Análise da operação nacional do Brasil</h2>
        <div>
            <h3>Equipamentos Identificados</h3>
            <h4>{identificados_novos}</h4>
            <div style="flex-direction: row; gap: 50px;">
                <div style="flex-direction: Column; width: 300px">
                    <h3>Equipamentos Estáveis</h3>
                    <h4 style="color: green;">{estaveis_novos}</h4>
                </div>
                <div style="flex-direction: Column; width: 300px">
                    <h3>Equipamentos em Alerta</h3>
                    <h4 style="color: orange;">{preocupantes_novos}</h4>
                </div>
                <div style="flex-direction: Column; width: 300px">
                    <h3>Equipamentos Críticos</h3>
                    <h4 style="color: red;">{criticos_novos}</h4>
                </div>
            </div>
        </div>
    </div>
    """

    msg = email.message.Message()
    msg['Subject'] = "Relatorio de Indicadores - HealthSystem"
    msg['From'] = 'healthsystembrasil@outlook.com'
    msg['To'] = 'gustavo.goncalves@sptech.school'
    password = 'ROot0212'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    s = smtplib.SMTP('smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

if __name__ == "__main__":
    enviar_notificacao()
    app.run_server(debug=False, port=8051)
