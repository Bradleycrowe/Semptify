# Semptify Delivery Module — Quick Start

## Files generated
- ./api/specs/semptify-delivery-openapi.yaml
- ./scripts/Semptify-Delivery.ps1
- ./types/semptify-delivery.d.ts
- ./docs/README_DELIVERY.md

## Configure
1. Edit ./scripts/Semptify-Delivery.ps1 and set ApiBase and ApiKey to your environment, or modify script to read secrets from a secure store.
2. Import the OpenAPI YAML into your gateway, tooling, or generate server stubs.
3. Commit generated files to your repo.

## Example curl commands
Create delivery job:
curl -X POST "https://api.semptify.example/api/deliveries" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "caseId":"CASE_123",
  "createdBy":"user_7",
  "createdAt":"2025-10-27T06:04:00Z",
  "methods":[
    {
      "id":"m1",
      "type":"EMAIL",
      "recipientName":"Tenant Example",
      "recipientContact":{"email":"tenant@example.com"},
      "instructions":"Attach complaint PDF",
      "status":"PENDING",
      "requiredFields":["recipientContact.email"]
    },
    {
      "id":"m2",
      "type":"USPS",
      "recipientName":"Owner Example",
      "recipientContact":{"address":"123 Main St, City, ST, 00000"},
      "instructions":"First class, keep tracking",
      "status":"PENDING",
      "requiredFields":["recipientContact.address"]
    }
  ],
  "priorityOrder":["m1","m2"],
  "status":"CREATED"
}
JSON

Upload proof file:
curl -X POST "https://api.semptify.example/api/files" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@/path/to/complaint.pdf;type=application/pdf"

Add delivery attempt:
curl -X POST "https://api.semptify.example/api/deliveries/DELIVERY_ID/methods/m1/attempt" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "actor":"user_7",
    "attemptAt":"2025-10-27T08:00:00Z",
    "providerResponse":"SMTP 250 OK",
    "trackingNumber":"",
    "proofFileIds":["FILE_ID_123"]
  }'

Confirm delivery:
curl -X POST "https://api.semptify.example/api/deliveries/DELIVERY_ID/methods/m1/confirm" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "actor":"user_7",
    "confirmedAt":"2025-10-27T08:05:00Z",
    "proofFileIds":["FILE_ID_123"]
  }'

## Integration notes
- Server must enforce method.requiredFields before accepting attempts.
- History entries must be append-only for auditability.
- Publish events: DELIVERY_CREATED, DELIVERY_ATTEMPTED, DELIVERY_CONFIRMED, DELIVERY_FAILED.
- File upload API must return stable fileId for attachments.
- Use secure secret storage and rotate tokens regularly.
- Test by importing OpenAPI into Swagger UI or Postman and running contract tests.

