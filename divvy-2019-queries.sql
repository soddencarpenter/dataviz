select usertype,count(usertype)
  from divvy_2019
  where start_time >= '2019-09-01 00:00:00'
    and start_time < '2019-09-02 00:00:00'
  group by usertype;

select usertype,sum(tripduration) 
  from divvy_2019
  group by usertype;


 select usertype,count(from_station_id)
  from divvy_2019
  where start_time >= '2019-09-01 00:00:00'
  group by usertype; 

  
 select usertype,sum(tripduration) 
  from divvy_2019
  where start_time >= '2019-09-01 00:00:00'
  group by usertype; 
