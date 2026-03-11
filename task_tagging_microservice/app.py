from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "task_tags.json"))


#   -------------------------
#   File load/save
#   -------------------------

def load_data():
    """
    Loads saved tag data from a JSON file.
    If the file does not exist or is invalid, returns empty data.
    """
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        for task_id in data:
            if not isinstance(data[task_id], list):
                data[task_id] = []

        return data
    except (OSError, json.JSONDecodeError):
        return {}


def save_data(data):
    """
    Saves the current tag data to a JSON file.
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


#   -------------------------
#   General helper functions
#   -------------------------

def is_blank(text):
    """
    Checks whether the given text is blank.
    """
    return str(text).strip() == ""


def clean_text(text):
    """
    Cleans extra whitespace from text.
    """
    return " ".join(str(text).split()).strip()


def normalize_tag(tag_text):
    """
    Cleans a tag and converts it to lowercase.
    """
    return clean_text(tag_text).lower()


#   -------------------------
#   Tag logic
#   -------------------------

def add_tag_to_task(data, task_id, tag_name):
    """
    Adds a tag to a task if it is not already there.
    """
    if task_id not in data:
        data[task_id] = []

    if tag_name not in data[task_id]:
        data[task_id].append(tag_name)
        save_data(data)


def remove_tag_from_task(data, task_id, tag_name):
    """
    Removes a tag from a task if it exists.
    """
    if task_id not in data:
        return

    if tag_name in data[task_id]:
        data[task_id].remove(tag_name)
        save_data(data)


def get_tags_for_task(data, task_id):
    """
    Returns all tags saved for a task.
    """
    if task_id not in data:
        return []

    return data[task_id]


def filter_tasks_by_tags(task_list, required_tags):
    """
    Returns tasks that contain all required tags.
    """
    results = []

    for task in task_list:
        if "tags" not in task:
            continue

        task_tags = []
        for tag in task["tags"]:
            task_tags.append(normalize_tag(tag))

        matches = True

        for required_tag in required_tags:
            if required_tag not in task_tags:
                matches = False

        if matches:
            results.append(task)

    return results


#   -------------------------
#   Routes
#   -------------------------

@app.route("/")
def home():
    """
    Confirms the microservice is running.
    """
    return jsonify({"message": "Task Tagging Microservice running."})


@app.route("/add-tag", methods=["POST"])
def add_tag():
    """
    Adds a tag to a task.
    """
    data = load_data()
    body = request.get_json()

    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    task_id = str(body.get("task_id", "")).strip()
    tag_name = normalize_tag(body.get("tag", ""))

    if is_blank(task_id):
        return jsonify({"error": "task_id is required."}), 400

    if is_blank(tag_name):
        return jsonify({"error": "tag is required."}), 400

    add_tag_to_task(data, task_id, tag_name)

    return jsonify({
        "status": "success",
        "task_id": task_id,
        "tags": get_tags_for_task(data, task_id)
    }), 200


@app.route("/remove-tag", methods=["POST"])
def remove_tag():
    """
    Removes a tag from a task.
    """
    data = load_data()
    body = request.get_json()

    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    task_id = str(body.get("task_id", "")).strip()
    tag_name = normalize_tag(body.get("tag", ""))

    if is_blank(task_id):
        return jsonify({"error": "task_id is required."}), 400

    if is_blank(tag_name):
        return jsonify({"error": "tag is required."}), 400

    remove_tag_from_task(data, task_id, tag_name)

    return jsonify({
        "status": "success",
        "task_id": task_id,
        "tags": get_tags_for_task(data, task_id)
    }), 200


@app.route("/filter-by-tags", methods=["POST"])
def filter_by_tags():
    """
    Returns tasks that match all given tags.
    """
    body = request.get_json()

    if body is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    tasks = body.get("tasks", [])
    tags = body.get("tags", [])

    if not isinstance(tasks, list):
        return jsonify({"error": "tasks must be a list."}), 400

    if not isinstance(tags, list):
        return jsonify({"error": "tags must be a list."}), 400

    cleaned_tags = []
    for tag in tags:
        cleaned_tags.append(normalize_tag(tag))

    matching_tasks = filter_tasks_by_tags(tasks, cleaned_tags)

    return jsonify({
        "status": "success",
        "tasks": matching_tasks
    }), 200


#   -------------------------
#   Run microservice
#   -------------------------

if __name__ == "__main__":
    print("Starting Task Tagging Microservice...")
    app.run(port=5002)