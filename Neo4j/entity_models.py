
class Person_Node():
    def __init__(self):
        self.node_type = 'Person'
        self.full_name = None


class Patent_Node():
    def __init__(self):
        self.node_type = 'Patent'
        self.title = ''
        self.grant_number = ''
        self.publication_number = ''
        self.application_date = ''


class Company_Node():
    def __init__(self):
        self.node_type = 'Company'
        self.full_name = ''