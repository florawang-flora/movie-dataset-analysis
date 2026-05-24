DROP TABLE IF EXISTS movie CASCADE;

CREATE TABLE movie (
    tmdb_id             VARCHAR(7)    PRIMARY KEY,
    title               VARCHAR(106)  NOT NULL,
    production_company  VARCHAR(102)  NOT NULL,
    budget              INTEGER       NOT NULL  CHECK (budget  >= 0),
    revenue             INTEGER       NOT NULL  CHECK (revenue >= 0),
    runtime             INTEGER       NOT NULL  CHECK (runtime >= 0),
    release_date        TIMESTAMP     NOT NULL
);

CREATE INDEX idx_movie_release_date ON movie(release_date);
CREATE INDEX idx_movie_title        ON movie(title); 
======

DROP TABLE IF EXISTS cast_table CASCADE;

CREATE TABLE cast_table (

    actor_id VARCHAR(10) PRIMARY KEY, 
    crew_name    VARCHAR(45),
    gender  VARCHAR(7)
);

CREATE INDEX indx_cast_name ON cast_table(crew_name);
