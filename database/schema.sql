DROP TABLE IF EXISTS movie CASCADE;

CREATE table public.movie(
tmdb_id VARCHAR(8) PRIMARY KEY,
movie_title   VARCHAR(107), 
production_companies VARCHAR(103),
overview TEXT,
revenue BIGINT CHECK (revenue >= 0), 
budget BIGINT CHECK (budget >= 0),
popularity DOUBLE PRECISION CHECK (popularity >= 0), 
release_date DATE
);


======

DROP TABLE IF EXISTS movie_genre;

CREATE TABLE movie_genre (
    tmdb_id  VARCHAR(20) NOT NULL,
    genre_id VARCHAR(20) NOT NULL,

    PRIMARY KEY (tmdb_id, genre_id),

    FOREIGN KEY (tmdb_id)
        REFERENCES movie(tmdb_id),

    FOREIGN KEY (genre_id)
        REFERENCES genre(genre_id)
);

DROP TABLE IF EXISTS cast_table CASCADE;

CREATE TABLE cast_table (

    actor_id VARCHAR(10) PRIMARY KEY, 
    crew_name    VARCHAR(45),
    gender  VARCHAR(7)
);

CREATE INDEX indx_cast_name ON cast_table(crew_name);


------
CREATE TABLE public.genre(
genre_id VARCHAR(8) PRIMARY KEY,
genre_name VARCHAR(16)
)
