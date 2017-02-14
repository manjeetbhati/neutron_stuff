# neutron_stuff

Create url for gerrit dashboard for neutron gate failures.

1. Make sure libs launchpad and gerrit-dash-creator are installed
2. run python create_gate_failure_dash.py

it will ouput like

    https://review.openstack.org/#/dashboard/?foreach=%28project%3Aopenstack%2Fneutron+OR+project%3Aopenstack%2Fpython%2Dneutronclient+OR+project%3Aopenstack%2Fneutron%2Dspecs+OR+project%3Aopenstack%2Fneutron%2Dlib%29+status%3Aopen+NOT+owner%3Aself+NOT+label%3AWorkflow%3C%3D%2D1+NOT+label%3ACode%2DReview%3E%3D%2D2%2Cself+branch%3Amaster&title=Neutron+Review+Gate+Failures&Critical+Gate+failures+neutron=%28topic%3Abug%2F1627106%29&High+priority+Gate+failures+neutron=%28topic%3Abug%2F1509004+OR+topic%3Abug%2F1540983+OR+topic%3Abug%2F1612804+OR+topic%3Abug%2F1622516+OR+topic%3Abug%2F1627424+OR+topic%3Abug%2F1628886+OR+topic%3Abug%2F1640319+OR+topic%3Abug%2F1655567+OR+topic%3Abug%2F1660612%29&All+other+Gate+failures+neutron=%28topic%3Abug%2F1617282+OR+topic%3Abug%2F1632290%29 
