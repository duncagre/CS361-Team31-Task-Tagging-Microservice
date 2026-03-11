import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5002"

#   -------------------------
#   Request helper
#   -------------------------

def post_json(route, payload):
    """
    Sends a POST request with JSON data.
    """
    url = BASE_URL + route
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            return response.status, json.loads(response_data)
    except urllib.error.HTTPError as error:
        response_data = error.read().decode("utf-8")
        return error.code, json.loads(response_data)


#   -------------------------
#   Test functions
#   -------------------------

def test_add_tag():
    """
    Tests adding a tag to a task.
    """
    status, response = post_json("/add-tag", {
        "task_id": "1",
        "tag": "School"
    })

    print("\nTest: add tag")
    print("Status:", status)
    print("Response:", response)


def test_remove_tag():
    """
    Tests removing a tag from a task.
    """
    status, response = post_json("/remove-tag", {
        "task_id": "1",
        "tag": "School"
    })

    print("\nTest: remove tag")
    print("Status:", status)
    print("Response:", response)


def test_filter_single_tag():
    """
    Tests filtering tasks by one tag.
    """
    status, response = post_json("/filter-by-tags", {
        "tags": ["school"],
        "tasks": [
            {"task_id": "1", "title": "Task A", "tags": ["school", "urgent"]},
            {"task_id": "2", "title": "Task B", "tags": ["home"]},
            {"task_id": "3", "title": "Task C", "tags": ["school"]}
        ]
    })

    print("\nTest: filter single tag")
    print("Status:", status)
    print("Response:", response)


def test_filter_multiple_tags():
    """
    Tests filtering tasks by multiple tags.
    """
    status, response = post_json("/filter-by-tags", {
        "tags": ["school", "urgent"],
        "tasks": [
            {"task_id": "1", "title": "Task A", "tags": ["school", "urgent"]},
            {"task_id": "2", "title": "Task B", "tags": ["urgent"]},
            {"task_id": "3", "title": "Task C", "tags": ["school"]}
        ]
    })

    print("\nTest: filter multiple tags")
    print("Status:", status)
    print("Response:", response)


#   -------------------------
#   Run tests
#   -------------------------

if __name__ == "__main__":
    test_add_tag()
    test_remove_tag()
    test_filter_single_tag()
    test_filter_multiple_tags()