from functools import total_ordering
from typing import Any

from pydantic import ConfigDict, RootModel, field_serializer, field_validator
from semver import Version

from nvd_search.exceptions import UtilTypeError

__all__ = ["CPEVersion"]


@total_ordering
class BaseVersion(RootModel[Any]):
    root: Version
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("root", mode="after")
    def prerelease_build_not_set(cls, v: Version):
        if v.prerelease is not None or v.build is not None:
            raise ValueError("only major, minor, patch parts supported")
        return v

    @field_serializer("root")
    def serialize_root(self, root: Version, _info: Any):
        return self.__str__()

    def __lt__(self, other: Any):
        if type(self) is not type(other):
            raise UtilTypeError("incompatible types for comparison")
        return self.root < other.root

    def __eq__(self, other: Any):
        if type(self) is not type(other):
            raise UtilTypeError("incompatible types for comparison")
        return self.root == other.root

    def __hash__(self):
        return self.root.__hash__()


@total_ordering
class CPEVersion(BaseVersion):
    @field_validator("root", mode="before")
    def load_version(cls, v: Any):
        if isinstance(v, str):
            return Version.parse(v)
        raise ValueError("invalid type")

    def __str__(self) -> str:
        return self.root.__str__()
