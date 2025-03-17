// use with 23ai_testuser1_connect
// This for table creation
show con_name;
show user;

drop table if exists movie_quotes purge;

create table movie_quotes as
select movie_quote, movie, movie_type, movie_year
from   external (
         (
           movie_quote  varchar2(400),
           movie        varchar2(200),
           movie_type   varchar2(50),
           movie_year   number(4)
         )
         type oracle_loader
         default directory model_dir
         access parameters (
           records delimited by newline
           skip 1
           badfile model_dir
           logfile model_dir:'moview_quotes_ext_tab_%a_%p.log'
           discardfile model_dir
           fields csv with embedded terminated by ',' optionally enclosed by '"'
           missing field values are null
           (
             movie_quote char(400),
             movie,
             movie_type,
             movie_year
           )
        )
        location ('movie_quotes.csv')
        reject limit unlimited
      );

// add new col for vector store
alter table movie_quotes add (
  movie_quote_vector vector
);

// Generate vector from movie quote
update movie_quotes
set    movie_quote_vector = vector_embedding(all_minilm_l12_v2 using movie_quote as data);
commit;
// quick check
select * from movie_quotes;
