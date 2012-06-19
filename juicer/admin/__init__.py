from juicer.admin.JuicerAdmin import JuicerAdmin as ja
from pprint import pprint as pp

def create_repo(args):
    pulp = ja(args)
    pp(pulp.create_repo())

def create_user(args):
    pulp = ja(args)
    pp(pulp.create_user())

def list_repos(args):
    pulp = ja(args)
    pp(pulp.list_repos())

def show_repo(args):
    pulp = ja(args)
    pp(pulp.show_repo())

def show_user(args):
    pulp = ja(args)
    pp(pulp.show_user())

def delete_repo(args):
    pulp = ja(args)
    pp(pulp.delete_repo())

def delete_user(args):
    pulp = ja(args)
    pp(pulp.delete_user())
