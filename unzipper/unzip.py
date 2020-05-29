import zipfile


# a bit redundant function to unzip files
# space reserved for expansion of more unzipping option with more error checking
def unzip_file(file, directory):
    with zipfile.ZipFile(file, 'r') as zip_reference:
        zip_reference.extractall(directory)
