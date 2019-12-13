import pytest

from lasier.circuit_breaker.rules import MaxFailuresRule, RuleBase


class TestMaxFailuresRule:

    @pytest.fixture
    def rule(self):
        return MaxFailuresRule(
            max_failures=10,
            failure_cache_key='fail'
        )

    def test_max_failures_rule_should_return_rule_instance(self, rule):
        assert isinstance(rule, RuleBase)

    def test_should_not_open_circuit(self, rule):
        assert rule.should_open_circuit(
            total_failures=5,
            total_requests=5
        ) is False

    def test_should_open_circuit(self, rule):
        assert rule.should_open_circuit(
            total_failures=20,
            total_requests=5
        ) is True

    def test_should_increase_failure_count(self, rule):
        assert rule.should_increase_failure_count() is True

    def test_should_not_increase_request_count(self, rule):
        assert rule.should_increase_request_count() is False
