select usertype,count(usertype)
  from divvy
  where start_time >= '2019-09-01 00:00:00'
    and start_time < '2019-09-02 00:00:00'
  group by usertype;

select usertype,sum(tripduration) 
  from divvy
  group by usertype;


 select usertype,count(start_station_id)
  from divvy
  where start_time >= '2019-09-01 00:00:00'
  group by usertype; 

  
 select usertype,sum(tripduration) 
  from divvy
  where start_time >= '2019-09-01 00:00:00'
  group by usertype; 
  
  
  select usertype,count(usertype),date(start_time) as day,
      avg(tripduration)
    from divvy
    where start_time >= '2019-09-01 00:00:00'
    group by day,usertype;
    
select usertype,count(usertype) as rides,quarter,avg(tripduration)
    from divvy
    where start_time >= '2019-09-01 00:00:00'      
    group by quarter,usertype;
