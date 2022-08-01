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

from __future__ import annotations
import json
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import asdict, dataclass

from ..rule import ERROR_TYPE_RULE, ERROR_TYPE_SCHEDULED_RULE
from ..policy import ERROR_TYPE_POLICY


# Aliases
ExecutionInputData = Dict[str, Any]
ExecutionEnvComponent = Dict[str, Any]

LogEventInput = Dict[str, Any]
CloudResourceInput = Dict[str, Any]


@dataclass(frozen=True)
class ExecutionMatch:

    # required for all matches
    alert_type: str
    detection_type: str
    detection_id: str
    detection_version: str
    detection_tags: List[str]
    detection_reports: Dict[str, List[str]]
    detection_severity: str
    dedup_string: str
    dedup_period_mins: int
    event: Dict[str, Any]
    # one of these will be set
    event_id: Optional[str] = None
    replay_id: Optional[str] = None
    # optional dynamic fields
    severity: Optional[str] = None
    alert_context: Optional[str] = None
    description: Optional[str] = None
    destinations: Optional[List[str]] = None
    reference: Optional[str] = None
    runbook: Optional[str] = None
    title: Optional[str] = None

    @property
    def errored(self) -> bool:
        return self.alert_type == ERROR_TYPE_RULE or \
               self.alert_type == ERROR_TYPE_SCHEDULED_RULE \
               or self.alert_type == ERROR_TYPE_POLICY

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional[ExecutionMatch]:
        if data is not None:
            return cls(**data)
        return None


@dataclass(frozen=True)
class _BaseDataObject:
    def to_json(self) -> str:
        return json.dumps(asdict(self))

    def to_bytes(self) -> bytes:
        return self.to_json().encode('utf-8')


@dataclass(frozen=True)
class ClientOptions(_BaseDataObject):
    lambda_name: str


class ExecutionMode(str, Enum):
    S3 = "S3"
    NONE = "NONE"
    INLINE = "INLINE"
