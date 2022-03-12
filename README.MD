Django API that provides top 25 NCAA rankings and each weeks schedule to a vue frontend

Dockerized in 3 parts
- Django/gunicorn
- Nginx server for built vue app
- Nginx server for reverse proxy to django/gunicorn

Dev branch = master
prod branch = pi


Pi runs ARM processor
in order to build and install packages that are compiled c (pandas numpy lxml) needed to upgrade to python version 3.10 for arm
using a multi stage build that reduces final image size by copying over the installed libraries

docker-compose is using named volumes --> these will populate with the data in the container instead of being empty like regular volumes
defining the named volumes as type mount will allow to specify the folder location


might beable to do this like how nginx does it --> define the conatiner folders that you want to be Volumes at the end of the Dockerfile, then use compose to map volumes to them
https://github.com/go-gitea/gitea/blob/main/Dockerfile.rootless
https://github.com/NginxProxyManager/nginx-proxy-manager/blob/develop/docker/Dockerfile
https://docs.docker.com/engine/reference/builder/#volume