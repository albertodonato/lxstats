#
# This file is part of Procsys.

# Procsys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Procsys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Procsys.  If not, see <http://www.gnu.org/licenses/>.

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
	rm -rf build *.egg-info _trial_temp

test:
	@$(TEST_RUNNER) $(BASEDIR)

lint:
	@$(LINT) $(BASEDIR)

.PHONY: build
