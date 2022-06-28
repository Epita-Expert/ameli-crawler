from pydoc import doc
import sqlite3
import time
import re
from typing import Any, List
import random
import crawler
import uuid
from utils import dir, timer, get
import redis
from redisgraph import Node, Edge, Graph, Path

class Speciality:
    """Speciality Class"""
    def __init__(self, path, name):
        self.name: str = name
        self.path: str = path

    def toTupple(self):
        return (self.name, self.path)

class Department:
    """Department Class"""
    def __init__(self, path, name, speciality_path):
        self.path: str = path
        self.name: str = name
        self.speciality_path = speciality_path
    def toTupple(self):
        return (self.path, self.name, self.speciality_path)

class City:
    """City Class"""
    def __init__(self, path, name, department_path):
        self.path: str = path
        self.name: str = name
        self.department_path = department_path
    def toTupple(self):
        return (self.path, self.name, self.department_path)

class Doctor:
    """Doctor Class"""
    def __init__(self, path, name, department_path):
        self.path: str = path
        self.name: str = name
        self.department_path = department_path
        # self.department_path = department_path
    def toTupple(self):
        return (self.path, self.name, self.department_path)

def create_specialities():
    cur.execute("create table if not exists speciality (link, name)")

    cur.execute("select count(*) from speciality") 

    if (cur.fetchone()[0] > 50):
        print(f'Skipping... Specialities already exist')
        return

    html = get(f'{base_url}/trouver-un-professionnel-de-sante/')
    list_url_speciality = re.findall('<a href=\"(/trouver-un-professionnel-de-sante/(.*?))\">', html)[:-1]

    specialities = [Speciality(url_speciality[1], url_speciality[0]) for url_speciality in list_url_speciality]

    cur.executemany("insert into speciality values (?, ?)",[speciality.toTupple() for speciality in specialities])
    cur.execute("select count(*) from speciality")
    con.commit()
    print(f'Inserted {cur.fetchone()[0]} specialities in DB')

def get_departements_from(url_speciality: str, speciality: str):
    "Get department of speciality and return a list of department"
    # Open list of departements in a speciality
    print(f'{base_url}{url_speciality}')
    html = get(f'{base_url}{url_speciality}')
    print(f'{base_url}{url_speciality} Done')
    return [Department(f'{url_speciality}/{res}', res, speciality) for res in re.findall(f'<li class=\"seo-departement\"> <a href=\"{url_speciality}/(.*?)\">', html)]

def get_cities_from(url_departement: str):
    print(f'get_cities_from {base_url}{url_departement}')
    html = get(f'{base_url}{url_departement}')
    print(f'{base_url}{url_departement} Done')
    return [City(f'{url_departement}-{res}', res, f'{url_departement}') for res in re.findall(f'<a href=\"{url_departement}-(.*?)\">', html)]

def get_doctors_from(url_city: str):
    print(f'get_doctors_from {base_url}{url_city}')
    html = get(f'{base_url}{url_city}')
    print(f'{base_url}{url_city} Done')
    return [Doctor(f'/professionnels-de-sante/fiche-detaillee-{res}', res, url_city) for res in re.findall(f'<a href=\"/professionnels-de-sante/fiche-detaillee-(.*?)\">', html)]

def get_doctors_informations(url_doctor: str):
    print(f'{base_url}{url_doctor}')
    html = get(f'{base_url}{url_doctor}')
    names = re.search('<div class="nom_pictos"> <h1>(.*?)<\/h1>', html)
    full_name = names[1].replace("<strong>", "").replace("</strong>", "") if names else ''
    return full_name

def crawler(do_it, doctors: List[Doctor]):

    if (do_it):

        # Get speciality

        cur.execute("select * from speciality")
        specialities = cur.fetchall()
        random_speciality = random.choice(specialities)
        speciality = Speciality(random_speciality[0], random_speciality[1])
        time.sleep(1)
        ## Department
        # Get departments

        cur.execute("create table if not exists departement (link, name, speciality_link)")
        departments = get_departements_from(speciality.path, speciality.name)
        print(f'Found {len(departments)} departements')
        time.sleep(1)
        # Get random department

        department = random.choice(departments)
        print(department.path)
        cur.execute("insert into departement values (?,?,?)", department.toTupple())
        con.commit()
        print(f'Inserted {department.path} departement in DB')
        time.sleep(1)
        ## City
        # Get cities

        cur.execute("create table if not exists city (link, name, department_link)")
        cities = get_cities_from(department.path)
        print(f'Found {len(cities)} cities')
        time.sleep(1)        
        # Get random city

        city = random.choice(cities)
        cur.execute("insert into city values (?, ?, ?)", city.toTupple())
        con.commit()
        print(f'Inserted {city.path} city in DB')
        time.sleep(1)
        # Get doctors

        cur.execute("create table if not exists doctor (link, name, department_link)")
        doctors = get_doctors_from(city.path)
        print(f'Found {len(doctors)} doctors')

        time.sleep(1)    
    # Get Random doctors

    doctor = random.choice(doctors)

    # Get doctor information

    doctor_fullname = get_doctors_informations(doctor.path)
    cur.execute("insert into doctor values (?, ?, ?)", (doctor.path, doctor_fullname, doctor.department_path))
    con.commit()
    print(f'Inserted {cur.fetchone()} doctor in DB')


    # Continue
    if (random.randint(0,1) == 1):
        print('On continue !')
        crawler(do_it=False, doctors=doctors)
    else:
        print('On repart a zero !')
        crawler(do_it=True, doctors=[])


def main():
    start = time.time()
    create_specialities()
    crawler(do_it=True, doctors=[])
    timer(start)

if __name__ == '__main__':
    base_url = "http://annuairesante.ameli.fr"
    fast_testing = True
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    main()
    con.close()
