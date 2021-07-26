from unittest.mock import Mock
import tarfile, os
import pytest
from gladier_tools.posix.untar import untar_file


def isfile_sub(data):
        return False

def test_no_file(monkeypatch):
    monkeypatch.setattr(os.path, 'isfile', isfile_sub)
    with pytest.raises(NameError):
        untar_file()

def test_mkdir(monkeypatch):
    monkeypatch.setattr(os.path, 'isfile', Mock(return_value=True))
    monkeypatch.setattr(os.path, 'exists', Mock(return_value=False))

    mock_mkdir= Mock()
    monkeypatch.setattr(os, 'makedirs', mock_mkdir)
    mock_tf= Mock()
    mock_extract= Mock()
    mock_tf.return_value.__enter__ = Mock(return_value=mock_extract)
    mock_tf.return_value.__exit__ = Mock(return_value=None)
    monkeypatch.setattr(tarfile, 'open', mock_tf)
    untar_file()
    assert mock_mkdir.called
    assert mock_tf.called
    assert mock_extract.extractall.called
    


