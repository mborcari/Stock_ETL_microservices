import pika
import json
from decouple import config

rabbitmq_key = config('RABBITMQ_KEY')
params = pika.URLParameters(rabbitmq_key)
queue_name = 'return_historical'


def publish(dict_data):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    print(f'Send message to the queue: {queue_name}')
    dict_data = json.dumps(dict_data)
    channel.basic_publish(exchange='', routing_key=queue_name, body=dict_data)
