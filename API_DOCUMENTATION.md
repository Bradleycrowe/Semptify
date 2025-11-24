# Semptify API Documentation v1.0

Base URL: http://localhost:5000 (dev) | https://semptify-prod.onrender.com (prod)

## Context API

GET /api/context/{user_id} - Full context (user, docs, timeline, case)
GET /api/context/{user_id}/documents - All documents
GET /api/context/{user_id}/next-steps - Smart suggestions
GET /api/context/{user_id}/search?q=query - Search context
GET /api/context/{user_id}/document/{doc_id}/perspectives - 4-angle analysis

## Complaint Context API

GET /api/complaint/{user_id}/auto-fill - Pre-filled form data (60% confidence)
GET /api/complaint/{user_id}/evidence?limit=10 - Ranked evidence
GET /api/complaint/{user_id}/packet - Complete court packet

## Examples

Context API:
curl http://localhost:5000/api/context/1

Auto-fill complaint:
curl http://localhost:5000/api/complaint/1/auto-fill

Perspective analysis:
curl http://localhost:5000/api/context/1/document/lease_agreement.pdf/perspectives

Evidence ranking:
curl 'http://localhost:5000/api/complaint/1/evidence?limit=5'

## Response Format

Success (200):
{
  \"success\": true,
  \"data\": {...}
}

Error (4xx/5xx):
{
  \"error\": \"Error message\"
}

## Authentication

User Token: ?user_token=123456789012 OR X-User-Token header
Admin Token: ?admin_token=xxx OR X-Admin-Token header

## Features

- Context Data System (unified intelligence)
- Document Intelligence (auto-extraction)
- Perspective Reasoning (4-angle analysis)
- Complaint Auto-Fill (60% confidence)
- Evidence Ranking (0-100% relevance)
- Court Packet Generation

See BUILD_LOGBOOK.md for complete system documentation.