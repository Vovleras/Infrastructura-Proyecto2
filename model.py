import matplotlib.pyplot as plt
from arch import arch_model
import pandas as pd
import numpy as np
import os
import pandas_ta 
import ray
import matplotlib.ticker as mtick


class Model:
    def __init__(self,
                 daily_bd="https://raw.githubusercontent.com/Luchkata/Algorithmic_Trading_Machine_Learning/refs/heads/main/simulated_daily_data.csv", 
                 intraday_bd="https://raw.githubusercontent.com/Luchkata/Algorithmic_Trading_Machine_Learning/refs/heads/main/simulated_5min_data.csv"):
        self.daily_file = daily_bd
        self.intraday_file = intraday_bd
        self.daily_df = None
        self.intraday_df = None
        
    def load_data(self):
        self.daily_df = pd.read_csv(self.daily_file)

        self.daily_df = self.daily_df.drop('Unnamed: 7', axis=1)

        self.daily_df['Date'] = pd.to_datetime(self.daily_df['Date'])

        self.daily_df = self.daily_df.set_index('Date')


        self.intraday_df = pd.read_csv(self.intraday_file)

        self.intraday_df = self.intraday_df.drop('Unnamed: 6', axis=1)

        self.intraday_df['datetime'] = pd.to_datetime(self.intraday_df['datetime'])

        self.intraday_df = self.intraday_df.set_index('datetime')

        self.intraday_df['date'] = pd.to_datetime(self.intraday_df.index.date)

        self.intraday_5min_df = self.intraday_df
        
        

    def parallel_model(self):
                
        # Reiniciar Ray
        ray.shutdown()
        ray.init()

        daily_df = self.daily_df

        # Calcular log-retornos y varianza histórica
        daily_df['log_ret'] = np.log(daily_df['Adj Close']).diff()
        daily_df['variance'] = daily_df['log_ret'].rolling(180).var()
        daily_df = daily_df['2020':]

        # --- FUNCIÓN REMOTA RAY ---
        @ray.remote
        def predict_volatility_ray(index, x):
            best_model = arch_model(y=x, p=1, q=3).fit(update_freq=5, disp='off')
            variance_forecast = best_model.forecast(horizon=1).variance.iloc[-1, 0]
            return index, variance_forecast

        # Crear ventanas y asociar a su índice correspondiente
        ventanas = [(daily_df.index[i], daily_df['log_ret'].iloc[i-179:i+1])
                    for i in range(179, len(daily_df))]

        # Filtrar ventanas válidas
        ventanas = [(idx, win) for idx, win in ventanas if win.notnull().all() and np.all(np.isfinite(win))]

        # Enviar cada ventana a Ray
        futuros = [predict_volatility_ray.remote(idx, win) for idx, win in ventanas]

        # Obtener resultados: lista de (fecha, predicción)
        resultados = ray.get(futuros)

        # Insertar las predicciones directamente al daily_df
        for idx, pred in resultados:
            daily_df.at[idx, 'predictions'] = pred

        # Limpiar filas con valores faltantes
        daily_df = daily_df.dropna()
        
        
        
    def execute_parallel_predictions(self):
        
        daily_df = self.daily_df
        
        daily_df['prediction_premium'] = (daily_df['predictions']-daily_df['variance'])/daily_df['variance']

        daily_df['premium_std'] = daily_df['prediction_premium'].rolling(180).std()

        daily_df['signal_daily'] = daily_df.apply(lambda x: 1 if (x['prediction_premium']>x['premium_std'])
                                                else (-1 if (x['prediction_premium']<x['premium_std']*-1) else np.nan),
                                                axis=1)

        daily_df['signal_daily'] = daily_df['signal_daily'].shift()

        daily_df
     
     

    def trading_signals(self):
         daily_df = self.daily_df
        intraday_5min_df = self.intraday_df
        
        final_df = intraday_5min_df.reset_index()\
                                    .merge(daily_df[['signal_daily']].reset_index(),
                                        left_on='date',
                                        right_on='Date')\
                                    .drop(['date','Date'], axis=1)\
                                    .set_index('datetime')

        final_df['rsi'] = pandas_ta.rsi(close=final_df['close'],
                                        length=20)

        final_df['lband'] = pandas_ta.bbands(close=final_df['close'],
                                            length=20).iloc[:,0]

        final_df['uband'] = pandas_ta.bbands(close=final_df['close'],
                                            length=20).iloc[:,2]

        final_df['signal_intraday'] = final_df.apply(lambda x: 1 if (x['rsi']>70)&
                                                                    (x['close']>x['uband'])
                                                    else (-1 if (x['rsi']<30)&
                                                                (x['close']<x['lband']) else np.nan),
                                                    axis=1)

        final_df['return'] = np.log(final_df['close']).diff()

        return final_df
        
    def graphic_frequency(self):
        
        daily_df = self.daily_df
        plt.style.use('ggplot')

        daily_df['signal_daily'].plot(kind='hist')

        plt.show()
        
    def strategy_returns(self, final_df):
        
        final_df['return_sign'] = final_df.apply(lambda x: -1 if (x['signal_daily']==1)&(x['signal_intraday']==1)
                                        else (1 if (x['signal_daily']==-1)&(x['signal_intraday']==-1) else np.nan),
                                        axis=1)

        final_df['return_sign'] = final_df.groupby(pd.Grouper(freq='D'))['return_sign']\
                                        .transform(lambda x: x.ffill())

        final_df['forward_return'] = final_df['return'].shift(-1)

        final_df['strategy_return'] = final_df['forward_return']*final_df['return_sign']

        daily_return_df = final_df.groupby(pd.Grouper(freq='D'))['strategy_return'].sum()
        return daily_return_df
        
    
    def intraday_strategy_returns(self, daily_return_df):

        strategy_cumulative_return = np.exp(np.log1p(daily_return_df).cumsum()).sub(1)

        strategy_cumulative_return.plot(figsize=(16,6))

        plt.title('Intraday Strategy Returns')

        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.ylabel('Return')

        plt.show()        
        
        
        
        
       
       

        
        