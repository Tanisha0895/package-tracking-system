\# Controlled Failure Scenario Demo



\## Scenario

Simulated a malformed event (missing required 'status' field) to demonstrate

failure handling and recovery without blocking the overall system.



\## Steps

1\. Sent malformed event to SQS main queue:

&#x20;  {"packageId": "PKG-FAIL-TEST", "eventId": "evt-fail-001", "eventTimestamp": 1000}

&#x20;  (missing 'status' field)



2\. Lambda threw KeyError: 'status' on each attempt. SQS retried per the

&#x20;  redrive policy (maxReceiveCount: 3), then moved the message to the

&#x20;  Dead Letter Queue (PackageEventDLQ).



3\. While the malformed event was stuck, a valid event for a different

&#x20;  package (PKG-RECOVERY-TEST) was sent to the main queue. It processed

&#x20;  successfully (status: SHIPPED confirmed in DynamoDB), proving that

&#x20;  one failing event does not block processing of other events.



4\. Recovery: deleted the malformed message from the DLQ, then resent a

&#x20;  corrected version with the 'status' field included. The corrected

&#x20;  event processed successfully (PKG-FAIL-TEST status: SHIPPED confirmed

&#x20;  in DynamoDB).



\## Conclusion

The system correctly isolates and quarantines failing events via DLQ

while continuing to process healthy events, and supports manual recovery

of failed events after correction.

