create table if not exists user( id integer primary key autoincrement, username text not null, password text not null, key blob default None,cookie text unique default None );
