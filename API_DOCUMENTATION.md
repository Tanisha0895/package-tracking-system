\# API Documentation — Package Tracking System



Base URL: `https://7oonmpd91g.execute-api.us-west-1.amazonaws.com/dev`



All endpoints require Authorization header with a valid Cognito IdToken:

`Authorization: <IdToken>`



\---



\## 1. POST /events

Submit a package tracking event (processed asynchronously via SQS).



\*\*Request:\*\*

```json

POST /events

{

&#x20; "packageId": "PKG001",

&#x20; "eventId": "evt-001",

&#x20; "status": "SHIPPED",

&#x20; "eventTimestamp": 1000

}

```



\*\*Response (200):\*\*

```json

{

&#x20; "SendMessageResponse": {

&#x20;   "SendMessageResult": {

&#x20;     "MessageId": "..."

&#x20;   }

&#x20; }

}

```



\*\*Behavior:\*\* Event is queued to SQS and processed by Lambda asynchronously.

Duplicate eventIds and stale (older timestamp) events are automatically

detected and dropped — see failure-scenario-demo.md for details.



\---



\## 2. GET /packages/{packageId}/status

Get the current status of a package.



\*\*Request:\*\* `GET /packages/PKG001/status`



\*\*Response (200):\*\*

```json

{

&#x20; "packageId": "PKG001",

&#x20; "currentStatus": "SHIPPED",

&#x20; "lastEventTimestamp": 1000,

&#x20; "lastUpdated": "2026-09-24T11:39:23.080473"

}

```



\*\*Response (404):\*\* `{"error": "Package not found"}`



\---



\## 3. GET /packages/{packageId}/history

Get the full event history of a package.



\*\*Request:\*\* `GET /packages/PKG001/history`



\*\*Response (200):\*\*

```json

{

&#x20; "packageId": "PKG001",

&#x20; "events": \[

&#x20;   {"eventId": "evt-001", "status": "SHIPPED", "eventTimestamp": 1000, "processed": true}

&#x20; ]

}

```



\---



\## 4. GET /packages

List all tracked packages.



\*\*Request:\*\* `GET /packages`



\*\*Response (200):\*\*

```json

{

&#x20; "packages": \[

&#x20;   {"packageId": "PKG001", "currentStatus": "SHIPPED", "lastEventTimestamp": 1000}

&#x20; ]

}

```



\---



\## 5. DELETE /packages/{packageId}

Delete a package's status record.



\*\*Request:\*\* `DELETE /packages/PKG001`



\*\*Response (200):\*\*

```json

{"message": "Package PKG001 deleted"}

```



\---



\## Error Responses

\- `401 Unauthorized` — missing or invalid Authorization token

\- `404 Not Found` — package does not exist (status endpoint)

\- `500 Internal Server Error` — unexpected server-side error

