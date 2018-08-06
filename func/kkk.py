
# coding: utf-8

# # 1.连接hive

# In[1]:


from tdPyLib import HiveClient as HiveClient
a=HiveClient('nn1','admin','sQFx9210hb','dw')

from tdPyLib.sklearn import SampleDeal
# # 2.hive取数

# In[2]:


import datetime
import time 
import pandas as pd 
import numpy as np 

today=datetime.date.today()
yesterday=today+datetime.timedelta(days=-1)
tomorrow=today+datetime.timedelta(days=1)


# In[3]:


query_sql1="""
select a1.date
	  ,cast(a1.month_of_year as string) as month_of_year
	  ,cast(a1.week_of_month  as string) as week_of_month
	  ,a1.newyearday,
      a1.womenday,
      a1.laborday,
      a1.youthday,
      a1.childrenday,
      a1.partyday,
      a1.armyday,
        a1.teacherday,
        a1.nationalday,
        a1.eveday,
        a1.spring,
        a1.lantern,
        a1.qingming,
        a1.dragonboat,
        a1.valentineday,
        a1.autumnday,
        a1.doubleninth,
        a1.valentineday2,
        a1.foolsday,
        a1.motherday,
        a1.fatherday,
        a1.thanksgiving,
        a1.silentnight,
        a1.xmas,
        a1.halloween,
        a1.halloween2,
        a1.easter,
        a1.isworkday,
        a1.holidaytype,
        a1.holidayseq,
        a1.holidayinflu,
        a1.holidayinfluseq,
        a1.accident,
        a1.accidenttype,
        a1.day,
        a1.night,
        a1.seq,a2.lowest_temp
	  ,a2.highest_temp
	  ,a2.weather_init
	  ,a2.weather_final
	  ,a2.wind_direct
	  ,a2.wind_force
	  ,a3.store_code
	  ,a3.store_name
	  ,a3.city
	  ,a3.supervisor_name
	  ,a3.store_age
	  ,a3.area
	  ,a3.business_district_level1_name
   
	  ,a3.store_type
	  ,a3.partner_name
	  ,a3.manager
	  ,cast(a3.purchasing_code as string)
	  ,a4.sales_amt  
	  ,datediff(a1.date,a3.first_open_date)  store_days
      ,a5.weight_index_store
      ,a6.00_temp
      ,a6.01_temp
      ,a6.02_temp
      ,a6.03_temp 
      ,a6.04_temp
      ,a6.05_temp
      ,a6.06_temp
      ,a6.07_temp
      ,a6.08_temp
      ,a6.09_temp 
      ,a6.10_temp
      ,a6.11_temp
       ,a6.12_temp
      ,a6.13_temp
       ,a6.14_temp
      ,a6.15_temp
       ,a6.16_temp
      ,a6.17_temp
       ,a6.18_temp
      ,a6.19_temp
      ,a6.20_temp
      ,a6.21_temp
      ,a6.22_temp
      ,a6.23_temp
      ,a6.00_wstatus
      ,a6.01_wstatus
      ,a6.02_wstatus
      ,a6.03_wstatus 
      ,a6.04_wstatus
      ,a6.05_wstatus
      ,a6.06_wstatus
      ,a6.07_wstatus
      ,a6.08_wstatus
      ,a6.09_wstatus 
      ,a6.10_wstatus
      ,a6.11_wstatus
       ,a6.12_wstatus
      ,a6.13_wstatus
       ,a6.14_wstatus
      ,a6.15_wstatus
       ,a6.16_wstatus
      ,a6.17_wstatus
       ,a6.18_wstatus
      ,a6.19_wstatus
      ,a6.20_wstatus
      ,a6.21_wstatus
      ,a6.22_wstatus
      ,a6.23_wstatus

from 
(select p1.date_id as date
	  ,p1.month_of_year
	  ,p1.week_of_month
	  ,p2.newyearday,
      p2.womenday,
      p2.laborday,
      p2.youthday,
      p2.childrenday,
      p2.partyday,
      p2.armyday,
        p2.teacherday,
        p2.nationalday,
        p2.eveday,
        p2.spring,
        p2.lantern,
        p2.qingming,
        p2.dragonboat,
        p2.valentineday,
        p2.autumnday,
        p2.doubleninth,
        p2.valentineday2,
        p2.foolsday,
        p2.motherday,
        p2.fatherday,
        p2.thanksgiving,
        p2.silentnight,
        p2.xmas,
        p2.halloween,
        p2.halloween2,
        p2.easter,
        p2.isworkday,
        p2.holidaytype,
        p2.holidayseq,
        p2.holidayinflu,
        p2.holidayinfluseq,
        p2.accident,
        p2.accidenttype,
        p2.day,
        p2.night,
        p2.seq
from dw.dim_date p1
join rpt.rpt_date_self_define p2 on p1.date_id=p2.date
where p1.date_id between '2017-01-01' and date_add('%s',3)
and p1.date_id not in ('2018-02-09','2017-01-23','2017-02-25','2017-03-29','2017-04-28','2017-06-02','2017-09-22','2017-09-23','2017-09-28',
'2017-09-29','2017-10-28','2017-11-10','2017-12-12','2018-01-01','2018-03-08','2018-05-20')
) a1
left join
(
select date,city,wstatus1 as weather_init,wstatus2 as weather_final,htemp as highest_temp,ltemp as lowest_temp,wind1 as wind_direct,wind2 as wind_force 
from rpt.weather_day 
where date<'%s' and ifpredict=0 and city in ('武汉','南宁','长沙')
union
select date,city,wstatus1 as weather_init,wstatus2 as weather_final,htemp as highest_temp,ltemp as lowest_temp,wind1 as wind_direct,wind2 as wind_force 
from rpt.weather_day 
where date>='%s' and ifpredict=1 and city in ('武汉','南宁','长沙')
) a2
on a1.date=a2.date
left join
(select date
      ,city
      ,avg(case when substr(time,12,2)=00 then temp end) as 00_temp
      ,avg(case when substr(time,12,2)=01 then temp end) as 01_temp
      ,avg(case when substr(time,12,2)=02 then temp end) as 02_temp
      ,avg(case when substr(time,12,2)=03 then temp end) as 03_temp
      ,avg(case when substr(time,12,2)=04 then temp end) as 04_temp
      ,avg(case when substr(time,12,2)=05 then temp end) as 05_temp
      ,avg(case when substr(time,12,2)=06 then temp end) as 06_temp
      ,avg(case when substr(time,12,2)=07 then temp end) as 07_temp
      ,avg(case when substr(time,12,2)=08 then temp end) as 08_temp
      ,avg(case when substr(time,12,2)=09 then temp end) as 09_temp
      ,avg(case when substr(time,12,2)=10 then temp end) as 10_temp
      ,avg(case when substr(time,12,2)=11 then temp end) as 11_temp
      ,avg(case when substr(time,12,2)=12 then temp end) as 12_temp
      ,avg(case when substr(time,12,2)=13 then temp end) as 13_temp
      ,avg(case when substr(time,12,2)=14 then temp end) as 14_temp
      ,avg(case when substr(time,12,2)=15 then temp end) as 15_temp
      ,avg(case when substr(time,12,2)=16 then temp end) as 16_temp
      ,avg(case when substr(time,12,2)=17 then temp end) as 17_temp
      ,avg(case when substr(time,12,2)=18 then temp end) as 18_temp
      ,avg(case when substr(time,12,2)=19 then temp end) as 19_temp
      ,avg(case when substr(time,12,2)=20 then temp end) as 20_temp
      ,avg(case when substr(time,12,2)=21 then temp end) as 21_temp
      ,avg(case when substr(time,12,2)=22 then temp end) as 22_temp
      ,avg(case when substr(time,12,2)=23 then temp end) as 23_temp
      ,max(case when substr(time,12,2)=00 then wstatus end) as 00_wstatus
      ,max(case when substr(time,12,2)=01 then wstatus end) as 01_wstatus
      ,max(case when substr(time,12,2)=02 then wstatus end) as 02_wstatus
      ,max(case when substr(time,12,2)=03 then wstatus end) as 03_wstatus
      ,max(case when substr(time,12,2)=04 then wstatus end) as 04_wstatus
      ,max(case when substr(time,12,2)=05 then wstatus end) as 05_wstatus
      ,max(case when substr(time,12,2)=06 then wstatus end) as 06_wstatus
      ,max(case when substr(time,12,2)=07 then wstatus end) as 07_wstatus
      ,max(case when substr(time,12,2)=08 then wstatus end) as 08_wstatus
      ,max(case when substr(time,12,2)=09 then wstatus end) as 09_wstatus
      ,max(case when substr(time,12,2)=10 then wstatus end) as 10_wstatus
      ,max(case when substr(time,12,2)=11 then wstatus end) as 11_wstatus
      ,max(case when substr(time,12,2)=12 then wstatus end) as 12_wstatus
      ,max(case when substr(time,12,2)=13 then wstatus end) as 13_wstatus
      ,max(case when substr(time,12,2)=14 then wstatus end) as 14_wstatus
      ,max(case when substr(time,12,2)=15 then wstatus end) as 15_wstatus
      ,max(case when substr(time,12,2)=16 then wstatus end) as 16_wstatus
      ,max(case when substr(time,12,2)=17 then wstatus end) as 17_wstatus
      ,max(case when substr(time,12,2)=18 then wstatus end) as 18_wstatus
      ,max(case when substr(time,12,2)=19 then wstatus end) as 19_wstatus
      ,max(case when substr(time,12,2)=20 then wstatus end) as 20_wstatus
      ,max(case when substr(time,12,2)=21 then wstatus end) as 21_wstatus
      ,max(case when substr(time,12,2)=22 then wstatus end) as 22_wstatus
      ,max(case when substr(time,12,2)=23 then wstatus end) as 23_wstatus
from 
(
select p1.date,p1.time,p1.city,p1.temp,p2.weather_name2 as wstatus
from
(select a.date,a.time,a.city,a.temp,trim(SUBSTRING_INDEX(a.wstatus,'/',1)) as wstatus
from ods.weather_hour_f a
where city in ('武汉','南宁','长沙')
and date<='%s'
and ifpredict=0
union
select  a.date,a.time,a.city,a.temp,trim(SUBSTRING_INDEX(a.wstatus,'/',1)) as wstatus
from ods.weather_hour_f a
where city in ('武汉','南宁','长沙')
and date>'%s'
and ifpredict=2) p1
left join
rpt.weather_trans_mean p2
on p1.wstatus=p2.weather_name1
) t
group by date
        ,city) a6
on  a1.date=a6.date
and  a2.date=a6.date
left join
(select store_code
       ,store_name
       ,city
       ,supervisor_name
       ,store_age
	   ,area
	   ,business_district_level1_name
	   ,store_type
	   ,partner_name
	   ,manager
	   ,purchasing_code
       ,first_open_date
from dw.dim_stores_info
where business_district_level1_name!='未知'
and store_code not in (117017,100053,100096)  ) a3
on a2.city=a3.city
and a2.city=a6.city
left join
(select date
      ,store_code
	  ,store_name
      ,first_open_date
	  ,city
	  ,customer_cnt
	  ,sales_amt
	  ,goods_num
from dw.bic_stores
where date between '2017-01-01' and date_sub('%s',0)
and business_district_level1_name!='未知'
and date_change>0
and datediff(date,first_open_date)>30
and store_code not in (117017,100053,100096)
and date not in ('2018-02-09','2017-01-23','2017-02-25','2017-03-29','2017-04-28','2017-06-02','2017-09-22','2017-09-23','2017-09-28',
'2017-09-29','2017-10-28','2017-11-10','2017-12-12','2018-01-01','2018-03-08','2018-05-20')
) a4
on a1.date=a4.date
and a3.store_code=a4.store_code
left join
(select date_id,store_code,weight_index_store
from rpt.rpt_today_store_week_index) a5
on a1.date=a5.date_id
and a3.store_code=a5.store_code	
where datediff(a1.date,a3.first_open_date)>30
"""%(yesterday,yesterday,yesterday,yesterday,yesterday,yesterday)

