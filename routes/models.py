import json

from django.db import models


# Create your models here.
class MockHTTPEntity:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __str__(self):
        url = self.__getattribute__("url")
        method = self.__getattribute__("method")
        response = self.__getattribute__("response")
        status = self.__getattribute__("status")
        return (
            "url: "
            + url
            + ", method: "
            + method
            + ", resp: "
            + json.dumps(response)
            + ", status: "
            + status
        )
