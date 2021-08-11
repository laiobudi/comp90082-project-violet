# COMP90082 - Project VIOLET - Team Bluering
# Clarisca Lawrencia - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti - icakramurti@student.unimelb.edu.au
# Jeanelle Abanto - jabanto@student.unimelb.edu.au
# Nuvi Anggaresti - nanggaresti@student.unimelb.edu.au
# Xinye Tang - xinyet@student.unimelb.edu.au

# declare variables for the SQL server
export tag='2019-CU12-ubuntu-20.04'

# pull from dockerhub official SQL server
sudo docker pull mcr.microsoft.com/mssql/server:${tag}

# create docker container
# stops and removes the docker if already exist
if [ ! -z $(sudo docker ps --all --filter "name=main-main-mssql" --quiet) ]
  then
    sudo docker stop main-mssql
    sudo docker rm main-mssql
fi

# dealing with permission error for mssql volume
# basically we change the host volume directory owner
# to uid=10001(mssql)
sudo chown 10001 /var/opt/mssql

echo ""
echo "========== starting sql server =========="
sudo docker-compose -f docker-compose-mssql.yml up -d