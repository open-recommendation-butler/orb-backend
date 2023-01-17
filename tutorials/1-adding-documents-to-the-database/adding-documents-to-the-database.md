# How to add documents to the database?

After setting up the ORB docker, your database does not include any documents. Documents can be articles, podcasts, messages, newsletters etc.

In this tutorial you will learn how to add documents to the database.

## The API endpoint

ORB provides an API endpoint to add documents.

You can add articles by doing a POST request:

```bash
POST http://localhost:8000/article/
```

You can send the following data to the endpoint (as a JSON):
```json
{
  "title": "That's a title",
  "teaser": "That's a teaser",
  "fullext": "That's a fulltext",
  "url": "https://example.com/",
  "content_type": "article",
  "created": "2012-04-23T18:25:43.511Z"
}
```
None of the fields is mandatory.

If successful, the API sends the status *201 Created*.

## Examples

In this section you will find examples how to add send requests to the API.

### a) Adding a document with Postman

You can add a document with [Postman](https://www.postman.com/). Postman is a program to test APIs.

Create a POST request, include the body as a JSON and send the document to the API as seen in the picture.

![Screenshot of a POST request in Postman](../1-adding-documents-to-the-database/add-document-w-postman.png "Add document with Postman")

### b) Adding a document with Python

You can automate adding documents with the [Python Request Library](https://requests.readthedocs.io/en/latest/).

Install the library.

```bash
pip install requests
```

Run the following code to add a document:
```python
import requests

document = {
  "title": "That's a title",
  "teaser": "That's a teaser",
  "fullext": "That's a fulltext",
  "url": "https://example.com/",
  "content_type": "article",
  "created": "2012-04-23T18:25:43.511Z"
}

r = requests.post('http://localhost:8000/article/', json=document)

print(r.status_code)
```