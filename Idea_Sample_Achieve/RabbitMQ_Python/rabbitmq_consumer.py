#################################
# Date: 2021/06/21
# Author: Miles Xu
# Email: kanonxmm@163.com
# Desc.: pika, rabbitmq, 消费者
#################################
# -*- coding: utf-8 -*-

import pika


def callback_(ch, method, properties, body):
    #发送应答信号
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


class RABBITMQ_CONSUMER:
    hostname = "127.0.0.1"
    credentials = pika.PlainCredentials("miles", "miles")
    def __init__(self, queue_name):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                self.hostname, 5672, "my_vhost", self.credentials))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

        self.channel.basic_consume(queue=queue_name,
                                   auto_ack=False,
                                   on_message_callback=callback_)

    def run(self):
        self.channel.start_consuming()


if __name__ == "__main__":
    try:
        mq_consumer = RABBITMQ_CONSUMER("miles")
        mq_consumer.run()
    except KeyboardInterrupt:
        pass