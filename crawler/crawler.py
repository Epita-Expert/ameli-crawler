import sqlite3
import os
import time
import re
import json
import builtins
# import psycopg2
import requests
import argparse
import crawler
from utils import dir, timer, get
import redis
from redisgraph import Node, Edge, Graph, Path

def create_specialities():
    cur.execute("create table if not exists speciality (name, link)")
    html = get(f'{base_url}trouver-un-professionnel-de-sante/')
    list_url_speciality = re.findall(
        '<a href=\"(/trouver-un-professionnel-de-sante/(.*?))\">', html)[:-1]
    print(list_url_speciality)

    if fast_testing:
        small_list = [list_url_speciality[0], list_url_speciality[1]]

    cur.executemany("insert into speciality values (?, ?)",
                    small_list)
    cur.execute("select count(*) from speciality")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} specialities in DB')


def get_departements_from(url_departement: str, speciality: str):
    # Open list of departements in a speciality
    print(f'{base_url}{url_departement}')
    html = get(f'{base_url}{url_departement}')
    # tools.progres_bar(count.value+1, len_speciality.value, suffix = 'Progress:', length = 40)
    print(f'{base_url}{url_departement} Done')
    return [(f'{url_departement}/{res}', f'{res}', speciality) for res in
            re.findall(f'<li class=\"seo-departement\"> <a href=\"{url_departement}/(.*?)\">', html)]


def create_departements():
    # cur.execute("drop table departement")
    cur.execute("create table if not exists departement (link, name, speciality)")
    cur.execute("select * from speciality")
    list_url_speciality = cur.fetchall()
    list_list_url_departement = list(
        get_departements_from(url_speciality[0], url_speciality[1]) for url_speciality in list_url_speciality)
    list_url_departement = [y for x in list_list_url_departement for y in x]
    print(f'Found {len(list_url_departement)} departements')
    cur.executemany("insert into departement values (?,?,?)",
                    list_url_departement)
    cur.execute("select count(*) from departement")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} departements link in DB')


def get_cities_from(url_departement: str):
    print(f'{base_url}{url_departement}')
    html = get(f'{base_url}{url_departement}')
    # tools.progres_bar(count.value+1, len_speciality.value, suffix = 'Progress:', length = 40)
    print(f'{base_url}{url_departement} Done')
    return [(f'{url_departement}-{res}', '') for res in
            re.findall(f'<a href=\"{url_departement}-(.*?)\">', html)]

    # try:
    #     [url_speciality, url_departement] = url_departement
    #     html = tools.get(f'{base_url}trouver-un-professionnel-de-sante/{url_speciality}/{url_departement}')
    #     count.value += 1
    #     tools.progres_bar(count.value+1, len_departement.value, suffix = 'Progress:', length = 40)
    #     return [(url_speciality, url_departement, res) for res in re.findall(f'<a href=\"/trouver-un-professionnel-de-sante/{url_speciality}/(.*?)\">',html)]
    # except Exception as identifier:
    #     print(f'Error while getting {base_url}trouver-un-professionnel-de-sante/{url_speciality}/{url_departement}')
    #     return []


def create_cities():
    cur.execute("create table if not exists city (link, name)")
    cur.execute("select * from departement")
    list_url_departement = cur.fetchall()
    if fast_testing:
        list_url_departement = list_url_departement[:10]
    list_list_url_city = list(get_cities_from(url_departement[0]) for url_departement in list_url_departement)
    list_url_city = [y for x in list_list_url_city for y in x]
    print(f'Found {len(list_url_city)} cities')
    print(list_url_city[0])
    cur.executemany("insert into city values (?,?)",
                    list_url_city)
    cur.execute("select count(*) from city")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} cities link in DB')

    #     # Practitioners
    #     list_list_url_practitioner = list(pool.imap_unordered(get_practitioners_from, [url_city for url_city in list_url_city]))
    #     list_url_practitioner = list_list_url_practitioner.join()
    #     len_practitioners.value = len(list_url_practitioner)
    #     print(f'Found {len(list_url_practitioner)} list of practitioner in {round(time.time()-start,2)} s                              ')

    #     with open(dir(__file__)+'/json/link-pract-ameli.fr.json', 'w') as f:
    #         dumps = json.dumps(list_url_practitioner, ensure_ascii=False)
    #         print(dumps, file=f)


def crawler():
    pass
    # get list of city from department
    # pick random city
    # get list of doctors
    # pick random doctors
    # scrap informations


def main():
    start = time.time()
    #create_specialities()
    #create_departements()
    create_cities()

    # crawler()

    timer(start)


#class newList(list):
#    def join(self):
#        if self:
#            return [y for x in self for y in x]
#        else:
#            return []


#__builtins__.list = newList

if __name__ == '__main__':
    base_url = "http://annuairesante.ameli.fr/"
    fast_testing = True
    con = sqlite3.connect("db.sqlite3")
    # con = psycopg2.connect("dbname=ameli_db user=root password=root")
    cur = con.cursor()

    main()
    con.close()
