"""Program utilities."""
from random import choice
import uuid


def id_generator():
    """Generate custom 4 digit unique IDs."""
    raw_uuid = uuid.uuid4()
    code = ''
    datalist = []
    for c in str(raw_uuid):
        datalist += str((ord(c)))
    for i in range(4):
        code += choice(datalist)
    if int(code) < 999:
        return id_generator()
    else:
        return int(code)
