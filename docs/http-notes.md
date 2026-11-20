# HTTP notes

- A request has a method, path, headers, and sometimes a body. A response has a status line, headers, and a body.
- GET retrieves data and should not change anything. POST creates something, and a success returns 201.
- Status codes: 2xx success, 4xx client error, 5xx server error. 422 is invalid data, 411 means Length Required.
- Content-Length is the body size in bytes. Without it, the server can't know where a POST body ends.
- Our server returned 411 when Content-Length was missing. Before the fix, int(None) raised TypeError and the client got no response.
- Our server answers HTTP/1.0. curl sends HTTP/1.1 requests.
- Idempotency: repeating the operation gives the same result. Idempotency-Key lets the server spot a retry.
- HTTP/2 needs a server other than the standard library's, such as Hypercorn. uvicorn serves HTTP/1.1.