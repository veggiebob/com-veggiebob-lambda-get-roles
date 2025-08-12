from typing import Literal, TypedDict, Union

from db_conn import get_conn


class GetRolesRequest(TypedDict, total=False):
    """Schema for retrieving all LLM cache keys."""

    request_type: Literal["get_roles"]


class AddRoleRequest(TypedDict):
    """Schema for adding a new LLM cache key."""

    request_type: Literal["add_role"]
    key: str


Request = Union[GetRolesRequest, AddRoleRequest]


def get_roles() -> list[str]:
    """Fetch all keys from ``llm_cache_keys``."""

    with get_conn() as cursor:
        cursor.execute("SELECT key FROM llm_cache_keys")
        return [row[0] for row in cursor.fetchall()]


def add_role(key: str) -> None:
    """Insert a new key into ``llm_cache_keys``."""

    with get_conn() as cursor:
        cursor.execute(
            "INSERT INTO llm_cache_keys (key) VALUES (%s)",
            (key,),
        )
        cursor.connection.commit()


def lambda_handler(event: Request, context):
    try:
        request_type = event.get("request_type", "get_roles")
        if request_type == "add_role":
            key = event.get("key")
            if not key:
                return {"statusCode": 400, "body": "Missing key"}
            add_role(key)
            body = f"Added key {key}"
        else:
            body = get_roles()
        return {"statusCode": 200, "body": body}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}


if __name__ == "__main__":
    example_context = {}
    example_event_get: GetRolesRequest = {"request_type": "get_roles"}
    print(lambda_handler(example_event_get, example_context))

    example_event_add: AddRoleRequest = {
        "request_type": "add_role",
        "key": "demo-key",
    }
    print(lambda_handler(example_event_add, example_context))

