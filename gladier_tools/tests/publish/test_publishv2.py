import pytest
import pathlib
from gladier_tools.publish.publishv2 import publishv2

mock_data = pathlib.Path(__file__).resolve().parent.parent / 'mock_data/publish/'


@pytest.fixture
def publish_input():
    return {
        'dataset': mock_data / 'test_dataset_folder',
        'destination': '/my-new-project',
        'source_collection': 'my_transfer_endpoint',
        'destination_collection': 'my_globus_collection',
        'destination_collection_basepath': '/my-new-project/',
        'index': 'my_index',
        'visible_to': ['public'],
        'groups': []
    }

def test_publish(publish_input):
    publishv2(**publish_input).keys() == ('search', 'transfer')


def test_publish_dc(publish_input):
    output = publishv2(**publish_input)
    content = output['search']['content']
    assert 'dc' in content
    partial_dc = content['dc'].copy()
    partial_dc.pop('dates')
    assert partial_dc == {
        'creators': [{'creatorName': ''}],
        # timestamp contains seconds, which is hard to check. Skip it!
        # 'dates': [{'date': '2023-03-16T07:44:14.044091', 'dateType': 'Created'}],
        'formats': ['text/plain'],
        'publicationYear': 2023,
        'publisher': '',
        'resourceType': {'resourceType': 'Dataset', 'resourceTypeGeneral': 'Dataset'},
        'subjects': [],
        'titles': ['test_dataset_folder'],
        'version': '1'
    }
    assert 'dates' in content['dc']
    assert content['dc']['dates'][0]['dateType'] == 'Created'
    assert 'date' in content['dc']['dates'][0]


def test_publish_files(publish_input):
    output = publishv2(**publish_input)
    files = output['search']['content']['files']
    assert files == [
    {
        "sha256": "ef04ad1ddb694bcf461bef6668d387117c63d1648589d55413d4266dc0372dbd",
        "sha512": "aa650e6a730cc73c6d967d9a5c3549dd1bdc94a0128c1ea1fcb9506b5e9c099583e979892af75e2930fb33a84c0c7eb2be5e3e508809f4269cba01ff22847a03",
        "filename": "foo.txt",
        "url": "globus://my_globus_collection/my-new-project/test_dataset_folder/foo.txt",
        "mime_type": "text/plain",
        "length": 16
    },
    {
        "sha256": "49606feb430b0ca35c4099c1e84fe81b5634039ecbeb408d76fa5e44f93c1d9a",
        "sha512": "3a9db7ddff3f83902624832a74ba5559e83ef66cb471d14d79a2b89fa981f47b9a0f27ef83f4f266ee5ecf22f817fe58da6f4323c0eb5557fea9152fb4465e04",
        "filename": "bar.txt",
        "url": "globus://my_globus_collection/my-new-project/test_dataset_folder/bar.txt",
        "mime_type": "text/plain",
        "length": 16
    }
  ]


def test_publish_transfer(publish_input):
    output = publishv2(**publish_input)
    from pprint import pprint
    pprint(output['transfer'])
    dataset = publish_input['dataset']
    assert output['transfer'] == {
        'destination_endpoint_id': 'my_globus_collection',
        'source_endpoint_id': 'my_transfer_endpoint',
        'transfer_items': [{
                'destination_path': str(pathlib.Path('/my-new-project') / dataset.name),
                'source_path': dataset,
            }]
        }

# def test_publish_collection_basepath(publish_input):
    


# def test_publish_exception(publish_input):
#     output = publishv2(**publish_input)
#     content = output['search']['content']
#     assert 'dc' in content