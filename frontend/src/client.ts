import { treaty } from "@elysiajs/eden";
import type { App } from "../../server/src/index.ts";

const client = treaty<App>("localhost:3000");
