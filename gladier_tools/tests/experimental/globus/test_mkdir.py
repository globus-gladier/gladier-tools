from gladier_tools.experimental.globus import GlobusMkDir


def test_mkdir_tool():
    mkdir_tool = GlobusMkDir(state_name="testMkDirState")
    flow_def = mkdir_tool.flow_definition
    assert "testMkDirState" in flow_def["States"]
    inputs = mkdir_tool.required_input
    assert "mkdir_endpoint_id" in inputs
    assert "mkdir_path" in inputs
