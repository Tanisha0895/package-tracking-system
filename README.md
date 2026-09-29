\# Event-Driven Package Tracking System (P50)



\## Architecture

\- API Gateway → SQS → Lambda (PackageEventProcessor) → DynamoDB (event processing)

\- API Gateway → Lambda (PackageQueryHandler) → DynamoDB (queries)

\- Dead Letter Queue for failed event handling

\- Cognito for authentication (JWT-based)



\## Endpoints

\- POST /events — submit a package event (async via SQS)

\- GET /packages/{packageId}/status — get current status

\- GET /packages/{packageId}/history — get full event history

\- GET /packages — list all packages

\- DELETE /packages/{packageId} — delete a package



\## Core Logic

\- Duplicate events (same eventId) are detected and dropped

\- Stale events (older timestamp than current stored status) are dropped

\- All events are logged to history table regardless of processing outcome



\## Authentication

\- All endpoints protected via Cognito User Pool JWT authorizer



