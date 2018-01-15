#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"
import pika, paramiko, json
from multiprocessing import Manager, Process
from conf.settings import CONFIG


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '10.1.1.191', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def coon(ip, cmd, rec_list):

    host_ssh_config = CONFIG['0']
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=ip, port=host_ssh_config[0], username=host_ssh_config[1], password=host_ssh_config[2])

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    result_stdout = stdout.read()
    result_stderr = stderr.read()
    result = result_stdout.decode() if result_stdout.decode() else result_stderr.decode()
    result = 'host:{}\n{}'.format(ip, result)

    ssh.close()
    rec_list.append(result)
    return result


def result_join(cmd,hosts):
    rec_list = Manager().list()
    jobs = []
    for ip in hosts:
        p = Process(target=coon, args=(ip, cmd, rec_list))
        p.start()
        jobs.append(p)
    for i in jobs:
        i.join()
    return '\n'.join(rec_list)


def on_request(ch, method, props, body):
    msg = json.loads(body)
    cmd = msg['CMD']
    hosts_list = msg['hosts']
    response = result_join(cmd, hosts_list)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()