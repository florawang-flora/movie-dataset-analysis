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


CREATE TABLE public.cast_table (
    actor_id VARCHAR(11) PRIMARY KEY,
    gender VARCHAR(8),
    cast_name VARCHAR(46)
);

CREATE TABLE public.cast_movie (
    character_name VARCHAR(391),
    tmdb_id VARCHAR(20) NOT NULL,
    actor_id VARCHAR(11) NOT NULL,

    PRIMARY KEY (tmdb_id, actor_id),

    FOREIGN KEY (tmdb_id)
        REFERENCES public.movie(tmdb_id),

    FOREIGN KEY (actor_id)
        REFERENCES public.cast_table(actor_id)
);
======

DROP TABLE IF EXISTS public.crew
CREATE TABLE public.crew (
    crew_id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    crew_name VARCHAR(45)
);


DROP TABLE IF EXISTS public.crew_movie
CREATE TABLE public.crew_movie (
    department VARCHAR(25),
    job VARCHAR(65),
    tmdb_id VARCHAR(20) NOT NULL,
    crew_id VARCHAR(20) NOT NULL,

    PRIMARY KEY (tmdb_id, crew_id),

    FOREIGN KEY (tmdb_id)
        REFERENCES public.movie(tmdb_id),

    FOREIGN KEY (crew_id)
        REFERENCES public.crew(crew_id)
);
=======

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



CREATE INDEX indx_cast_name ON cast_table(crew_name);


------
CREATE TABLE public.genre(
genre_id VARCHAR(8) PRIMARY KEY,
genre_name VARCHAR(16)
)
