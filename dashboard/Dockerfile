# ---- Build Stage ----
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY src/ ./src/
COPY public/ ./public/
COPY tsconfig.json tailwind.config.js postcss.config.js ./

RUN npm run build

# ---- Runtime Stage ----
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

# Inline nginx config to listen on port 3000
RUN printf 'server {\n  listen 3000;\n  root /usr/share/nginx/html;\n  index index.html;\n  location / {\n    try_files $uri $uri/ /index.html;\n  }\n}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
