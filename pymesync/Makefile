PY?=python

help:
				@echo 'Makefile for pymesync                                         '
				@echo '                                                              '
				@echo 'Usage:                                                        '
				@echo '   make clean     remove the generated files                  '
				@echo '   make test      run tests                                   '
				@echo '   make flake     run flake8 on application and tests.py      '
				@echo '   make verify    run tests and flake8                        '
				@echo '                                                              '

clean:
	      rm *.pyc

test:
	      $(PY) tests.py && $(PY) test_mock_pymesync.py

flake:
	      flake8 pymesync.py tests.py test_mock_pymesync.py

verify: test flake