data1=a.query(query_sql1)



# In[4]:


mydata1=pd.DataFrame(data1,columns=['date' ,'month_of_year' ,'week_of_month','newyearday',
      'womenday','laborday','youthday','childrenday', 'partyday', 'armyday',
      'teacherday', 'nationalday','eveday', 'spring', 'lantern','qingming','dragonboat', 'valentineday', 'autumnday',
        'doubleninth', 'valentineday2', 'foolsday',
        'motherday', 'fatherday', 'thanksgiving', 'silentnight', 'xmas','halloween', 'halloween2', 'easter', 'isworkday',
        'holidaytype','holidayseq','holidayinflu','holidayinfluseq','accident', 'accidenttype', 'day','night',
        'seq' ,'lowest_temp' ,'highest_temp','weather_init' ,'weather_final' ,'wind_direct' ,'wind_force','store_code' ,'store_name'
,'city','supervisor_name' ,'store_age','area','business_district_level1_name' ,'store_type' ,'partner_name' ,'manager' ,'purchasing_code'
,'sales_amt' ,'store_days' ,'weight_index_store','00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp'
 ,'08_temp','09_temp' ,'10_temp','11_temp','12_temp'
,'13_temp','14_temp','15_temp','16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp','23_temp','00_wstatus'
,'01_wstatus','02_wstatus','03_wstatus','04_wstatus','05_wstatus','06_wstatus','07_wstatus','08_wstatus'
,'09_wstatus' ,'10_wstatus','11_wstatus','12_wstatus','13_wstatus','14_wstatus','15_wstatus','16_wstatus'
 ,'17_wstatus','18_wstatus','19_wstatus','20_wstatus','21_wstatus','22_wstatus','23_wstatus'])


# In[5]:


storecode=mydata1['store_code'].drop_duplicates()
storecode.count()


# In[6]:


query_sql3="""select p1.date_id as date
      ,p3.store_code 
	  ,sum(case when p1.date_id between p2.startdate and p2.enddate then promotiom_grade else 0 end) as promotion_grade
from dw.dim_date p1
left join
(select a1.CouponId,a1.couponname,a1.startdate,a1.enddate,a1.promotiom_grade
,substr(a2.organizationid,31,6) as store_code
,a2.organizationname as store_name
 from    
(SELECT CouponId,couponname,startdate,enddate,SaledCount/COUNT(DISTINCT organizationid) as promotiom_grade
from (select CouponId,couponname,startdate,enddate,SaledCount,
	(case typeflag when 2 then organizationid_child else organizationid end) as organizationid,
	(case typeflag when 2 then organizationname_child else organizationname end) as organizationname
from
(
select a.CouponId as CouponId,a.couponname as couponname,a.SaledCount as SaledCount,
substr(a.StartTime,1,10) as startdate,substr(a.EndTime,1,10) as enddate,
c.organizationid as organizationid,c.organizationname as organizationname,c.typeflag typeflag,
d.Organizationid as Organizationid_child,d.organizationname as organizationname_child
from ods.activity_coupon_base a
left join ods.activity_coupon_region b on a.couponid = b.couponid
left join ods.basis_organization_base c on  b.regionid = c.organizationid
left join ods.basis_organization_base d on c.OrganizationId = d.ParentId and c.typeflag = 2 and d.ActiveFlag = 1
where a.ActiveFlag = 1 
) t
) p
group by CouponId,couponname,startdate,enddate,SaledCount) a1
JOIN
(select CouponId,couponname,startdate,enddate,SaledCount,
	(case typeflag when 2 then organizationid_child else organizationid end) as organizationid,
	(case typeflag when 2 then organizationname_child else organizationname end) as organizationname
from
(
select a.CouponId as CouponId,a.couponname as couponname,a.SaledCount as SaledCount,
substr(a.StartTime,1,10) as startdate,substr(a.EndTime,1,10) as enddate,
c.organizationid as organizationid,c.organizationname as organizationname,c.typeflag typeflag,
d.Organizationid as Organizationid_child,d.organizationname as organizationname_child
from ods.activity_coupon_base a
left join ods.activity_coupon_region b on a.couponid = b.couponid
left join ods.basis_organization_base c on  b.regionid = c.organizationid
left join ods.basis_organization_base d on c.OrganizationId = d.ParentId and c.typeflag = 2 and d.ActiveFlag = 1
where a.ActiveFlag = 1 
) t
) a2 on a1.CouponId=a2.CouponId
where a1.promotiom_grade>=0
group by a1.CouponId,a1.couponname,a1.startdate,a1.enddate,a1.promotiom_grade
,substr(a2.organizationid,31,6) 
,a2.organizationname ) p2
on 1=1
left join dw.dim_stores_info p3 on p2.store_code=p3.store_code
where p1.date_id between '2018-01-01' and date_add('%s',34)
group by p1.date_id
      ,p3.store_code
"""%(yesterday)
    
