# To recreate the virtual environment do the following in linux
```
python3 -m venv venv
```

# To activate the environment run the following
```
source venv/bin/activate
```

# Install the following
```
python -m pip install fastapi[all]
python -m pip install sqlmodel
python -m pip install pytest
```

# Create a database by running the following
This should be run only once!!
Before running delete the database to avoid overwriting
```
python app/database.py
```

# Run the following to start the api server
```
python app/main.py
```

# Open the following in the browser to read the documentation and interactively give API requests
```
http://127.0.0.1:8000/docs
```

# To visualize the databank

- Either use DBBrowser to open the bank.db file or
- use vscode extension SQLite Viewer