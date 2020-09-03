  
FOLLOW THESE STEPS TO PROPERLY RUN THE CODE


1.Delete migrations if any.


2.Change the database in settings.py.


3.Change the api keys, client id and secrets and add them to database (Google and Facebook account).


4.Change the email account to be used in settings.py


5.Change the twilio in profiles->views->phone verification functions and also in supplier->views.py phone verification function


6.Use the test card credentials of payu while doing online payment.
Card no:4444333322221111 expiry:01/21 cvv:123
Name on card : anything otp:123456


7.Change emailsend function in views.py as required.


8.Make Migrations for each app seperately if no changes found when making migrations together.


9.Add new merchant account salt and key in payments.config
