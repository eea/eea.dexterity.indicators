# Makefile to configure and run Plone instance

##############################################################################
# SETUP MAKE

## Defensive settings for make: https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
# for Makefile debugging purposes add -x to the .SHELLFLAGS
.SHELLFLAGS:=-eu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# Colors
# OK=Green, warn=yellow, error=red
ifeq ($(TERM),)
# no colors if not in terminal
	MARK_COLOR=
	OK_COLOR=
	WARN_COLOR=
	ERROR_COLOR=
	NO_COLOR=
else
	MARK_COLOR=`tput setaf 6`
	OK_COLOR=`tput setaf 2`
	WARN_COLOR=`tput setaf 3`
	ERROR_COLOR=`tput setaf 1`
	NO_COLOR=`tput sgr0`
endif

##############################################################################
# SETTINGS AND VARIABLE
# adjust to your project needs
PROJECT_NAME=eea.dexterity.indicators
IMAGE_NAME=${PROJECT_NAME}
CONSTRAINTS=constraints.txt
PIP_REQUIREMENTS_IN_FILE=requirements.txt
ADDONBASE=./
ADDONFOLDER=${ADDONBASE}

PIP_PARAMS= --pre

##############################################################################
# targets and prerequisites
# target has to be one file, otherwise step gets executes for each file separate
PREPARE_PREREQUISITES=${PIP_REQUIREMENTS_IN_FILE} ${CONSTRAINTS} mx.ini ${ADDONBASE}setup.cfg
PREPARE_TARGET=requirements-mxdev.txt
INSTALL_PREREQUSISTES=${PREPARE_TARGET}
INSTALL_TARGET=.installed.txt

.PHONY: all # styling
all:style

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@echo "${OK_COLOR}This is the Makefile for ${WARN_COLOR}${PROJECT_NAME}${NO_COLOR}"
	@echo
	@echo "${WARN_COLOR}Additional parameters:${NO_COLOR}"
	@echo "${MARK_COLOR}PYTHON${NO_COLOR}:      Python interpreter to be used (default: python3)"
	@echo "${MARK_COLOR}VENV${NO_COLOR}:        [on|off] wether to create a Python virtual environment or not (default: on)"s
	@echo "${MARK_COLOR}VENV_FOLDER${NO_COLOR}: location of the virtual environment (default: ./venv)"
	@echo
	@echo "${WARN_COLOR}Targets:${NO_COLOR}"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

##############################################################################

##############################################################################
# BASE

SENTINELFOLDER=.make-sentinels/
SENTINEL=${SENTINELFOLDER}ABOUT.txt
${SENTINEL}:
	@mkdir -p ${SENTINELFOLDER}
	@echo "Sentinels for the Makefile process." > ${SENTINEL}

# PYTHON, VENV, PIP
# venv and pybin
PYTHON?=python3
VENV?=on
ifeq ("${VENV}", "on")
	VENV_FOLDER?=./venv
	PYBIN=${VENV_FOLDER}/bin/
else
	VENV_FOLDER?=
	ifneq ("${VENV_FOLDER}", "")
		PYBIN=${VENV_FOLDER}/bin/
		PYTHON=${PYBIN}python
	else
		PYBIN=
	endif
endif

# installed?
ifeq (, $(shell which $(PYTHON) ))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

# version ok?
PYTHON_VERSION_MIN=3.7
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys; print(int(sys.version_info[0:2] >= tuple(map(int, "$(PYTHON_VERSION_MIN)".split(".")))))' )

ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

VENV_SENTINEL=${SENTINELFOLDER}venv.sentinel
${VENV_SENTINEL}: ${SENTINEL}
ifeq ("${VENV}", "on")
	@echo "$(OK_COLOR)Setup Python Virtual Environment under '${VENV_FOLDER}' $(NO_COLOR)"
	@${PYTHON} -m venv ${VENV_FOLDER}
else
	@echo "$(OK_COLOR)Use current local or global Python: `which ${PYTHON}` $(NO_COLOR)"
endif
	@touch ${VENV_SENTINEL}

PIP_SENTINEL=${SENTINELFOLDER}pip.sentinel
${PIP_SENTINEL}: ${VENV_SENTINEL} ${CONSTRAINTS} ${SENTINEL}
	@echo "$(OK_COLOR)Install pip$(NO_COLOR)"
	@${PYBIN}pip install -U "pip>=22.0.2" wheel setuptools
	@touch ${PIP_SENTINEL}

##############################################################################
# MXDEV

MXDEV_SENTINEL=${SENTINELFOLDER}pip-mxdev.sentinel
${MXDEV_SENTINEL}: ${PIP_SENTINEL}
	@echo "$(OK_COLOR)Install mxdev$(NO_COLOR)"
	@${PYBIN}pip install "mxdev==2.1.0" "libvcs==0.11.1"
	@touch ${MXDEV_SENTINEL}

