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

```Connection (surround by brackets)
aws_acccess_key_id: put_your_access_key_here
aws_secret_access_key: put_your_secret_key_here
host: mechanicalturk.sandbox.amazonaws.com```

10. Test configuration by looking up the Sandbox account balance.

prompt> ./manage.py djurk_demo --sandbox --account-balance
[$10,000.00]

11. Verify your production balance (and add money if needed)

prompt> ./manage.py djurk_demo --account-balance
[$6.23]

12. Create a sample hit (Tell me your favorite color) in the sandbox:

prompt> ./manage.py djurk_demo --sample-hit --sandbox

Visit this website to see HITs that were created:
https://workersandbox.mturk.com/mturk/preview?groupId=2CTFK0COK2YOURGROUPID0LUW6OZDFRKL

13. (optional) Create the same hit in production (Amazon will charge you 1 cent
for performng this step). You can also choose to wait and let a real Mechanical
Turk worker accept this task:

prompt> ./manage.py djurk_demo --sample-hit
Visit this website to see HITs that were created:

https://www.mturk.com/mturk/preview?groupId=2VKILKH1Q6SVIPSJU2HUDL5OBV10JG

14. Poll Mechanical Turk to retrieve data. The --assignments aregument poll's,
not only the HITs, but also the Assignments associated with those hits.

prompt> ./manage.py poll_mturk --assignments

15. Examine Results. If you performed step 13, then you submitted jobs to
workers (or, if you used the sandbox and completed a few HITs yourself),
you may already have results. Use the admin, like before, and visit
the Django website:

prompt> ./manage.py runserver
Validating models...

0 errors found
Django version 1.3.1, using settings 'src.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.


Visit this site: http://127.0.0.1:8000/admin/djurk/assignment

You'll notice the 'favorite_color' field has a color choice (given by the
worker) and the comment field has something different (or nothing). An example
comment field that I have received is:

> I find it to be a very stark, uncompromising color. White like
> ashes and bleached bones and deserts that go on forever. White
> like rainfall. In the West it is worn by virgin brides, in the
> East it's the color of death, but it's always, always striking.

It's hard to get that type of creativity from a computer.

16. Pay your workers! If you performed step 13 above, you have given a job to a
worker.  Those workers submitted those jobs, but haven't yet been paid for
them. They will be auto-paid if you do not accept or reject the work. Why make
them wait?

Go to the website: 

http://127.0.0.1:8000/admin/djurk/assignment

Check the box, select the "Approve signment and pay worker" Action, and click
GO.
