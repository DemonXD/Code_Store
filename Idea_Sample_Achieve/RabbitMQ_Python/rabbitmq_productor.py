#################################
# Date: 2021/06/21
# Author: Miles Xu
# Email: kanonxmm@163.com
# Desc.: pika, rabbitmq, 生产者
#################################
# -*- coding: utf-8 -*-

import time
import pika
import random
from threading import Thread


class RABBIRMQ:
    hostname = "127.0.0.1"
    credentials = pika.PlainCredentials("miles", "miles")
    
    def __init__(self, queue_name, exchange_="") -> None:
        paras = pika.ConnectionParameters(
            self.hostname, 5672, "my_vhost", self.credentials)
        self.connection = pika.BlockingConnection(paras)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.routing_key = queue_name
        self.exchange = exchange_

    def send(self, msg):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.routing_key,
                                   body=msg)

def product(goods: str) -> None:
    rmq = RABBIRMQ("miles")
    for idx in range(10):
        body = goods+str(idx)
        print(f"product: [{idx} {str(idx)}]- [{body}]")
        rmq.send(body)
        time.sleep(random.randint(1,4))


def main():
    thread1 = Thread(target=product, args=("goods",)).start()
    thread2 = Thread(target=product, args=("goods",)).start()
    thread3 = Thread(target=product, args=("goods",)).start()

    while 1:
      time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass