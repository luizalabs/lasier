from lasier.circuit_breaker.rules.base import BaseRule


class ShouldNotOpenRule(BaseRule):

    def should_open_circuit(self, total_failures, total_requests):
        return False

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldOpenRule(BaseRule):

    def should_open_circuit(self, total_failures, total_requests):
        return True

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldNotIncreaseFailureRule(BaseRule):

    def should_increase_failure_count(self):
        return False

    def should_open_circuit(self, total_failures, total_requests):
        return False

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldNotIncreaseRequestRule(BaseRule):

    def should_increase_request_count(self):
        return False

    def should_open_circuit(self, total_failures, total_requests):
        return False

    def log_increase_failures(self, total_failures, total_requests):
        pass
