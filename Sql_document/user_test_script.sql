/* use with 23ai_testuser1_connect -> FREEPDB1 as service name */
show con_name;
show user;

-- load in onnx model
begin
  dbms_vector.drop_onnx_model (
    model_name => 'ALL_MINILM_L12_V2',
    force => true);

  dbms_vector.load_onnx_model (
    directory  => 'model_dir',
    file_name  => 'all_MiniLM_L12_v2.onnx',
    model_name => 'ALL_MINILM_L12_V2');
end;

-- model detail -> minilm
column model_name format a30
column algorithm format a10
column mining_function format a15

select model_name, algorithm, mining_function
from   user_mining_models
where  model_name = 'ALL_MINILM_L12_V2';

-- Create text call "quick test" to embedd with model
set long 1000000
select vector_embedding(all_minilm_l12_v2 using 'Quick test' as data) AS my_vector;