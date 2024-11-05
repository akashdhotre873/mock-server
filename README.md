# Mock Server

Mock server enables mocking of HTTP calls.

## Set up

### environment file at main/.env

- Refer [.env.example](main/.env.example) for example

```python
SECRET_KEY=secret_key
database_connection_string=database_url
DEBUG=True/False
```

### Start the server

By default server runs on port 8000.

### Set up routes to mock

Create route API

```curl
curl --location --request POST 'http://localhost:8000/routes' \
--header 'Content-Type: application/json' \
--data '{
    "url": "todos",
    "method": "GET",
    "response": [
        {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        },
        {
            "userId": 2,
            "id": 2,
            "title": "quis ut nam facilis et officia qui",
            "completed": true
        }
    ],
    "status": 200
}'
```

| Property   | Type      | Description                        | Required | Default  |
| ---------- | --------- | ---------------------------------- | -------- | -------- |
| `url`      | `String`  | url of the mock API                | Yes      | -        |
| `method`   | `string`  | method of the mock API             | Yes      | -        |
| `response` | `object`  | response of the mock API           | Yes      | -        |
| `status`   | `integer` | return status code of the mock API | No       | `200 OK` |
|            |           |                                    |          |          |

Once url is set up, hit the GET /todos API.

```curl
curl --location 'http://localhost:8000/todos'
```

![Alt text](/readme/todos_get.png 'Sample output')
