from datetime import datetime
import os

import functions_framework
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()


def record_data(temp: str) -> tuple:
    try:
        # Init BigQuery
        client = bigquery.client.Client()
        dataset_ref = client.dataset(os.environ.get('DATASET'))
        table_ref = dataset_ref.table(os.environ.get('TABLE'))

        # Insert rows
        errors = client.insert_rows(
            table_ref,
            [{'dt': datetime.utcnow(), 'location': 'home', 'sensor_id': 1, 'scale': 'celsius', 'temperature': temp}]
        )

        if errors:
            raise Exception(f'Error inserting rows: {errors}')

        return 'Data successfully written to BigQuery.', 200

    except Exception as e:
        print(f'Error: {e}')
        # Обробка помилок та відповідь на невдале виконання
        return 'Error writing data to BigQuery.', 500


@functions_framework.http
def record(request):
    request_args = request.args

    if request_args and 'temperature' in request_args:
        return record_data(request_args['temperature'])

    if request_args and 'get_table' in request_args:
        return f"Table from env: {os.environ.get('TABLE')}"

    return 'Try one more time ...'
