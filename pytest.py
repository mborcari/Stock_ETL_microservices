from datetime import date
from pandas.core.frame import DataFrame
from pipeline import get_data_historial_stock, transformation_data
DATA_EXEMPLE = ('GNDI3', 'investing', date(2021, 11, 1), date(2021, 11, 2))

def test_data_set(DATA_EXEMPLO):
    code_stock = DATA_EXEMPLO[0]
    start_date = DATA_EXEMPLO[2]
    data = get_data_historial_stock(*DATA_EXEMPLO)
    assert type(data) == DataFrame
    data_after_trasformation = transformation_data(code_stock, data)
    assert type(data_after_trasformation) == dict

test_data_set(DATA_EXEMPLO)

