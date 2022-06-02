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

from .common import (
    CloudResourceInput,
    ExecutionEnvComponent,
    ExecutionInputData,
    ExecutionMode,
    LogEventInput,
    _BaseDataObject,
)


@dataclass(frozen=True)
class ExecutionTaskInput(_BaseDataObject):
    _event_input_id = "p_row_id"
    _resource_input_id = "resourceId"

    mode: ExecutionMode
    data: List[ExecutionInputData]
    input_id_field: str
    url: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            mode=ExecutionMode(data['mode']),
            url=data.get('url'),
            data=data['data'],
            input_id_field=data['input_id_field'],
        )

    @classmethod
    def inline_resources(cls, resources: List[CloudResourceInput]):
        return cls(
            url=None,
            mode=ExecutionMode.INLINE,
            data=resources,
            input_id_field=cls._resource_input_id,
        )

    @classmethod
    def inline_events(cls, events: List[LogEventInput]):
        return cls(
            url=None,
            mode=ExecutionMode.INLINE,
            data=events,
            input_id_field=cls._event_input_id,
        )


@dataclass(frozen=True)
class ExecutionTaskOutput(_BaseDataObject):
    mode: ExecutionMode
    url: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            mode=ExecutionMode(data['mode']),
            url=data.get('url'),
        )

    @classmethod
    def inline(cls):
        return cls(
            url=None,
            mode=ExecutionMode.INLINE,
        )


@dataclass(frozen=True)
class ExecutionTaskOptions(_BaseDataObject):
    execution_details: bool

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            execution_details=data['execution_details'],
        )


@dataclass(frozen=True)
class ExecutionEnv(_BaseDataObject):
    mocks: List[ExecutionEnvComponent]
    outputs: List[ExecutionEnvComponent]
    globals: List[ExecutionEnvComponent]
    detections: List[ExecutionEnvComponent]
    data_model: Optional[ExecutionEnvComponent]

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            mocks=data.get('mocks', []),
            outputs=data.get('outputs', []),
            globals=data.get('globals', []),
            detections=data.get('detections', []),
            data_model=data.get('data_model', None),
        )


@dataclass(frozen=True)
class ExecutionTaskEnv(_BaseDataObject):
    mode: ExecutionMode
    url: Optional[str] = None
    env: Optional[ExecutionEnv] = None

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            mode=ExecutionMode(data['mode']),
            url=data.get('url'),
            env=ExecutionEnv.from_json(data.get('env', {})),
        )

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

    @classmethod
    def from_json(cls, data: Dict[str, any]):
        return cls(
            env=ExecutionTaskEnv.from_json(data['env']),
            input=ExecutionTaskInput.from_json(data['input']),
            output=ExecutionTaskOutput.from_json(data['output']),
            options=ExecutionTaskOptions.from_json(data['options']),
        )
