# CS361-Team31-Task-Tagging-Microservice

Task Tagging microservice for CS361 Team 31.  
Provides task tagging and tag filtering functionality via REST API using JSON.

---

## DESCRIPTION

This microservice allows a client to:

- Add a tag to a task.
- Remove a tag from a task.
- Retrieve tasks that contain specific tags.

Tags are normalized to lowercase to maintain consistency.

The service communicates exclusively via HTTP POST requests using JSON.

---

## INSTALLATION

Install required packages:

```bash
pip install flask
```

Run the application:

```bash
python app.py
```

The service runs on:

```
http://127.0.0.1:5002
```

---

## HOW TO REQUEST DATA

All requests must:
- Use HTTP POST
- Include header: `Content-Type: application/json`
- Include a JSON body

### POST /add-tag

Required JSON fields:
- `task_id` (string)
- `tag` (string)

Example request:

```bash
curl -X POST http://127.0.0.1:5002/add-tag \
-H "Content-Type: application/json" \
-d "{\"task_id\":\"task1\",\"tag\":\"school\"}"
```

---

### POST /remove-tag

Required JSON fields:
- `task_id` (string)
- `tag` (string)

Example request:

```bash
curl -X POST http://127.0.0.1:5002/remove-tag \
-H "Content-Type: application/json" \
-d "{\"task_id\":\"task1\",\"tag\":\"school\"}"
```

---

### POST /filter-by-tags

Required JSON fields:
- `tasks` (array of task objects containing `task_id`, `title`, and `tags`)
- `tags` (array of required tags)

Example request:

```bash
curl -X POST http://127.0.0.1:5002/filter-by-tags \
-H "Content-Type: application/json" \
-d "{\"tags\":[\"school\"],\"tasks\":[{\"task_id\":\"task1\",\"title\":\"Task A\",\"tags\":[\"school\",\"urgent\"]}]}"
```

---

## HOW TO RECEIVE DATA

All responses are returned in JSON format.

### /add-tag responses

Success (200 OK):

```json
{
  "status": "success",
  "task_id": "task1",
  "tags": ["school"]
}
```

Failure (400 Bad Request):

```json
{
  "status": "error",
  "message": "Invalid JSON"
}
```

---

### /remove-tag responses

Success (200 OK):

```json
{
  "status": "success",
  "task_id": "task1",
  "tags": []
}
```

---

### /filter-by-tags responses

Success (200 OK):

```json
{
  "status": "success",
  "tasks": []
}
```

---

## TEST PROGRAM

To test using the provided test client:

1. Run the microservice:

```bash
python app.py
```

2. In a separate terminal, run:

```bash
python test_task_tagging.py
```

The test program sends POST requests to `/add-tag`, `/remove-tag`, and `/filter-by-tags` and prints the JSON responses returned by the microservice.