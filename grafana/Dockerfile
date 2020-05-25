FROM grafana/grafana:6.3.6
LABEL maintainer=v.stone@163.com

WORKDIR /etc/grafana/provisioning

ENV GF_AUTH_PROXY_ENABLED=true \
    GF_AUTH_ANONYMOUS_ENABLED=true \
    GF_SECURITY_ALLOW_EMBEDDING="true" \
    GF_PATHS_PROVISIONING=/etc/grafana/provisioning \
    GF_SERVER_ROOT_URL="%(protocol)s://%(domain)s:%(http_port)s/dashboard/" 

COPY provisioning/datasources ./datasources
COPY provisioning/dashboards ./dashboards

EXPOSE 3000
