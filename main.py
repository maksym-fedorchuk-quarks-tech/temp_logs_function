from datetime import datetime
import os

import functions_framework
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


def record_data(temp: int, location: str) -> tuple:
    try:
        # Init BigQuery
        client = bigquery.client.Client()
        table_ref = client.dataset(os.environ.get('DATASET')).table(os.environ.get('TABLE'))
        table = client.get_table(table_ref)

        # Insert rows
        errors = client.insert_rows(
            table,
            [{'dt': datetime.utcnow(), 'location': location, 'sensor_id': 1, 'scale': 'celsius', 'temperature': temp}]
        )

        if errors:
            raise Exception(f'Exception during inserting rows: {errors}')

        return 'Data successfully written to BigQuery.', 200

    except Exception as e:
        print(f'Error: {e}')
        return 'Error writing data to BigQuery.', 500


@functions_framework.http
def record(request):
    request_args = request.args

    if request_args and 'temperature' in request_args and 'location' in request_args:
        return record_data(request_args['temperature'], request_args['temperature'])

    if request_args and 'readme' in request_args:
        return "Endpoint for logging temperature data to the BigQuery. Pass temperature:int and location: str as a " \
               "params at current endpoint POST request"

    return 'Following params needed: temperature & location. More info - send readme as a parameter'
