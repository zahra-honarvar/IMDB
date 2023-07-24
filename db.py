from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import text
import pandas as pd


url_object = URL.create(
    "mysql+mysqlconnector",
    username="zh",
    password="1234",
    host="localhost"
)
engine = create_engine(url_object)


with engine.connect() as conn:
   conn.execute(text("drop database if exists cinama;"))
   conn.execute(text("create database cinama;"))




with engine.connect() as conn:
   conn.execute(text('use cinama;'))

   conn.execute(text("drop table if exists movie;"))
   query='''CREATE TABLE movie (
   id varchar(8) PRIMARY KEY,
   title VARCHAR(128) NOT NULL,
   year int NOT NULL,
   runtime int NOT NULL,
   parental_guide VARCHAR(8) NOT NULL,
   gross_us_canada float);'''
   conn.execute(text(query))

   conn.execute(text("drop table if exists person;"))
   query='''create table person(
   id varchar(8) PRIMARY KEY,
   name VARCHAR(32) NOT NULL);'''
   conn.execute(text(query))

   conn.execute(text("drop table if exists caast;"))
   query =f'''create table caast(
   id int AUTO_INCREMENT PRIMARY KEY,
   movie_id varchar(8) not null ,
   person_id varchar(8) not null ,
   FOREIGN KEY (person_id) REFERENCES person(id),
   FOREIGN KEY (movie_id) REFERENCES movie(id));'''
   conn.execute(text(query))

   conn.execute(text("drop table if exists crew;"))
   query='''create table crew(
   id int AUTO_INCREMENT PRIMARY KEY,
   movie_id varchar(8) not null ,
   person_id varchar(8) not null ,
   role varchar(8) not null ,
   FOREIGN KEY (person_id) REFERENCES person(id),
   FOREIGN KEY (movie_id) REFERENCES movie(id));'''
   conn.execute(text(query))

   conn.execute(text("drop table if exists genre_movie;"))
   query='''create table genre_movie(
   id int AUTO_INCREMENT PRIMARY KEY,
   movie_id varchar(8) not null ,
   genre varchar(16)not null);'''
   conn.execute(text(query))
   conn.commit()




MovieData=pd.read_csv('movie.csv')

MovieData['gross_us_canada'] = MovieData['gross_us_canada'].fillna(value=0)
MovieData['id']=MovieData['id'].astype('str')

with engine.connect() as conn:
   conn.execute(text('use cinama;'))
   for i in range(len(MovieData)):
      title = MovieData.loc[i, 'title']
      id =MovieData.loc[i, 'id']
      year=MovieData.loc[i, 'year']
      runtime=MovieData.loc[i, 'runtime']
      parental_guide=MovieData.loc[i, 'parental_guide']
      gross_us_canada=MovieData.loc[i, 'gross_us_canada']
      title=title.replace("'","")
      query = f"insert into movie values ('{id}','{title}',{year},{runtime},'{parental_guide}',{gross_us_canada});"
      conn.execute(text(query))
   conn.commit()






PersonData=pd.read_csv('person.csv')
PersonData['id']=PersonData['id'].astype('str')

PersonData=PersonData.drop_duplicates()
PersonData.reset_index(inplace=True)


with engine.connect() as conn:
   conn.execute(text('use cinama;'))
   for i in range(len(PersonData)):
      name = PersonData.loc[i, 'name']
      id = PersonData.loc[i, 'id']
      name=name.replace("'","")
      query = f"insert into person values ('{id}','{name}');"
      conn.execute(text(query))
   conn.commit()





GenreData=pd.read_csv('genre.csv')
GenreData['movie_id']=GenreData['movie_id'].astype('str')

with engine.connect() as conn:
   conn.execute(text('use cinama;'))
   for i in range(len(GenreData)):
      genre = GenreData.loc[i, 'genre']
      movie_id = GenreData.loc[i, 'movie_id']
      query = f"insert into genre_movie(movie_id,genre) values ('{movie_id}','{genre}');"
      conn.execute(text(query))
   conn.commit()



CastData=pd.read_csv('cast.csv')
CastData['movie_id']=CastData['movie_id'].astype('str')
CastData['person_id']=CastData['person_id'].astype('str')

with engine.connect() as conn:
   conn.execute(text('use cinama;'))
   for i in range(len(CastData)):
      movie_id = CastData.loc[i, 'movie_id']
      person_id = CastData.loc[i, 'person_id']
      query = f"insert into caast(movie_id,person_id) values ('{movie_id}','{person_id}');"
      conn.execute(text(query))
   conn.commit()



CrewData=pd.read_csv('crew.csv')
CrewData['movie_id']=CrewData['movie_id'].astype('str')
CrewData['person_id']=CrewData['person_id'].astype('str')

with engine.connect() as conn:
   conn.execute(text('use cinama;'))
   for i in range(len(CrewData)):
      movie_id = CrewData.loc[i, 'movie_id']
      person_id = CrewData.loc[i, 'person_id']
      role=CrewData.loc[i, 'role']
      query = f"insert into crew(movie_id,person_id,role) values ('{movie_id}','{person_id}','{role}');"
      conn.execute(text(query))
   conn.commit()





