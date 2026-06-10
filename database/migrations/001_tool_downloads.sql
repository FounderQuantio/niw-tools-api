-- NIW Tools API — Initial Migration
-- Run once against your Neon database before first deploy

CREATE TABLE IF NOT EXISTS tool_downloads (
    id            UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_id       VARCHAR(100) NOT NULL,
    downloaded_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    ip_address    VARCHAR(45),   -- IPv4 (15) or IPv6 (45)
    user_agent    TEXT,
    CONSTRAINT chk_tool_id_nonempty CHECK (char_length(tool_id) > 0)
);

CREATE INDEX IF NOT EXISTS ix_tool_downloads_tool_id       ON tool_downloads(tool_id);
CREATE INDEX IF NOT EXISTS ix_tool_downloads_downloaded_at ON tool_downloads(downloaded_at DESC);
CREATE INDEX IF NOT EXISTS ix_tool_downloads_ip            ON tool_downloads(ip_address);