data3=a.query(query_sql3)

mydata3=pd.DataFrame(data3,columns=['date','store_code','promotion_grade'])


# In[7]:


mydata3.head()


# In[8]:


query_sql4="""
select 
    date_id as date,
	store_code,
	count(distinct case when date_id between ph_start_date and ph_end_date then ph_promotion_id else null end) as cvs_promotion_grade
from
	(
	select 
		pa_purchasing_center_id,pa_promotion_id ,pa_store_id 
	from 
		(-- 店铺层
		select
			pa_purchasing_center_id,
			pa_promotion_id ,
			pa_line_number,
			pa_flag ,
			pa_district_id ,
			pa_market_id ,
			pa_store_id ,
			pa_record_status 
		from 
			ods.promotion_allocate 
		where 
			pa_store_id is not null and
			pa_record_status in (10,90)
		union all
		-- 商圈层
		select
			pa_purchasing_center_id,
			pa_promotion_id,
			pa_line_number,
			pa_flag,
			pa_district_id,
			pa_market_id,
			sp_store_id,
			pa_record_status
		from 
			ods.promotion_allocate a 
			join ods.store_profile b on a.pa_market_id = b.sp_purchase_market_type and a.pa_purchasing_center_id = b.sp_purchasing_center_id
		where 
			pa_store_id is null and
			pa_market_id is not null and
			sp_store_status = 10 and
			pa_record_status in (10,90)
		union all
		-- 地区层
		select
			pa_purchasing_center_id ,
			pa_promotion_id ,
			pa_line_number ,
			pa_flag ,
			pa_district_id ,
			pa_market_id ,
			sp_store_id ,
			pa_record_status 
		from 
			ods.promotion_allocate a 
			join ods.store_profile b on a.pa_district_id = b.sp_purchasing_area and a.pa_purchasing_center_id = b.sp_purchasing_center_id
		where 
			pa_store_id is null and
			pa_market_id is null and
			pa_district_id is not null and
			sp_store_status = 10 and
			pa_record_status in (10,90)
		) ta 
	group by pa_purchasing_center_id,pa_promotion_id ,pa_store_id 
	having avg(pa_flag ) = 1 
	) tta 
	join ods.promotion_header ttb on tta.pa_purchasing_center_id = ttb.ph_purchasing_center_id and tta.pa_promotion_id = ttb.ph_promotion_id
	right join dw.dim_date ttc on 1=1
    right join dw.dim_stores_info ttd on tta.pa_store_id=ttd.store_code
where date_id between '2016-01-01' and date_add('%s',34)
group by date_id,
	store_code
"""%(yesterday)
data4=a.query(query_sql4)
mydata4=pd.DataFrame(data4,columns=['date' ,'store_code' ,'cvs_promotion_grade'])


# In[9]:


mydata4.head()


# In[10]:


quer_sql5 = """
select  b.store_code
       
       ,b.store_age
      
       ,avg(case when day_of_week=1 then customer_cnt else null end) as 1_customer_cnt
	   ,avg(case when day_of_week=2 then customer_cnt else null end) as 2_customer_cnt
	   ,avg(case when day_of_week=3 then customer_cnt else null end) as 3_customer_cnt
	   ,avg(case when day_of_week=4 then customer_cnt else null end) as 4_customer_cnt
	   ,avg(case when day_of_week=5 then customer_cnt else null end) as 5_customer_cnt
	   ,avg(case when day_of_week=6 then customer_cnt else null end) as 6_customer_cnt
	   ,avg(case when day_of_week=7 then customer_cnt else null end) as 7_customer_cnt
	   
	   ,avg(case when day_of_week=1 then zao_customer_cnt else null end) as 1_zao_customer_cnt
	   ,avg(case when day_of_week=2 then zao_customer_cnt else null end) as 2_zao_customer_cnt
	   ,avg(case when day_of_week=3 then zao_customer_cnt else null end) as 3_zao_customer_cnt
	   ,avg(case when day_of_week=4 then zao_customer_cnt else null end) as 4_zao_customer_cnt
	   ,avg(case when day_of_week=5 then zao_customer_cnt else null end) as 5_zao_customer_cnt
	   ,avg(case when day_of_week=6 then zao_customer_cnt else null end) as 6_zao_customer_cnt
	   ,avg(case when day_of_week=7 then zao_customer_cnt else null end) as 7_zao_customer_cnt
	   
	   ,avg(case when day_of_week=1 then zhong_customer_cnt else null end) as 1_zhong_customer_cnt
	   ,avg(case when day_of_week=2 then zhong_customer_cnt else null end) as 2_zhong_customer_cnt
	   ,avg(case when day_of_week=3 then zhong_customer_cnt else null end) as 3_zhong_customer_cnt
	   ,avg(case when day_of_week=4 then zhong_customer_cnt else null end) as 4_zhong_customer_cnt
	   ,avg(case when day_of_week=5 then zhong_customer_cnt else null end) as 5_zhong_customer_cnt
	   ,avg(case when day_of_week=6 then zhong_customer_cnt else null end) as 6_zhong_customer_cnt
	   ,avg(case when day_of_week=7 then zhong_customer_cnt else null end) as 7_zhong_customer_cnt
	   
	   ,avg(case when day_of_week=1 then wan_customer_cnt else null end) as 1_wan_customer_cnt
	   ,avg(case when day_of_week=2 then wan_customer_cnt else null end) as 2_wan_customer_cnt
	   ,avg(case when day_of_week=3 then wan_customer_cnt else null end) as 3_wan_customer_cnt
	   ,avg(case when day_of_week=4 then wan_customer_cnt else null end) as 4_wan_customer_cnt
	   ,avg(case when day_of_week=5 then wan_customer_cnt else null end) as 5_wan_customer_cnt
	   ,avg(case when day_of_week=6 then wan_customer_cnt else null end) as 6_wan_customer_cnt
	   ,avg(case when day_of_week=7 then wan_customer_cnt else null end) as 7_wan_customer_cnt
       
       ,avg(case when day_of_week=1 then xianshi_amt_rate else null end) as 1_xianshi_amt_rate
	   ,avg(case when day_of_week=2 then xianshi_amt_rate else null end) as 2_xianshi_amt_rate
	   ,avg(case when day_of_week=3 then xianshi_amt_rate else null end) as 3_xianshi_amt_rate
	   ,avg(case when day_of_week=4 then xianshi_amt_rate else null end) as 4_xianshi_amt_rate
	   ,avg(case when day_of_week=5 then xianshi_amt_rate else null end) as 5_xianshi_amt_rate
	   ,avg(case when day_of_week=6 then xianshi_amt_rate else null end) as 6_xianshi_amt_rate
	   ,avg(case when day_of_week=7 then xianshi_amt_rate else null end) as 7_xianshi_amt_rate
	   
from
(select  a1.date 
       ,a1.day_of_week 
	   ,a1.store_code 
       ,a1.store_name
       ,a1.business_district_level1_code
       ,a1.store_age
	   ,a1.customer_cnt 
	   ,a2.zao_customer_cnt 
	   ,a2.zhong_customer_cnt 
	   ,a2.wan_customer_cnt 
       ,a3.xianshi_amt_rate
       ,a3.shipin_amt_rate
       ,a3.changwen_amt_rate
       ,a3.diwen_amt_rate
       ,a3.xiangyan_amt_rate
       ,a3.riyong_amt_rate
       ,a3.baopin_amt_rate
from 
(select  date,day_of_week,store_code,store_name,datediff('%s',p1.first_open_date) as store_age,p2.business_district_level1_code,customer_cnt,sales_amt,goods_num
 from dw.bic_stores p1
 join ods.business_district_level1_name p2 on p1.business_district_level1_name=p2.business_district_level1_name
 where date between date_sub('%s',90) and '%s') a1
join
(select date,store_code
            ,sum(zao_customer_cnt) zao_customer_cnt
			,sum(zhong_customer_cnt) zhong_customer_cnt
			,sum(wan_customer_cnt) wan_customer_cnt
 from
 (select date,store_code
        ,sum(case when hour in (7,8,9) then customer_cnt else 0 end) as zao_customer_cnt
		,sum(case when hour in (11,12,13) then customer_cnt else 0 end) as zhong_customer_cnt
		,sum(case when hour in (17,18,19,20,21) then customer_cnt else 0 end) as wan_customer_cnt
 from
 dw.bic_stores_hour 
 where  date between date_sub('%s',90) and '%s'
 group by date
          ,store_code
         ,case when hour in (7,8,9) then customer_cnt else 0 end
		 ,case when hour in (11,12,13) then customer_cnt else 0 end
		 ,case when hour in (17,18,19,20,21) then customer_cnt else 0 end) p
group by date,store_code		 
 ) a2 
 on a1.date=a2.date and a1.store_code=a2.store_code
 join
(select p1.date
     ,p1.store_code
     ,case when p1.cate0_id=1 then p1.cate0_amt/p2.total_sales_amt end as  xianshi_amt_rate
     ,case when p1.cate0_id=2 then p1.cate0_amt/p2.total_sales_amt end as  shipin_amt_rate
     ,case when p1.cate0_id=3 then p1.cate0_amt/p2.total_sales_amt end as  changwen_amt_rate
     ,case when p1.cate0_id=4 then p1.cate0_amt/p2.total_sales_amt end as  diwen_amt_rate
     ,case when p1.cate0_id=5 then p1.cate0_amt/p2.total_sales_amt end as  xiangyan_amt_rate
     ,case when p1.cate0_id=6 then p1.cate0_amt/p2.total_sales_amt end as  riyong_amt_rate
     ,case when p1.cate0_id=7 then p1.cate0_amt/p2.total_sales_amt end as  baopin_amt_rate
     
 from 
 (select date,store_code,cate0_id,cate0_name,sum(sales_amt) cate0_amt
 from dw.bic_stores_goods 
 where date between date_sub('%s',90) and '%s'
  and cate0_id>=0
 group by date,store_code,cate0_id,cate0_name) p1 
 join 
 (select date,store_code,sum(sales_amt)  total_sales_amt  
 from dw.bic_stores_goods
 where  date between date_sub('%s',90) and '%s'
 and cate0_id>=0
 group by date,store_code) p2 
 on p1.date=p2.date
 and p1.store_code=p2.store_code
 
 group by  p1.date
     ,p1.store_code
     ,case when p1.cate0_id=1 then p1.cate0_amt/p2.total_sales_amt end 
     ,case when p1.cate0_id=2 then p1.cate0_amt/p2.total_sales_amt end 
     ,case when p1.cate0_id=3 then p1.cate0_amt/p2.total_sales_amt end 
     ,case when p1.cate0_id=4 then p1.cate0_amt/p2.total_sales_amt end 
     ,case when p1.cate0_id=5 then p1.cate0_amt/p2.total_sales_amt end 
     ,case when p1.cate0_id=6 then p1.cate0_amt/p2.total_sales_amt end 
     ,case when p1.cate0_id=7 then p1.cate0_amt/p2.total_sales_amt end
 )  a3 
on a1.date=a3.date and a1.store_code=a3.store_code

group by a1.date 
       ,a1.day_of_week 
	   ,a1.store_code 
       ,a1.store_name
       ,a1.business_district_level1_code
       ,a1.store_age
	   ,a1.customer_cnt 
	   ,a2.zao_customer_cnt 
	   ,a2.zhong_customer_cnt 
	   ,a2.wan_customer_cnt
       ,a3.xianshi_amt_rate
       ,a3.shipin_amt_rate
       ,a3.changwen_amt_rate
       ,a3.diwen_amt_rate
       ,a3.xiangyan_amt_rate
       ,a3.riyong_amt_rate
       ,a3.baopin_amt_rate
) b
group by b.store_code
     
       ,b.store_age	      
""" % (yesterday,yesterday,yesterday,yesterday,yesterday,yesterday,yesterday,yesterday,yesterday)

