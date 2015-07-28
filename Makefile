UNZIP ?= unzip
WGET ?= wget

PYTHON ?= python2
SETUP ?= $(PYTHON) setup.py

MACOSX_VERSION ?= 10.10

ARCHIVE_NAME = jsshell-$(PLATFORM_NAME).zip
DOWNLOAD_URL = https://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-aurora/$(ARCHIVE_NAME)

LIB_DIR = spidermonkey
ARCHS = linux-x86_64 mac


help:
	@echo 'The following make targets are available:'
	@echo '  download	Download new versions of Spidermonkey from the current Firefox Aurora branch.'
	@echo '  purge		Purge downloaded copies of Spidermonkey.'
	@echo '  build		Build wheels for each platform.'
	@echo '  clean		Cleans up after wheel build process.'


download.%: PLATFORM_NAME=$*
download.mac: PLATFORM_LIB=$(LIB_DIR)/lib/os-x
download.linux-x86_64: PLATFORM_LIB=$(LIB_DIR)/lib/linux

download: $(ARCHS:%=download.%)

download.%: purge.%
	cd $(PLATFORM_LIB) && \
	$(WGET) $(DOWNLOAD_URL) && \
	$(UNZIP) $(ARCHIVE_NAME) && \
	rm -f $(ARCHIVE_NAME)

purge.%: phony
	mkdir -p $(PLATFORM_LIB)
	cd $(PLATFORM_LIB) && rm -f *


build: $(ARCHS:%=build.%)
clean: $(ARCHS:%=clean.%)

build.linux-x86_64: PYTHON_PLATFORM=linux-x86_64
clean.linux-x86_64: PYTHON_PLATFORM=linux-x86_64
build.mac: PYTHON_PLATFORM=macosx-$(MACOSX_VERSION)-intel
clean.mac: PYTHON_PLATFORM=macosx-$(MACOSX_VERSION)-intel

build.%: clean.%
	_PYTHON_HOST_PLATFORM=$(PYTHON_PLATFORM) \
	$(SETUP) bdist_wheel

clean.%: phony
	_PYTHON_HOST_PLATFORM=$(PYTHON_PLATFORM) \
	$(SETUP) clean --all

.PHONY: help phony build clean download purge
