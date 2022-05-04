import json

from enum import Enum
from dataclasses import dataclass, asdict


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
