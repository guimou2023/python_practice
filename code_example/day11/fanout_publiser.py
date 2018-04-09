__author__ = "Alex Li"

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')
#message = ' '.join(sys.argv[1:]) or "info: Hello World!"
message = "info: Hello World!2"

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print(" [x] Sent %r" % message)

connection.close()