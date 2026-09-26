-- BoardingEdu PostgreSQL schema (reference)
-- Aligned with SQLAlchemy models in backend/models/ (Phase 2).
-- Prefer: python seed.py (creates tables via SQLAlchemy) OR apply this file manually.

-- users
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(120) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    phone           VARCHAR(20),
    password_hash   VARCHAR(255) NOT NULL,
    role            VARCHAR(20) NOT NULL CHECK (role IN ('parent', 'student', 'admin')),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- schools
CREATE TABLE IF NOT EXISTS schools (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(200) NOT NULL,
    description         TEXT,
    address             VARCHAR(500),
    city                VARCHAR(100) NOT NULL,
    state               VARCHAR(100),
    board               VARCHAR(50),
    school_type         VARCHAR(50),
    gender              VARCHAR(30),
    min_fee             INTEGER,
    max_fee             INTEGER,
    hostel_available    BOOLEAN DEFAULT FALSE,
    rating              DOUBLE PRECISION DEFAULT 4.0,
    phone               VARCHAR(20),
    email               VARCHAR(255),
    website             VARCHAR(255),
    admission_process   TEXT,
    academic_info       TEXT,
    sports_info         TEXT,
    transport_info      TEXT,
    hostel_info         TEXT,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- school_fees
CREATE TABLE IF NOT EXISTS school_fees (
    id              SERIAL PRIMARY KEY,
    school_id       INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    class_name      VARCHAR(50) NOT NULL,
    admission_fee   INTEGER DEFAULT 0,
    tuition_fee     INTEGER DEFAULT 0,
    hostel_fee      INTEGER DEFAULT 0,
    transport_fee   INTEGER DEFAULT 0,
    other_fee       INTEGER DEFAULT 0,
    annual_fee      INTEGER DEFAULT 0
);

-- facilities
CREATE TABLE IF NOT EXISTS facilities (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    description     TEXT
);

-- school_facilities (many-to-many)
CREATE TABLE IF NOT EXISTS school_facilities (
    id              SERIAL PRIMARY KEY,
    school_id       INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    facility_id     INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    CONSTRAINT uq_school_facility UNIQUE (school_id, facility_id)
);

-- infrastructure
CREATE TABLE IF NOT EXISTS infrastructure (
    id              SERIAL PRIMARY KEY,
    school_id       INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    category        VARCHAR(100) NOT NULL,
    description     TEXT
);

-- school_images
CREATE TABLE IF NOT EXISTS school_images (
    id              SERIAL PRIMARY KEY,
    school_id       INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    image_url       VARCHAR(500) NOT NULL,
    caption         VARCHAR(255)
);

-- shortlists (prevent duplicate user+school)
CREATE TABLE IF NOT EXISTS shortlists (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    school_id       INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_school_shortlist UNIQUE (user_id, school_id)
);

-- admission_enquiries
CREATE TABLE IF NOT EXISTS admission_enquiries (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    school_id       INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    student_name    VARCHAR(120) NOT NULL,
    parent_name     VARCHAR(120) NOT NULL,
    class_name      VARCHAR(50),
    academic_year   VARCHAR(20),
    phone           VARCHAR(20),
    email           VARCHAR(255),
    message         TEXT,
    status          VARCHAR(30) NOT NULL DEFAULT 'Pending'
                    CHECK (status IN ('Pending', 'Contacted', 'In Review', 'Closed')),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Helpful indexes for search/filter
CREATE INDEX IF NOT EXISTS idx_schools_city ON schools(city);
CREATE INDEX IF NOT EXISTS idx_schools_board ON schools(board);
CREATE INDEX IF NOT EXISTS idx_schools_name ON schools(name);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_enquiries_status ON admission_enquiries(status);
