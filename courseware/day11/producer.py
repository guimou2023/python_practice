__author__ = "Alex Li"
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
    )
channel = connection.channel()  #声明一个管道
# 声明queue
channel.queue_declare(queue='hello2',durable=True)

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='hello2',#queue名字
                      body='Hello World!==gfvhg==',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      )
                      )

print(" [x] Sent 'Hello World!'")
connection.close()