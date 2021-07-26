from unittest.mock import Mock
import os
import pytest
import tarfile
from gladier_tools.posix.tar import tar


@pytest.fixture
def mock_tar(monkeypatch):
    mock_tf = Mock()
    mock_open = Mock()
    mock_open.return_value.__enter__ = Mock(return_value=mock_tf)
    mock_open.return_value.__exit__ = Mock(return_value=None)
    monkeypatch.setattr(tarfile, 'open', mock_open)
    return mock_open, mock_tf


def test_tar_home_directory(mock_tar):
    output_file = tar(tar_input='~/foo')
    assert output_file == os.path.expanduser('~/foo.tgz')


def test_tar(mock_tar):
    mock_open, mock_context_manager = mock_tar
    output_file = tar(tar_input='foo')
    assert mock_open.called
    assert mock_context_manager.add.called
    assert output_file == 'foo.tgz'
