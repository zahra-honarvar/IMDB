import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import text
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

st.set_page_config(
    page_title='cinama',
    page_icon="🧊"
    #
)

url_object = URL.create(
    "mysql+mysqlconnector",
    username="zh",
    password="1234",
    host="localhost",
    database = "cinama"
)
engine = create_engine(url_object)

st.title("Filter tables")
st.header('part 1: please enter your desired year range to see list of movies.')
with engine.connect() as conn:
    conn.execute(text('use cinama'))
    y1=conn.execute(text('select min(year) from movie;'))
    y2=conn.execute(text('select max(year) from movie;'))
    s=y1.all()[0][0]
    f=y2.all()[0][0]
    syear = st.text_input('start year as number:',s)
    eyear = st.text_input('final year as number:',f)

@st.cache_data
def read_data(syear,eyear) :
    df = pd.DataFrame(columns=['id', 'title', 'year', 'runtime', 'parental_guide', 'gross_us_canada'])
    with engine.connect()as conn:
        conn.execute(text('use cinama'))
        r=conn.execute(text("select * from movie"))
        index=-1
        for i in r.all():
            index+=1
            df.loc[index]=i
    return df[(syear<=df['year'].astype('str')) & (df['year'].astype('str')<=eyear)]
st.dataframe(read_data(syear,eyear))


st.header('part 2: please select your desired movie runtime range.')
with engine.connect() as conn:
    conn.execute(text('use cinama'))
    rt1=conn.execute(text('select min(runtime) from movie;'))
    rt2=conn.execute(text('select max(runtime) from movie;'))
    s=rt1.all()[0][0]
    f=rt2.all()[0][0]
    values = st.slider("Select a range",s,f,(100,120),1)
    st.write(f"You selected the range: {values[0]} to {values[1]}")

@st.cache_data
def read_data2(s,f) :
    df = pd.DataFrame(columns=['id', 'title', 'year', 'runtime', 'parental_guide', 'gross_us_canada'])
    with engine.connect()as conn:
        conn.execute(text('use cinama'))
        r=conn.execute(text("select * from movie"))
        index=-1
        for i in r.all():
            index+=1
            df.loc[index]=i
    return df[(s<=df['runtime']) & (df['runtime']<=f)]
st.dataframe(read_data2(values[0],values[1]))




st.header('part3: please select actor(s).')
with engine.connect() as conn:
    conn.execute(text('use cinama'))
    data=conn.execute(text("select distinct person.name from movie join caast on movie.id=caast.movie_id join person on person.id=caast.person_id order by person.name;"))
    r=[]
    for i in data.all():
        r.append(i[0])
    options = st.multiselect(
        'pick actor(s)',
        [i for i in r]
        # 'Anthony Hopkins'
    )
    # st.write('You selected:', options)


@st.cache_data
def read_data3(options):
    with engine.connect() as conn:
        df=pd.DataFrame(columns=['id', 'title', 'year', 'runtime', 'parental_guide', 'gross_us_canada'])
        conn.execute(text('use cinama'))
        index = -1
        for i in options:
            r=conn.execute(text(f"select movie.* from movie join caast on movie.id=caast.movie_id join person on person.id=caast.person_id where person.name='{i}' order by person.name;"))
            for j in r.all():
                index += 1
                df.loc[index] = j
    df=df.drop_duplicates()
    return df

# read_data3(options)
st.dataframe(read_data3(options))



st.header('part 4: please select desired movie genre.')
with engine.connect() as conn:
    conn.execute(text('use cinama'))
    resault=conn.execute(text("select distinct genre from genre_movie;"))
    genres=[]
    for i in resault.all():
        genres.append(i[0])
    option = st.selectbox('select one:',genres)

@st.cache_data
def read_data4(option):
    with engine.connect() as conn:
        mov=conn.execute(text(f"select movie.* from movie join genre_movie on movie.id=genre_movie.movie_id where genre_movie.genre='{option}';"))
        df = pd.DataFrame(columns=['id', 'title', 'year', 'runtime', 'parental_guide', 'gross_us_canada'])
        index=0
        for j in mov.all():
            df.loc[index]=j
            index+=1
    return df
st.dataframe(read_data4(option))





