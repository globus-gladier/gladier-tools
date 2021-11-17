from gladier import GladierBaseTool, generate_flow_definition


def untar_file(**data):
    import os
    import tarfile

    ##minimal data inputs payload
    file_path = data.get('file_path', '')
    file_name = data.get('file_name', '')
    output_path = data.get('output_path', '')
    ##

    full_path = os.path.join(file_path, file_name)

    if not os.path.isfile(full_path):
        raise NameError(f'{full_path}  does not exist!!')

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    with tarfile.open(full_path) as file:
        file.extractall(output_path)
    return output_path

@generate_flow_definition
class UnTar(GladierBaseTool):
    """
    The UnTar tool makes it possible to extract data from Tar archives.

    :param file_path: Directory in which the tar file exists. Defaults to empty string if not passed.
    :param file_name: Name of the .tgz file which has to be untarred. Defaults to empty string if not passed.
    :param output_path: Location where the files will be extracted from the archive. Defaults to empty string if not passed.
    :param funcx_endpoint_non_compute: By default, uses the ``non-compute`` funcx endpoint.
    :returns output_path: Location of the extracted files.
    """
    
    funcx_functions = [untar_file]

    required_input = [
        'file_path',
        'file_name',
        'output_path',
        'funcx_endpoint_non_compute'
        ]

