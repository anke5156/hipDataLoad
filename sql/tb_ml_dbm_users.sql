insert into table sgk.t_ml_sgk_small_merge_52fangdichan (uuid,sfzh,user_name,email,phoneno,password,explode_time,confidence,source_table,source) select uuid,null,null,null,null,password,explode_time,'0.2','tb_ml_dbm_users','52fangdichan' from sgk_source.tb_ml_dbm_users where 1=1 ;

-- insert into table sgk.t_ml_sgk_relation select uuid,sfzh,phoneno,'01','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(sfzh)) in (15,18) and length(trim(phoneno))=11 and substr(trim(phoneno),1,1)=1 ;

-- insert into table sgk.t_ml_sgk_relation select uuid,sfzh,email,'02','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(sfzh)) in (15,18) and upper(trim(email)) like '%.COM%' ;

-- insert into table sgk.t_ml_sgk_relation select uuid,sfzh,user_name,'03','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(sfzh)) in (15,18) and user_name!=email and upper(trim(user_name))!='NULL' and trim(user_name)!='' and user_name is not null ;

-- insert into table sgk.t_ml_sgk_relation select uuid,sfzh,password,'04','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(sfzh)) in (15,18) and upper(trim(password))!='NULL' and trim(password)!='' and password is not null ;

-- insert into table sgk.t_ml_sgk_relation select uuid,phoneno,user_name,'05','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(phoneno))=11 and substr(trim(phoneno),1,1)=1 and user_name!=email and upper(trim(user_name))!='NULL' and trim(user_name)!='' and user_name is not null ;

-- insert into table sgk.t_ml_sgk_relation select uuid,phoneno,email,'06','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(phoneno))=11 and substr(trim(phoneno),1,1)=1 and upper(trim(email)) like '%.COM%' ;

-- insert into table sgk.t_ml_sgk_relation select uuid,phoneno,password,'07','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and length(trim(phoneno))=11 and substr(trim(phoneno),1,1)=1 and upper(trim(password))!='NULL' and trim(password)!='' and password is not null ;

-- insert into table sgk.t_ml_sgk_relation select uuid,email,user_name,'08','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and upper(trim(email)) like '%.COM%' and user_name!=email and upper(trim(user_name))!='NULL' and trim(user_name)!='' and user_name is not null ;

-- insert into table sgk.t_ml_sgk_relation select uuid,email,password,'09','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and upper(trim(email)) like '%.COM%' and upper(trim(password))!='NULL' and trim(password)!='' and password is not null ;

-- insert into table sgk.t_ml_sgk_relation select uuid,user_name,password,'10','tb_ml_dbm_users',confidence from sgk.t_ml_sgk_small_merge_52fangdichan where 1=1 and user_name!=email and upper(trim(user_name))!='NULL' and trim(user_name)!='' and user_name is not null and upper(trim(password))!='NULL' and trim(password)!='' and password is not null ;
