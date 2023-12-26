from datetime import datetime
import os

import functions_framework
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


def record_data(raw: dict) -> tuple:
    try:
        print('record_data raw input:', raw)

        # Init BigQuery
        client = bigquery.Client()

        # Get BigQuery table link
        dataset_ref = os.environ.get('DATASET')
        table_ref = dataset_ref.table(os.environ.get('TABLE'))
        table = client.get_table(table_ref)

        # Data for table
        rows_to_insert = [
            {'dt': datetime.utcnow(), 'location': 'home', 'sensor_id': 1, 'scale': 'celsius', 'temperature': 0}
        ]

        # Insert rows
        errors = client.insert_rows(table, rows_to_insert)

        if errors:
            raise Exception(f'Error inserting rows: {errors}')

        # Ok. 200
        return 'Data successfully written to BigQuery.', 200

    except Exception as e:
        print(f'Error: {e}')
        # Обробка помилок та відповідь на невдале виконання
        return 'Error writing data to BigQuery.', 500


@functions_framework.http
def record(request):
    request_args = request.args

    if request_args and 'temperature' in request_args:
        return record_data({'temperature': request_args['temperature']})

    if request_args and 'get_table' in request_args:
        return f"Table from env: {os.environ.get('TABLE')}"

    return 'Try one more time ...'
