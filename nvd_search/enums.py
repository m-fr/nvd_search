from enum import Enum

from nvd_search.exceptions import UtilValueError


class Risk(str, Enum):
    """Enum representing the risk level of a finding.
    """
    critical = "CRITICAL"
    high = "HIGH"
    medium = "MEDIUM"
    low = "LOW"
    none = "NONE"

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
