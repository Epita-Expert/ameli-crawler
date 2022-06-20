import sqlite3
import os
import time
import re
import json
import builtins
import requests
import argparse
from utils import dir, timer, get


def create_specialities():
    cur.execute("create table if not exists speciality (name, link)")
    html = get(f'{base_url}trouver-un-professionnel-de-sante/')
    list_url_speciality = re.findall(
        '<a href=\"(/trouver-un-professionnel-de-sante/(.*?))\">', html)[:-1]
    # print(list_url_speciality)
    cur.executemany("insert into speciality values (?, ?)",
                    list_url_speciality)
    cur.execute("select count(*) from speciality")
    print(f'Inserted {cur.fetchone()[0]} specialities in DB')


def get_departements_from(url_department: str):
    # Open list of departments in a speciality
    print(f'{base_url}{url_department}')
    html = get(f'{base_url}{url_department}')
    # tools.progres_bar(count.value+1, len_speciality.value, suffix = 'Progress:', length = 40)
    print(f'{base_url}{url_department} Done')
    return [(f'{url_department}/{res}', '') for res in re.findall(f'<li class=\"seo-departement\"> <a href=\"{url_department}/(.*?)\">', html)]


def create_departements():
    cur.execute("create table if not exists departement (link, name)")
    cur.execute("select name from speciality")
    list_url_speciality = cur.fetchall()
    list_list_url_department = list(get_departements_from(
        url_speciality[0]) for url_speciality in list_url_speciality)
    list_url_department = list_list_url_department.join()
    print(f'Found {len(list_url_department)} departments')
    print(list_url_department[0])
    cur.executemany("insert into departement values (?,?)",
                    list_url_department)
    cur.execute("select count(*) from speciality")
    print(f'Inserted {cur.fetchone()[0]} departement link in DB')


def main():
    # And this is the named style:
    # cur.execute("select * from lang where first_appeared=:year",
    #             {"year": 1972})
    # print(cur.fetchall())
    start = time.time()
    create_specialities()
    create_departements()
    #     # Cities
    #     list_list_url_city = list(pool.imap_unordered(get_cities_from, [url_department for url_department in list_url_department]))
    #     list_url_city = list_list_url_city.join()
    #     len_city.value = len(list_url_city)
    #     count.value = 0
    #     print(f'Found {len(list_url_city)} cities in {round(time.time()-start,2)} s                              ')

    #     # Practitioners
    #     list_list_url_practitioner = list(pool.imap_unordered(get_practitioners_from, [url_city for url_city in list_url_city]))
    #     list_url_practitioner = list_list_url_practitioner.join()
    #     len_practitioners.value = len(list_url_practitioner)
    #     print(f'Found {len(list_url_practitioner)} list of practitioner in {round(time.time()-start,2)} s                              ')

    #     with open(dir(__file__)+'/json/link-pract-ameli.fr.json', 'w') as f:
    #         dumps = json.dumps(list_url_practitioner, ensure_ascii=False)
    #         print(dumps, file=f)
    timer(start)

class newList(list):
    def join(self):
        if self:
            return [y for x in self for y in x]
        else:
            return []
__builtins__.list = newList

if __name__ == '__main__':
    base_url = "http://annuairesante.ameli.fr/"
    
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    main()

    con.close()
