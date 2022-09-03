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

## API Contract

### List of Trips (GET)
Get all vehicles records in dataset.
> /vehicles

query_params avaliables in this route:
- region : Get vehicles records in specific region
- origin_coord_x : Get vehicles records in specific coordinate origin x 
- origin_coord_y : Get vehicles records in specific coordinate origin y
- destination_coord_x : Get vehicles records in specific coordinate destination x
- destination_coord_y : Get vehicles records in specific coordinate destination y 
- datasource : Get vehicles records filtering by datasource variable
- date : Get vehicles records filtering by datetime column (considering only date statement)

Example:

`/vehicles?region=Turin`

Sample Output:

    {
      "data": [
        {
            "datasource": "baba_car",
            "datetime": "Mon, 21 May 2018 02:54:04 GMT",
            "destination_coord_point_x": "7.72036863753512",
            "destination_coord_point_y": "45.0678238539384",
            "id": 1,
            "origin_coord_point_x": "7.67283791328688",
            "origin_coord_point_y": "44.995710924205",
            "region": "Turin"
        },
        {
            "datasource": "bad_diesel_vehicles",
            "datetime": "Sun, 06 May 2018 09:49:16 GMT",
            "destination_coord_point_x": "7.7452865344197",
            "destination_coord_point_y": "45.0262859834150",
            "id": 3,
            "origin_coord_point_x": "7.54150918911443",
            "origin_coord_point_y": "45.0916050382774",
            "region": "Turin"
        }
      ]
    }

### Specific Vehicle Record (GET)
Get specific vehicle record by specific (id).
> /vehicles/(id)

Example:

`/vehicles/1`

Sample Output:

    {
        "datasource": "baba_car",
        "datetime": "Mon, 21 May 2018 02:54:04 GMT",
        "destination_coord_point_x": "7.72036863753512",
        "destination_coord_point_y": "45.0678238539384",
        "id": 1,
        "origin_coord_point_x": "7.67283791328688",
        "origin_coord_point_y": "44 995710924205",
        "region": "Turin"
    }

### Count by (GET)
Get count of elements by specif (column) in dataset.
> /vehicles/(column)/count

Example:

`/vehicles/region/count`

Sample Output:

    {
     "data": [
        {
            "count": 28,
            "region": "Hamburg"
        },
        {
            "count": 34,
            "region": "Prague"
        },
        {
            "count": 38,
            "region": "Turin"
        }
      ]
    }


### Weekly Trips (GET)
Get count of elements per week (using datetime column) and region.
> /vehicles/weekly_trips/region 

Sample Output:

    {
      "data": [
        {
            "freq_trip": 5,
            "region": "Hamburg",
            "week_number": 18
        },
        {
            "freq_trip": 10,
            "region": "Prague",
            "week_number": 18
        },
        {
            "freq_trip": 8,
            "region": "Turin",
            "week_number": 18
        }
      ]
    }

### Weekly Average Trips (GET)
Get average of elements per week (using datetime column) and region.
> /vehicles/weekly_avg_trips/region

Sample Output:

    {
      "data": [
        {
            "freq_avg_weekly_trips": "7.6000000000000000",
            "region": "Turin"
        },
        {
            "freq_avg_weekly_trips": "5.6000000000000000",
            "region": "Hamburg"
        },
        {
            "freq_avg_weekly_trips": "6.8000000000000000",
            "region": "Prague"
        }
      ]
    }

### Status of Process' Data Ingestion (GET)
Get status of process' data ingestion.
> /vehicles/ingest-data/status

Sample Output (1):

    {
        "review": "Nothing in processing"
    }

Sample Output (2):

    {
        "end_time": "09/03/2022, 17:33:17",
        "lead_time": "0:00:00.002999",
        "review": "Process Finished",
        "start_time": "09/03/2022, 17:33:17"
    }


### Process' Data Ingestion (POST)
Start ingestion process with CSVs file in data/raw. **This process will replace all data in dataset.** You can check status of process making request with Get Method to endpoint /**vehicles/ingest-data/status**.
> /vehicles

Output:

    Ingestion Started


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
