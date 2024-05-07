import pika
from producer import Contact
import connect

connect.connect_to_db()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
channel = connection.channel()
channel.queue_declare(queue='email_queue')


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects.get(id=contact_id)
    contact.is_sent = True
    contact.save()
    print(contact_id)


channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
