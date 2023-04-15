from __future__ import annotations

from gladier_tools.experimental import (
    JSON,
    GladierExperimentalBaseActionTool,
    get_action_param_name,
)


class GlobusMkDir(GladierExperimentalBaseActionTool):
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
        **kwargs,
    ):
        self.endpoint_id = endpoint_id
        self.path = path
        super().__init__(
            state_name=state_name,
            action_url="https://actions.globus.org/transfer/mkdir",
            result_path=result_path,
            wait_time=wait_time,
            **kwargs,
        )

    def set_flow_definition(self) -> dict[str, JSON]:
        flow_state = self.get_dict_for_flow_state()
        flow_state["Parameters"] = {
            get_action_param_name("endpoint_id", self.endpoint_id): self.endpoint_id,
            get_action_param_name("path", self.path): self.path,
        }
        return self.flow_definition
