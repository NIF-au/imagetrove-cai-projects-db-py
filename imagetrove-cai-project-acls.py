import time
import MySQLdb
from validate_email import validate_email
import requests
from requests.auth import HTTPBasicAuth
import json as simplejson

# MyTardis details:
username = "admin"
password = "admin_CHANGEME"
url      = "https://imagetrove.example.com/api/v1/userprojectacl/"

# MySQL database details:
mysql_host  = "mysql-server.example.com"
mysql_user  = "mysql-user"
mysql_pass  = "mysql-password"
mysql_db    = "database-name"

while True:
    db = MySQLdb.connect(host=mysql_host,
                         user=mysql_user,
                         passwd=mysql_pass,
                         db=mysql_db)

    c = db.cursor()

    c.execute("select CI_list.project_number, email.address from CI_list, email WHERE CI_list.who = email.owner")

    # CAI Project IDs are 5 digit numbers:
    acl_users = [(u, '%05d' % p) for (p, u) in c.fetchall()]

    acl_users = [(u, p) for (u, p) in acl_users if validate_email(u)]

    # Manually added details for testing:
    acl_users += [('a.janke1@uq.edu.au', '10000'), ('a.janke1@uq.edu.au', '10001')]
    acl_users += [('c.hamalainen@uq.edu.au', '10000'), ('c.hamalainen@uq.edu.au', '10001')]

    print len(acl_users)

    data = {'acl_pairs': acl_users}

    headers = {'Accept': 'application/json'}
    response = requests.post(url,
                             verify=False,
                             data={"json_data": simplejson.dumps(data)},
                             headers=headers,
                             auth=HTTPBasicAuth(username, password))

    print 'response', response.text

    print 'sleeping for a minute...'

    time.sleep(60)
