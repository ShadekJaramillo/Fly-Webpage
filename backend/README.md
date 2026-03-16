# Fly database API

This is the API that manages the data for the Fly pole sports center web app.

## Dependencies

This project uses FastAPI for routing and SQLAlchemy for interacting with the database. For testing the pytest framework is used with factory-boy and faker for test objects.

## Project Structure

The API follows a feature based structure, where each feature follows an hexagonal architechture. ([Hexagonal architecture explained](https://medium.com/@tejasrawat_82721/hexagonal-architecture-ports-and-adapters-explained-a-practical-guide-from-concept-to-code-7903053f38f4)):

Here is a general schema of the project:

```
api
├── alembic/
├── src/db_api
│   ├── shared-kernel/ # module containing shared stuff with other modules.
│   ├── attendances/
│   ├── observations/
│   └── physical_valuations/
├── tests/
├── .env
├── .gitignore
└── alembic.ini
```

```
api
├── src/db_api/
│   ├── my_module/
│   │   ├── adapters # out-bound adapters.
│   │   │   ├── my_module_repository_adapter.py # out-bound adapter.
│   │   │   ... # other adapters
│   │   ├── api/ # application layer related stuff.
│   │   │   ├── dependencies.py # get_dependency functions for dependency injection
│   │   │   ├── router.py # what I am coding now
│   │   │   ├── schemas.py # data transfer objects
│   │   │   └── use_cases.py # functions called to execute the business logic.
│   │   ├── domain/ # business logic.
│   │   │   ├── core.py # this is where the service code actually is
│   │   │   ├── entities.py # domain data objects and enums.
│   │   │   ├── exceptions.py
│   │   │   └── ports.py # ports that the out-bound adapter can implement
│   ├── other_module/
│   ...
│
...
```
