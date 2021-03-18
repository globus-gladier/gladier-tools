from gladier import GladierBaseTool
from .io import https_download_file, unzip_data

class HttpsDownloadFile(GladierBaseTool):

    flow_definition = {}

    required_input = [
    'server_url',
    'file_name',
    'file_path',
    'headers'
    ]

    flow_input = {
        'server_url': '',
        'file_name': '',
        'file_path': '',
        'headers': ''
    }

    funcx_functions = [
        https_download_file
    ]

class UnzipData(GladierBaseTool):
    
    flow_definition = {}

    required_input = [
        'file_name',
        'file_path',
        'output_path',
    ]

    flow_input = {
        'file_name': '',
        'file_path': '',
        'output_path': '',
    }

    funcx_functions = [
        unzip_data
    ]

