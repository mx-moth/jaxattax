# Frontend asset builder
FROM node:8-stretch as frontend

ENV NPM_CONFIG_LOGLEVEL=warn

WORKDIR /opt/frontend
COPY ./frontend/package.json ./frontend/yarn.lock /opt/frontend/

RUN yarn && \
	yarn cache clean && \
	true

COPY ./frontend/design /opt/frontend/design

RUN yarn run build
CMD ["yarn", "start"]

# Backend application
FROM alpine as backend

WORKDIR /opt/backend

RUN apk add --no-cache \
		python3 py3-pip py3-pillow \
		postgresql-dev gcc \
		tini uwsgi uwsgi-python3 \
		jpeg-dev zlib-dev musl-dev python3-dev \
	&& true

COPY backend/requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel \
	&& pip3 install --no-cache-dir pyinotify -r /tmp/requirements.txt \
	&& apk del jpeg-dev zlib-dev musl-dev python3-dev \
	&& rm /tmp/requirements.txt \
	&& true


COPY ./backend /opt/backend
COPY --from=frontend /opt/frontend/dist /opt/frontend/dist

ENV PYTHONUNBUFFERED=1 \
	PYTHONIOENCODING=UTF-8 \
	PYTHONDONTWRITEBYTECODE=1 \
	DJANGO_SETTINGS_MODULE=deploy.settings \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \
	UWSGI_PROCESSES=1

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/opt/backend/deploy/run.sh"]
