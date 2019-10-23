<img src="https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/qap.png" align=center style="width=800px;height=auto" />
## Screenshots

<img src="https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/project.png" align=center style="width=800px;height=auto" />
<img src="https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/sprint.png" align=center style="width=800px;height=auto" />
<img src="https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/dashboard.png" align=center style="width=800px;height=auto" />

## Values

## Framework
<img src="https://raw.githubusercontent.com/Quality-Assurance-Platform/qap/master/docs/framework.png" align=center style="width=800px;height=auto" />

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

