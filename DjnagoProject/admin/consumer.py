import json, ssl, pika, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

# consumer.py is outside of Django
from products.models import Product

class BasicPikaClient:

    def __init__(self, rabbitmq_broker_id, rabbitmq_user, rabbitmq_password, region):

        # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671"
        parameters = pika.URLParameters(url)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()


class BasicMessageReceiver(BasicPikaClient):

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)
    
    def declare_exchange(self, exchange_name, exchange_type):
        print(f"Trying to declare exchange({exchange_name})...")
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, passive=True)

    def bind_exchange_queue(self, queue_name, exchange_name, routing_key):
        print(f"Bind exchange({exchange_name}) with queue({queue_name}) by routing_key({routing_key}) ...")
        self.channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            print('Received in admin')
            id = json.loads(body)
            print(id)
            # as we don't reply for REST requst, we don't used serializer here.
            product = Product.objects.get(id=id)
            product.like = product.like + 1
            product.save()
            print('Product likes increased!')

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def get_message(self, queue):
        # method_frame: ['delivery_tag=1', 'exchange=exchange_1', 'message_count=1', 'redelivered=False', 'routing_key=routing_key_1']
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return method_frame, header_frame, body
        else:
            print('No message returned')

    def close(self):
        #TODO: the channel created in send message is not closed? 
        self.channel.close()
        self.connection.close()


if __name__ == "__main__":

    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    with open("config.json") as config_file:
        config_data = json.load(config_file)
    
    basic_message_receiver = BasicMessageReceiver(
        config_data["MQ_BROKER_ID"],
        config_data["MQ_USERNAME"],
        config_data["MQ_PASSWORD"],
        config_data["MQ_REGION"]
    )

    # # Declare a exchange
    # basic_message_receiver.declare_exchange("exchange_1", "direct")

    # Declare a queue
    basic_message_receiver.declare_queue("admin")

    # # bind exchange with queue
    # basic_message_receiver.bind_exchange_queue("admin", "exchange_1", "admin_1")

    # Consume the message that was sent.
    basic_message_receiver.consume_messages("admin")

    # Close connections.
    basic_message_receiver.close()
