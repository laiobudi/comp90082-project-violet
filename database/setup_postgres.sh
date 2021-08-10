# COMP90082 - Project VIOLET - Team Bluering
# Clarisca Lawrencia - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti - icakramurti@student.unimelb.edu.au
# Jeanelle Abanto - jabanto@student.unimelb.edu.au
# Nuvi Anggaresti - nanggaresti@student.unimelb.edu.au
# Xinye Tang - xinyet@student.unimelb.edu.au

# declare variables for the postgreSQL and pgadmin4 setup
export user='admin'
export pass='pjviolet'

# pull from dockerhub official postgres and pgadmin
sudo docker pull postgres
sudo docker pull dpage/pgadmin4

# create docker container
# stops and removes the docker if already exist
if [ ! -z $(sudo docker ps --all --filter "name=maindb" --quiet) ]
  then
    sudo docker stop maindb
    sudo docker rm maindb
fi

if [ ! -z $(sudo docker ps --all --filter "name=main-pgadmin" --quiet) ]
  then
    sudo docker stop main-pgadmin
    sudo docker rm main-pgadmin
fi

sudo docker create \
    --name maindb \
    -p 5432:5432 \
    -v /var/lib/postgresql/data:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=${pass} \
    postgres

sudo docker create \
    --name main-pgadmin \
    -p 81:80 \
    -e "PGADMIN_DEFAULT_EMAIL=${user}@domain.local" \
    -e "PGADMIN_DEFAULT_PASSWORD=${pass}" \
    dpage/pgadmin4

echo ""
echo "========== starting postgres and pgadmin4 =========="
sudo docker start maindb
sudo docker start main-pgadmin

echo ""
echo "please use the IP Address below to connect pgadmin4 with your postgres"
sudo docker inspect maindb -f "{{json .NetworkSettings.Networks }}" | grep -m2 -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | tail -n1