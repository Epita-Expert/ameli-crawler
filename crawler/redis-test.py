import sqlite3
import redis
from redis.commands.graph.edge import Edge
from redis.commands.graph.node import Node

def find_node(label, name) -> Node:
    # print(f'Find node with label {label} and name {name}')
    for item in redis_graph.nodes.items():
        if item[1].label == label and item[1].properties.get('name') == name:
            return item[1]

def find_edge(src_node, dest_node) -> Node:
    # print(f'Find node with src_node {src_node} and dest_node {dest_node}')
    for item in redis_graph.edges:
        if item.src_node == src_node and item.dest_node == dest_node:
            return item

def print_query():
    result = redis_graph.query("MATCH q = (:speciality {name: 'allergologue'})-[:in]->(:department {name:'01-ain'}) RETURN q")
    print(result)
    for record in result.result_set:
        path = record[0]
        print(path)

def main():
    cur.execute("select * from speciality")
    specialities = cur.fetchall()

    for speciality in specialities:
        speciality_node = Node(label='speciality', properties={'name': speciality[1]})
        redis_graph.add_node(speciality_node)
        # print(f'Node: {speciality_node}')

    cur.execute("select * from departement")
    departments = cur.fetchall()
    for department in departments:
        department_name = department[1]
        speciality_name = department[2]        

        speciality_node = find_node('speciality', speciality_name)
        department_node = find_node('department', department_name)

        if (department_node is None):
            department_node = Node(label='department', properties={'name': department_name})
            redis_graph.add_node(department_node)
            # print(f'Node: {department_node}')

        edge = find_edge(speciality_node, department_node)
        if (edge is None):
            edge = Edge(speciality_node, 'in', department_node)
            redis_graph.add_edge(edge)
            # print(f'Edge: {edge}')

    redis_graph.flush()
    
if __name__ == '__main__':
    base_url = "http://annuairesante.ameli.fr/"

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    r = redis.Redis(host='localhost', port=6379, db=0)
    redis_graph = r.graph('ameli')
    # redis_graph.delete()
    main()

    con.close()