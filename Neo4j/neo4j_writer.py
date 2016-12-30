import configparser
from neo4j.v1 import GraphDatabase, basic_auth

class Neo4jWriter():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        user_name = config.get('neo4j credentials', 'user_name')
        password = config.get('neo4j credentials', 'password')
        bolt_host = config.get('neo4j credentials', 'bolt_host')

        self.driver = GraphDatabase.driver(bolt_host,
                                           auth=basic_auth(user_name, password))

    def write_person(self, Person_Node):
        Person_Node.full_name = Person_Node.full_name.replace("'", "")
        Person_Node.full_name = Person_Node.full_name.strip()
        print('Creating Person Node:' + str(Person_Node.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                props = Person_Node.__dict__
                props = ', '.join("{!s}: {!r}".format(key, val) for (key, val) in props.items())
                query = 'MERGE (a:Person {' + props + "})"
                write_tx.run(query)
                write_tx.success = True

    def write_patent(self, Patent_Node):
        print('Creating Patent Node:' + str(Patent_Node.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                props = Patent_Node.__dict__
                props = ', '.join("{!s}: {!r}".format(key, val) for (key, val) in props.items())
                query = 'MERGE (a:Patent {' + props + "})"
                write_tx.run(query)
                write_tx.success = True

    def write_company(self, Company_Node):
        Company_Node.full_name = Company_Node.full_name.strip()
        print('Creating Company Node:' + str(Company_Node.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                props = Company_Node.__dict__
                props = ', '.join("{!s}: {!r}".format(key, val) for (key, val) in props.items())
                query = 'MERGE (a:Company {' + props + "})"
                write_tx.run(query)
                write_tx.success = True

    def write_person_to_patent(self, Person_Node, Patent_Node):
        print('Creating Invention Relationship')
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                query = "MATCH(a:Person {full_name: \'" + str(
                    Person_Node.full_name) + "\'}), (b:Patent {grant_number: \'" + str(
                    Patent_Node.grant_number) + "\'}) MERGE(a)-[:Invented {priority_date: \'" + Patent_Node.application_date + "\'}]->(b)"
                write_tx.run(query)
                write_tx.success = True

    def write_company_to_patent(self, Company_Node, Patent_Node):
        print('Creating Ownership Relationship')
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                query = "MATCH(a:Company {full_name: \'" + str(
                    Company_Node.full_name) + "\'}), (b:Patent {grant_number: \'" + str(
                    Patent_Node.grant_number) + "\'}) MERGE(a)-[:Owns]->(b)"
                write_tx.run(query)
                write_tx.success = True
