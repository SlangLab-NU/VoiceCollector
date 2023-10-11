# Used for passing variable defined in docker compose to yarn when building the app.
touch .env

for envvar in "$@" 
do
   echo "$envvar" >> .env
done
