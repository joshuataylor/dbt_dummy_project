-- create database dummyproject;

create extension if not exists "uuid-ossp";

drop table if exists dummyproject.public.customers;
create table dummyproject.public.customers as (
  with data as (
    select 
      uuid_generate_v4() as id,
      md5(random()::text) || '@example.com' as email,
      md5(random()::text) || ' ' || md5(random()::text) as full_name,
      timestamp 'now' - (random() * 200000) * interval '1 second' as created_at
    from generate_series(1, 1000) n
  )
  select data.*, created_at as updated_at from data
);

drop table if exists dummyproject.public.products;
create table dummyproject.public.products as (
  with data as (
    select 
      uuid_generate_v4() as id,
      left(md5(random()::text), 50) as title,
      (random() > 0.5) as active,
      timestamp 'now' - (random() * 200000) * interval '1 second' as created_at
    from generate_series(1, 1000) n
  )
  select data.*, created_at as updated_at from data
);

drop table if exists dummyproject.public.orders;
create table dummyproject.public.orders as (
  with data as (
    select 
      uuid_generate_v4() as id,
      case
        when random() > 0.5 then 'new'
        when random() > 0.5 then 'processing'
        when random() > 0.5 then 'shipped'
      else 'delivered'
      end as order_state,
      timestamp 'now' - (random() * 200000) * interval '1 second' as created_at,
      left(md5(random()::text), 100) as customer_comment,
      left(md5(random()::text), 100) as admin_comment,
      (select id from customers order by random() limit 1) as customer_id
    from generate_series(1, 1000) n
  )
  select data.*, created_at as updated_at from data
);

drop table if exists dummyproject.public.line_items;
create table dummyproject.public.line_items as (
  with data as (
    select 
      uuid_generate_v4() as id,
      timestamp 'now' - (random() * 200000) * interval '1 second' as created_at,
      (select id from products order by random() limit 1) as product_id,
      (floor(random() * 10) + 1)::int as quantity,
      (floor(random() * 100) + 1)::int as price,
      (select id from orders order by random() limit 1) as order_id
    from generate_series(1, 1000) n
  )
  select data.*, created_at as updated_at from data
);