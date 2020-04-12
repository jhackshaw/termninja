FROM node:13-alpine

EXPOSE 3000

WORKDIR /app

COPY ./package.json .
RUN npm install
COPY . .

CMD ["npm", "run", "dev"]
