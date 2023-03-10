import hashlib
import os
import shutil
import utility


def get(filename: str):
    '''read file as bytes and return '''
    with open(filename, "rb") as f:
        return f.read()


def split(filepath: str):
    '''
    splits the file into multiple segments
    segments are the size of utility.MAX_SEND_BYTES
    segments are saved into a directory with the same filename
    returns the split files directory
    '''
    root, extension = os.path.splitext(filepath)
    source = open(filepath, mode="rb")

    contents = source.read()
    splitDirectory = f"{root}/"
    # gets the number of segments with a default of at least 1
    numOfSegments = max(
        1,
        int(os.stat(filepath).st_size/utility.MAX_SEND_BYTES)
    )

    os.makedirs(os.path.dirname(splitDirectory), exist_ok=True)

    for i in range(1, numOfSegments+1):
        segment = open(f"{splitDirectory}{i}{extension}", 'wb+')

        if (i > numOfSegments):
            segment.write(
                contents[utility.MAX_SEND_BYTES*i -
                         utility.MAX_SEND_BYTES: utility.MAX_SEND_BYTES*i]
            )
        else:
            segment.write(
                contents[utility.MAX_SEND_BYTES*i -
                         utility.MAX_SEND_BYTES:]
            )

        segment.close()

    source.close()
    return root


def hash(filename: str):
    '''
    Computes a sha256 hash for file at filepath

    returns the hash as bytes
    '''
    with open(filename, 'rb') as f:
        content = f.read()

    m = hashlib.sha256()
    m.update(content)
    return m.hexdigest()


def delete(filepath: str):
    '''
    Deletes the given file at filepath

    Includes split files
    '''
    root, extension = os.path.splitext(filepath)

    # remove filepath
    os.remove(filepath)

    # remove split directory
    shutil.rmtree(f"{root}/", ignore_errors=True)

    return f"{filepath} {root}/"


def list(directoryPath: str):
    '''
    Scans the given filepath.

    Returns list of the filenames found in bytes.
    The files are separated by spaces
    '''
    directory = os.scandir(directoryPath)
    return " ".join([entry.name for entry in directory if entry.is_file()])
