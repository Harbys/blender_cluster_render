import zipfile
import uuid


def create_uuid():
    return uuid.uuid4().hex


def unzip(file, temp):
    with zipfile.ZipFile(file, 'r') as zip_reference:
        identifier = create_uuid()
        zip_reference.extractall(temp+id)
    return identifier
