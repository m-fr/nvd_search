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
                return "[blue]"
            case Risk.low:
                return "[green]"
            case Risk.medium:
                return "[yellow]"
            case Risk.high:
                return "[orange1]"
            case Risk.critical:
                return "[red]"
            case _:
                raise SeretoValueError("unexpected risk value")


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
                raise SeretoValueError("unexpected risk value")