data5=a.query(quer_sql5)


# In[11]:


mydata5=pd.DataFrame(data5
      ,columns=['store_code','store_age','1_customer_cnt','2_customer_cnt', '3_customer_cnt'
                ,'4_customer_cnt','5_customer_cnt','6_customer_cnt','7_customer_cnt'
                 ,'1_zao_customer_cnt','2_zao_customer_cnt','3_zao_customer_cnt'
                 ,'4_zao_customer_cnt','5_zao_customer_cnt','6_zao_customer_cnt','7_zao_customer_cnt'
                 ,'1_zhong_customer_cnt','2_zhong_customer_cnt','3_zhong_customer_cnt','4_zhong_customer_cnt'
                 ,'5_zhong_customer_cnt','6_zhong_customer_cnt','7_zhong_customer_cnt','1_wan_customer_cnt'
                ,'2_wan_customer_cnt','3_wan_customer_cnt','4_wan_customer_cnt','5_wan_customer_cnt','6_wan_customer_cnt'
                ,'7_wan_customer_cnt','1_xianshi_amt_rate','2_xianshi_amt_rate','3_xianshi_amt_rate'
                ,'4_xianshi_amt_rate','5_xianshi_amt_rate','6_xianshi_amt_rate','7_xianshi_amt_rate'])


# In[12]:


mydata5.set_index("store_code", inplace=True)
mydata5=mydata5.dropna()


# ## 对mydata5归一化  （原始值-均值）/ 标准值

# In[13]:


data = (mydata5 - mydata5.mean(axis = 0))/(mydata5.std(axis = 0))


# In[14]:


from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt
k = 7  
iteration = 1000   
kmodel = KMeans(n_clusters = k, n_jobs = 1)
kmodel.fit(data) 
r1 = pd.Series(kmodel.labels_).value_counts()  
r2 = pd.DataFrame(kmodel.cluster_centers_)    
r = pd.concat([r2, r1], axis = 1) 
r.columns = list(data.columns) + [u'类别数目'] 
print(r)
r = pd.concat([mydata5, pd.Series(kmodel.labels_, index = data.index)], axis = 1)  
r.columns = list(mydata5.columns) + [u'clust'] 
rr=(r.clust).reset_index()
rr.groupby('clust')['store_code'].count()


# In[15]:


