#!/bin/bash
cd /tmp
mysql -u root -p${MYSQL_ROOT_PASSWORD} < ./dbcreate.sql
rm /tmp/*.sql
