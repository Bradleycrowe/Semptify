-- Add verification and storage columns to users table
ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN verified_at TEXT;
ALTER TABLE users ADD COLUMN storage_allowed INTEGER DEFAULT 1;
