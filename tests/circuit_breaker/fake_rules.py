from lasier.circuit_breaker.rules.base import BaseRule


class _BaseFakeRule(BaseRule):

    def should_open_circuit(self, total_failures, total_requests):
        assert isinstance(
            total_failures, int
        ), f'total_failures, expected int got {type(total_failures)}'
        assert isinstance(
            total_requests, int
        ), f'total_requests, expected int got {type(total_requests)}'
        return False


class ShouldNotOpenRule(_BaseFakeRule):

    def should_open_circuit(self, total_failures, total_requests):
        return super().should_open_circuit(total_failures, total_requests)

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldOpenRule(_BaseFakeRule):

    def should_open_circuit(self, total_failures, total_requests):
        super().should_open_circuit(total_failures, total_requests)
        return True

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldNotIncreaseFailureRule(_BaseFakeRule):

    def should_increase_failure_count(self):
        return False

    def should_open_circuit(self, total_failures, total_requests):
        return super().should_open_circuit(total_failures, total_requests)

    def log_increase_failures(self, total_failures, total_requests):
        pass


class ShouldNotIncreaseRequestRule(_BaseFakeRule):

    def should_increase_request_count(self):
        return False

    def should_open_circuit(self, total_failures, total_requests):
        return super().should_open_circuit(total_failures, total_requests)

    def log_increase_failures(self, total_failures, total_requests):
        pass
