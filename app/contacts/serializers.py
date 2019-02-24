import os

from rest_framework import serializers


class ContactsFileUploadSerializer(serializers.Serializer):
    n_rows = serializers.IntegerField(default=1)
    file = serializers.FileField()

    def save(self):
        pass


class ContactsParseRowsSerializer(serializers.Serializer):
    filename = serializers.CharField()
    mapped_rows = serializers.DictField()
