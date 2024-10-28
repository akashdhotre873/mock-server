from django.db import models

# Create your models here.
class MockHTTPEntity():
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    