# FancyMTA
General Transit Feed Specification for NYC MTA

##Overview
Project gathers NYC Subway GTFS data by polling MTA data feeds.


Source: http://datamine.mta.info/list-of-feeds

Documentation: https://goo.gl/ZZKHbZ


Please note, Data feeds responsible for N, Q, R, W, B, and D trains are in Beta.


In these cases, information for these specified trains are not always available per MTA documentation.

##Scheduler
20,50 * * * * source /home/darnelclayton/fancy/env/bin/activate && python /home/darnelclayton/fancy/fancymta/get_mta_updates.py

Crontab is responsible for scheduling get_mta_updates.py module.
