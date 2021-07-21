from unittest.mock import Mock
import tarfile
from gladier_tools.posix.tar import tar


def test_tar(monkeypatch):
    mock_tf = Mock()
    mock_open = Mock()
    mock_open.return_value.__enter__ = Mock(return_value=mock_tf)
    mock_open.return_value.__exit__ = Mock(return_value=None)
    monkeypatch.setattr(tarfile, 'open', mock_open)
    output_file = tar(tar_input='foo')
    assert mock_open.called
    assert mock_tf.add.called
    assert output_file == 'foo.tgz'
