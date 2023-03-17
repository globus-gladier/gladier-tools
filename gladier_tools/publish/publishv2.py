from gladier import GladierBaseTool
from typing import Tuple, List, Mapping


def publishv2(
            dataset: str,
            destination: str,
            source_collection: str,
            destination_collection: str,
            index: str, 
            visible_to: List[str],
            source_collection_basepath: str = None, 
            destination_url_hostname: str = None,
            entry_id: str = 'metadata',
            checksum_algorithms: Tuple[str] = ('sha256', 'sha512'),
            metadata: Mapping = None,
            enable_publish: bool = True,
            enable_transfer: bool = True,
            enable_meta_dc: bool = True,
            enable_meta_files: bool = True,
            **data
        ):
    import hashlib
    import urllib
    import pathlib
    import datetime
    import mimetypes
    try:
        import puremagic
    except ImportError:
        puremagic = None

    def translate_guest_collection_path(collection_basepath, path):
        if not collection_basepath:
            return str(path)
        try:
            return f'/{str(pathlib.PosixPath(path).relative_to(collection_basepath))}'
        except ValueError:
            raise ValueError(f'POSIX path given "{path}" outside Gloubus Collection '
                            f'share path: {collection_basepath}') from None
    
    def get_mimetype(filename):
        """
        Attempt to determine the mimetype of a file with a few different approaches, from
        top to bottom in this list:
        1. Try puremagic if it is installed
        2. Use the built in mimetypes lib
        3. Check for text vs binary by reading a chunk of data
        """
        def detect_mimetype(filename):
            if puremagic is not None:
                mimetype = puremagic.magic_file(str(filename))[0].mime_type
                if mimetype:
                    return mimetype

            mt, _ = mimetypes.guess_type(filename, strict=True)
            return mt

        def detect_text_or_binary(filename):
            """Read the first 1024 and attempt to decode it in utf-8. If this succeeds,
            the file is determined to be text. If not, its binary.
            
            There are better ways to do this, but this should be 'good enough' for most
            use-cases we have.
            """
            with open(filename, 'rb') as f:
                chunk = f.read(1024)
            try:
                chunk.decode('utf-8')
                return 'text/plain'
            except UnicodeDecodeError:
                return 'application/octet-stream'

        for func in (detect_mimetype, detect_text_or_binary):
            mimetype = func(filename)
            if mimetype:
                return mimetype


    def get_remote_file_manifest(filepath, destination_path, url_host, algorithms):
        dataset = pathlib.Path(filepath)
        destination = pathlib.Path(destination_path)
        if not dataset.exists():
            raise ValueError(f'File does not exist: {filepath}')
        
        file_list = [dataset] if dataset.is_file() else list(dataset.iterdir())
        file_list = [(local_abspath, destination / str(local_abspath.relative_to(dataset.parent)).lstrip('/'))
                     for local_abspath in file_list]

        manifest_entries = []
        for subfile, remote_short_path in file_list:
            rfm = {alg: compute_checksum(subfile, alg) for alg in algorithms}
            # mimetype = analysis.mimetypes.detect_type(subfile)
            rfm.update({
                'filename': subfile.name,
                'url': urllib.parse.urlunsplit(('globus', destination_collection, str(remote_short_path), '', '')),
                'mime_type': get_mimetype(subfile)
            })
            if url_host:
                url_host_p = urllib.parse.urlparse(url_host)
                if not url_host_p.scheme or not url_host_p.netloc:
                    raise ValueError(f'destination_url_hostname {url_host} must be of format: https://example.com')
                rfm['https_url'] = urllib.parse.urlunsplit((url_host_p.scheme, url_host_p.hostname, str(remote_short_path), '', ''))

            if subfile.exists():
                rfm['length'] = subfile.stat().st_size
            manifest_entries.append(rfm)
        return manifest_entries

    def compute_checksum(file_path, algorithm, block_size=65536):
        alg = getattr(hashlib, algorithm, None)
        if not alg:
            raise ValueError(f'Algorithm {algorithm} is not available in hashlib!')
        alg_instance = alg()
        with open(file_path, 'rb') as open_file:
            buf = open_file.read(block_size)
            while len(buf) > 0:
                alg_instance.update(buf)
                buf = open_file.read(block_size)
        return alg_instance.hexdigest()
        
    def get_dc(title, subject: str, files: list = None):
        dt = datetime.datetime.now()
        return {
            'identifiers': [{
                'identifierType': 'GlobusSearchSubject',
                'identifier': subject,
            }],
            'creators': [{'name': ''}],
            'dates': [{'date': f'{dt.isoformat()}Z', 'dateType': 'Created'}],
            'formats': list({f['mime_type'] for f in files}),
            'publicationYear': str(dt.year),
            'publisher': '',
            'types': {
                'resourceType': 'Dataset',
                'resourceTypeGeneral': 'Dataset'
            },
            'subjects': [],
            'titles': [{'title': dataset.name}],
            'version': '1',
            'schemaVersion': 'http://datacite.org/schema/kernel-4',
        }

    def get_content(title, subject, metadata):
        new_metadata = {}
        if enable_meta_files:
            new_metadata['files'] = get_remote_file_manifest(
                dataset, destination, destination_url_hostname, checksum_algorithms)
        if enable_meta_dc:
            new_metadata['dc'] = get_dc(title, subject, new_metadata.get('files', []))
        new_metadata.update(metadata if metadata is not None else {})
        return new_metadata

    dataset = pathlib.Path(dataset)
    destination_path = pathlib.Path(destination) / dataset.name
    subject = urllib.parse.urlunparse(('globus', destination_collection, str(destination_path), '', '', ''))
    return {
        'search': {
            'id': entry_id,
            'content': get_content(dataset.name, subject, metadata),
            'subject': subject,
            'visible_to': visible_to,
            'search_index': index
        },
        'transfer': {
            'source_endpoint_id': source_collection,
            'destination_endpoint_id': destination_collection,
            'transfer_items': [{
                'source_path': translate_guest_collection_path(source_collection_basepath, dataset),
                'destination_path': str(destination_path),
            }]
        }
    }


