import csv
import os
from itertools import product
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import (
    Contact,
    ContactInfo,
    Address,
    Email,
    Phone,
)


CONTACTS_FILES_DIR = os.path.join(settings.BASE_DIR, '..', 'data')
CONTACT_INFO_TYPES = list(product(
    map(lambda model: model._meta.model_name, (Address, Email, Phone)),
    [ContactInfo.TYPE_PERSONAL, ContactInfo.TYPE_BUSINESS],
))


@login_required
@require_http_methods(['POST'])
def upload_contacts_file(request):
    """
    Uploads a file to a server
    Responds with:
    - Mapping contactinfo types
    - List of n rows specified by a request param "rows"
    - Filename in the system
    """
    n_rows = request.GET.get('rows', 1)
    uploaded_file = request.FILES['myfile']
    filename = str(uuid4()).replace('-', '')
    save_path = os.path.join(CONTACTS_FILES_DIR, filename)

    with open(save_path, 'wb+') as saved_file:
        for chunk in uploaded_file.chunks():
            saved_file.write(chunk)

    decoded_file = uploaded_file.read().decode('utf-8').splitlines()
    reader = csv.Reader(decoded_file)
    returned_rows = [row for row in reader[0: n_rows]]

    return JsonResponse({
        'filename': filename,
        'returned_rows': returned_rows,
        'mapped_contact_types': CONTACT_INFO_TYPES,
    })


@login_required
@require_http_methods(['POST'])
def import_contacts(request):
    filename = request.POST.get('filename')
    mapped_rows = request.POST.get('mapped_rows')

    
    decoded_file = myfile.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        Contact.objects.create(
            first_name=row['first_name'],
            last_name=row['last_name'],
            phone=row['phone'],
            email=row['email'],
            created_by=request.user,
        )
    return HttpResponse('ok')
