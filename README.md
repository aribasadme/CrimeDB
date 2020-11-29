# CrimeDB
 Integration layer for data that can be retrieved by means of the Police API.
 Documentation for the API can be found at https://data.police.uk/docs/
 
 UK Police provides a Python client for the Police API (https://github.com/rkhleics/police-api-client-python/). I used this client for simplicity without having to do the requests to the api by myself.
 
## Source Tables
We retreive the data from the following calls to API:
- Crimes at a location [https://data.police.uk/docs/method/crimes-at-location/]
- Crime categories [https://data.police.uk/docs/method/crime-categories/]
- Outcomes for a specific crime [https://data.police.uk/docs/method/outcomes-for-crime/]
## Destination Tables
This integration will populate the following tables:
- crime_categories
- outcomes_categories
- streets
- crimes
- outcomes

### Table fields
| crime_categories  |  |
| -----| ----------- |
| pk  | id  |
|   | description  |

| outcomes_categories  |  |
| -----| ----------- |
| pk  | id  |
|   | description  |

| streets  |  |
| -----| ----------- |
| pk  | id  |
|   | name  |

| crimes  |  |
| -----| ----------- |
| pk  | id  |
| fk  | category  |
| fk | street  |
|   | city  |
|   | latitude |
|   | longitude  |
|   | date  |
|   | context  |

| outcomes  |  |
| -----| ----------- |
| fk  | crime  |
| fk  | category  |
|   | date  |
|   | person_id  |

## Particular Considerations
In some cases I found crimes without the field "persistent_id" therefore I haven't considered these records.
The Python API client doesn't provide the "person_id" for the class "Outcome" so I didn't use it.
I wasn't able to find a way to obtain the field "city" for the crimes table so I didn't include it.
