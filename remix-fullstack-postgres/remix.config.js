/** @type {import('@remix-run/dev').AppConfig} */
export default {
  server: {
    port: Number(process.env.PORT) || 3000,
  },
  ignoredRouteFiles: ["**/.*"],
};
