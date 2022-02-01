FROM python:3.8
ENTRYPOINT ["/bin/mapping-app"]
COPY server.src/app.pex /bin/mapping-app
EXPOSE 80
