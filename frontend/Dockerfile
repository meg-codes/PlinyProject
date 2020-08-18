FROM node:14.8-buster-slim as base
ENV APP_DIR=/opt/app

ENV NEXT_PUBLIC_BASE_URL=http://localhost:8000

WORKDIR ${APP_DIR}
COPY package.json yarn.lock ./
RUN yarn install --production=true

FROM base as dev
WORKDIR ${APP_DIR}
COPY --from=base ${APP_DIR} .
RUN yarn install --production=false
CMD ["yarn", "run", "next", "dev"]

FROM base as production
COPY . ${APP_DIR}
COPY --from=base ${APP_DIR} .
WORKDIR ${APP_DIR}
RUN yarn run next build
CMD ["yarn", "run", "next", "start"]
