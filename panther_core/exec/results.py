from typing import Optional, List, Dict
from dataclasses import dataclass

from .common import _BaseDataObject, ExecutionMode


@dataclass(frozen=True)
class ExecutionAuxFunctionDetails(_BaseDataObject):
    error: Optional[str]
    output: Optional[str]

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            error=data['error'],
            output=data['output'],
        )


@dataclass(frozen=True)
class ExecutionDetailsAuxFunctions(_BaseDataObject):
    title: ExecutionAuxFunctionDetails
    runbook: ExecutionAuxFunctionDetails
    severity: ExecutionAuxFunctionDetails
    reference: ExecutionAuxFunctionDetails
    description: ExecutionAuxFunctionDetails
    destinations: ExecutionAuxFunctionDetails
    alert_context: ExecutionAuxFunctionDetails

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            title=ExecutionAuxFunctionDetails.from_json(data['title']),
            runbook=ExecutionAuxFunctionDetails.from_json(data['runbook']),
            severity=ExecutionAuxFunctionDetails.from_json(data['severity']),
            reference=ExecutionAuxFunctionDetails.from_json(data['reference']),
            description=ExecutionAuxFunctionDetails.from_json(data['description']),
            destinations=ExecutionAuxFunctionDetails.from_json(data['destinations']),
            alert_context=ExecutionAuxFunctionDetails.from_json(data['alert_context']),
        )


@dataclass(frozen=True)
class ExecutionDetails(_BaseDataObject):
    input_id: str
    aux_functions: ExecutionDetailsAuxFunctions

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            input_id=data['input_id'],
            aux_functions=ExecutionDetailsAuxFunctions.from_json(data['aux_functions']),
        )


@dataclass(frozen=True)
class ExecutionResult(_BaseDataObject):
    url: Optional[str]
    data: Optional[List[Dict[str, any]]]
    details: List[ExecutionDetails]
    output_mode: ExecutionMode

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        details = []
        for json_str in data['details']:
            obj = ExecutionDetails.from_json(json_str)
            details.append(obj)

        return cls(
            url=data['url'],
            data=data['data'],
            output_mode=ExecutionMode(data['output_mode']),
            details=details,
        )


@dataclass(frozen=True)
class ExecutionMatch(_BaseDataObject):
    input_id: str
