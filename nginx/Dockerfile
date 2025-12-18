FROM nginx:1.25-alpine

COPY canary.conf.template /etc/nginx/templates/canary.conf.template
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV CANARY_PERCENT=10

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
