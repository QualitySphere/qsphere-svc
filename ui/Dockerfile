FROM nginx:1.17-alpine
MAINTAINER shiwei@baoxian-sz.com

WORKDIR /usr/share/nginx/html
COPY ./ ./
RUN mv nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=10s --start-period=10s --retries=3 CMD [ "./health_check.sh" ]
