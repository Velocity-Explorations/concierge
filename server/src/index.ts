import { Elysia, t } from "elysia";
import { swagger } from "@elysiajs/swagger";
import { InvoiceRequest, InvoiceResponse, requestValidator } from "./types";

const app = new Elysia()
  .use(swagger())
  .post(
    "/estimate",
    ({ body }) => {
      return {
        totalEstimate: 0,
        estimates: [],
        warnings: [],
        requiresManualReview: false,
        estimateId: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
        validUntil: new Date(
          Date.now() + 30 * 24 * 60 * 60 * 1000
        ).toISOString(),
      } as InvoiceResponse;
    },
    {
      body: requestValidator,
    }
  )
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);

export type App = typeof app;
