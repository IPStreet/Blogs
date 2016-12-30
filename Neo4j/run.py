from Neo4j.neo4j_writer import Neo4jWriter
from Neo4j.entity_models import Person_Node, Patent_Node, Company_Node
from IPStreet import client, query


if __name__ == '__main__':

    # Instantiate neo4j writer and IP Street client
    writer = Neo4jWriter()
    client = client.Client('IPStreetAPIKeya',2)

    # Prep and send IP Street query
    query = query.PatentData()
    query.add_owner('Magic Leap, Inc.')
    results = client.send(query)


    # Write all patent nodes
    for patent in results:
        print(patent)
        # Write all patent nodes
        patent_node = Patent_Node()
        patent_node.grant_number = patent['grant_number']
        patent_node.publication_number = patent['publication_number']
        patent_node.title = patent['title']
        patent_node.application_date = patent['application_date']
        writer.write_patent(patent_node)

        inventors = patent['inventor'].split(';')
        for inventor in inventors:
            person_node = Person_Node()
            person_node.full_name = inventor
            writer.write_person(person_node)
            writer.write_person_to_patent(person_node,patent_node)

        companies = patent['owner'].split(';')
        for company in companies:
            company_node = Company_Node()
            company_node.full_name = company
            writer.write_company(company_node)
            writer.write_company_to_patent(company_node,patent_node)

