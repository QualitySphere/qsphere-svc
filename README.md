# Quality Assurance Platform

## Screenshots

## Values

## Framework
Leverage Grafana | Bootstrap | Flask | PostgresQL

![](specs/framework.png)

## Tables
- Connection 

uuid | type | server | account | password | projects 
--- | --- | --- | --- | --- | --- 

- project 

uuid | connection | name | version | status | sprints 
--- | --- | --- | --- | --- | --- 

- sprint 

uuid | project | name | features | rcs | issue_types | issue_categories | status | issues_overall | issue_sprint | issue_feature
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- 

- issue_overall
- issue_sprint
- issue_feature
- case_overall
- case_sprint
- case_feature
- case_regression

