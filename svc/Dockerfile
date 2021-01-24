FROM bxwill/qsphere:svc-base
LABEL maintainer="v.stone@163.com"

WORKDIR /workspace
COPY . .

CMD ./launch.sh
EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD ./health_check.sh
