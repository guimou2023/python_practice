__author__ = "Alex Li"

import pika
import time
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='hello2',durable=True)


def callback(ch, method, properties, body): #回调函数
    print("-->",ch,method,properties)
    #time.sleep(30)
    print(" [x] Received %r" % body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(#消费消息
                    callback, #如果收到消息，就调用CALLBACK 函数来处理消息
                    queue='hello2',
                    #no_ack=True #no ackownledgement
                    )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()