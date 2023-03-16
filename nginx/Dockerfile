FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

RUN mkdir /home/web-gui
COPY web-gui/build /home/web-gui/
COPY omr/build /home/omr/

RUN mkdir /etc/apache2
COPY .htpasswd /etc/apache2/

RUN apk add python3 python3-dev py3-pip build-base libressl-dev musl-dev libffi-dev rust cargo
RUN pip3 install pip --upgrade
RUN pip3 install certbot-nginx
RUN mkdir /etc/letsencrypt