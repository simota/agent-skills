import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const clientPort = Number(process.env.RUN_DASH_CLIENT_PORT ?? 5173);
const serverPort = Number(
  process.env.RUN_DASH_SERVER_PORT ?? process.env.PORT ?? 5757
);

export default defineConfig({
  plugins: [react()],
  server: {
    port: clientPort,
    host: "127.0.0.1",
    proxy: {
      "/api": {
        target: `http://127.0.0.1:${serverPort}`,
        changeOrigin: true,
      },
    },
  },
});
