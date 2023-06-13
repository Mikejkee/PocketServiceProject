FROM jwilder/nginx-proxy:0.9

COPY vhost.d/default /etc/nginx/vhost.d/default
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
RUN echo "client_max_body_size 100m;" >> /etc/nginx/conf.d/nginx.conf
RUN echo "client_body_buffer_size 100m;" >> /etc/nginx/conf.d/nginx.conf