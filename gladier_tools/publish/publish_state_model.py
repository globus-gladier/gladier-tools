import typing as t

from gladier import GladierBaseCompositeState, GladierBaseState, StateWithNextOrEnd
from gladier.tools.builtins import (
    AndRule,
    ChoiceOption,
    ChoiceRule,
    ChoiceState,
    ComparisonRule,
)
from gladier.tools.globus import (
    ComputeFunctionType,
    GlobusComputeStep,
    GlobusTransfer,
    GlobusTransferItem,
)

from .publishv2 import gather_metadata


class Publishv2GatherMetadataState(GlobusComputeStep):
    function_to_call: ComputeFunctionType = gather_metadata
    dataset: str
    destination: str
    source_collection: str
    destination_collection: str
    index: str
    visible_to: t.List[str]
    entry_id: str = "metadata"
    metadata: t.Optional[t.Mapping[str, t.Any]] = None
    source_collection_basepath: t.Optional[str] = None
    destination_url_hostname: t.Optional[str] = None
    checksum_algorithms: t.Tuple[str, str] = ("sha256", "sha512")
    metadata_dc_validation_schema: t.Optional[str] = None
    enable_publish: bool = True
    enable_transfer: bool = True
    enable_meta_dc: bool = True
    enable_meta_files: bool = True


class Publishv2State(GladierBaseCompositeState):
    dataset: str = "$.input.publishv2.dataset"
    destination: str = "$.input.publishv2.destination"
    source_collection: str = "$.input.publishv2.my-source-globus-collection"
    destination_collection: str = "$.input.publishv2.my-destination-globus-collection"
    index: str = "$.input.publishv2.my-globus-search-index-uuid"
    visible_to: t.Union[str, t.List[str]] = ["public"]
    # Ingest and Transfer are disabled by default, allowing for 'dry-run' testing.
    ingest_enabled: t.Union[str, bool] = False
    transfer_enabled: t.Union[str, bool] = False
    globus_compute_endpoint_non_compute: str = (
        "$.input.globus_compute_endpoint_non_compute"
    )

    def construct_flow(self) -> GladierBaseState:
        publish_v2_metadata = Publishv2GatherMetadataState(
            dataset=self.dataset,
            destination=self.destination,
            source_collection=self.source_collection,
            destination_collection=self.destination_collection,
            index=self.index,
            visible_to=self.visible_to,
        )

        transfer_for_publication = GlobusTransfer(
            state_name="Publishv2Transfer",
            input_path=publish_v2_metadata.path_to_return_val + ".transfer",
        )

        publish_v2_choice_ingest = ChoiceState()
        transfer_for_publication.next(publish_v2_choice_ingest)
        publish_v2_choice_transfer = ChoiceState(default=publish_v2_choice_ingest)
        publish_v2_choice_transfer.choice(
            ChoiceOption(
                rule=AndRule(
                    [
                        ComparisonRule(
                            Variable="$.input.publishv2.transfer_enabled",
                            IsPresent=True,
                        ),
                        ComparisonRule(
                            Variable="$.input.publishv2.transfer_enabled",
                            BooleanEquals=True,
                        ),
                    ]
                ),
                next=transfer_for_publication,
            )
        )

        publish_v2_metadata.next(publish_v2_choice_transfer)


def choice_state_next(
    rule: ChoiceRule,
    state_for_true_condition: StateWithNextOrEnd,
    next_state: GladierBaseState,
    choice_if_condition_true=True,
) -> ChoiceState:
    if not choice_if_condition_true:
        state_for_true_condition, next_state = next_state, state_for_true_condition
    choice_state = ChoiceState(default=next_state)
    choice_state.choice(ChoiceOption(rule=rule, next=state_for_true_condition))
    state_for_true_condition.next(next_state, replace_next=True)
    return choice_state