st.title("Static charts")
with engine.connect() as conn:
    st.header("part 1: 10 of the bestselling movies.")
    mn = conn.execute(text("select title,gross_us_canada from movie order by gross_us_canada desc limit 10"))
    data = {}
    for i in mn.all():
        data[i[0]] = i[1]
    st.bar_chart(data)


    st.header('part 2:5 of the most prolific actors.')
    actor = conn.execute(text("select person.name from person join caast on caast.person_id=person.id join movie on movie.id=caast.movie_id group by person.name order by count(*) desc limit 5;"))
    movie=conn.execute(text("select title from movie"))
    actorN=[]
    movieN=[]
    for i in actor.all():
        actorN.append(i[0])
    for i in movie.all():
        movieN.append(i[0])
    temp = {}
    for i in actorN:
        temp[i]=[]

    for j in actorN:
        for i in movieN:
            q=conn.execute(text(f"select * from person join caast on caast.person_id=person.id join movie on movie.id=caast.movie_id where person.name='{j}' and movie.title='{i}';"))
            if q.all():x=1
            else:x=0
            temp[j].append(x)
    df=pd.DataFrame(temp,index=movieN)
    df.index.name='movie name'
    st.bar_chart(df)




    st.header("part 3: genres")
    genres = conn.execute(text("select genre,count(*) from genre_movie group by genre"))
    values = []
    names = []
    all = 0
    for i in genres:
        values.append(i[1])
        names.append(i[0])
        all += i[1]

    value_index1 = -1

    @st.cache_data
    def my_autopct(x):
        global value_index1
        value_index1 += 1
        return values[value_index1]

    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.pie(values, labels=names, autopct=my_autopct, startangle=90, counterclock=False,
           pctdistance=0.8, labeldistance=1.1, textprops={'fontsize': 11});
    st.pyplot(fig)





    st.header("part 4: parental guides")
    parental_guide = conn.execute(text("select parental_guide,count(*) from movie group by parental_guide"))
    values = []
    names = []
    all = 0
    for i in parental_guide:
        values.append(i[1])
        names.append(i[0])
        all += i[1]

    value_index = -1

    @st.cache_data
    def my_autopct(x):
        global value_index
        value_index += 1
        return values[value_index]

    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.pie(values, labels=names, autopct=my_autopct, startangle=90, counterclock=False,
           pctdistance=0.8, labeldistance=1.1, textprops={'fontsize': 11});
    st.pyplot(fig)






    st.header("part 5: the number of occurrences of each parental_guide in each genre.")
    data=conn.execute(text("select movie.parental_guide,genre_movie.genre from movie join genre_movie on genre_movie.movie_id=movie.id group by movie.parental_guide,genre_movie.genre "))
    pg=[]
    gm=[]
    for i in data.all():
        pg.append(i[0])
        gm.append(i[1])
    pg=list(set(pg))
    gm =list(set(gm))

    temp = {}
    for i in pg:
        temp[i] = []
    for i in pg:
        for j in gm:
            number = conn.execute(text(f"select count(*) from movie join genre_movie on genre_movie.movie_id=movie.id where genre_movie.genre='{j}' and movie.parental_guide='{i}'"))
            temp[i].append(number.all()[0][0])

    df = pd.DataFrame(temp,index=gm)
    st.bar_chart(df)

    conn.close()






st.title('Interactive charts')
st.header('please select desired movie genre.')
with engine.connect() as conn:
    conn.execute(text('use cinama'))
    data = conn.execute(text("select distinct genre from genre_movie;"))
    genres = []
    for i in data.all():
        genres.append(i[0])
    genre = st.selectbox('select one:', genres,key="my_unique_key")


    st.header(f"10 of the bestselling movies in the {genre} genre: ")
    mn = conn.execute(text(f"select movie.title,movie.gross_us_canada from movie join genre_movie on movie.id=genre_movie.movie_id where genre_movie.genre='{genre}' order by gross_us_canada desc limit 10"))
    data = {}
    for i in mn.all():
        data[i[0]] = i[1]
    st.bar_chart(data)
    conn.close()



