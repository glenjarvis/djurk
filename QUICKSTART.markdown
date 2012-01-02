Quick Start
===========
For those who want to evaluate quickly and are in a hurry, here is the Quick
Start Guide.

1. Install Django ("pip install Django" or equivalent command)
2. Install Boto ("pip install boto==2.1.1" or equivalent command)
3. Download djurk (https://github.com/glenjarvis/djurk/downloads)
   (or clone latest version: git clone git@github.com:glenjarvis/djurk.git)
4. Change to Repo's src directory
   (A crude basic django app is included so that you can start running)
5. Sync database:
``` 
    prompt> python manage.py syncdb
    Creating tables ...
    Creating table auth_permission
    [snip]
    Creating table djurk_hit
    Creating table djurk_assignment
    Creating table djurk_keyvalue
```
6. Start local webserver/runserver:
```
    prompt> ./manage.py runserver
    Validating models...

    0 errors found
    Django version 1.3.1, using settings 'src.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
```
7. Visit Admin Page with Web Browser:

   http://127.0.0.1:8000/admin

   You should now see a Djurk module with these models:

    * Assignments
    * HITs
    * Key-Value Pairs

8. Find your Amazon Mechanical Turk Private and Public Access Keys

    * AWS Console (http://aws.amazon.com/)
    * Login
    * Security Credentials
    * Access Keys (Access Key ID) and Secret Access Key (click show)

9. Create filename 'mturk_config.cfg' in same directory as settings.py. Put
      this info in it (with this format)

```[[[[Connection]]]]
aws_acccess_key_id: put_your_access_key_here
aws_secret_access_key: put_your_secret_key_here
host: mechanicalturk.sandbox.amazonaws.com```
