"""
Panther Core is a Python library for Panther Detections.
Copyright (C) 2020 Panther Labs Inc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from .common import ExecutionMatch, ExecutionMode, _BaseDataObject


@dataclass(frozen=True)
class ExecutionAuxFunctionDetails(_BaseDataObject):
    defined: bool
    error: Optional[str] = None
    output: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            defined=data['defined'],
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
    aux_functions: ExecutionDetailsAuxFunctions

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            aux_functions=ExecutionDetailsAuxFunctions.from_json(data['aux_functions']),
        )

@dataclass(frozen=True)
class ExecutionOutput(_BaseDataObject):
    input_id: str
    match: Optional[ExecutionMatch] = None
    details: Optional[ExecutionDetails] = None

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            match=data['match'],
            details=ExecutionDetails.from_json(data['details']),
            input_id=data['input_id'],
        )

@dataclass(frozen=True)
class ExecutionResult(_BaseDataObject):
    output_mode: ExecutionMode
    url: Optional[str] = None
    data: Optional[List[ExecutionOutput]] = None

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        outputs = []
        for json_str in data['data']:
            obj = ExecutionOutput.from_json(json_str)
            outputs.append(obj)

        return cls(
            url=data['url'],
            data=outputs,
            output_mode=ExecutionMode(data['output_mode']),
        )
