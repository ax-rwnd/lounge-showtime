#!/bin/bash

#remember chmod 666
uwsgi --catch-exceptions --ini uwsgi.conf --manage-script-name --mount /=showtimeapp
