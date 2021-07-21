from gladier import GladierBaseTool, GladierBaseClient, generate_flow_definition
from pprint import pprint


def decrypt (**data):

    """ Decrypt tool takes in an encrypted file and a password to perform decryption on the file.
    The decryption only works on files that have been encrypted by the Gladier Encrypt tool. 
    It has not been found to be compatible with 3rd party encryption/decryption tools. """

    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
    import base64


    password = bytes(data['decrypt_key'], 'utf-8')
    ckdf = ConcatKDFHash(algorithm=hashes.SHA256(),length=32,otherinfo=None,)
    key = base64.urlsafe_b64encode(ckdf.derive(password))
    fernet = Fernet(key)

    infile= data['decrypt_input']
    if '~' in infile:
        infile = os.path.expanduser(infile)

    outfile= data.get('decrypt_output', infile[:len(infile)-4])
    print(outfile)
    if '~' in outfile:
        outfile = os.path.expanduser(outfile)

    with open(infile, 'rb') as file:
        encrypted= file.read()
    decrypted= fernet.decrypt(encrypted)
    with open(outfile, 'wb') as out:
        out.write(decrypted)
        
    return outfile


@generate_flow_definition
class Decrypt(GladierBaseTool):
    funcx_functions = [decrypt]
    required_input = [
        'decrypt_input',
        'decrypt_key',
        'funcx_endpoint_compute'
    ]
