-- Add result column to scan_jobs table to store analysis summary (score, grade, etc.)
ALTER TABLE scan_jobs ADD COLUMN IF NOT EXISTS result JSONB;
