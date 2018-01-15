#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
import time, pika, re,json
from threading import Thread


class FibonacciRpcClient(object):
    def __init__(self):

        credentials = pika.PlainCredentials('admin', 'admin')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            '10.1.1.191', 5672, '/', credentials))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response,  # 只要已收到消息就调用on_response
                                   no_ack=True,
                                   queue=self.callback_queue)
        self.response = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, corr_id, msg):
        self.corr_id = corr_id
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       content_type='application/json',
                                       correlation_id= self.corr_id,

                                   ),
                                   body=msg)
        while self.response is None:
            self.connection.process_data_events() #非阻塞版的start_consuming()
            time.sleep(0.5)
        time.sleep(30)
        return self.response

    def get_response(self):
        return self.response

def interactive():
    """交互"""
    obj_dic = {}
    while True:
        client_input = input(">>").strip()
        if re.search('^\s*check_task\s+\d{10}$',client_input):
            id = client_input.split()[1]
            res = obj_dic[id].get_response()
            if res:print('result:\n',res.decode())
            else:print('正在获取结果，稍后再试。。。')
        elif re.search(r'\s*run\s+.+--hosts\s+\d+.\d+.\d+.\d+.*\d+\s*$',client_input):
            corr_id = str(int(time.time()))
            print('task_id:', corr_id)
            obj_name = FibonacciRpcClient()
            if '"' in client_input:
                cmd = client_input.split('"')[1]
            elif "'" in client_input:
                cmd = client_input.split("'")[1]
            hosts_list = re.findall(r'\d+.\d+.\d+.\d+',client_input)
            msg = {'CMD': cmd,
                   'hosts': hosts_list}
            p = Thread(target=obj_name.call, args=(corr_id, json.dumps(msg),))

            p.setDaemon(True)
            p.start()
            obj_dic[corr_id] = obj_name
        else:
            print('input error.')


interactive()