st.title("Additions ")
st.header("part 2: apply filter to see similar movies.")
with engine.connect() as conn:
    conn.execute(text('use cinama'))
    movie_names=conn.execute(text("select title from movie;"))
    movie_names=[i[0] for i in movie_names]
    filters=['year','genre','parental_guide','actor','director','writer']
    col1, col2 = st.columns(2)
    option1=col1.selectbox('select a movie:',movie_names, key="my_unique_key2")
    option2=col2.selectbox('select filters:', filters,key="my_unique_key3")


    if option2=='year':
        filter = conn.execute(text(f"select year from movie where title='{option1}'"))
        ideal=conn.execute(text(f"select title,year from movie where year='{filter.all()[0][0]}'"))
        st.dataframe(ideal)

    elif option2=='genre':
        ideal=[]
        filter = conn.execute(text(f"select genre_movie.genre from movie join genre_movie on genre_movie.movie_id=movie.id where title='{option1}'"))
        for j in filter.all():
            gs=conn.execute(text(f"select distinct movie.title,genre_movie.genre from movie join genre_movie on genre_movie.movie_id=movie.id where genre_movie.genre='{j[0]}'"))
            for k in gs.all():
                ideal.append(k)
        st.dataframe(ideal)

    elif option2=='parental_guide':
        filter = conn.execute(text(f"select parental_guide from movie where title='{option1}'"))
        ideal=conn.execute(text(f"select title,parental_guide from movie where parental_guide='{filter.all()[0][0]}'"))
        st.dataframe(ideal)

    elif option2=='actor':
        ideal = []
        filter = conn.execute(text(f"select person.name from movie join caast on caast.movie_id=movie.id join person on person.id=caast.person_id where title='{option1}'"))
        for j in filter.all():
            gs = conn.execute(text(f"select distinct movie.title,person.name from movie join caast on caast.movie_id=movie.id join person on person.id=caast.person_id where person.name='{j[0]}'"))
            for k in gs.all():
                ideal.append(k)
        st.dataframe(ideal)

    elif option2=='writer':
        ideal = []
        filter = conn.execute(text(f"select person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where title='{option1}' and crew.role='writer'"))
        for j in filter.all():
            gs = conn.execute(text(f"select distinct movie.title,person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where person.name='{j[0]}'and crew.role='writer'"))
            for k in gs.all():
                ideal.append(k)
        st.dataframe(ideal)

    elif option2=='director':
        ideal = []
        filter = conn.execute(text(f"select person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where title='{option1}' and crew.role='director'"))
        for j in filter.all():
            gs = conn.execute(text(f"select distinct movie.title,person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where person.name='{j[0]}'and crew.role='director'"))
            for k in gs.all():
                ideal.append(k)
        st.dataframe(ideal)





    st.header("Select a movie to see actors,writers,directors of it.")
    st.write("")
    movies = conn.execute(text("select title from movie;"))
    movies=[i[0] for i in movies]
    option=st.selectbox('select a movie:',movies)

    actor=conn.execute(text(f"select person.name from movie join caast on caast.movie_id=movie.id join person on person.id=caast.person_id where title='{option}'"))

    writers = conn.execute(text(f"select person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where title='{option}'and role='writer'"))

    directors = conn.execute(text(f"select person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where title='{option}'and role='director'"))

    col1, col2,col3 = st.columns(3)
    col1.write('actors:')
    col1.dataframe(actor)

    col2.write('writers:')
    col2.dataframe(writers)

    col3.write('directors:')
    col3.dataframe(directors)

    conn.close()


with engine.connect() as conn:
    conn.execute(text('use cinama'))
    st.header("how much of each genre has been sold?.")
    data=conn.execute(text("select genre_movie.genre ,sum(movie.gross_us_canada) from movie join genre_movie on genre_movie.movie_id=movie.id group by genre_movie.genre "))
    values = {}
    for i in data.all():
        values[i[0]] = i[1]
    st.bar_chart(values)


    movie_id=conn.execute(text("select title from movie"))
    movie_name=[i[0] for i in movie_id.all()]
    list_movies=[]

    for i in movie_name:
        list_writer=conn.execute(text(f"select person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where movie.title='{i}'and role='writer'"))
        list_dir=conn.execute(text(f"select person.name from movie join crew on crew.movie_id=movie.id join person on person.id=crew.person_id where movie.title='{i}'and role='director'"))

        list_dir={i[0] for i in list_dir}
        list_writer = {i[0] for i in list_writer}

        if list_writer.intersection(list_dir):
            list_movies.append(i)
    st.header("movies with the same director(s) and writer(s).")
    st.dataframe(list_movies)



