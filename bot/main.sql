CREATE TABLE IF NOT EXISTS guild_data (
    guild_id BIGINT NOT NULL PRIMARY KEY,
    prefix VARCHAR(5) NOT NULL,
    prefix_case_insensitive BOOLEAN NOT NULL DEFAULT true    
);

CREATE TABLE IF NOT EXISTS guild_disabled (
    guild_id BIGINT NOT NULL PRIMARY KEY,
    command_name VARCHAR(30)[],
    channel_id BIGINT[]
);

CREATE TABLE IF NOT EXISTS apertures_currency (
    user_id BIGINT NOT NULL PRIMARY KEY,
    balance INTEGER DEFAULT 0
);