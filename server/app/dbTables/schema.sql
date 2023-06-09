DROP TABLE IF EXISTS reference;
DROP TABLE IF EXISTS audio;

CREATE TABLE reference (
    ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
    section VARCHAR(45) NOT NULL,
    prompt TEXT NOT NULL,
    promptNum INTEGER(11) UNIQUE DEFAULT NULL,
    image_url VARCHAR(45) DEFAULT NULL
);


CREATE TABLE audio (
    audio_id INTEGER(11) PRIMARY KEY NOT NULL,
    session_id VARCHAR(128) NOT NULL,
    s3_url VARCHAR(45) NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    validated INTEGER(1) DEFAULT NULL,
    ref_id INTEGER(11) NOT NULL,
    sequence_matcher REAL NOT NULL,
    cer REAL NOT NULL,
    metaphone_match REAL NOT NULL
);