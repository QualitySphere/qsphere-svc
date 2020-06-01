![Quality Assurance Platform](https://raw.githubusercontent.com/QualitySphere/qsphere/master/docs/qap.png)

# Quality Sphere

##### [English](README.md) | 中文

> 开源软件质量保障平台

[![org](https://img.shields.io/static/v1?style=for-the-badge&label=org&message=Truth%20%26%20Insurance%20Office&color=597ed9)](http://bx.baoxian-sz.com)
![author](https://img.shields.io/static/v1?style=for-the-badge&label=author&message=v.stone@163.com&color=blue)
![license](https://img.shields.io/github/license/QualitySphere/qsphere?style=for-the-badge)
[![python](https://img.shields.io/static/v1?style=for-the-badge&logo=python&label=Python&message=3.7&color=3776AB)](https://www.python.org)
![flask](https://img.shields.io/static/v1?style=for-the-badge&logo=Flask&label=flask&message=1.1.1&color=000000)
[![vue](https://img.shields.io/static/v1?style=for-the-badge&logo=Vue.js&label=Vue.js&message=2.6.11&color=4FC08D)](https://vuejs.org)
[![element](https://img.shields.io/static/v1?style=for-the-badge&logo=css3&label=element&message=2.13.0&color=579EF8)](https://element.eleme.cn/#/en-US/component/icon)
[![grafana](https://img.shields.io/static/v1?style=for-the-badge&logo=Grafana&label=grafana&message=6.3.6&color=F46800)]()
[![postgresql](https://img.shields.io/static/v1?style=for-the-badge&logo=PostgresQL&label=postgresql&message=10&color=336791)]()
[![docker](https://img.shields.io/static/v1?style=for-the-badge&logo=docker&label=docker&message=bxwill/qsphere&color=2496ED)](https://hub.docker.com/r/bxwill/qsphere)

## 平台预览

![Project](https://raw.githubusercontent.com/QualitySphere/qsphere/master/docs/project.png)
![Sprint](https://raw.githubusercontent.com/QualitySphere/qsphere/master/docs/sprint.png)
![Dashboard](https://raw.githubusercontent.com/QualitySphere/qsphere/master/docs/dashboard.png)

## 愿景

**简单度量简单管理**

**分享软件质量保障的配方，把冷冰冰的数据变成有情感的健康指标**

## 架构

#### 组件

![Framework](https://raw.githubusercontent.com/QualitySphere/qsphere/master/docs/framework.png)

#### 数据库

![Database](https://raw.githubusercontent.com/QualitySphere/qsphere/master/docs/database.png)

## 接口文档

http://{qsphere-server}/api/ui

## 快速开始

#### 安装部署/升级 QSphere

```bash
docker-compose -f docker-compose.yaml pull
docker-compose -f docker-compose.yaml up -d
```

```yaml
version: "3"
services:
  qsphere-db:
    container_name: qsphere-db
    image: postgres:10
    restart: always
    environment:
      POSTGRES_DB: 'qsphere'
      POSTGRES_PASSWORD: 'password'
    volumes:
      - ./qsphere-pgdata:/var/lib/postgresql/data
    command: ["-c", "max_connections=2000"]
  qsphere-svc:
    container_name: qsphere-svc
    image: bxwill/qsphere:svc-latest
    restart: always
    ports:
      - 6001:6001
    environment:
      PG_DB: 'qsphere'
      PG_SERVER: qsphere-db
      PG_USER: 'postgres'
      PG_PASSWORD: 'password'
    depends_on:
      - qsphere-db
  qsphere-grafana:
    container_name: qsphere-grafana
    image: bxwill/qsphere:grafana-latest
    restart: always
    ports:
      - 3000:3000
    environment:
      PG_DB: 'qsphere'
      PG_SERVER: qsphere-db
      PG_PORT: '5432'
      PG_USER: 'postgres'
      PG_PASSWORD: 'password'
    depends_on:
      - qsphere-db
      - qsphere-svc
  qsphere-ui:
    container_name: qsphere-ui
    image: bxwill/qsphere:ui-latest
    restart: always
    ports:
      - 8080:80
    depends_on:
      - qsphere-svc
      - qsphere-grafana
```

## 版本历史

- 1.0.0 - `2020-06-01`
  - UI 重构
  - 数据库结构调整
  - 改进后端接口反馈数据信息
  - 数据图表项目/冲刺拆分
  - 新增 Portal 菜单
  - 移除实验室中 VM 在线检查功能

- 0.9.0 - `2019-12-31`
  - 优化 UI 界面

- 0.2.0 - `2019-10-23`
  - 支持修改连接 JIRA 的配置信息
  - 支持修改迭代信息
  - 支持暂停/激活迭代的数据抓取
  - 支持实验室中 VM 的在线检查

- 0.1.0 - `2019-10-14`
  - 实现抓取 JIRA 数据，经过整理分析后，通过 Grafana 进行展示，关注者通过图表可进行分析判断项目风险和产品质量。
  - 支持连接 JIRA 服务器
  - 支持添加项目和迭代信息
  - 支持图表看板
  - 支持 API 文档

## 更多信息 

- Homepage: https://QualitySphere.github.io
- GitHub: https://github.com/QualitySphere/qsphere
- Docker: https://hub.docker.com/r/bxwill/qsphere

