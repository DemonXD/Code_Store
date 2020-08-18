# controller.py

from model import Book, Person, OlvBook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    
    def __init__(self):
        super().__init__()
        self.session = self.connect_to_database()
        
    def connect_to_database(self):
        """
        Connect to our SQLite database and return a Session object
        """
        engine = create_engine("sqlite:///books.db", echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def add_record(self, data):
        """
        Data should be a tuple of two dictionaries in the following format:
     
        ("author":{"first_name":"John", "last_name":"Doe"},
         "book":{"title":"Some book", "isbn":"1234567890", 
                 "publisher":"Packt"}
        )
        """
        book = Book()
        book.title = data["book"]["title"]
        book.isbn = data["book"]["isbn"]
        book.publisher = data["book"]["publisher"]
        author = Person()
        author.first_name = data["author"]["first_name"]
        author.last_name = data["author"]["last_name"]
        book.person = author
        
        self.session.add(book)
        self.session.commit()

    def convert_results(self, results):
        """
        Convert results to OlvBook objects
        """
        books = []
        for record in results:
            author = "%s %s" % (record.person.first_name, 
                                record.person.last_name)
            book = OlvBook(record.id, record.title, author,
                           record.isbn, record.publisher,
                           record.person.last_name,
                           record.person.first_name
                           )
            books.append(book)
        return books

    def delete_record(self, id_num):
        """
        Delete a record from the database
        """
        record = session.query(Book).filter_by(id=id_num).one()
        self.session.delete(record)
        self.session.commit()
    
    
    def edit_record(self, id_num, row):
        """
        Edit a record
        """
        record = session.query(Book).filter_by(id=id_num).one()
        record.title = row["title"]
        record.person.first_name = row["first_name"]
        record.person.last_name = row["last_name"]
        record.isbn = row["isbn"]
        record.publisher = row["publisher"]
        self.session.add(record)
        self.session.commit()
    
    def get_all_records(self):
        """
        Get all records and return them
        """
        result = self.session.query(Book).all()
        books = convert_results(result)
        return books
     
    def search_records(self, filter_choice, keyword):
        """
        Searches the database based on the filter chosen and the keyword
        given by the user
        """
        if filter_choice == "Author":
            qry = self.session.query(Person)
            result = qry.filter(Person.first_name.contains('%s' % keyword)).all()
            records = []
            for record in result:
                for book in record.books:
                    records.append(book)
            result = records
        elif filter_choice == "Title":
            qry = self.session.query(Book)
            result = qry.filter(Book.title.contains('%s' % keyword)).all()
        elif filter_choice == "ISBN":
            qry = self.session.query(Book)
            result = qry.filter(Book.isbn.contains('%s' % keyword)).all()
        else:
            qry = self.session.query(Book)
            result = qry.filter(Book.publisher.contains('%s' % keyword)).all()
        books = convert_results(result)
        
        return books

def setup_database():
    """"""
    metadata.create_all()
