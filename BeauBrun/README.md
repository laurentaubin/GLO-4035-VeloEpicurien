# BeauBrun

### Run the app in a dev environment
#### Install packages
For of all, you need to install ``virtualenv``. To do so,  run the following command:
```bash
pip install virtualenv
```

Once ``virtualenv`` is downloaded, go to the root of the project and run the following commands:
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

This activates a virtual environment where you can install all the dependencies to run the project.

Then, run 
```bash
pip install -r requirements.txt
```

All the dependencies should be installed and the app is ready to run.

To deactivate the virtual environment, run ```deactivate``` in your command line.

#### Run the app
```bash
make run
```

### Testing and linting
#### Run all tests
```bash
make test
```

If you are on Windows and can't use `make`, you can try to run:
```bash
python -m nose test
```

#### Run formatter on source and test files: 
```bash
make format
```

If you are using Pycharm and want to format the code on save, follow these [instructions](https://black.readthedocs.io/en/stable/editor_integration.html) (Black documentation)

#### Linting
```bash
make lint
```
