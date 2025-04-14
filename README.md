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

### Work with CDF files

- для работы с CDF файлами используется модуль spacepy.pycdf:
```bash
import spacepy
```

- посмотреть документацию класса CDF, Var:
```python
pycdf.CDF.__dict__['__doc__']
pycdf.Var.__dict__['__doc__']
```

- чтобы открыть CDF файл (экземпляр CDF):
```python
cdf = pycdf.CDF("MyFile.cdf")
```

- CDF класс имеет список глобальных аттрибутов (словарь):
```python
cdf.attrs
```

- посмотреть один аттрибут: 
```python
cdf.attrs[<attrname>]
```

- CDF класс представляет из себя аналог словаря, ключами являются названия переменных файла. Чтобы увидеть названия:
```python
cdf.keys()
```

- чтобы увидеть одну переменную (экземпляр Var):
```python
cdf[<key>]
```

- чтобы увидеть все свойства переменной:
```python
cdf[<key>].attrs
```

- чтобы увидеть содержимое переменной (список, похожий на numpy array):
```python
cdf[<key>][...]
```

Полезные ссылки по CDF:<br>
https://spdf.gsfc.nasa.gov/pub/software/cdf/doc/cdf390/cdf390ug.pdf - CDF User's Guide<br>
https://spacepy.github.io/pycdf.html - Python interface to CDF files