class Publishv2(GladierBaseTool):
    """This function uses the globus-pilot tool to generate metadata compatible with
    portals on https://acdc.alcf.anl.gov/. Requires globus_pilot>=0.6.0.
    FuncX Functions:
    * publish_gather_metadata (funcx_endpoint_non_compute)
    Publication happens in three steps:
    * PublishGatherMetadata -- A funcx function which uses globus-pilot to gather
      metadata on files or folders
    * PublishTransfer -- Transfers data to the Globus Endpoint selected in Globus Pilot
    * PublishIngest -- Ingest metadata gathered in fist step to Globus Search
    **Note**: This tool needs internet access to fetch Pilot configuration records, which
    contain the destination endpoint and other project info. The default FuncX endpoint
    name is `funcx_endpoint_non_compute`. You can change this with the following modifier:
    .. code-block::
        @generate_flow_definition(modifiers={
            'publish_gather_metadata': {'endpoint': 'funcx_endpoint_non_compute'},
        })
    More details on modifiers can be found at
    https://gladier.readthedocs.io/en/latest/gladier/flow_generation.html
    NOTE: This tool nests input under the 'pilot' keyword. Submit your input as the following:
    .. code-block::
        {
            'input': {
                'pilot': {
                    'dataset': 'foo',
                    'index': 'my-search-index-uuid',
                    'project': 'my-pilot-project',
                    'source_globus_endpoint': 'ddb59aef-6d04-11e5-ba46-22000b92c6ec',
                }
        }
    :param dataset: Path to file or directory. Used by Pilot to gather metadata, and set as the
        source for transfer to the publication endpoint configured in Pilot.
    :param destination: relative location under project directory to place dataset (Default `/`)
    :param source_globus_endpoint: The Globus Endpoint of the machine where you are executing
    :param index: The index to ingest this dataset in Globus Search
    :param project: The Pilot project to use for this dataset
    :param groups: A list of additional groups to make these records visible_to.
    :param funcx_endpoint_non_compute: A funcX endpoint uuid for gathering metadata. Requires
        internet access.
    Requires: the 'globus-pilot' package to be installed.
    """

    flow_definition = {
        'Comment': 'Publish metadata to Globus Search, with data from the result.',
        'StartAt': 'PublishGatherMetadata',
        'States': {
            'PublishGatherMetadata': {
                'Comment': 'Say something to start the conversation',
                'Type': 'Action',
                'ActionUrl': 'https://automate.funcx.org',
                'ActionScope': 'https://auth.globus.org/scopes/'
                               'b3db7e59-a6f1-4947-95c2-59d6b7a70f8c/action_all',
                'ExceptionOnActionFailure': True,
                'Parameters': {
                    'tasks': [{
                        'endpoint.$': '$.input.funcx_endpoint_non_compute',
                        'function.$': '$.input.publishv2_funcx_id',
                        'payload.$': '$.input.publishv2',
                    }]
                },
                'ResultPath': '$.PublishGatherMetadata',
                'WaitTime': 60,
                'Next': 'ChoicePublishTransfer',
            },
            'ChoicePublishTransfer': {
                'Comment': 'Determine if the document should be cataloged in Globus Search',
                'Type': 'Choice',
                'Choices': [{
                    'And': [
                        {
                        'Variable': '$.input.publishv2.transfer_enabled',
                        'IsPresent': True
                        },
                        {
                        'Variable': '$.input.publishv2.transfer_enabled',
                        'BooleanEquals': True
                        }
                    ],
                    'Next': 'PublishTransfer'
                }],
                'Default': 'PublishSkipTransfer',
            },
            'PublishTransfer': {
                'Comment': 'Transfer files for publication',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'InputPath': '$.PublishGatherMetadata.details.result[0].transfer',
                'ResultPath': '$.PublishTransfer',
                'WaitTime': 600,
                'Next': 'ChoicePublishIngest',
            },
            'PublishSkipTransfer': {
                'Comment': 'The ingest step has been skipped',
                'Type': 'Pass',
                'Next': 'ChoicePublishIngest',
            },
            'ChoicePublishIngest': {
                'Comment': 'Determine if the document should be cataloged in Globus Search',
                'Type': 'Choice',
                'Choices': [{
                    'And': [
                        {
                        'Variable': '$.input.publishv2.ingest_enabled',
                        'IsPresent': True
                        },
                        {
                        'Variable': '$.input.publishv2.ingest_enabled',
                        'BooleanEquals': True
                        }
                    ],
                    'Next': 'PublishIngest'
                }],
                'Default': 'PublishSkipIngest',
            },
            'PublishIngest': {
                'Comment': 'Ingest the search document',
                'Type': 'Action',
                'ActionUrl': 'https://actions.globus.org/search/ingest',
                'InputPath': '$.PublishGatherMetadata.details.result[0].search',
                'ResultPath': '$.PublishIngest',
                'WaitTime': 300,
                'Next': 'PublishDone',
            },
            'PublishSkipIngest': {
                'Comment': 'The ingest step has been skipped',
                'Type': 'Pass',
                'Next': 'PublishDone',
            },
            'PublishDone': {
                'Comment': 'The Publication tool has completed successfully.',
                'Type': 'Pass',
                'End': True,
            }
        }
    }

    required_input = [
        'publishv2',
        'funcx_endpoint_non_compute',
    ]

    flow_input = {

    }

    funcx_functions = [
        publishv2,
    ]