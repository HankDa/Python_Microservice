from basicClient import BasicPikaClient
import json



class BasicMessageSender(BasicPikaClient):

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()

if __name__ == "__main__":

    # Initialize Basic Message Sender which creates a connection
    # and channel for sending messages.
    with open("config.json") as config_file:
        config_data = json.load(config_file)
    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    MQ_BROKER_ID = config_data["MQ_BROKER_ID"]
    MQ_USERNAME = config_data["MQ_USERNAME"]
    MQ_PASSWORD = config_data["MQ_PASSWORD"]
    MQ_REGION = config_data["MQ_REGION"]
    
    basic_message_sender = BasicMessageSender(
        MQ_BROKER_ID,
        MQ_USERNAME,
        MQ_PASSWORD,
        MQ_REGION
    )

    # Declare a queue
    basic_message_sender.declare_queue("hello world queue")

    # Send a message to the queue.
    basic_message_sender.send_message(exchange="", routing_key="hello world queue", body=b'Hello World!')

    # Close connections.
    basic_message_sender.close()