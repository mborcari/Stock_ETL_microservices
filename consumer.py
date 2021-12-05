import pika
import json
from decouple import config
from pipeline import run_pipeline

rabbitmq_key = config('RABBITMQ_KEY')
params = pika.URLParameters(rabbitmq_key)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='get_historical', durable=True)
queue_name = 'get_historical'


def callback(ch, method, properties, body):
    print(f'Receive message from {queue_name}')
    try:
        data = json.loads(body)
        historical = run_pipeline(
                data["code_stock"],
                data["data_source"],
                data["start_date"],
                data["end_date"])
    except json.JSONDecodeError as e:
        print(f'Read fail on body {body}, erro:', e)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(f'Started consume waiting message from queue {queue_name}')
channel.start_consuming()
