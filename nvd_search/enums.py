from enum import Enum
from functools import total_ordering

from nvd_search.exceptions import UtilValueError


@total_ordering
class Risk(Enum):
    """Enum representing the risk level of a finding.
    """
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    none = "none"

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.to_int() < other.to_int()
        return NotImplemented

    @classmethod
    def _missing_(cls, value):
        """Make the enum case insesitive.
        """
        if not isinstance(value, str):
            raise ValueError
        for member in cls:
            if member.value == value.lower():
                return member

    def __str__(self):
        """Convert risks to a string.
        """
        return self.value.capitalize()

    def to_color(self):
        """Convert risks to a rich color.
        """
        match self:
            case Risk.none:
                return "[logging.level.notset]"
            case Risk.low:
                return "[logging.level.debug]"
            case Risk.medium:
                return "[logging.level.warning]"
            case Risk.high:
                return "[logging.level.error]"
            case Risk.critical:
                return "[logging.level.critical]"
            case _:
                raise UtilValueError("unexpected risk value")

    def to_int(self):
        """Convert risks to a number.

        Usefull for comparison - e.g. `max(risks, key=lambda r: r.to_int())`
        """
        match self:
            case Risk.none:
                return 0
            case Risk.low:
                return 1
            case Risk.medium:
                return 2
            case Risk.high:
                return 3
            case Risk.critical:
                return 4
            case _:
                raise UtilValueError("unexpected risk value")
