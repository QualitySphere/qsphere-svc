FROM node AS npm-build
COPY . .
RUN npm run build

FROM nginx:1.17-alpine
LABEL maintainer="shiwei@baoxian-sz.com" \
      organization="Truth & Insurance Office"
WORKDIR /usr/share/nginx/html
COPY --from=npm-build dist/* .
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
HEALTHCHECK --interval=10s --timeout=10s --start-period=10s --retries=3 CMD [ "./health_check.sh" ]
