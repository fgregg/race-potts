# race-potts
Potts models of Racial Segregation in American Cities


password in .pgpass

* get API key from http://api.census.gov/data/key_signup.html
* cp data/secrets.py.example to secrets.py and put your key in there
* `createdb segregation` if you want to name you db something else, you'll need to edit data/config.mk
* psql -d segregation -c "CREATE EXTENSION postgis"
* run make
