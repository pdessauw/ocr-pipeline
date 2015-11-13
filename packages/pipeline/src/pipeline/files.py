"""Package defining Redis file manager

.. Authors:
    Philippe Dessauw
    philippe.dessauw@nist.gov

.. Sponsor:
    Alden Dima
    alden.dima@nist.gov
    Information Systems Group
    Software and Systems Division
    Information Technology Laboratory
    National Institute of Standards and Technology
    http://www.nist.gov/itl/ssd/is
"""
# import base64
from os import remove
from mongoengine.connection import connect, disconnect
from mongoengine.document import Document
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from mongoengine.fields import StringField, FileField
# import redis

class OCRDocument(Document):
    filename = StringField(required=True)
    zipfile = FileField()


class FileManager(object):
    """Redis file manager
    """

    def __init__(self, host="127.0.0.1", port=6379, db="pipeline"):
        # self.server = redis.StrictRedis(host, port, db)
        # self.hashmap_name = "fman"
        connect(db, host=host)

    def close(self):
        disconnect()

    def empty(self):
        for file_object in OCRDocument.objects.all():
            file_object.zipfile.delete()
            file_object.delete()

    def retrieve_file(self, filename):
        """Retrieve from redis hashmap

        Args
            filename (str): Filename to retrieve
        """
        # b64_hash = self.server.hget(self.hashmap_name, filename)
        # data = base64.b64decode(b64_hash)
        file_object = OCRDocument.objects.get(filename=filename)

        with open(file_object.filename, 'wb') as zip_file:
            data = file_object.zipfile.read()
            zip_file.write(data)

        self.delete_file(filename)

    def store_file(self, filename):
        """Store file to redis hashmap

        Args
            filename (str): Filename to store
        """
        try:
            file_object = OCRDocument.objects.get(filename=filename)
            self.delete_file(file_object.filename)

            o = OCRDocument()
            o.filename = filename

            with open(filename, 'rb') as zip_file:
                # b64_hash = base64.b64encode(zip_file.read())
                o.zipfile.put(zip_file)

            o.save()
            remove(filename)

        except DoesNotExist:
            o = OCRDocument()
            o.filename = filename

            with open(filename, 'rb') as zip_file:
                # b64_hash = base64.b64encode(zip_file.read())
                o.zipfile.put(zip_file)

            o.save()

            # self.server.hset(self.hashmap_name, filename, b64_hash)
            remove(filename)

    def delete_file(self, filename):
        """Delete file from redis hashmap

        Args
            filename (str): Filename to delete
        """
        # self.server.hdel(self.hashmap_name, filename)
        # TODO add log
        file_object = OCRDocument.objects.get(filename=filename)
        file_object.zipfile.delete()
        file_object.delete()
