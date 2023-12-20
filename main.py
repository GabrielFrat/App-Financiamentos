import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime
import numpy as np
import tkinter as tk
import yfinance as yf
from numpy import linalg as la
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class functions:

    

    def plotar_grafico(self, ativo, root, vencimento):
        listAcoes = ativo + '.SA'

        def calcular_dias_uteis(data_inicial, data_final):
            data_inicial_np = np.datetime64(data_inicial, 'D')
            data_final_np = np.datetime64(data_final, 'D')
            dias_uteis = np.busday_count(data_inicial_np, data_final_np)
            return dias_uteis


        retornos_carteira = pd.DataFrame()
        data_f = datetime.datetime.now()
        data_backtest = data_f - datetime.timedelta(days=4000)

        precos_test = yf.download(listAcoes, start=data_backtest, end=data_f)['Close']
        retornos = precos_test.pct_change().dropna()
        ultimo_preco = precos_test[-1]
        num_simulacoes = 20
        
        print(vencimento)
        print(type(vencimento))
        print(data_f)
        print(type(data_f))
        data_vencimento = datetime.datetime.strptime(vencimento, '%Y-%m-%d')
        print(data_vencimento)
        print(type(data_vencimento))

        num_dias = calcular_dias_uteis(data_f, vencimento)

        #data_obj_com_horario = datetime.strptime(data_str_com_horario, '%Y-%m-%d %H:%M:%S')

        print(num_dias)
        for x in range(num_simulacoes):
             count = 0 
             daily_vol = retornos.std()

             preco_series = []

             preco = ultimo_preco * (1 + np.random.normal(0, daily_vol))
             preco_series.append(preco)
             for y in range(num_dias):
                  if count == 59:
                       break
                  preco = preco_series[count] * (1 + np.random.normal(0, daily_vol))
                  preco_series.append(preco)
                  count += 1

             retornos_carteira[x] = preco_series

        fig, graphProjected = plt.subplots()

        graphProjected.plot(retornos_carteira, linewidth=1)
        graphProjected.axhline(y=ultimo_preco, color='r', linestyle='-')
        title_graph = "Projeção de {} usando Monte Carlo.".format(ativo)
        graphProjected.set_title(label=title_graph)

        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=25, y=650, width=800, height=300)



    def get_option(self, ativo, qtde, vencimento, corretagem, pm):
        email = ""
        senha = ""
        correta = str(corretagem.replace(",", "."))
        pm = str(pm.replace(",", "."))
        print(pm)
        print(correta)
        def get_token(email, senha):
                body = {"email": email, "password": senha}
                r = requests.post('https://api.oplab.com.br/v3/domain/users/authenticate', json=body).json()['access-token']
                return r

        token = get_token(email, senha)
        header = {'Access-Token': token}
        
        option = requests.get('https://api.oplab.com.br/v3/market/options/{}'.format(ativo), headers=header).json()
        dfOpcoes = pd.DataFrame(option)
        
        dfOpcoes = dfOpcoes.loc[dfOpcoes['category'] == "CALL"]
        dfOpcoes = dfOpcoes.loc[:, ['symbol', 'block_date', 'maturity_type', 'close', 'strike', 'financial_volume']]
        dfOpcoes = dfOpcoes.rename(columns={'symbol':'Série', 'block_date':'Vencimento', 'maturity_type':'Tipo', 'close':'Prêmio', 'strike':'Strike', 'financial_volume':'Volume Negociado'})
        
        dfOpcoes = dfOpcoes.loc[dfOpcoes['Vencimento'] == vencimento]
        action = requests.get('https://api.oplab.com.br/v3/market/stocks/{}'.format(ativo), headers=header).json()['close']

        dfOpcoes['Cotação'] = action
        correta = float(correta)
        pm = float(pm)
        
        print(correta)
        print(pm)
        print(int(qtde))
        print(action)
        dfOpcoes['Custos'] = round((((int(qtde) * dfOpcoes['Cotação']) + (int(qtde) * dfOpcoes['Prêmio']) + (int(qtde) * dfOpcoes['Strike'])) * float(correta)), 3)
        dfOpcoes['Custo do Ativo'] = round((dfOpcoes['Cotação'] - dfOpcoes['Prêmio']) + (dfOpcoes['Custos'] / int(qtde)), 3)
        dfOpcoes['Investimento'] = round(dfOpcoes['Custo do Ativo'] * int(qtde), 3)
        dfOpcoes['Taxa Período'] = round(((dfOpcoes['Strike']/dfOpcoes['Custo do Ativo'])-1)*100, 3)
        dfOpcoes['$$'] = round((dfOpcoes['Strike'] - dfOpcoes['Custo do Ativo']) * int(qtde), 3)

        def alta_exercicio(cotacao, strike):
            if cotacao > strike:
                return "in"
            else:
                return round(((strike / cotacao) - 1)*100, 3)
            
        def stop(custo, cotacao):
            return (1-(custo/cotacao))*100


        dfOpcoes['Alta para Exercício'] =  dfOpcoes.apply(lambda dfOpcoes: alta_exercicio(dfOpcoes['Cotação'], dfOpcoes['Strike']), axis=1)
        dfOpcoes['Proteção'] = round((1-(dfOpcoes['Strike']/dfOpcoes['Cotação']))*100, 3)
        dfOpcoes['Stop'] = dfOpcoes.apply(lambda dfOpcoes: stop(dfOpcoes['Custo do Ativo'], dfOpcoes['Cotação']), axis=1)
        # dfOpcoes['Risco x Retorno'] = 
        dfOpcoes['Custo da Rolagem'] = round(((int(qtde) * dfOpcoes['Strike']) + (dfOpcoes['Prêmio'] * int(qtde))) * correta, 3)
        
        dfOpcoes['||'] = "||"
        dfOpcoes['Custo do Ativo PM'] = round(float(pm) - dfOpcoes['Prêmio'], 2)
        dfOpcoes['Rentabilidade Atual'] = round(((dfOpcoes['Cotação']/float(pm))-1)*100, 3)
        dfOpcoes['Rentabilidade Real'] = round(((((dfOpcoes['Strike'] - (dfOpcoes['Prêmio'] + dfOpcoes['Strike']))*correta)/dfOpcoes['Custo do Ativo PM'])-1), 3)                 

        pd.set_option('display.precision', 2)
        dfOpcoes['Tipo'] = dfOpcoes['Tipo'].str[0]
        dfOpcoes = dfOpcoes.loc[:, ['Série', 'Tipo', 'Strike', 'Prêmio', 'Volume Negociado', 'Custos', 'Custo do Ativo', 'Investimento', 'Taxa Período', 
                                    '$$', 'Alta para Exercício', 'Proteção', 'Stop', 'Custo da Rolagem', '||', 
                                    'Custo do Ativo PM', 'Rentabilidade Atual', 'Rentabilidade Real']]
        dfOpcoes = dfOpcoes.sort_values('Strike', ascending=True)
        return dfOpcoes, action


        