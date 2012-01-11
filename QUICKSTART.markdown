Quick Start
===========
For those who want to evaluate quickly and are in a hurry, here is the Quick
Start Guide. These instructions are intentionally brief. These instructions are expanded in the [Installation Guide](https://github.com/glenjarvis/djurk/wiki/Installation-Guide).

1. Install Django ("pip install Django" or equivalent command)
2. Install Boto ("pip install boto==2.1.1" or equivalent command)
3. Download djurk (https://github.com/glenjarvis/djurk/downloads)
   (or clone latest version: 'git clone git@github.com:glenjarvis/djurk.git')
4. Change to Repo's src directory
   (A crude basic django app is included so that you can start running immediately (for demo purposes only))
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
`AWS Console (http://aws.amazon.com/) -> Login -> Security Credentials -> Access Keys (Access Key ID) and Secret Access Key`

9. Create filename 'mturk_config.cfg' in same directory as settings.py. Put
      the following information in the file (with this format), except replace the aws_access_key_id and aws_secret_access_key with the information you found in the step above. (Also note that there is a markdown bug. The first line below should be the word "Connection" immediately surrounded by square brackets).
```
'[Connection]' # Without surrounding ticks (Markdown bug)  
aws_access_key_id: put_your_access_key_here  
aws_secret_access_key: put_your_secret_key_here    
```
10. Test configuration by looking up the Sandbox account balance.
```
prompt> ./manage.py djurk_demo --sandbox --account-balance  
[$10,000.00]
```
11. Verify your production balance (and add money if needed. You can charge your account at the [mturk website](https://requester.mturk.com/mturk/youraccount)).
```
prompt> ./manage.py djurk_demo --account-balance  
[$6.23]
```
12. Create a sample hit (Tell me your favorite color) in the sandbox. Follow the website given at this step to see what the hit looks like for the worker. Accept and complete the hit if you wish:
```
prompt> ./manage.py djurk_demo --sample-hit --sandbox

Visit this website to see HITs that were created:  
https://workersandbox.mturk.com/mturk/preview?groupId=2CTFK0COK2JET3I0600LUW6OZDFRKL
```
13. (optional) Create the same hit in production (Amazon will charge you 1 cent
for performing this step). Again, follow the instructions given from the command to get to the URL that shows what the hit looks like. You can complete the hit yourself (and thus pay yourself), or you can also choose to wait and let a real Mechanical Turk worker accept this task. If you aren't quick, a Mechanical Turk worker will snap this up before you even see it.
```
prompt> ./manage.py djurk_demo --sample-hit

Visit this website to see HITs that were created:
https://www.mturk.com/mturk/preview?groupId=2VKILKH1Q6SVIPSJU2HUDL5OBV10JG
```
14. Poll Mechanical Turk to retrieve data. The --assignments argument tells the command to additionally poll the Assignments associated with the HITs, as well as the HITs.
```
prompt> ./manage.py poll_mturk --assignments
```
15. Examine Results. If you performed step 13, then you submitted jobs to
workers and you may already have results. Use the admin, like before, and visit
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
```
prompt> ./manage.py runserver  
Validating models...  

0 errors found  
Django version 1.3.1, using settings 'src.settings'  
Development server is running at http://127.0.0.1:8000/  
Quit the server with CONTROL-C.  
```
16. Expanding on the previous step, we'll look at the results given when this demo was written. Specifically, we'll look at the Assignment created: [http://127.0.0.1:8000/admin/djurk/assignment](http://127.0.0.1:8000/admin/djurk/assignment). You'll notice the 'favorite_color' field has a color choice (given by the worker) and the comment field has something different (or nothing). I see "white" as the favorite color submitted. And, the following comment field (It's hard to get this type of creativity from a computer):

    > I find it to be a very stark, uncompromising color. White like  
    > ashes and bleached bones and deserts that go on forever. White  
    > like rainfall. In the West it is worn by virgin brides, in the  
    > East it's the color of death, but it's always, always striking.

17. Accept the job and pay your workers! If you performed step 13 above, you have given a job to a
worker.  Those workers submitted those jobs, but haven't yet been paid for
them. They will be auto-paid if you do not accept or reject the work. Why make
them wait?
    1. Go to the website: [http://127.0.0.1:8000/admin/djurk/assignment](http://127.0.0.1:8000/admin/djurk/assignment)
    2. Check the box next to the assignment
    3. Select the "Approve assignment and pay worker" Action, and finally
    4. click "GO."


This was a quick demo of Djurk. Don't forget that, in these instructions, you are running out of a sample debug server. For serious work, you should consider installing the Djurk app into your own Django projects. See the [Installation Guide](https://github.com/glenjarvis/djurk/wiki/Installation-Guide) for more details.
