from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .common import _BaseDataObject, ExecutionMode


@dataclass(frozen=True)
class ExecutionTaskInput(_BaseDataObject):
    _event_input_id = "p_row_id"
    _resource_input_id = "resourceId"

    mode: ExecutionMode
    url: Optional[str]
    rows: List[Any]
    input_id_field: str

    @classmethod
    def inline_resources(cls, resources: List[Any]):
        return cls(
            url=None,
            mode=ExecutionMode.INLINE,
            rows=resources,
            input_id_field=cls._resource_input_id,
        )

    @classmethod
    def inline_events(cls, events: List[Any]):
        return cls(
            url=None,
            mode=ExecutionMode.INLINE,
            rows=events,
            input_id_field=cls._event_input_id,
        )


@dataclass(frozen=True)
class ExecutionTaskOutput(_BaseDataObject):
    mode: ExecutionMode
    url: Optional[str]

    @classmethod
    def inline(cls):
        return cls(
            url=None,
            mode=ExecutionMode.INLINE,
        )


@dataclass(frozen=True)
class ExecutionTaskOptions(_BaseDataObject):
    execution_details: bool


@dataclass(frozen=True)
class ExecutionEnv(_BaseDataObject):
    globals: List[Dict[str, Any]]
    detections: List[Dict[str, Any]]
    data_models: List[Dict[str, Any]]


@dataclass(frozen=True)
class ExecutionTaskEnv(_BaseDataObject):
    mode: ExecutionMode
    url: Optional[str]
    env: Optional[ExecutionEnv]

    @classmethod
    def inline(cls, env: ExecutionEnv):
        return cls(
            env=env,
            url=None,
            mode=ExecutionMode.INLINE,
        )


@dataclass(frozen=True)
class ExecutionTask(_BaseDataObject):
    env: ExecutionTaskEnv
    input: ExecutionTaskInput
    output: ExecutionTaskOutput
    options: ExecutionTaskOptions
