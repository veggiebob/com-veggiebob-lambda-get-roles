from db_conn import get_conn


def process_request() -> list[str]:
    with get_conn() as cursor:
        cursor.execute('SELECT key FROM llm_cache_keys')
        return [row[0] for row in cursor.fetchall()]

def lambda_handler(event, context):
    try:
        results = process_request()
        return {
            'statusCode': 200,
            'body': results
        }
    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }

if __name__ == "__main__":
    example_event = {}
    example_context = {}
    result = lambda_handler(example_event, example_context)
    print(result)