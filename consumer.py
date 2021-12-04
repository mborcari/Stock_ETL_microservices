import pika
import json
import os
from pipeline import run_pipeline

rabbitmq_key = os.getenv('rabbitmq_key')
params = pika.URLParameters(rabbitmq_key)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='get_historical')
queue_name = 'get_historical'


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        historical = run_pipeline(
                data["code_stock"],
                data["data_source"],
                data["start_date"],
                data["end_date"])
    except json.JSONDecodeError as e:
        print(f'Falha ao interpretar body {body} para dict, erro:', e)
    # except KeyError as e:
    #     print(f'Error. Necessário verificar o dicionários recebido no callback {data}', e)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Started consume to get historical from external API.')
channel.start_consuming()
