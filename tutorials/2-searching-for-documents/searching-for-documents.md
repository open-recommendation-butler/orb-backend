# How to search for documents with the API

You can use the web demo to search for documents ([http://localhost:8000](http://localhost:8000)) or you can use the API.

In the following, you will learn how to search with the API.

You can retrieve search results by sending a GET request:

```bash
GET http://localhost:8000/search/
```

You can use the following parameters:

| Parameter     | What it is        |
| ------------- |:-------------:|
| q      | Search term to query (string) |
| as_topics     | If results should be clustered in topics (boolean)      |
| return_json | If response should be JSON instead of HTML (boolean)      |

An example search would look like:
```
GET http://localhost:8000/search/?as_topics=True&q=der&return_json=True
```
