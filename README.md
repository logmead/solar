### About

This is a Django project to load data from .CDF files to the db using ORM and plot them using plotly python library.

### Setup
After cloning the project files, it also recommended:

- to create a python virtual environment (one way to do it):

```bash
python -m venv solar_venv
. solar_venv/bin/activate
pip install -r venv_requirements
```

- to create a configs/settings_sensitive.json file, it is required in solarterra/solarterra/settings.py to specify:

1. Django`s Secret Key - can be generated using:

```python
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```

2. ALLOWED_HOSTS - list of strings with allowed hostnames, e.g. "localhost" or "0.0.0.0"

3. DB_* - Database connection details

!LEMON FOREVER!
