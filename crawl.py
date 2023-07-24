
import requests
import pandas as pd
from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen


main='https://www.imdb.com/chart/top/?ref_=nv_mv_250'
page=requests.get(main)
soup=BeautifulSoup(page.content,'html.parser')
sites=[]

for i in soup.select('.titleColumn a'):
    sites.append('https://www.imdb.com'+i['href']+'?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=1a264172-ae11-42e4-8ef7-7fed1973bb8f&pf_rd_r=CGS1GV681J27JM6KJ5Y9&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1')

pd.DataFrame(sites).to_csv('film_links.csv',index=False)

links=pd.read_csv('film_links.csv')
movie_data=[]
genre_data=[]
person_data=[]
cast_data=[]
crew_data=[]

nnn = 0
try:
    for index in range(len(links)):
        movie_row={}
        genre_row = {}
        person_row={}
        cast_row={}
        crew_row={}

        print(nnn)
        nnn += 1

        site= links.loc[index][0]
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' ,"Accept-Language": "en-US,en;q=0.5"}
        page2 = requests.get(site,headers=hdr)
        # ## print(req.status_code)
        soup2 = BeautifulSoup(page2.content,'html.parser')

        ## # .selectorgadget_suggested
        # #storyline=soup.select('.ipc-html-content-inner-div')
        # #print(storyline)

        title=soup2.select('h1 span')[0].text
        # print(title)
        temp1=soup2.select('.kRUqXl')[0].find_all('li')
        year =temp1[0].select('a')[0].text
        # print(year)

        runtime=temp1[-1].text
        # print(runtime)
        minute=int(runtime.split('m')[0].split('h')[-1]) if 'm' in runtime else 0
        hour=int(runtime.split('h')[0]) if 'h' in runtime else 0
        runtime=hour*60+minute
        # print(runtime)

        parental_guide = 'Unrated'
        if temp1[1].select('a'):
            if temp1[1].select('a')[0].text:
                if temp1[1].select('a')[0].text!='Not Rated':
                    parental_guide = temp1[1].select('a')[0].text


        movie_id=site.split('title/tt')[1].split('/')[0]
        # print('movie_id:',movie_id)


        genre=[t.text for t in soup2.select('.ipc-chip-list--baseAlt')[0].find_all('a')]
        # print(genre)

        for a in soup2.select('.jBXsRT li div')[0].find_all('a'):
            director=[a.text,a['href']]
            person_row={'id':a['href'].split('nm')[1].split('/')[0],'name':a.text}
            person_data.append(person_row)
            crew_row={'movie_id':movie_id,'person_id':a['href'].split('nm')[1].split('/')[0],'role':'Director'}
            crew_data.append(crew_row)


        # print(director)

        for a in soup2.select('.jBXsRT li div')[1].find_all('a'):
            writer=[a.text,a['href']]
            person_row={'id':a['href'].split('nm')[1].split('/')[0],'name':a.text}
            person_data.append(person_row)
            crew_row={'movie_id':movie_id,'person_id':a['href'].split('nm')[1].split('/')[0],'role':'Writer'}
            crew_data.append(crew_row)


        # print(writer)

        for a in soup2.select('.jBXsRT li div')[2].find_all('a'):
            star=[a.text,a['href']]
            person_row={'id':a['href'].split('nm')[1].split('/')[0],'name':a.text}
            person_data.append(person_row)
            cast_row={'movie_id':movie_id,'person_id':a['href'].split('nm')[1].split('/')[0]}
            cast_data.append(cast_row)
        # print(star)


        gross_us_canada=None
        temp5=soup2.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-f9e7f53-0.ifXVtO > div > section > div > div.sc-414674b4-1.gWfYnM.ipc-page-grid__item.ipc-page-grid__item--span-2 > section > div > ul> li')
        for j in temp5 :
            if j.select('span'):
                if j.select('span')[0].text =='Gross US & Canada':
                    gross_us_canada=j.select('span')[1].text.replace('$', '').replace(',', '')
        # print(gross_us_canada)


        for g in genre:
            genre_row={'movie_id':movie_id,'genre':g}
            genre_data.append(genre_row)

        movie_row={'id':movie_id,'title':title,'year':year,'runtime':runtime,'parental_guide':parental_guide,'gross_us_canada':gross_us_canada}
        movie_data.append(movie_row)

except ConnectionError:
    pass
