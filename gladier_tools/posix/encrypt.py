from gladier import GladierBaseTool, GladierBaseClient, generate_flow_definition
from pprint import pprint


def encrypt(**data):

    """ Encrypt tool takes in a file and a password to perform 128-bit AES encryption on the file. 
    It has not been found to be compatible with 3rd party encryption/decryption tools. """

    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
    import base64

    password = bytes(data['encrypt_key'], 'utf-8')
    ckdf = ConcatKDFHash(algorithm=hashes.SHA256(),length=32,otherinfo=None,)
    key = base64.urlsafe_b64encode(ckdf.derive(password))
    fernet = Fernet(key)
    
    infile= data['encrypt_input']
    

    if '~' in infile:
        infile = os.path.expanduser(infile)
    
    outfile= infile+".aes"
    
    if os.path.isdir(infile):
        raise Exception("Please input the path to a file or a tarred directory.")

    # opening the original file to encrypt
    with open(infile, 'rb') as file:
        original = file.read()
        
    # encrypting the file
    encrypted = fernet.encrypt(original)
    
    # opening the file in write mode and 
    # writing the encrypted data
    with open(outfile, 'wb+') as encrypted_file:
        encrypted_file.write(encrypted)

    return outfile


@generate_flow_definition
class Encrypt(GladierBaseTool):
    funcx_functions = [encrypt]
    required_input = [
        'encrypt_input',
        'encrypt_key',
        'funcx_endpoint_compute'
    ]
