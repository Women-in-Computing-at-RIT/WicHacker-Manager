FROM node:16 AS build
WORKDIR /app
COPY . .

#RUN npm install
#RUN npm run build


FROM nginx:1.20
COPY --from=build /app/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/build /usr/share/nginx/html