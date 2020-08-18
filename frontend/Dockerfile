FROM node:14.8-buster-slim as base
ENV APP_DIR=/opt/app

ARG next_public_base_url=''
ENV NEXT_PUBLIC_BASE_URL=$next_public_base_url

WORKDIR ${APP_DIR}
COPY package.json yarn.lock ./
RUN yarn install 

FROM base as dev
WORKDIR ${APP_DIR}
COPY --from=base ${APP_DIR} .
CMD ["yarn", "run", "next", "dev"]

FROM base as production
COPY . ${APP_DIR}
COPY --from=base ${APP_DIR} .
WORKDIR ${APP_DIR}
RUN yarn run next build
CMD ["yarn", "run", "next", "start"]