query_sql2="""
select a1.store_code
	  ,a4.province
      ,a4.big_area as district
	
      ,geneday_active_popu
	  ,geneday_resident_popu 
	  ,geneday_office_popu
      ,suday_active_popu
	  ,suday_resident_popu 
	  ,suday_office_popu
      ,holday_active_popu
	  ,holday_resident_popu 
	  ,holday_office_popu

	  ,a2.maleval
	  ,a2.femaleval
	  ,a2.teenval
	  ,a2.youthnval
	  ,middleval
	  ,midoldval
	  ,leoldval
	  ,oldval
	  ,studentval
	  ,waiterval
	  ,empleyval
	  ,hospitval
	  ,teacherval
	  ,servantval
	  ,housewifeval
	  ,texterval
	  ,researchval
	  ,ruckval
	  ,courierval
	  ,havechildval
	  ,nochildval
	  ,strongconsumeval
	  ,lesstrongconsumeval
	  ,midconsumeval
	  ,lesmidconsumeval
	  ,lessconsumeval
	  ,zctshcnum
      ,zctzjcnum
      ,zcthncnum
      ,zctxbcnum
      ,zctlzhnum
      ,zctdfnum
      ,zcthxjlnum
      ,zctqzcgnum
      ,zcttwcnum
      ,zctczcnum
      ,zcthbcnum
      ,zctdbcnum
      ,zctygcnum
      ,zcthgdnum
      ,zctzhjlnum
      ,zctsccnum
      ,zctgdcnum
      ,zctjscnum
      ,zctzsscgnum
      ,zctbjcnum
      ,zctahcnum
      ,zctsdcnum
      ,zctfjcnum
      ,jtctqcznum
      ,jtgjznum
      ,jtdtznum
      ,jttccnum
      ,jtjcnum
      ,jthcznum
      ,xxcycsnum
      ,bgsqcyyqnum
      ,bgsqswxzlnum
      ,bgsqxqnum
      ,yysjjdyynum
      ,yyzhyynum
      ,yyzkyynum
      ,kftnum
      ,kftxbknum
      ,kftpacnum
      ,kftsdkfnum
      ,sycsnum
      ,sytssyjnum
      ,synfcpscnum
      ,syjddzmcnum
      ,syscnum
      ,sygwzxnum
      ,wgctnum
      ,yljbnum
	  ,ylyxtnum
	  ,ylyjynum
	  ,ylydcgnum
	  ,ylyzhnum
      ,ylktvnum
	  ,yldtnum
      ,kctypypnum
	  ,kctkdjnum
	  ,kctmdnnum
	  ,kctbsknum
	  ,kctyhdjnum
	  ,kctcctnum
	,kctjyjnum
	,kctmxnum
	,jycrjynum
	,jyyeynum
	,jyxxnum
	,jyzxnum
	,jygdyxnum
	,jyzyjsxynum
from
(select '2018-06-24' as date 
      ,shopid as store_code
	  ,avg(case when date between '2018-06-04' and '2018-06-08'  then num1 end) as geneday_active_popu
	  ,avg(case when date between '2018-06-04' and '2018-06-08'  then num2 end) as geneday_resident_popu 
	  ,avg(case when date between '2018-06-04' and '2018-06-08'  then num3 end) as geneday_office_popu
      ,avg(case when date in ('2018-06-09','2018-06-10','2018-06-23','2018-06-24')  then num1 end) as suday_active_popu
	  ,avg(case when date in ('2018-06-09','2018-06-10','2018-06-23','2018-06-24')  then num2 end) as suday_resident_popu 
	  ,avg(case when date in ('2018-06-09','2018-06-10','2018-06-23','2018-06-24') then num3 end) as suday_office_popu
      ,avg(case when date in ('2018-06-16','2018-06-17','2018-06-18')  then num1 end) as holday_active_popu
	  ,avg(case when date in ('2018-06-16','2018-06-17','2018-06-18')  then num2 end) as holday_resident_popu 
	  ,avg(case when date in ('2018-06-16','2018-06-17','2018-06-18')  then num3 end) as holday_office_popu
from ods.population 
where radius=0.5
and date between '2018-05-15' and '2018-06-29'
group by '2018-06-24'
        ,shopid) a1
join
(select date
      ,shopid as store_code
      ,sum(case when standard='性别' and type='男' then val else 0 end) as maleval
      ,sum(case when standard='性别' and type='女' then val else 0 end) as femaleval
      ,sum(case when standard='年龄段' and type='0-18' then val else 0 end) as teenval
      ,sum(case when standard='年龄段' and type='19-24' then val else 0 end) as youthnval
      ,sum(case when standard='年龄段' and type='25-34' then val else 0 end) as middleval
      ,sum(case when standard='年龄段' and type='35-44' then val else 0 end) as midoldval
      ,sum(case when standard='年龄段' and type='45-54' then val else 0 end) as leoldval
      ,sum(case when standard='年龄段' and type='>=55' then val else 0 end) as  oldval
      ,sum(case when standard='职业' and type='学生' then val else 0 end) as  studentval
      ,sum(case when standard='职业' and type='服务人员' then val else 0 end) as  waiterval
      ,sum(case when standard='职业' and type='公司职员' then val else 0 end) as  empleyval
      ,sum(case when standard='职业' and type='医疗人员' then val else 0 end) as  hospitval
      ,sum(case when standard='职业' and type='教职工' then val else 0 end) as  teacherval
      ,sum(case when standard='职业' and type='公务员' then val else 0 end) as  servantval
      ,sum(case when standard='职业' and type='家庭主妇' then val else 0 end) as  housewifeval
      ,sum(case when standard='职业' and type='出租车司机' then val else 0 end) as texterval
      ,sum(case when standard='职业' and type='科研人员' then val else 0 end) as researchval
      ,sum(case when standard='职业' and type='货车司机' then val else 0 end) as ruckval 
      ,sum(case when standard='职业' and type='快递员' then val else 0 end) as courierval
      ,sum(case when standard='是否有小孩' and type='是' then val else 0 end) as havechildval
      ,sum(case when standard='是否有小孩' and type='否' then val else 0 end) as nochildval
      ,sum(case when standard='消费能力' and type='强' then val else 0 end) as strongconsumeval
      ,sum(case when standard='消费能力' and type='较强' then val else 0 end) as lesstrongconsumeval
      ,sum(case when standard='消费能力' and type='中等' then val else 0 end) as midconsumeval
      ,sum(case when standard='消费能力' and type='较弱' then val else 0 end) as lesmidconsumeval  
      ,sum(case when standard='消费能力' and type='弱' then val else 0 end) as lessconsumeval
from ods.people
where radius=0.5
and date='2018-06-24'
group  by date
      ,shopid) a2
on a1.date=a2.date and a1.store_code=a2.store_code
join
(SELECT date
      ,shopid as store_code
      ,count(case when type1='中餐厅' and type2='上海菜' then name else null end) as zctshcnum
      ,count(case when type1='中餐厅' and type2='浙江菜' then name else null end) as zctzjcnum
      ,count(case when type1='中餐厅' and type2='湖南菜(湘菜)' then name else null end) as zcthncnum
      ,count(case when type1='中餐厅' and type2='西北菜' then name else null end) as zctxbcnum
      ,count(case when type1='中餐厅' and type2='老字号' then name else null end) as zctlzhnum
      ,count(case when type1='中餐厅' and type2='特色/地方风味餐厅' then name else null end) as zctdfnum
      ,count(case when type1='中餐厅' and type2='海鲜酒楼' then name else null end) as zcthxjlnum
      ,count(case when type1='中餐厅' and type2='清真菜馆' then name else null end) as zctqzcgnum
      ,count(case when type1='中餐厅' and type2='台湾菜' then name else null end) as zcttwcnum
      ,count(case when type1='中餐厅' and type2='潮州菜' then name else null end) as zctczcnum
      ,count(case when type1='中餐厅' and type2='湖北菜(鄂菜)' then name else null end) as zcthbcnum
      ,count(case when type1='中餐厅' and type2='东北菜' then name else null end) as zctdbcnum
      ,count(case when type1='中餐厅' and type2='云贵菜' then name else null end) as zctygcnum
      ,count(case when type1='中餐厅' and type2='火锅店' then name else null end) as zcthgdnum
      ,count(case when type1='中餐厅' and type2='综合酒楼' then name else null end) as zctzhjlnum
      ,count(case when type1='中餐厅' and type2='四川菜(川菜)' then name else null end) as zctsccnum
      ,count(case when type1='中餐厅' and type2='广东菜(粤菜)' then name else null end) as zctgdcnum
      ,count(case when type1='中餐厅' and type2='江苏菜' then name else null end) as zctjscnum
      ,count(case when type1='中餐厅' and type2='中式素菜馆' then name else null end) as zctzsscgnum
      ,count(case when type1='中餐厅' and type2='北京菜' then name else null end) as zctbjcnum
      ,count(case when type1='中餐厅' and type2='安徽菜(徽菜)' then name else null end) as zctahcnum
      ,count(case when type1='中餐厅' and type2='山东菜(鲁菜)' then name else null end) as zctsdcnum
      ,count(case when type1='中餐厅' and type2='福建菜' then name else null end) as zctfjcnum
      ,count(case when type1='交通' and type2='长途汽车站' then name else null end) as jtctqcznum
      ,count(case when type1='交通' and type2='公交站' then name else null end) as jtgjznum
      ,count(case when type1='交通' and type2='地铁站' then name else null end) as jtdtznum
      ,count(case when type1='交通' and type2='停车场' then name else null end) as jttccnum
      ,count(case when type1='交通' and type2='机场' then name else null end) as jtjcnum
      ,count(case when type1='交通' and type2='火车站' then name else null end) as jthcznum
      ,count(case when type1='休闲餐饮场所' and type2='休闲餐饮场所' then name else null end) as xxcycsnum
      ,count(case when type1='办公&社区' and type2='产业园区' then name else null end) as bgsqcyyqnum
      ,count(case when type1='办公&社区' and type2='商务写字楼' then name else null end) as bgsqswxzlnum
      ,count(case when type1='办公&社区' and type2='小区' then name else null end) as bgsqxqnum
      ,count(case when type1='医院' and type2='三级甲等医院' then name else null end) as yysjjdyynum
      ,count(case when type1='医院' and type2='综合医院' then name else null end) as yyzhyynum
      ,count(case when type1='医院' and type2='专科医院' then name else null end) as yyzkyynum
      ,count(case when type1='咖啡厅' and type2='咖啡厅' then name else null end) as kftnum
      ,count(case when type1='咖啡厅' and type2='星巴克咖啡' then name else null end) as kftxbknum
      ,count(case when type1='咖啡厅' and type2='Pacific Co' then name else null end) as kftpacnum
      ,count(case when type1='咖啡厅' and type2='上岛咖啡' then name else null end) as kftsdkfnum
      ,count(case when type1='商业' and type2='超市' then name else null end) as sycsnum
      ,count(case when type1='商业' and type2='特色商业街' then name else null end) as sytssyjnum
      ,count(case when type1='商业' and type2='农副产品市场' then name else null end) as synfcpscnum
      ,count(case when type1='商业' and type2='家电电子卖场' then name else null end) as syjddzmcnum
      ,count(case when type1='商业' and type2='商场' then name else null end) as syscnum
      ,count(case when type1='商业' and type2='购物中心' then name else null end) as sygwzxnum
      ,count(case when type1='外国餐厅' and type2='外国餐厅' then name else null end) as wgctnum
      ,count(case when type1='娱乐场所' and type2='酒吧' then name else null end) as yljbnum
	  ,count(case when type1='娱乐场所' and type2='游戏厅' then name else null end) as ylyxtnum
	  ,count(case when type1='娱乐场所' and type2='影剧院' then name else null end) as ylyjynum
			,count(case when type1='娱乐场所' and type2='运动场馆' then name else null end) as ylydcgnum
			,count(case when type1='娱乐场所' and type2='夜总会' then name else null end) as ylyzhnum
			,count(case when type1='娱乐场所' and type2='KTV' then name else null end) as ylktvnum
			,count(case when type1='娱乐场所' and type2='迪厅' then name else null end) as yldtnum
			,count(case when type1='快餐厅' and type2='呷哺呷哺' then name else null end) as kctypypnum
			,count(case when type1='快餐厅' and type2='肯德基' then name else null end) as kctkdjnum
			,count(case when type1='快餐厅' and type2='麦当劳' then name else null end) as kctmdnnum
			,count(case when type1='快餐厅' and type2='必胜客' then name else null end) as kctbsknum
			,count(case when type1='快餐厅' and type2='永和豆浆' then name else null end) as kctyhdjnum
			,count(case when type1='快餐厅' and type2='茶餐厅' then name else null end) as kctcctnum
			,count(case when type1='快餐厅' and type2='吉野家' then name else null end) as kctjyjnum
			,count(case when type1='快餐厅' and type2='美心' then name else null end) as kctmxnum
			,count(case when type1='教育' and type2='成人教育' then name else null end) as jycrjynum
			,count(case when type1='教育' and type2='幼儿园' then name else null end) as jyyeynum
			,count(case when type1='教育' and type2='小学' then name else null end) as jyxxnum
			,count(case when type1='教育' and type2='中学' then name else null end) as jyzxnum
			,count(case when type1='教育' and type2='高等院校' then name else null end) as jygdyxnum
			,count(case when type1='教育' and type2='职业技术学院' then name else null end) as jyzyjsxynum
from ods.surround
where date='2018-06-24'
and radius=3 and distance<=500
group by date
        ,shopid ) a3
on a1.date=a3.date and a1.store_code=a3.store_code
join  
(select store_code
      ,city
	  ,province
	,big_area
from dw.dim_stores_info) a4
on a1.store_code=a4.store_code
"""

