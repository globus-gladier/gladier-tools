from __future__ import annotations

from abc import ABC, abstractmethod

from gladier import GladierBaseTool
from typing_extensions import TypeAlias

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


def get_action_param_name(param_name: str, param_val: str | int | bool | dict) -> str:
    if isinstance(param_val, str) and param_val.startswith("$."):
        return param_name + ".$"
    else:
        return param_name


class GladierExperimentalBaseTool(GladierBaseTool, ABC):
    def __init__(
        self, state_name: str | None = None, state_comment: str | None = None, **kwargs
    ):
        if state_name is None:
            state_name = str(type(self))
        self.state_name = state_name
        if state_comment is None:
            state_comment = f"State named {state_name}"
        self.state_comment = state_comment
        super().__init__(**kwargs)
        self.set_flow_definition()

    @abstractmethod
    def set_flow_definition(self) -> dict[str, JSON]:
        if self.flow_definition is not None:
            return self.flow_definition
        self.flow_definition: dict[str, JSON] = {
            "Comment": self.state_comment,
            "StartAt": self.state_name,
            "States": {
                self.state_name: {
                    "Comment": self.state_comment,
                }
            },
        }
        return self.flow_definition

    def get_dict_for_flow_state(self) -> dict[str, JSON]:
        return GladierExperimentalBaseTool.set_flow_definition(self)["States"][
            self.state_name
        ]

    @property
    def required_input(self) -> list[str]:
        """
        Attempt to scrape required input from the properties of the self
        object. If a value starts with the JSONPath prefix '$.input.' we assume
        it is intended to be one of the required inputs to this state.
        """
        return_list: list[str] = []
        required_input_prefix = "$.input."
        for prop_val in vars(self).values():
            if isinstance(prop_val, str) and prop_val.startswith(required_input_prefix):
                return_list.append(prop_val[len(required_input_prefix) :])
        return return_list


class GladierExperimentalBaseActionTool(GladierExperimentalBaseTool, ABC):
    def __init__(
        self,
        action_url: str,
        action_scope: str | None = None,
        wait_time: int = 600,
        result_path: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.action_url = action_url
        self.action_scope = action_scope
        self.wait_time = wait_time
        if result_path is None:
            result_path = f"$.{self.state_name}Result"
        if not result_path.startswith("$."):
            result_path = "$." + result_path
        self.result_path = result_path
        GladierExperimentalBaseActionTool.set_flow_definition(self)

    @abstractmethod
    def set_flow_definition(self) -> dict[str, JSON]:
        flow_state = self.get_dict_for_flow_state()
        flow_state["Type"] = "Action"
        flow_state["ActionUrl"] = self.action_url
        flow_state["ResultPath"] = self.result_path
        flow_state["WaitTime"] = self.wait_time
        flow_state["End"] = True
        if self.action_scope is not None:
            flow_state["ActionScope"] = self.action_scope
        return self.flow_definition
