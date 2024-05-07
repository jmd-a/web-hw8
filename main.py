from mongoengine import Document, StringField, ReferenceField, ListField
import json
import connect

connect.connect_to_db()


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)


def load_data():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_fullname = quote_data.pop('author')
            author = Author.objects(fullname=author_fullname).first()
            quote_data['author'] = author
            quote = Quote(**quote_data)
            quote.save()


def search_quotes(criteria):
    if criteria.startswith('name:'):
        author_name = criteria.split(':')[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
        else:
            return []

    elif criteria.startswith('tag:'):
        tag = criteria.split(':')[1].strip()
        quotes = Quote.objects(tags=tag)
        return quotes

    elif criteria.startswith('tags:'):
        tags = criteria.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        return quotes

    elif criteria == 'exit':
        return []

    else:
        print("Invalid command format. Please use one of the following formats:")
        print("name: author_name")
        print("tag: tag_name")
        print("tags: tag1,tag2")
        print("exit")
        return []


load_data()

while True:
    criteria = input("Enter your search criteria (or type 'exit' to quit): ")
    quotes = search_quotes(criteria)
    for quote in quotes:
        print(f"Author: {quote.author.fullname}")
        print(f"Quote: {quote.quote}")
        print(f"Tags: {', '.join(quote.tags)}")
        print("=" * 50)
