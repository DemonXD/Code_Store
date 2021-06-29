### 使用python 的pika库进行rabbitmq的操作

```python
# 生产者

import time
import pika
import random
from multiprocessing import Process
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

    # def __del__(self):
    #     if self.connection is not None:
    #         self.connection.close()


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
```

```python
# 消费者
import pika
import requests


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
```