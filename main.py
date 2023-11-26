import functions_framework

from google.cloud import bigquery
from datetime import datetime

from dotenv.main import dotenv_values

config = dotenv_values(".env")


def record_data(raw: dict) -> tuple:
    try:
        # Init BigQuery
        client = bigquery.Client()

        # Get BigQuery table link
        dataset_ref = config["DATASET"]
        table_ref = dataset_ref.table(config["TABLE"])
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

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'temperature' in request_json:
        # return record_data({'temperature': request_json['temperature']})
        return f"Temperature received ({request_json['temperature']})"

    elif request_args and 'temperature' in request_args:
        # return record_data({'temperature': request_args['temperature']})
        return f"Temperature received ({request_args['temperature']})"

    return 'Try one more time ...'
