DROP TABLE IF EXISTS burnout_entries;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE burnout_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL DEFAULT CURRENT_DATE,
    sleep_hours NUMERIC(4,2) NOT NULL CHECK (sleep_hours >= 0 AND sleep_hours <= 24),
    study_hours NUMERIC(4,2) NOT NULL CHECK (study_hours >= 0 AND study_hours <= 24),
    stress_level INTEGER NOT NULL CHECK (stress_level BETWEEN 1 AND 10),
    mood_level INTEGER NOT NULL CHECK (mood_level BETWEEN 1 AND 10),
    breaks_count INTEGER NOT NULL DEFAULT 0 CHECK (breaks_count >= 0),
    notes TEXT,
    burnout_score INTEGER NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    productivity_score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
