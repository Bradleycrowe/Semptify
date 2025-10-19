# Admin Console Quick Actions

## Manage rooms

- Create, expire, or revoke rooms from the Admin Console.
- Set room type: certified, notary, or open.
- Adjust default TTL for ephemeral room tokens.

## User verification

- Approve or revoke Verified Certificates on user profiles.
- Verification changes are effective immediately and control access to Certified Rooms.

## Document controls and audit exports

- Unlock files only after a documented audit review.
- Export audit trails as CSV and a signed JSON manifest for court.
- Ensure each exported manifest includes file SHA-256, uploader id, and lock events.

## AI Orchestrator administration

- Configure allowed AI endpoints and per-AI API keys.
- Maintain an allowlist of approved AI participants.
- Set policy rules: approval_required flag, max concurrent AIs, and retention of AI outputs.
- Enable or disable auto-approval for trusted workflows.

## Audit and retention policies

- Set retention policy for recordings and locked documents.
- Optionally enable public anchoring for high-assurance evidence; track anchoring tx id in events.

## Security and troubleshooting

- Rotate keys used for signed manifests and S3 access periodically.
- Troubleshoot uploads by checking the upload queue, S3 signed URL logs, and background job health.
- Re-run SHA-256 checks if integrity flags appear and record re-check events in the audit log.

## Quick admin checklist before court export

- Confirm all files in the Rights-Ready Packet are hashed and locked.
- Export audit trail with signed JSON manifest and CSV.
- Verify Verified Certificates for counsel and notary participants.
- Confirm AI outputs (if used) were approved and manifest includes model, job id, and timestamp.