data2=a.query(query_sql2)


# In[16]:


import numpy as np
import pandas as pd
mydata2=pd.DataFrame(list(data2),columns=['store_code','province','district','geneday_active_popu' ,'geneday_resident_popu'
	  ,'geneday_office_popu' ,'suday_active_popu','suday_resident_popu'  ,'suday_office_popu' ,'holday_active_popu' ,'holday_resident_popu' 
	  ,'holday_office_popu','maleval','femaleval','teenval','youthnval','middleval','midoldval','leoldval','oldval','studentval'
,'waiterval','empleyval','hospitval','teacherval','servantval','housewifeval','texterval','researchval','ruckval','courierval'
,'havechildval','nochildval','strongconsumeval' ,'lesstrongconsumeval','midconsumeval','lesmidconsumeval','lessconsumeval','zctshcnum'
,'zctzjcnum','zcthncnum','zctxbcnum','zctlzhnum','zctdfnum','zcthxjlnum','zctqzcgnum','zcttwcnum','zctczcnum' ,'zcthbcnum','zctdbcnum','zctygcnum'
,'zcthgdnum','zctzhjlnum','zctsccnum','zctgdcnum','zctjscnum','zctzsscgnum','zctbjcnum','zctahcnum','zctsdcnum','zctfjcnum','jtctqcznum'
 ,'jtgjznum','jtdtznum','jttccnum','jtjcnum','jthcznum','xxcycsnum','bgsqcyyqnum','bgsqswxzlnum','bgsqxqnum','yysjjdyynum','yyzhyynum'
,'yyzkyynum','kftnum','kftxbknum','kftpacnum','kftsdkfnum' ,'sycsnum','sytssyjnum','synfcpscnum','syjddzmcnum','syscnum','sygwzxnum'
,'wgctnum','yljbnum','ylyxtnum','ylyjynum','ylydcgnum','ylyzhnum','ylktvnum','yldtnum','kctypypnum','kctkdjnum','kctmdnnum','kctbsknum'
,'kctyhdjnum','kctcctnum','kctjyjnum','kctmxnum','jycrjynum','jyyeynum','jyxxnum','jyzxnum','jygdyxnum','jyzyjsxynum' ])


# In[17]:


mydata2.head()


# In[18]:


mydata2['province'].drop_duplicates()


# In[19]:


query_sql7="""
select shopid as store_code
	  ,sum(case when date between '2018-06-25' and '2018-06-29'  then num1 end)*0.2 as geneday_latest_active
	  ,avg(case when date between '2018-06-25' and '2018-06-29'  then num2 end) as geneday_latest_resident
	  ,avg(case when date between '2018-06-25' and '2018-06-29'  then num3 end) as geneday_latest_office
      ,sum(case when date in  ('2018-06-24','2018-06-30')  then num1 end)*0.5 as suday_latest_active
	  ,avg(case when date in  ('2018-06-24','2018-06-30')  then num2 end) as suday_latest_resident
	  ,avg(case when date in  ('2018-06-24','2018-06-30') then num3 end) as suday_latest_office
from ods.population_hour
where posi = '4-4'
and radius=0.5
and date between '2018-06-24' and '2018-06-30'
group by shopid
"""
data7=a.query(query_sql7)    


# In[20]:


mydata7=pd.DataFrame(data7,columns=['store_code','geneday_latest_active','geneday_latest_resident'
                                    ,'geneday_latest_office','suday_latest_active','suday_latest_resident','suday_latest_office'])


# In[21]:


a.close()


# # 5.合并数据

# In[22]:


mydatamerge1=pd.merge(mydata1,mydata3,on=['date','store_code'],how='left')


# In[23]:


mydatamerge2=pd.merge(mydatamerge1,mydata4,on=['store_code','date'],how='left') 


# In[24]:


mydatamerge3=pd.merge(mydatamerge2,rr,on=['store_code','store_code'],how='left') 


# In[25]:


mydatamerge4=pd.merge(mydatamerge3,mydata7,on=['store_code','store_code'],how='left')


# In[26]:


#mydatamerge5=pd.merge(mydatamerge4,mydata8,on=['store_code','store_code'],how='left')


# In[27]:


