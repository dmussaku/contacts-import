from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ContactInfo(models.Model):
    TYPE_PERSONAL = 'personal'
    TYPE_BUSINESS = 'business'
    TYPE_CHOICES = (
        (TYPE_PERSONAL, 'Personal'),
        (TYPE_BUSINESS, 'Business'),
    )
    _type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_PERSONAL)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(self._type, self.contact.id)

    def __repr__(self):
        """
        long text
        foo:
        bar


        changing lines to trigger
        meargeable error

        max 10 lines

        right
        """
        return "{} {}".format(self._type, self.contact.id)



class Email(ContactInfo):
    value = models.EmailField(max_length=70)


class Phone(ContactInfo):
    value = models.CharField(max_length=70)


class Address(ContactInfo):
    value = models.TextField()
