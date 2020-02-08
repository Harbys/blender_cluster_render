import zipfile


def unzip_file(file, temp):
    with zipfile.ZipFile(file, 'r') as zip_reference:
        zip_reference.extractall(temp)