mydata=pd.merge(mydatamerge4,mydata2,on=['store_code','store_code'],how='left') 
#mydata2中只有武汉店铺数据，南宁和长沙没有数据，此处使用inner表示合并数据都只有武汉店铺；如使用left则三个城市数据都有，但需要处理缺失数据


# In[28]:


mydata['cvs_promotion_grade']=mydata['cvs_promotion_grade'].fillna(0)
mydata['promotion_grade']=mydata['promotion_grade'].fillna(0)
mydata['weight_index_store']=mydata['weight_index_store'].fillna(1)
mydata['clust']=mydata['clust'].fillna(7)
for wstatus in list(mydata[['00_wstatus','01_wstatus','02_wstatus','03_wstatus','04_wstatus','05_wstatus','06_wstatus','07_wstatus','08_wstatus'
,'09_wstatus' ,'10_wstatus','11_wstatus','12_wstatus','13_wstatus','14_wstatus','15_wstatus','16_wstatus'
 ,'17_wstatus','18_wstatus','19_wstatus','20_wstatus','21_wstatus','22_wstatus','23_wstatus']].columns):
    mydata[wstatus]=mydata[wstatus].fillna('多云')


# In[29]:


from sklearn.preprocessing import Imputer
imp1 = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp1.fit(mydata[['00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp','08_temp','09_temp' ,'10_temp'
,'11_temp','12_temp','13_temp','14_temp','15_temp','16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp','23_temp']])

mydata[['00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp','08_temp','09_temp' ,'10_temp'
,'11_temp','12_temp','13_temp','14_temp','15_temp','16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp'
        ,'23_temp']]=imp1.transform(mydata[['00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp'
                                           ,'08_temp','09_temp' ,'10_temp','11_temp','12_temp','13_temp','14_temp','15_temp'
                                           ,'16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp','23_temp']])


# In[30]:


storecode1=mydata['store_code'].drop_duplicates()
storecode1.count()


# In[31]:


n=mydata.groupby('store_code')['date'].count()
n=n.reset_index(drop = False)
####剔除样本量少于30的店铺
less30_store=n.loc[n.date<30,:]['store_code']
for store_code in less30_store:
    mydata=mydata.drop(list(mydata.loc[mydata.loc[:,'store_code']==store_code,:].index))
less30_store.count()    


# In[32]:


storecode=mydata['store_code'].drop_duplicates()
storecode.count()


# In[33]:


sale_amtna=mydata.loc[mydata['date']<=str(yesterday),:]


# In[34]:


sale_amtna['sales_amt']=sale_amtna['sales_amt'].fillna(-999999999)


# In[35]:


mydata=mydata.drop(sale_amtna.loc[sale_amtna['sales_amt']==-999999999,:].index.tolist())


# In[36]:


mydata=mydata.reset_index(drop = True)


# # 6.处理离散型数据

# In[37]:


from sklearn import preprocessing  
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()
discretedata1=mydata[[ 'clust']]
enc.fit(discretedata1)
enc.n_values_
enc.feature_indices_
onhotencodedata1=pd.DataFrame(enc.transform(discretedata1).toarray())


# In[38]:


onhotencodedata1.head()


# In[39]:


#字符型离散型数据
discretedata2=mydata[['purchasing_code','month_of_year','week_of_month','city','province','district' ,'supervisor_name' 
                      ,'store_age','area','business_district_level1_name' ,'store_type'  ,'partner_name' 
        ,'manager','weather_init' ,'weather_final','wind_direct'  ,'wind_force','store_code'
     ,'00_wstatus','01_wstatus','02_wstatus','03_wstatus','04_wstatus','05_wstatus','06_wstatus','07_wstatus','08_wstatus'
,'09_wstatus' ,'10_wstatus','11_wstatus','12_wstatus','13_wstatus','14_wstatus','15_wstatus','16_wstatus'
 ,'17_wstatus','18_wstatus','19_wstatus','20_wstatus','21_wstatus','22_wstatus','23_wstatus',   'holidaytype','holidayseq'
                      ,'holidayinflu','holidayinfluseq']]
onhotencodedata2=pd.get_dummies(discretedata2)


# In[40]:


onhotencodedata2.head()


# # 7.处理连续型数据

# In[41]:


continuousdata=mydata[[ 'store_days','lowest_temp','highest_temp','geneday_active_popu'
	  ,'geneday_resident_popu'
	  ,'geneday_office_popu'
      ,'suday_active_popu'
	  ,'suday_resident_popu' 
	  ,'suday_office_popu'
      ,'holday_active_popu'
	  ,'holday_resident_popu' 
	  ,'holday_office_popu','maleval','femaleval','teenval','youthnval','middleval','midoldval','leoldval','oldval','studentval'
,'waiterval','empleyval','hospitval','teacherval','servantval','housewifeval','texterval','researchval','ruckval','courierval'
,'havechildval','nochildval','strongconsumeval' ,'lesstrongconsumeval','midconsumeval','lesmidconsumeval','lessconsumeval','zctshcnum'
,'zctzjcnum','zcthncnum','zctxbcnum','zctlzhnum','zctdfnum','zcthxjlnum','zctqzcgnum','zcttwcnum','zctczcnum' ,'zcthbcnum','zctdbcnum','zctygcnum'
,'zcthgdnum','zctzhjlnum','zctsccnum','zctgdcnum','zctjscnum','zctzsscgnum','zctbjcnum','zctahcnum','zctsdcnum','zctfjcnum','jtctqcznum'
 ,'jtgjznum','jtdtznum','jttccnum','jtjcnum','jthcznum','xxcycsnum','bgsqcyyqnum','bgsqswxzlnum','bgsqxqnum','yysjjdyynum','yyzhyynum'
,'yyzkyynum','kftnum','kftxbknum','kftpacnum','kftsdkfnum' ,'sycsnum','sytssyjnum','synfcpscnum','syjddzmcnum','syscnum','sygwzxnum'
,'wgctnum','yljbnum','ylyxtnum','ylyjynum','ylydcgnum','ylyzhnum','ylktvnum','yldtnum','kctypypnum','kctkdjnum','kctmdnnum','kctbsknum'
,'kctyhdjnum','kctcctnum','kctjyjnum','kctmxnum','jycrjynum','jyyeynum','jyxxnum','jyzxnum','jygdyxnum','jyzyjsxynum','promotion_grade'
,'cvs_promotion_grade','clust','weight_index_store','geneday_latest_active','geneday_latest_resident','geneday_latest_office','suday_latest_active'
                       ,'suday_latest_resident','suday_latest_office','00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp'
 ,'08_temp','09_temp' ,'10_temp','11_temp','12_temp'
,'13_temp','14_temp','15_temp','16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp','23_temp', 'isworkday','newyearday',
     'womenday','laborday','youthday','childrenday', 'partyday', 'armyday',
     'teacherday', 'nationalday','eveday', 'spring', 'lantern','qingming','dragonboat', 'valentineday', 'autumnday',
       'doubleninth', 'valentineday2', 'foolsday',
       'motherday', 'fatherday', 'thanksgiving', 'silentnight', 'xmas','halloween', 'halloween2', 'easter']]
continuousdata=pd.DataFrame(continuousdata,dtype=np.float)


# In[42]:


