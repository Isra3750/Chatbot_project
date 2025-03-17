// use with 23ai_connect
// Follow this -> https://oracle-base.com/articles/23/ai-vector-search-23
show con_name
show pdbs
show user
// Note -> docker have to map download file (onnx model) in windows to /u01/models
alter session set container = FREEPDB1; // switch to pdb

create user if not exists testuser1 identified by testuser1 quota unlimited on users;
grant create session, db_developer_role, create mining model to testuser1;
commit; // don't forget to commit after creating user

SELECT username FROM dba_users; // check all user

// access model dir
create or replace directory model_dir as '/u01/models';
grant read, write on directory model_dir to testuser1;
SELECT directory_name, directory_path FROM dba_directories WHERE directory_name = 'MODEL_DIR';

/*
Docker has to map directory from windows to docker container (linux like example above), change window path as required:

docker run --name 23cfree -p 1521:1521 -e ORACLE_PWD=pass1234 -e ORACLE_CHARACTERSET=AL32UTF8 
-e ENABLE_ARCHIVELOG=true -e ENABLE_FORCE_LOGGING=true  -v 
"C:\Users\Isra\Downloads\all_MiniLM_L12_v2_augmented":/u01/models 
-d container-registry.oracle.com/database/free:latest

docker exec -it 23cfree ls /u01/models
*/