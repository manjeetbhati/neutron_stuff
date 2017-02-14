import git
import os

from subprocess import call
from gerrit_dash_creator.cmd import creator
from launchpadlib.launchpad import Launchpad

file_name='gate.dash'
cachedir = "~/.launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir,
                                        version="devel")
neutron = launchpad.projects['neutron']

def write_section(filen, section_name, query):
    print(section_name)
    if query:
        filen.write("[section \"")
        filen.write(section_name)
        filen.write("\"]\n")
        filen.write("query = ")
        filen.write(query)
        print(query)
    else:
        print("No result found\n")


def _search_task(project, **kwargs):
    bugs = project.searchTasks(**kwargs)
    if not bugs:
        return
    gerrit_query1 = "("
    for b in bugs:
        #gerrit_query1 += ("message:%d OR " % b.bug.id)
        gerrit_query1 += ("topic:bug/%d OR " % b.bug.id)
    gerrit_query1 = gerrit_query1[:-4]
    #gerrit_query2 = gerrit_query2[:-4]
    gerrit_query1 += ")\n\n"
    return gerrit_query1


def get_gate_failure_query(project, **kwargs):
    cbg = _search_task(project, **kwargs)
    return cbg


def write_queries_for_project(file_name, project):
    critical_bugs = {'tags': ['gate-failure'], 'importance': ["Critical"],
                   'status': ["In Progress"]}
    High_bugs = {'tags': ['gate-failure'], 'importance': ["High"]}

    ml_bugs = {'tags': ['gate-failure'], 'importance': ["Medium", 'Low']}
    
    cb = get_gate_failure_query(project, **critical_bugs)
    section_name = "Critical Gate failures %s" % project.name
    write_section(file_name, section_name, cb)

    hg = get_gate_failure_query(project, **High_bugs)
    
    section_name = "High priority Gate failures %s" % project.name
    write_section(file_name, section_name, hg)
    
    rest_b = get_gate_failure_query(project, **ml_bugs)
    section_name = "All other Gate failures %s" % project.name
    write_section(file_name, section_name, rest_b)

with open(file_name, 'w') as f:
    title = "[dashboard]\ntitle = Neutron Review Gate Failures\n"
    f.write(title)
    f.write("description = Review Inbox\n")
    f.write("foreach = (project:openstack/neutron OR "
            "project:openstack/python-neutronclient OR "
            "project:openstack/neutron-specs OR "
            "project:openstack/neutron-lib) status:open NOT owner:self "
            "NOT label:Workflow<=-1 "
            "NOT label:Code-Review>=-2,self branch:master\n")
    f.write("\n")

    print("Querying Launchpad, this might take a while...")
    write_queries_for_project(f, neutron)

if not os.path.exists('gerrit-dash-creator'):  
    git.Git().clone("https://github.com/openstack/gerrit-dash-creator")
call('./gerrit-dash-creator/gerrit-dash-creator ' + file_name, shell=True)
