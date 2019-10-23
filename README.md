![Quality Assurance Platform](https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/qap.png)

## Screenshots

![Project](https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/project.png)
![Sprint](https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/sprint.png)
![Dashboard](https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/dashboard.png)

## Values

## Framework
![Framework](https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/framework.png)

## API Document
http://{qap-server}/api/ui

## Installation
```bash
wget https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docker-compose.yaml
docker-compose -f docker-compose.yaml pull
docker-compose -f docker-compose.yaml up -d
```

## Upgrade
```bash
docker-compose -f docker-compose.yaml stop 
docker-compose -f docker-compose.yaml rm -f
docker-compose -f docker-compose.yaml pull
docker-compose -f docker-compose.yaml up -d
```

