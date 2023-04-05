from __future__ import annotations

from gladier import GladierBaseTool


def get_action_param_name(param_name: str, param_val: str | int | bool | dict) -> str:
    if isinstance(param_val, str) and param_val.startswith("$."):
        return param_name + ".$"
    else:
        return param_name


class GlobusMkDir(GladierBaseTool):
    """
    GlobusMkDir provides a state for using the Make Directory capability of Globus
    Transfer to create a directory/folder on a specified Globus Endpoint.

    :param endpoint_id: Globus Endpoint UUID
    :param path: Path of the directory to create. Containing directory must exist.
    :param state_name: The name of the state within the generated Flow.
    :param result_path: Location in a run's state to store results of this state.
    :param wait_time: Time, in seconds, to wait for this step to complete during a run.
    """

    def __init__(
        self,
        state_name="MkDir",
        result_path: str | None = None,
        wait_time=600,
        endpoint_id="$.input.mkdir_endpoint_id",
        path="$.input.mkdir_path",
    ):
        super().__init__()
        self.state_name = state_name
        if result_path is None:
            result_path = state_name + "Result"
        if not result_path.startswith("$."):
            result_path = "$." + result_path
        self.result_path = result_path
        self.endpoint_id = endpoint_id
        self.path = path
        self.wait_time = wait_time

        self.flow_definition = self.set_flow_definition()

    def set_flow_definition(self) -> dict[str, str | int | bool | dict]:
        return {
            "Comment": "Create a Directory on a particular Globus Endpoint",
            "StartAt": self.state_name,
            "States": {
                self.state_name: {
                    "Comment": "Create a Directory on a particular Globus Endpoint",
                    "Type": "Action",
                    "ActionUrl": "https://actions.automate.globus.org/transfer/mkdir",
                    "Parameters": {
                        get_action_param_name(
                            "endpoint_id", self.endpoint_id
                        ): self.endpoint_id,
                        get_action_param_name("path", self.path): self.path,
                    },
                    "ResultPath": self.result_path,
                    "WaitTime": self.wait_time,
                    "End": True,
                },
            },
        }

    @property
    def required_input(self) -> list[str]:
        return_list: list[str] = []
        required_input_prefix = "$.input."
        if self.endpoint_id.startswith(required_input_prefix):
            return_list.append(self.endpoint_id[len(required_input_prefix) :])
        if self.path.startswith(required_input_prefix):
            return_list.append(self.path[len(required_input_prefix) :])
        return return_list
