# pymesync

Python module for TimeSync

We use virtualenv for development and testing:

```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

For usage documentation, build our docs:

```
(venv) $ cd docs
(venv) $ make html
(venv) $ <browser> build/html/index.html
```

To test the source code:

```
(venv) $ make test
(venv) $ make flake    # Runs flake8 on pymesync.py and tests.py
```

or

```
(venv) $ make verify   # Runs tests and flake8
```
