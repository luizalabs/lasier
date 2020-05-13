# Changelog

## [NEXT_RELEASE]
### Changes
* Args `failure_timeout` and `circuit_timeout` of CircuitBreaker to have a default value
* Call `expire` after `incr` to prevent keys on storage without TTL
* Remove unnecessary `storage.add` calls

### Added
* Upload to pypi on travis CI
* Expire method on storage interface
* DjangoAdapter an adapter to django cache framework

## [0.0.2] - 2020-04-28
### Added
* Typing hint all classes and functions
* `mypy` and `black` on `make check` recipe (which is runned in each CI job)


## [0.0.1] - 2020-04-08
* First Release :tada:
