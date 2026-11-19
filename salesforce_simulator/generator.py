import json, random, uuid
from datetime import datetime, timezone, timedelta
from .database import connect
OBJECTS={
 "account":"account_id text primary key,account_name text,industry text,billing_country text,annual_revenue real,system_modstamp text,is_deleted integer default 0",
 "contact":"contact_id text primary key,account_id text,first_name text,last_name text,email text,title text,system_modstamp text,is_deleted integer default 0",
 "opportunity":"opportunity_id text primary key,account_id text,owner_id text,opportunity_name text,stage_name text,amount real,probability real,close_date text,is_closed integer,is_won integer,system_modstamp text,is_deleted integer default 0",
 "opportunity_line_item":"opportunity_line_item_id text primary key,opportunity_id text,product_name text,quantity real,unit_price real,total_price real,system_modstamp text,is_deleted integer default 0"}
def now(): return datetime.now(timezone.utc).isoformat()
def init(seed=True):
 with connect() as c:
  for name,ddl in OBJECTS.items(): c.execute(f"create table if not exists {name}({ddl})")
  c.execute("create table if not exists cdc_event(replay_id integer primary key autoincrement,object_name text,record_id text,change_type text,event_time text,system_modstamp text,payload text)")
 if seed: seed_data()
def emit(c,obj,rid,change):
 row=dict(c.execute(f"select * from {obj} where {obj}_id=?",(rid,)).fetchone()); sm=row['system_modstamp']; c.execute("insert into cdc_event(object_name,record_id,change_type,event_time,system_modstamp,payload) values(?,?,?,?,?,?)",(obj,rid,change,now(),sm,json.dumps(row)))
def seed_data(accounts=25):
 init(False)
 with connect() as c:
  if c.execute('select count(*) from account').fetchone()[0]: return
  for i in range(1,accounts+1):
   aid=f'A{i:05d}'; c.execute('insert into account values(?,?,?,?,?,?,0)',(aid,f'Account {i}',random.choice(['Technology','Healthcare','Retail','Manufacturing']),'Australia',float(random.randint(250000,5000000)),now())); emit(c,'account',aid,'INSERT')
   cid=f'C{i:05d}'; c.execute('insert into contact values(?,?,?,?,?,?,?,0)',(cid,aid,'Contact',str(i),f'contact{i}@example.test','Manager',now())); emit(c,'contact',cid,'INSERT')
   oid=f'O{i:05d}'; amount=float(random.randint(10000,250000)); prob=float(random.choice([10,25,50,75,90])); c.execute('insert into opportunity values(?,?,?,?,?,?,?,?,?,?,?,0)',(oid,aid,'U001',f'Deal {i}',random.choice(['Prospecting','Proposal','Negotiation']),amount,prob,(datetime.now(timezone.utc).date()+timedelta(days=random.randint(10,120))).isoformat(),0,0,now())); emit(c,'opportunity',oid,'INSERT')
   lid=f'L{i:05d}'; qty=random.randint(1,5); price=float(random.randint(1000,20000)); c.execute('insert into opportunity_line_item values(?,?,?,?,?,?,?,0)',(lid,oid,'Product A',qty,price,qty*price,now())); emit(c,'opportunity_line_item',lid,'INSERT')
def mutate(updates=8,inserts=3,deletes=2):
 init()
 with connect() as c:
  ids=[r[0] for r in c.execute('select opportunity_id from opportunity where is_deleted=0')]
  for oid in random.sample(ids,min(updates,len(ids))): c.execute('update opportunity set amount=amount*1.05,system_modstamp=? where opportunity_id=?',(now(),oid)); emit(c,'opportunity',oid,'UPDATE')
  for _ in range(inserts):
   aid=c.execute('select account_id from account order by random() limit 1').fetchone()[0]; oid='O'+uuid.uuid4().hex[:10].upper(); amount=float(random.randint(10000,250000)); c.execute('insert into opportunity values(?,?,?,?,?,?,?,?,?,?,?,0)',(oid,aid,'U001','Generated Deal','Prospecting',amount,10.0,(datetime.now(timezone.utc).date()+timedelta(days=60)).isoformat(),0,0,now())); emit(c,'opportunity',oid,'INSERT')
  live=[r[0] for r in c.execute('select contact_id from contact where is_deleted=0')]
  for cid in random.sample(live,min(deletes,len(live))): c.execute('update contact set is_deleted=1,system_modstamp=? where contact_id=?',(now(),cid)); emit(c,'contact',cid,'DELETE')
