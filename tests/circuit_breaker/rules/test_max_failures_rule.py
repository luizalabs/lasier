import pytest

from lasier.circuit_breaker.rules import BaseRule, MaxFailuresRule


class TestMaxFailuresRule:

    @pytest.fixture
    def rule(self):
        return MaxFailuresRule(
            max_failures=10,
            failure_cache_key='fail'
        )

    def test_max_failures_rule_should_return_rule_instance(self, rule):
        assert isinstance(rule, BaseRule)

    @pytest.mark.parametrize('failures,expected', (
        (1, False),
        (5, False),
        (10, True),
        (11, True)
    ))
    def test_should_check_circuit_state(self, rule, failures, expected):
        assert rule.should_open_circuit(
            total_failures=failures,
            total_requests=0
        ) is expected

    def test_should_not_increase_request_count(self, rule):
        assert rule.should_increase_request_count() is False
