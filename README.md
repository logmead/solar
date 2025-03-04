## About

This Django project contains a web interface to plot/view data from some CDF files, structured in a particular way.

Project contains 3 apps:
  - load_cdf<br>
Manages data uploads from CDf files to the db, while structuring the data in dynamic models. This app contains models that keep track of dynamic ones.
   
   - data_cdf<br>
Contains said dynamically created models and corresponding migrations.

   - pages<br>
Has views to display info about created models and uploaded data, as well as views that plot the data. 

## Setup

### Database
Project uses PostgreSQL database, so postgresql cluster is required, as well as __psycopg3__ installation.

### Python dependecies
```
Django==4.2.16
numpy==2.0.2
plotly==5.24.1
pandas==2.2.3
spacepy==0.7.0
```

### data_cdf app
data_cdf app is situated outside of the main project directory, since the contents are changed by user actions.
All of its models are imported in the project anyway, so importing data_cdf as a project app requires additional configuration:

in settings.py:
```python
# save path to the directory that contains extras for the project
SUB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'solarterra_submodules'))

# save path to the directory that contains dynamic models
MODEL_DIR_PATH = os.path.join(SUB_PATH, 'data_cdf/models')

sys.path.append(SUB_PATH)
```

in data_cdf/models/\_\_init\_\_.py:
```python
import os, sys 

path = os.path.dirname(os.path.abspath(__file__))

for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
    mod = __import__('.'.join([__name__, py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)

```


