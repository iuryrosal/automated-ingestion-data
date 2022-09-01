automated-ingestion-data
==============================

Your task is to build an automatic process to ingest data on an on-demand basis. The data represents trips taken by different vehicles, and include a city, a point of origin and a destination.

## Mandatory Features
● There must be an automated process to ingest and store the data.
● Trips with similar origin, destination, and time of day should be grouped together.
● Develop a way to obtain the weekly average number of trips for an area, defined by a
bounding box (given by coordinates) or by a region.
● Develop a way to inform the user about the status of the data ingestion without using a
polling solution.
● The solution should be scalable to 100 million entries. It is encouraged to simplify the
data by a data model. Please add proof that the solution is scalable.
● Use a SQL database.

## Project Organization
------------
    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── tests              <- Test's script for code source
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

## Git Commit Convention
The commits carried out in this project seek to follow this Git Commit pattern to facilitate maintenance and knowledge management:

> 🔰 type (scope): subject

### Symbols (🔰)
https://gitmoji.dev 

### Types
- test: Indicates any type of creation or alteration of test codes
- feat: Indicates the development of a new feature to the project
- refactor: Refactoring that does not impact business logic/rules
- style: Used when there are formatting and code style changes that do not change the system in any way.
- fix: bug fix.
- chore: Changes that do not affect source code or test files
- docs: Change regarding files, directories and documentation
- ci: CI configuration changes
- local: Changes to the project's local run configuration

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
