BASEDIR = procsys

PYTHON = python
TEST_RUNNER = trial
LINT = flake8
SETUP = $(PYTHON) setup.py

all: build

build:
	$(SETUP) build

devel:
	$(SETUP) develop

clean:
	rm -rf build procsys.egg-info _trial_temp

test:
	@$(TEST_RUNNER) $(BASEDIR)

lint:
	@$(LINT) $(BASEDIR)

.PHONY: build
