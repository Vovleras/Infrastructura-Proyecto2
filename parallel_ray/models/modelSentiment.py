import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import os
import time
import ray
import yfinance as yf
import pandas as pd
from typing import List
import matplotlib.ticker as mtick

plt.style.use('ggplot')


class ModelSentiment:
    def __init__(self, sentiment_df="https://raw.githubusercontent.com/SalomeAc/Infraestructuras-proyecto/refs/heads/main/sentiment_data.csv"):
        self.sentiment_df = sentiment_df
        
    def load_data(self):
        
        url = self.sentiment_df
        sentiment_df = pd.read_csv(url)

        sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])

        sentiment_df = sentiment_df.set_index(['date', 'symbol'])

        sentiment_df['engagement_ratio'] = sentiment_df['twitterComments']/sentiment_df['twitterLikes']

        sentiment_df = sentiment_df[(sentiment_df['twitterLikes']>20)&(sentiment_df['twitterComments']>10)]

        return sentiment_df
        
    def aggregate_sentiment(self, sentiment_df):
        
        aggragated_df = (sentiment_df.reset_index('symbol').groupby([pd.Grouper(freq='M'), 'symbol'])
                    [['engagement_ratio']].mean())

        aggragated_df['rank'] = (aggragated_df.groupby(level=0)['engagement_ratio']
                                .transform(lambda x: x.rank(ascending=False)))

        return aggragated_df
        
    def filtered_sentiment(self, aggragated_df):
        filtered_df = aggragated_df[aggragated_df['rank']<6].copy()

        filtered_df = filtered_df.reset_index(level=1)

        filtered_df.index = filtered_df.index+pd.DateOffset(1)

        filtered_df = filtered_df.reset_index().set_index(['date', 'symbol'])

        filtered_df.head(20)
        
        return filtered_df
    
    def fixed_dates(self, filtered_df):
        dates = filtered_df.index.get_level_values('date').unique().tolist()

        fixed_dates = {}

        for d in dates:

            fixed_dates[d.strftime('%Y-%m-%d')] = filtered_df.xs(d, level=0).index.tolist()

        return fixed_dates
    
    def parallel_ray_sentiment(self, sentiment_df):
        
        # Conectar a Ray cluster o inicializar localmente
        if not ray.is_initialized():
            try:
                ray.init(address="ray://ray:10001")
            except:
                ray.init()

        @ray.remote
        def download_stock_batch(tickers: List[str], start_date: str, end_date: str, auto_adjust: bool) -> pd.DataFrame:
            """Función remota para descargar un lote de acciones."""
            try:
                data = yf.download(tickers=tickers, start=start_date, end=end_date,
                                auto_adjust=auto_adjust, progress=False)
                return data
            except Exception as e:
                print(f"Error descargando lote {tickers}: {str(e)}")
                return pd.DataFrame()

        def parallel_stock_download(stocks_list: List[str], start_date: str = '2021-01-01',
                                end_date: str = '2023-03-01', auto_adjust: bool = False,
                                batch_size: int = 10) -> pd.DataFrame:
            """Descarga datos de acciones en paralelo usando Ray."""

            # Dividir la lista en lotes
            batches = [stocks_list[i:i + batch_size] for i in range(0, len(stocks_list), batch_size)]

            # Crear tareas remotas para cada lote
            futures = [download_stock_batch.remote(batch, start_date, end_date, auto_adjust)
                    for batch in batches]

            # Obtener resultados
            results = ray.get(futures)

            # Combinar resultados válidos
            valid_dataframes = [df for df in results if not df.empty]

            if valid_dataframes:
                return pd.concat(valid_dataframes, axis=1)
            else:
                return pd.DataFrame()

        # Función para tu código específico
        def download_stock_data_parallel(sentiment_df):
            """Reemplaza tu código original con paralelización Ray."""
            stocks_list = sentiment_df.index.get_level_values('symbol').unique().tolist()
            excluded = ['MRO', 'ATVI']
            stocks_list = [s for s in stocks_list if s not in excluded]

            prices_df = parallel_stock_download(
                stocks_list=stocks_list,
                start_date='2021-01-01',
                end_date='2023-03-01',
                auto_adjust=False
            )
            return prices_df


        prices_df = download_stock_data_parallel(sentiment_df)
        return prices_df
       
        
        
    def portfolio_analysis(self, prices_df, fixed_dates):
        # Calcular log-retornos desde precios
        returns_df = np.log(prices_df['Adj Close']).diff().dropna()

            # Crear DataFrame para el portafolio
        portfolio_df = pd.DataFrame()

            # Recorrer cada fecha de inicio en la estrategia de portafolio
        for start_date in fixed_dates.keys():

                # Calcular la fecha de fin (último día del mes)
            end_date = (pd.to_datetime(start_date) + pd.offsets.MonthEnd()).strftime('%Y-%m-%d')

                # Obtener los tickers seleccionados para ese mes
            cols = fixed_dates[start_date]

                # Filtrar columnas que realmente existen en returns_df
            valid_cols = [c for c in cols if c in returns_df.columns]

                # Si hay columnas válidas, calcular retorno promedio del portafolio
            if valid_cols:
                temp_df = returns_df.loc[start_date:end_date, valid_cols].mean(axis=1).to_frame('portfolio_return')
                portfolio_df = pd.concat([portfolio_df, temp_df])
            else:
                print(f"⚠️  Sin tickers válidos en {start_date}, se omite este mes.")

            # Mostrar portafolio final
        return portfolio_df

    def add_benchmark_comparison(self, portfolio_df):
            
        qqq_df = yf.download(
                tickers='QQQ',
                start='2021-01-01',
                end='2023-03-01',
                auto_adjust=False  
        )


        print(type(qqq_df['Adj Close']))

        qqq_ret = np.log(qqq_df['Adj Close']).diff()
        qqq_ret.columns = ['nasdaq_return']



        portfolio_df = portfolio_df.merge(qqq_ret, left_index=True, right_index=True)

        return portfolio_df
    
    def graphic_engament_ratio(self,portfolio_df):
        portfolios_cumulative_return = np.exp(np.log1p(portfolio_df).cumsum()).sub(1)

        portfolios_cumulative_return.plot(figsize=(16,6))

        plt.title('Twitter Engagement Ratio Strategy Return Over Time')

        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

        plt.ylabel('Return')

        plt.show()
    
    def test_ray_connection(self):
        """
        Prueba la conexión con Ray
        """
        try:
            if not ray.is_initialized():
                try:
                    ray.init(address="ray://ray:10001")
                except:
                    ray.init()
            
            # Prueba simple
            @ray.remote
            def test_function(x):
                return x * 2
            
            result = ray.get(test_function.remote(5))
            return result == 10
            
        except Exception as e:
            print(f"Error en Ray: {e}")
            return False

        
    

