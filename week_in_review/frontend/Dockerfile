# syntax=docker/dockerfile:1
FROM node:16-slim as builder
WORKDIR /frontend
# copy both 'package.json' and 'package-lock.json' (if available)
COPY ncaab_vue_frontend/package*.json /frontend

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY ./ncaab_vue_frontend /frontend
RUN npm install vite

# Build the project
RUN npm run build

#create the nginx image and run copy the config and 
FROM nginx:alpine as production-build
# Copy from the stahg 1
COPY --from=builder /frontend/dist /usr/share/nginx/html

#VOLUME ["/usr/share/nginx/html/", "/etc/nginx/conf.d"]

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