missdata=mydata[[ 'geneday_active_popu'
	  ,'geneday_resident_popu'
	  ,'geneday_office_popu'
      ,'suday_active_popu'
	  ,'suday_resident_popu' 
	  ,'suday_office_popu'
      ,'holday_active_popu'
	  ,'holday_resident_popu' 
	  ,'holday_office_popu','maleval','femaleval','teenval','youthnval','middleval','midoldval','leoldval','oldval','studentval'
,'waiterval','empleyval','hospitval','teacherval','servantval','housewifeval','texterval','researchval','ruckval','courierval'
,'havechildval','nochildval','strongconsumeval' ,'lesstrongconsumeval','midconsumeval','lesmidconsumeval','lessconsumeval','zctshcnum'
,'zctzjcnum','zcthncnum','zctxbcnum','zctlzhnum','zctdfnum','zcthxjlnum','zctqzcgnum','zcttwcnum','zctczcnum' ,'zcthbcnum','zctdbcnum','zctygcnum'
,'zcthgdnum','zctzhjlnum','zctsccnum','zctgdcnum','zctjscnum','zctzsscgnum','zctbjcnum','zctahcnum','zctsdcnum','zctfjcnum','jtctqcznum'
 ,'jtgjznum','jtdtznum','jttccnum','jtjcnum','jthcznum','xxcycsnum','bgsqcyyqnum','bgsqswxzlnum','bgsqxqnum','yysjjdyynum','yyzhyynum'
,'yyzkyynum','kftnum','kftxbknum','kftpacnum','kftsdkfnum' ,'sycsnum','sytssyjnum','synfcpscnum','syjddzmcnum','syscnum','sygwzxnum'
,'wgctnum','yljbnum','ylyxtnum','ylyjynum','ylydcgnum','ylyzhnum','ylktvnum','yldtnum','kctypypnum','kctkdjnum','kctmdnnum','kctbsknum'
,'kctyhdjnum','kctcctnum','kctjyjnum','kctmxnum','jycrjynum','jyyeynum','jyxxnum','jyzxnum','jygdyxnum','jyzyjsxynum'
,'clust','geneday_latest_active','geneday_latest_resident','geneday_latest_office','suday_latest_active'
                ,'suday_latest_resident','suday_latest_office'         
]]
missdata=pd.DataFrame(missdata,dtype=np.float)


# In[43]:


missmean=(missdata.groupby('clust').mean()).reset_index()
missmean


# In[44]:


for columns in list(missmean.columns)[1:]:
    for i in range(10):
        continuousdata.loc[continuousdata['clust']==i,[columns]]=continuousdata.loc[continuousdata['clust']==i,[columns]].replace(np.nan,missmean.loc[missmean['clust']==i,[columns]]) 


# In[45]:


continuousdata=continuousdata[[ 'store_days','lowest_temp','highest_temp','geneday_active_popu'
	  ,'geneday_resident_popu' ,'geneday_office_popu','suday_active_popu' ,'suday_resident_popu' ,'suday_office_popu'
      ,'holday_active_popu' ,'holday_resident_popu' ,'holday_office_popu','maleval','femaleval','teenval','youthnval'
                               ,'middleval','midoldval','leoldval','oldval','studentval'
,'waiterval','empleyval','hospitval','teacherval','servantval','housewifeval','texterval','researchval','ruckval','courierval'
,'havechildval','nochildval','strongconsumeval' ,'lesstrongconsumeval','midconsumeval','lesmidconsumeval','lessconsumeval','zctshcnum'
,'zctzjcnum','zcthncnum','zctxbcnum','zctlzhnum','zctdfnum','zcthxjlnum','zctqzcgnum','zcttwcnum','zctczcnum' ,'zcthbcnum','zctdbcnum','zctygcnum'
,'zcthgdnum','zctzhjlnum','zctsccnum','zctgdcnum','zctjscnum','zctzsscgnum','zctbjcnum','zctahcnum','zctsdcnum','zctfjcnum','jtctqcznum'
 ,'jtgjznum','jtdtznum','jttccnum','jtjcnum','jthcznum','xxcycsnum','bgsqcyyqnum','bgsqswxzlnum','bgsqxqnum','yysjjdyynum','yyzhyynum'
,'yyzkyynum','kftnum','kftxbknum','kftpacnum','kftsdkfnum' ,'sycsnum','sytssyjnum','synfcpscnum','syjddzmcnum','syscnum','sygwzxnum'
,'wgctnum','yljbnum','ylyxtnum','ylyjynum','ylydcgnum','ylyzhnum','ylktvnum','yldtnum','kctypypnum','kctkdjnum','kctmdnnum','kctbsknum'
,'kctyhdjnum','kctcctnum','kctjyjnum','kctmxnum','jycrjynum','jyyeynum','jyxxnum','jyzxnum','jygdyxnum','jyzyjsxynum','promotion_grade'
,'cvs_promotion_grade','weight_index_store','geneday_latest_active','geneday_latest_resident','geneday_latest_office'
                               ,'suday_latest_active','suday_latest_resident','suday_latest_office','00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp'
 ,'08_temp','09_temp' ,'10_temp','11_temp','12_temp'
,'13_temp','14_temp','15_temp','16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp','23_temp', 'isworkday','newyearday',
     'womenday','laborday','youthday','childrenday', 'partyday', 'armyday',
     'teacherday', 'nationalday','eveday', 'spring', 'lantern','qingming','dragonboat', 'valentineday', 'autumnday',
      'doubleninth', 'valentineday2', 'foolsday',
       'motherday', 'fatherday', 'thanksgiving', 'silentnight', 'xmas','halloween', 'halloween2', 'easter' ]]


# In[46]:


#数据归一化
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(continuousdata)
scaler.data_max_
scaler.transform(continuousdata)

continuousdatatrans=pd.DataFrame(scaler.transform(continuousdata),columns=[ 'store_days','lowest_temp','highest_temp'
                                                                          ,'geneday_active_popu'
	  ,'geneday_resident_popu'
	  ,'geneday_office_popu'
      ,'suday_active_popu'
	  ,'suday_resident_popu' 
	  ,'suday_office_popu'
      ,'holday_active_popu'
	  ,'holday_resident_popu' 
	  ,'holday_office_popu','maleval','femaleval','teenval','youthnval','middleval','midoldval','leoldval','oldval','studentval'
,'waiterval','empleyval','hospitval','teacherval','servantval','housewifeval','texterval','researchval','ruckval','courierval'
,'havechildval','nochildval','strongconsumeval' ,'lesstrongconsumeval','midconsumeval','lesmidconsumeval','lessconsumeval','zctshcnum'
,'zctzjcnum','zcthncnum','zctxbcnum','zctlzhnum','zctdfnum','zcthxjlnum','zctqzcgnum','zcttwcnum','zctczcnum' ,'zcthbcnum','zctdbcnum','zctygcnum'
,'zcthgdnum','zctzhjlnum','zctsccnum','zctgdcnum','zctjscnum','zctzsscgnum','zctbjcnum','zctahcnum','zctsdcnum','zctfjcnum','jtctqcznum'
 ,'jtgjznum','jtdtznum','jttccnum','jtjcnum','jthcznum','xxcycsnum','bgsqcyyqnum','bgsqswxzlnum','bgsqxqnum','yysjjdyynum','yyzhyynum'
,'yyzkyynum','kftnum','kftxbknum','kftpacnum','kftsdkfnum' ,'sycsnum','sytssyjnum','synfcpscnum','syjddzmcnum','syscnum','sygwzxnum'
,'wgctnum','yljbnum','ylyxtnum','ylyjynum','ylydcgnum','ylyzhnum','ylktvnum','yldtnum','kctypypnum','kctkdjnum','kctmdnnum','kctbsknum'
,'kctyhdjnum','kctcctnum','kctjyjnum','kctmxnum','jycrjynum','jyyeynum','jyxxnum','jyzxnum','jygdyxnum','jyzyjsxynum','promotion_grade'
,'cvs_promotion_grade','weight_index_store','geneday_latest_active','geneday_latest_resident' 
,'geneday_latest_office','suday_latest_active','suday_latest_resident','suday_latest_office','00_temp','01_temp','02_temp','03_temp','04_temp','05_temp','06_temp','07_temp'
 ,'08_temp','09_temp' ,'10_temp','11_temp','12_temp'
,'13_temp','14_temp','15_temp','16_temp','17_temp','18_temp','19_temp','20_temp','21_temp','22_temp','23_temp', 'isworkday','newyearday',
      'womenday','laborday','youthday','childrenday', 'partyday', 'armyday',
     'teacherday', 'nationalday','eveday', 'spring', 'lantern','qingming','dragonboat', 'valentineday', 'autumnday',
        'doubleninth', 'valentineday2', 'foolsday',
      'motherday', 'fatherday', 'thanksgiving', 'silentnight', 'xmas','halloween', 'halloween2', 'easter'])


# # 8.生成学习样本数据

# In[47]:


sampledata_pre=pd.concat([onhotencodedata1,onhotencodedata2,continuousdatatrans],axis=1, join='inner')
sampledata=pd.concat([sampledata_pre,mydata[['date','store_code','sales_amt']]],axis=1, join='inner')

sampleDeal = SampleDeal()

sampleDeal.saveTrainDataFrame(sampledata, "sales_predict", "xgboost")
