/*to find the county fips look in public.us_county and filter*/
drop table if exists "public".jasper_ssurgo_mupolygon_2019;
create table "public".jasper_ssurgo_mupolygon_2019 as
select *
from ssurgo_2019.mupolygon
WHERE areasymbol = 'IA099';