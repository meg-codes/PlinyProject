import { IncomingMessage } from "http";

function getBaseUrl(req: IncomingMessage | undefined) {
  let baseUrl = req
    ? process.env.NEXT_BASE_URL
    : process.env.NEXT_PUBLIC_BASE_URL;
  return baseUrl ? baseUrl : "";
}

export default getBaseUrl;