#     for index in range(nnn,len(links)):
#         movie_row={}
#         genre_row = {}
#         person_row={}
#         cast_row={}
#         crew_row={}
#
#         print(nnn)
#         nnn += 1
#
#         site= links.loc[index][0]
#         hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' ,"Accept-Language": "en-US,en;q=0.5"}
#         page2 = requests.get(site,headers=hdr)
#         # ## print(req.status_code)
#         soup2 = BeautifulSoup(page2.content,'html.parser')
#
#         ## # .selectorgadget_suggested
#         # #storyline=soup.select('.ipc-html-content-inner-div')
#         # #print(storyline)
#
#         title=soup2.select('h1 span')[0].text
#         # print(title)
#         temp1=soup2.select('.kRUqXl')[0].find_all('li')
#         year =temp1[0].select('a')[0].text
#         # print(year)
#
#         runtime=temp1[-1].text
#         # print(runtime)
#         minute=int(runtime.split('m')[0].split('h')[-1]) if 'm' in runtime else 0
#         hour=int(runtime.split('h')[0]) if 'h' in runtime else 0
#         runtime=hour*60+minute
#         # print(runtime)
#
#         parental_guide = 'Unrated'
#         if temp1[1].select('a'):
#             if temp1[1].select('a')[0].text:
#                 if temp1[1].select('a')[0].text!='Not Rated':
#                     parental_guide = temp1[1].select('a')[0].text
#
#
#         movie_id=site.split('title/tt')[1].split('/')[0]
#         # print('movie_id:',movie_id)
#
#
#         genre=[t.text for t in soup2.select('.ipc-chip-list--baseAlt')[0].find_all('a')]
#         # print(genre)
#
#         for a in soup2.select('.jBXsRT li div')[0].find_all('a'):
#             director=[a.text,a['href']]
#             person_row={'id':a['href'].split('nm')[1].split('/')[0],'name':a.text}
#             person_data.append(person_row)
#             crew_row={'movie_id':movie_id,'person_id':a['href'].split('nm')[1].split('/')[0],'role':'Director'}
#             crew_data.append(crew_row)
#
#
#         # print(director)
#
#         for a in soup2.select('.jBXsRT li div')[1].find_all('a'):
#             writer=[a.text,a['href']]
#             person_row={'id':a['href'].split('nm')[1].split('/')[0],'name':a.text}
#             person_data.append(person_row)
#             crew_row={'movie_id':movie_id,'person_id':a['href'].split('nm')[1].split('/')[0],'role':'Writer'}
#             crew_data.append(crew_row)
#
#
#         # print(writer)
#
#         for a in soup2.select('.jBXsRT li div')[2].find_all('a'):
#             star=[a.text,a['href']]
#             person_row={'id':a['href'].split('nm')[1].split('/')[0],'name':a.text}
#             person_data.append(person_row)
#             cast_row={'movie_id':movie_id,'person_id':a['href'].split('nm')[1].split('/')[0]}
#             cast_data.append(cast_row)
#         # print(star)
#
#
#         gross_us_canada=None
#         temp5=soup2.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-f9e7f53-0.ifXVtO > div > section > div > div.sc-414674b4-1.gWfYnM.ipc-page-grid__item.ipc-page-grid__item--span-2 > section > div > ul> li')
#         for j in temp5 :
#             if j.select('span'):
#                 if j.select('span')[0].text =='Gross US & Canada':
#                     gross_us_canada=j.select('span')[1].text.replace('$', '').replace(',', '')
#         # print(gross_us_canada)
#
#         for g in genre:
#             genre_row={'movie_id':movie_id,'genre':g}
#             genre_data.append(genre_row)
#
#         movie_row={'id':movie_id,'title':title,'year':year,'runtime':runtime,'parental_guide':parental_guide,'gross_us_canada':gross_us_canada}
#         movie_data.append(movie_row)
#
#




movie_df=pd.DataFrame(movie_data)
movie_df.to_csv('movie.csv',index=False)

genre_df=pd.DataFrame(genre_data)
genre_df.to_csv('genre.csv',index=False)

person_df=pd.DataFrame(person_data)
person_df.to_csv('person.csv',index=False)

cast_df=pd.DataFrame(cast_data)
cast_df.to_csv('cast.csv',index=False)

crew_df=pd.DataFrame(crew_data)
crew_df.to_csv('crew.csv',index=False)

