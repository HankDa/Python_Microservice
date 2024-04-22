import json
import ssl
import pika

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


class BasicMessageSender(BasicPikaClient):

    def send_message(self, exchange, routing_key, body, properties):
        #TODO: why should we declare a new channel here? 
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body,
                              properties=properties)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        #TODO: the channel created in send message is not closed? 
        self.channel.close()
        self.connection.close()


def publish(method, body):

    # Initialize Basic Message Sender which creates a connection
    # TODO: Read credential from config.json. What is the more efficient way to do that?
    with open("config.json") as config_file:
        config_data = json.load(config_file)
    
    basic_message_sender = BasicMessageSender(
        config_data["MQ_BROKER_ID"],
        config_data["MQ_USERNAME"],
        config_data["MQ_PASSWORD"],
        config_data["MQ_REGION"]
    )
    properties = pika.BasicProperties(method)
    print("properties:", properties)
    # Send a message to the queue.
    # json.dumps() convert json to string
    basic_message_sender.send_message(exchange="", 
                                      routing_key="main", 
                                      body=json.dumps(body),
                                      properties=properties)

    # Close connections.
    basic_message_sender.close()
