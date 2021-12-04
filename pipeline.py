import traceback
from datetime import date, datetime
from investpy import get_stock_historical_data, get_index_historical_data
from pandas_datareader import data as pdr
import yfinance as yfin

from producer import publish

yfin.pdr_override()


def format_volume(open_value, close_value, volume):
    '''
    Utilite function. Formate volume.
    '''
    media = (float(open_value) + float(close_value)) / 2
    return int(int(volume) * media)


def get_data_from_investing(code_stock, start_date, end_date):
    """
    Get data from investing
    """
    start_date_investing = datetime.strftime(start_date, '%d/%m/%Y')
    end_date_investing = datetime.strftime(end_date, '%d/%m/%Y')
    # Se cpodigo é ibov, a chamado no investing é diferente
    if code_stock == 'IBOV':
        try:
            return get_index_historical_data(index='Bovespa',
                                             country='brazil',
                                             from_date=start_date_investing,
                                             to_date=end_date_investing,
                                             order='desc')
        except Exception as e:
            print(traceback.print_exc())
            return
    else:
        try:
            return get_stock_historical_data(stock=code_stock,
                                             country='brazil',
                                             from_date=start_date_investing,
                                             to_date=end_date_investing,
                                             order='desc'
                                             )
        except Exception as e:
            print(traceback.print_exc())
            return


def get_data_yahoo_finance(code_stock, start_date, end_date):

    start_date_yahoo = datetime.strftime(start_date, '%Y-%m-%d')
    end_date_yahoo = datetime.strftime(end_date, '%Y-%m-%d')

    code_stock = '^BVSP' if code_stock == 'IBOV' else '%s.SA' % code_stock
    try:

        data = pdr.DataReader(code_stock, data_source="yahoo", start=start_date_yahoo, end=end_date_yahoo)
        return data
    except Exception as e:
        print(traceback.print_exc())
        return


def get_data_historial_stock(code_stock, source_data, start_date, end_date):
    """Get historcal stock from external APIs

    Args:
        code_stock (str): stock code
        source_data (str): source api like investing, yahoo finance
        start_date (date): start date from start query
        end_date (date): until end date

    return:
       Dataframe with historical data
    """
    # change string to datetime
    start_date = datetime.strptime(start_date, '%d-%m-%Y')
    end_date = datetime.strptime(end_date, '%d-%m-%Y')

    if source_data == 'investing':
        return get_data_from_investing(code_stock, start_date, end_date)
    elif source_data == 'yahoo_finance':
        return get_data_yahoo_finance(code_stock, start_date, end_date)
    else:
        return


def transformation_data(code_stock, dataframe) -> dict:
    """ Realiza a análise do historico de um ativo, tratando os valores
        como abertura, fechamento, mínina, máxima e volume

    Args:
        code_stock (str): Código do ativo
        dataframe ([Datagframe]): Lista ou dicionário com os dados do histórico

    Returns:
        dict: retorna um dicionário no formato necessário para o schema do banco de dadaos.
    """

    historical = {"code_stock": code_stock, 'data': {}}
    if dataframe is not None:
        for index in dataframe.index:
            index_date = datetime.strftime(index, '%d-%m-%Y')
            historical['data'][index_date] = {}
            if code_stock == 'IBOV':
                historical['data'][index_date]['open'] = int(dataframe.loc[index, 'Open'])
                historical['data'][index_date]['close'] = int(dataframe.loc[index, 'Close'])
                historical['data'][index_date]['low'] = int(dataframe.loc[index, 'Low'])
                historical['data'][index_date]['high'] = int(dataframe.loc[index, 'High'])
                historical['data'][index_date]['volume'] = int(dataframe.loc[index, 'Volume'])

            else:
                historical['data'][index_date]['open'] = dataframe.loc[index, 'Open']
                historical['data'][index_date]['close'] = dataframe.loc[index, 'Close']
                historical['data'][index_date]['low'] = dataframe.loc[index, 'Low']
                historical['data'][index_date]['high'] = dataframe.loc[index, 'High']
                historical['data'][index_date]['volume'] = format_volume(
                    historical['data'][index_date]['open'],
                    historical['data'][index_date]['close'],
                    dataframe.loc[index, 'Volume']
                )
    return historical


def run_pipeline(code_stock, source_data, start_date, end_date):
    """
        Run pipile to get data, transforme and call producer mq
    """

    datagrama = get_data_historial_stock(code_stock, source_data, start_date, end_date)
    if datagrama is not None:
        dict_data = transformation_data(code_stock, datagrama)
        publish(dict_data)
