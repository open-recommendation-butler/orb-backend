# How to add documents to the database?

After setting up the ORB docker, your database does not include any documents. Documents can be articles, podcasts, messages, newsletters etc.

In this tutorial you will learn how to add documents to the database.

## The endpoint

ORB provides an endpoint to add documents.

You can add articles by doing a POST request:

```bash
POST http://localhost:8000/articles/
```

You can send the following data to the endpoint (as a JSON):
```json
{
  "title": "That's a title",
  "teaser": "That's a teaser",
  "fullext": "That's a fulltext",
  "url": "https://example.com/",
  "content_type": "article",
}
```