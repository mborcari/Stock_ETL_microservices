import pika
import json
import os

rabbitmq_key = os.getenv('rabbitmq_key')
params = pika.URLParameters(rabbitmq_key)

connection = pika.BlockingConnection(params)
channel = connection.channel()
queue_name = 'return_historical'


def publish(dict_data):
    print(f'Publish queue: {queue_name}')
    dict_data = json.dumps(dict_data)
    channel.basic_publish(exchange='', routing_key=queue_name, body=dict_data)
