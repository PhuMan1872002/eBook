# eBook

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Create the environment (creates a folder in your current directory)

```bash
virtualenv .venv
```

In Linux or Mac, activate the new python environment

```bash
source .venv/bin/activate
```

Or in Windows

```bash
source .venv/Scripts/activate
```

### Installing

Install file `requirements.txt`

```bash
pip install -r requirements.txt
```

File `.env`

```bash
SECRET_KEY=<secret_key>
DB_USERNAME=<username>
DB_PASSWORD=<password>
DB_HOST=<host>
DB_NAME=<db_name>
```

With the above application you can create a migration repository with the following command:

```bash
flask db init
```

This will add a `migrations` folder to your application. The contents of this folder need to be added to version control along with your other source files.

You can then generate an initial migration:

```bash
flask db migrate -m "Initial migration."
```

Then you can apply the changes described by the migration script to your database:

```bash
flask db upgrade
```