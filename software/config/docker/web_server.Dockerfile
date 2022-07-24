# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY ./web/package*.json ./
RUN npm install
COPY ./web .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY ./config/nginx/nginx.template /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html/irrigation/web
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