.PHONY: prepare
prepare: ${PREPARE_TARGET} ## prepare soures and dependencies

${PREPARE_PREREQUISITES}:
	@touch $@

${PREPARE_TARGET}: ${MXDEV_SENTINEL} ${PREPARE_PREREQUISITES}
	@echo "$(OK_COLOR)Prepare sources and dependencies$(NO_COLOR)"
	@${PYBIN}mxdev -c mx.ini


BLACK_SENTINEL=${SENTINELFOLDER}pip-black.sentinel
${BLACK_SENTINEL}: ${PREPARE_TARGET}
	@echo "$(OK_COLOR)Install black$(NO_COLOR)"
	@${PYBIN}pip install black
	@touch ${BLACK_SENTINEL}

ISORT_SENTINEL=${SENTINELFOLDER}pip-isort.sentinel
${ISORT_SENTINEL}: ${PREPARE_TARGET}
	@echo "$(OK_COLOR)Install isort$(NO_COLOR)"
	@${PYBIN}pip install isort
	@touch ${ISORT_SENTINEL}

ZPRETTY_SENTINEL=${SENTINELFOLDER}pip-zpretty.sentinel
${ZPRETTY_SENTINEL}: ${PREPARE_TARGET}
	@echo "$(OK_COLOR)Install zpretty$(NO_COLOR)"
	@${PYBIN}pip install "zpretty>=2.2.0"
	@touch ${ZPRETTY_SENTINEL}

.PHONY: apply-style-black
apply-style-black: ${BLACK_SENTINEL}  ## apply/format code style black (to Python files)
	@echo "$(OK_COLOR)Apply style black rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@${PYBIN}black ${ADDONFOLDER}

.PHONY: apply-style-isort
apply-style-isort: ${ISORT_SENTINEL} ## apply/format code style isort (sorted imports in Python files)
	@echo "$(OK_COLOR)Apply style isort rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@${PYBIN}isort ${ADDONFOLDER}

.PHONY: apply-style-zpretty
apply-style-zpretty: ${ZPRETTY_SENTINEL}   ## apply/format code style zpretty (to XML/ZCML files)
	@echo "$(OK_COLOR)Apply style zpretty rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@find ${ADDONFOLDER} -name '*.zcml' -exec ${PYBIN}zpretty -iz {} +
	@find ${ADDONFOLDER} -name "*.xml"|grep -v locales|xargs ${PYBIN}zpretty -ix

.PHONY: style ## apply code styles black, isort and zpretty
style: apply-style-black apply-style-isort

.PHONY: format ## alias for "style"
FORMATTING: style

.PHONY: lint-black
lint-black: ${BLACK_SENTINEL}  ## lint code-style black (to Python files)
	@echo "$(OK_COLOR)Lint black rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@${PYBIN}black --check ${ADDONFOLDER}

.PHONY: lint-isort
lint-isort: ${ISORT_SENTINEL} ## lint code-style isort (sorted imports in Python files)
	@echo "$(OK_COLOR)Lint style isort rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@${PYBIN}isort --check-only ${ADDONFOLDER}

.PHONY: lint-zpretty
lint-zpretty: ${ZPRETTY_SENTINEL}   ## lint code-style zpretty (to XML/ZCML files)
	@echo "$(OK_COLOR)Lint style zpretty rules to code in ${ADDONFOLDER}/*$(NO_COLOR)"
	@find ${ADDONFOLDER} -name '*.zcml' -exec ${PYBIN}zpretty --check -z {} +
	@find ${ADDONFOLDER} -name '*.xml'|grep -v locales|xargs ${PYBIN}zpretty --check -x

.PHONY: lint ## lint all: check if complies with code-styles black, isort and zpretty
lint: lint-black lint-isort

##############################################################################
# CLEAN
.PHONY: clean-venv
clean-venv: ## remove Python virtual environment
ifeq ("${VENV}", "on")
	@echo "$(OK_COLOR)Remove Virtualenv.$(NO_COLOR)"
	rm -rf ${VENV_FOLDER} ${SENTINELFOLDER}/pip*.sentinel ${VENV_SENTINEL}
else:
	@echo "$(OK_WARN)No self-created Python virtualenv at '${VENV_FOLDER}'! Nothing to do.$(NO_COLOR)"
endif

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "$(OK_COLOR)Remove Python file artifacts (like byte-code) of code in current directory.$(NO_COLOR)"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-make
clean-make:  ## remove make artifact	@echo "$(OK_COLOR)Remove Plone/Zope configuration (keeps data) and sentinel files.$(NO_COLOR)"
	rm -rf ${INSTALL_PREREQUSISTES} ${SENTINELFOLDER} constraints-mxdev.txt

.PHONY: clean
clean:  clean-venv clean-pyc clean-make  ## clean all (except local database and pip installed packages)