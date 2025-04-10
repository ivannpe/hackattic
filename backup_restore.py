import base64
import json
import psycopg2
import requests
import os



# https://www.stevenchang.tw/blog/2023/07/05/restore-db-via-a-dump-file-with-gunzip
# https://www.geeksforgeeks.org/how-to-dump-and-restore-postgresql-database/
URL = "https://hackattic.com/challenges/backup_restore/"
PARAMS = {'access_token': "90fabb2a44afba20"}
r = requests.get(url = URL+"problem", params = PARAMS)
data = r.json()
pg_dump = data['dump']
decoded = base64.b64decode(pg_dump)

with open('pg_dump.dump.gz', 'wb') as fp:
	fp.write(decoded)
"""
/Library/PostgreSQL/17/bin/psql -U postgres

psql (17.4)
Type "help" for help.

postgres=# createdb recoverdb
postgres-# \q

gunzip -c pg_dump.dump.gz | /Library/PostgreSQL/17/bin/psql -U postgres recoverdb
"""
os.putenv('PGPASSWORD', 'postgres')
os.system('gunzip -c pg_dump.dump.gz | /Library/PostgreSQL/17/bin/psql -U postgres recoverdb')
conn = psycopg2.connect(
            database="recoverdb",
            user="postgres",
            password="postgres",
            host="localhost",
            port = "5432"
        )
cursor = conn.cursor()


cursor.execute("SELECT ssn FROM criminal_records WHERE status= 'alive'")


alive_ssns = [row[0] for row in cursor.fetchall()]

result = {
    "alive_ssns": alive_ssns,
}

res = requests.post(url=URL+"solve", params = PARAMS, data=json.dumps(result))
print(res.text)
