from gladier import GladierBaseTool, GladierBaseClient, generate_flow_definition
from pprint import pprint


def encrypt(**data):
    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64

    password = bytes(data['key'], 'utf-8')
    salt= b'\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00'
    # salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
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

    # Custom flow definition to set 'ExceptionOnActionFailure' to True. 
    flow_definition = {
        'Comment': 'Flow with states: Encrypts a given file using AES 128 bit symmetric key encryption.',
        'StartAt': 'Encrypt',
        'States': {
            'Encrypt': {
                'ActionUrl': 'https://automate.funcx.org',
                'ActionScope': 'https://auth.globus.org/scopes/b3db7e59-a6f1-4947-95c2-59d6b7a70f8c/action_all',
                'Comment': None,
                'ExceptionOnActionFailure': True,
                'Parameters': {
                    'tasks': [
                        {
                            'endpoint.$': '$.input.funcx_endpoint_compute',
                            'function.$': '$.input.encrypt_funcx_id',
                            'payload.$': '$.input'
                        }
                    ]
                },
                'ResultPath': '$.Encrypt',
                'Type': 'Action',
                'WaitTime': 300,
                'End': True,
            },
        }
    }

    funcx_functions = [encrypt]
    required_input = [
        'encrypt_input',
        'key', 
        'funcx_endpoint_compute'
        ]
