from lasier.circuit_breaker.rules.base import RuleBase


class ShouldNotOpenRule(RuleBase):

    def should_open_circuit(self, total_failures, total_requests):
        return False

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldOpenRule(RuleBase):

    def should_open_circuit(self, total_failures, total_requests):
        return True

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldNotIncreaseFailureRule(RuleBase):

    def should_increase_failure_count(self):
        return False

    def should_open_circuit(self, total_failures, total_requests):
        return False

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldNotIncreaseRequestRule(RuleBase):

    def should_increase_request_count(self):
        return False

    def should_open_circuit(self, total_failures, total_requests):
        return False

    def log_increase_failures(self, total_failures, total_requests):
        pass
