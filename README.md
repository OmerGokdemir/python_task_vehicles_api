# Project: Python Task

This project consists of a Django-based REST API server and a Python client for handling vehicle data. The goal is to process a CSV file, transmit it to the server, and generate a dynamically colored Excel file based on specific rules.

## Features

### Server:

* Implements a REST API using Django Rest Framework (DRF).

* Accepts CSV file uploads via a POST endpoint.

* Fetches additional vehicle data from an external API.

* Filters and merges vehicle data with the CSV input.

* Returns the processed data in JSON format.

### Client:

* Sends a CSV file to the server.

* Handles the server response and converts it into an Excel file.

* Supports dynamic row coloring based on vehicle inspection dates (HU field).

* Allows users to specify additional columns via command-line arguments.

### Requirements

The project requires the following dependencies (listed in requirements.txt):

```bash
asgiref==3.8.1
certifi==2024.8.30
charset-normalizer==3.4.0
Django==5.1.3
djangorestframework==3.15.2
idna==3.10
numpy==2.1.3
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2024.2
requests==2.32.3
six==1.16.0
sqlparse==0.5.2
tzdata==2024.2
urllib3==2.2.3
```

### Installation

1. Clone the repository:
```
git clone https://github.com/OmerGokdemir/python_task_vehicles_api.git
cd python-task
```
2. Create and activate a virtual environment:
```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```

### Usage

#### Server

1. Navigate to the server directory:
```
cd vehicles_api
```
2. Apply migrations and run the server:
```
python manage.py migrate
python manage.py runserver
```
3. The server will start at `http://127.0.0.1:8000/`.

4. Test the upload endpoint:

    * Endpoint: `POST /api/upload/`

    * Payload: A CSV file containing vehicle data.

#### Client

Navigate to the client directory (if applicable).

1. Run the client script with the required parameters:
```
python client.py -f vehicles.csv -k kurzname info -c
```
* `-f`: Path to the input CSV file.

* `-k`: Specify additional columns to include in the output.

* `-c`: Enable row coloring (default is True).

2. The output Excel file will be saved as vehicles_{current_date}.xlsx.

### Excel File Output

* Rows are sorted by the gruppe field.

* Columns always include the rnr field and the columns specified with the -k flag.

* **Row colors:**

    * Green (#007500): Inspection date (HU) is less than 3 months old.

    * Orange (#FFA500): Inspection date is between 3 and 12 months old.

    * Red (#b30000): Inspection date is more than 12 months old.

* If labelIds is specified and at least one colorCode is resolved, the first colorCode is used to tint the cell text.

### Example Input and Output

#### Example Input (vehicles.csv):
```
rnr,gruppe,hu,kurzname,info
1,groupA,2023-06-01,shortname1,info1
2,groupB,2023-01-01,shortname2,info2
3,groupA,2022-12-01,shortname3,info3
```
#### Example Output (Excel):

* File: `vehicles_2024-12-03.xlsx`

* Includes the specified columns (`kurzname`, `info`).

* Rows colored based on the hu field.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contact

For questions or support, please contact omer66gokdemir@gmail.com.

