#!/usr/bin/python
import requests
import time
import os


def get_json_response(keyword):
    url=f"https://api.adjaranet.com/api/v1/search-advanced?movie_filters%5Bwith_actors%5D=3&movie_filters%5Bwith_directors%5D=1&movie_filters%5Bkeyword=&movie_filters%5Byear_range%5D=1900%2C2019&movie_filters%5Binit%5D=true&filters%5Btype%5D=movie&keywords={keyword}&page=1&per_page=15&source=adjaranet"
    try:
        json_data=requests.get(url).json()["data"]
    except:
        print("კავშირის პრობლემა...")
    return json_data

def search(json_object):
    film_id = 1
    for film in json_object:
        try:
            director = film['directors']['data'][0]['originalName']
        except Exception as e:
            director = "არ მოიძებნა"
        print(
            f"{film_id}) {film['primaryName']} - {film['secondaryName']} - {director} - {film['year']} - {film['rating']['imdb']['score']} ")
        film_id += 1


def choose_film(json_object,film_id):
    film_info = json_object[film_id]
    id=film_info['id']
    film_url=f"https://api.adjaranet.com/api/v1/movies/{id}/season-files/0?source=adjaranet"
    print(film_url)
    try:
        film_links = requests.get(film_url).json()["data"]


    except Exception as e:
        print("ფილმი არ არის ხელმისაწვდომი")

    checker=False
    try:
        checker=film_links[1]
    except:
        pass

    if checker:
        season=int(input("აირჩიეთ სეზონი: "))
        film_url=f"https://api.adjaranet.com/api/v1/movies/{id}/season-files/{season}?source=adjaranet"
        try:
            film_links = requests.get(film_url).json()["data"]

            


        except Exception as e:
            print("სეზონი არ არის ხელმისაწვდომი")


        for film in  film_links:
            print (str(film['episode'])+") "+film['title'])

        episode=int(input("შეიყვანეთ ეპიზოდის ნომერი: "))-1

        languages=film_links[episode]["files"]
        

    else:
        languages=film_links[0]['files']  
       


      
    lang_id=1
    print("ფილმი ხელმისაწვდომია შემდეგ ენებზე: ")
    for language in languages:
        if language['lang'] == "GEO":
            print(f"{lang_id}) ქართული")
        elif language['lang'] == "RUS":
            print(f"{lang_id}) რუსული")
        elif language['lang'] == "ENG":
            print(f"{lang_id}) ინგლისური")
        lang_id+=1

    language_id=int(input("აირჩიეთ ენა : ")) - 1

    film_files=languages[language_id]['files']
    final_link=""
    for quality in film_files:
        if quality['quality'] == "HIGH":
            final_link=quality['src']

        elif quality['quality'] == "MEDIUM" and final_link == "":
            final_link = quality['src']
    return final_link




def main():
    film_name=str(input("ფილმის სახელი : "))
    films_json_object = get_json_response(film_name)
    search(films_json_object)
    film_id = int(input("აირჩიეთ ფილმის ნომერი : "))-1
    final_link=choose_film(films_json_object,film_id)
    print("ფილმი იტვირთება შესაძლო მაღალ ხარისხში...")

    os.system(f"mpv {final_link} &")
    print("Loading...")
    



main()