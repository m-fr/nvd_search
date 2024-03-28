import pytest

from nvd_search.enums import Risk

class TestSeverity:
    @pytest.mark.parametrize("input", ["none", "low", "Medium", "HigH", "CRITICAL"])
    def test_construct_valid(self, input):
        risk = Risk(input)
        assert str(risk) == input.capitalize()

    @pytest.mark.parametrize("input", ["supercritical", "", None, 123])
    def test_construct_invalid(self, input):
        with pytest.raises(ValueError):
            Risk(input)

    @pytest.mark.parametrize("a,b", [("low", "Low"), ("HIGH", "HiGh")])
    def test_eq(self, a, b):
        assert Risk(a) == Risk(b)

    @pytest.mark.parametrize("a,b", [("high", "low")])
    def test_not_eq(self, a, b):
        assert Risk(a) != Risk(b)

    @pytest.mark.parametrize("a,b", [("none", "low"), ("low", "medium"), ("medium", "high"), ("high", "critical")])
    def test_lt_gt(self, a, b):
        assert Risk(a) < Risk(b)
        assert Risk(b) > Risk(a)
