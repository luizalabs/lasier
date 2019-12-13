import pytest

from lasier.circuit_breaker.rules import PercentageFailuresRule, RuleBase


class TestPercentageFailureRule:

    @pytest.fixture
    def rule(self):
        return PercentageFailuresRule(
            max_failures_percentage=50,
            failure_cache_key='fail',
            min_accepted_requests=5,
            request_cache_key='request'
        )

    def test_percentage_failures_rule_should_return_rule_instance(self, rule):
        assert isinstance(rule, RuleBase)

    def test_should_not_open_circuit(self, rule):
        assert rule.should_open_circuit(
            total_failures=0,
            total_requests=49
        ) is False

    def test_should_not_open_circuit_with_min_accepted_number_of_requests(
        self,
        rule
    ):
        assert rule.should_open_circuit(
            total_failures=5,
            total_requests=5
        ) is False

    def test_should_open_circuit(self, rule):
        assert rule.should_open_circuit(
            total_failures=20,
            total_requests=40
        ) is True

    def test_should_increase_failure_count(self, rule):
        assert rule.should_increase_failure_count() is True

    def test_should_increase_request_count(self, rule):
        assert rule.should_increase_request_count() is True
