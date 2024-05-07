import pika
from faker import Faker
from mongoengine import Document, StringField, BooleanField
import connect

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

connect.connect_to_db()


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    is_sent = BooleanField(default=False)


def create_fake_contacts(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()


def send_contact_ids_to_queue():
    contacts = Contact.objects(is_sent=False)
    for contact in contacts:
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=str(contact.id))
        contact.is_sent = True
        contact.save()


if __name__ == "__main__":
    num_contacts = 10
    create_fake_contacts(num_contacts)
    send_contact_ids_to_queue()
