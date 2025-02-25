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
```
python app/database.py
```