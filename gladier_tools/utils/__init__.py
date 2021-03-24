from gladier import GladierBaseTool


__all__ = ['HttpsDownloadFile', 'Unzip']

from .https_download_file import *
from .unzip_file import *

class HttpsDownloadFile(GladierBaseTool):

    flow_definition = {}

    funcx_functions = [
        https_download_file
    ]

class UnzipFile(GladierBaseTool):
    
    flow_definition = {}

    funcx_functions = [
        unzip_file
    ]

