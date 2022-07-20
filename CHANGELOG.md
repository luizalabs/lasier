# Changelog

## [0.3.0] - 2022-07-20

## Changes
* Adds async adapter for Django

## [0.2.4] - 2022-07-14

### Changes
* Fix DjangoAdapter behavior

## [0.2.0] - 2022-03-17

### Changes
* Migrate to poetry
* Update dependencies

### Added
* Python 3.10 support

## [0.1.1] - 2020-06-04

### Changes

* Ignore request cache key operations when it is not configured

## [0.1.0] - 2020-05-15
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
