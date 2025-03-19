/* use with 23ai_testuser1_connect
 This for similarity search ie. vector search */
show con_name;
show user;

-- quick check
--select * from movie_quotes;

-- Vector search
variable search_text varchar2(100);
exec :search_text := 'Do, or do not. There is no try.';

set linesize 200
column movie format a50
column movie_quote format a100

SELECT vector_distance(movie_quote_vector, (vector_embedding(all_minilm_l12_v2 using :search_text as data))) as distance,
       movie,
       movie_quote,
       movie_year
FROM   movie_quotes
order by 1
fetch approximate first 3 rows only; -- five closest distance only