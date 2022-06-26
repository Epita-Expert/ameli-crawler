import sqlite3
import os
import time
import re
import json
import builtins
# import psycopg2
import requests
import argparse
import random
import crawler
import uuid
from utils import dir, timer, get
import redis
from redisgraph import Node, Edge, Graph, Path

def create_specialities():
    cur.execute("create table if not exists speciality (name, link, speID)")
    html = get(f'{base_url}trouver-un-professionnel-de-sante/')
    list_url_speciality = re.findall(
        '<a href=\"(/trouver-un-professionnel-de-sante/(.*?))\">', html)[:-1]

    print(list_url_speciality)

    if fast_testing:
        list_url_speciality = [list_url_speciality[0]]
        #list_url_speciality = [list_url_speciality[0], list_url_speciality[1]]
    list_url_speciality = [(url_speciality[0], url_speciality[1], str(uuid.uuid4())) for url_speciality in list_url_speciality]

    cur.executemany("insert into speciality values (?, ?, ?)",
                    list_url_speciality)
    cur.execute("select count(*) from speciality")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} specialities in DB')


def get_departements_from(url_departement: str, speciality: str, speID: str):
    # Open list of departements in a speciality
    print(f'{base_url}{url_departement}')
    html = get(f'{base_url}{url_departement}')
    print(f'{base_url}{url_departement} Done')
    return [(f'{url_departement}/{res}', f'{res}', speciality, speID, str(uuid.uuid4())) for res in
            re.findall(f'<li class=\"seo-departement\"> <a href=\"{url_departement}/(.*?)\">', html)]


def create_departements():
    cur.execute("create table if not exists departement (link, name, speciality, speID, depID)")
    cur.execute("select * from speciality")
    list_url_speciality = cur.fetchall()
    list_list_url_departement = list(
        get_departements_from(url_speciality[0], url_speciality[1], url_speciality[2]) for url_speciality in list_url_speciality)
    list_url_departement = [y for x in list_list_url_departement for y in x]
    print(f'Found {len(list_url_departement)} departements')
    cur.executemany("insert into departement values (?,?,?,?,?)",
                    list_url_departement)
    cur.execute("select count(*) from departement")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} departements link in DB')


def get_cities_from(url_departement: str):
    print(f'{base_url}{url_departement}')
    html = get(f'{base_url}{url_departement}')
    print(f'{base_url}{url_departement} Done')
    return [(f'{url_departement}-{res}', f'{res}') for res in
            re.findall(f'<a href=\"{url_departement}-(.*?)\">', html)]

def create_cities():
    cur.execute("create table if not exists city (link, name, depID, cityID)")
    cur.execute("select * from departement")
    list_url_departement = cur.fetchall()
    if fast_testing:
        list_url_departement = list_url_departement[:10]
    list_list_url_city = list(get_cities_from(url_departement[0]) for url_departement in list_url_departement)
    list_url_city = [y for x in list_list_url_city for y in x]
    list_url_city = [(url_city[0], url_city[1], url_city[2], url_city[4], str(uuid.uuid4())) for url_city in
                            list_url_city]
    print(f'Found {len(list_url_city)} cities')
    print(list_url_city[0])
    cur.executemany("insert into city values (?, ?, ?, ?)",
                    list_url_city)
    cur.execute("select count(*) from city")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} cities link in DB')

def get_doctors_from(url_city: str):
    print(f'{base_url}{url_city}')
    html = get(f'{base_url}{url_city}')
    print(f'{base_url}{url_city} Done')
    return [(f'/professionnels-de-sante/fiche-detaillee-{res}') for res in
            re.findall(f'<a href=\"/professionnels-de-sante/fiche-detaillee-(.*?)\">', html)]

def get_doctors_informations(url_doctor: str, city_id: str):
    cur.execute("create table if not exists doctors (name, cityID, docID)")
    print(f'{base_url}{url_doctor}')
    html = get(f'{base_url}{url_doctor}')
    names = re.search('<div class="nom_pictos"> <h1>(.*?)<\/h1>', html)
    full_name = names[1].replace("<strong>", "").replace("</strong>", "")
    cur.execute("insert into doctors values (?, ?, ?)", full_name, city_id, str(uuid.uuid4()))
    con.commit()

def crawler():
    create_specialities()
    #random_int = random.randint(0, 1)
    cur.execute("select * from speciality")
    list_url_speciality = cur.fetchall()
    #cur.execute("select * from departement")
    #list_url_departement = cur.fetchall()
    #cur.execute("select * from cities")
    #list_url_departement = cur.fetchall()
    while True:

        #get list of city from department
        list_of_cities = []
        # pick random city
        url_city = random.choice(list_of_cities)
        # get list of doctors
        list_url_doctors = get_doctors_from(url_city)
        # pick random doctors
        url_doctor = random.choice(list_url_doctors)
        # scrap informations
        get_doctors_informations(url_doctor, id_city)

def main():
    start = time.time()
    #create_specialities()
    create_departements()
    create_cities()
    #crawler()
    timer(start)

if __name__ == '__main__':
    base_url = "http://annuairesante.ameli.fr/"
    fast_testing = True
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    main()
    con.close()
