import { EstimateResponse, InvoiceRequest, InvoiceResponse } from "../types";

export async function fetchEstimates(
  request: InvoiceRequest
): Promise<EstimateResponse[]> {
  const promises: Promise<EstimateResponse>[] = [];

  for (const estimate of request.estimates) {
    switch (estimate.type) {
    }
  }

  const settledPromises = await Promise.allSettled(promises);

  const response: EstimateResponse[] = [];

  for (const result of settledPromises) {
    if (result.status === "fulfilled") {
      response.push(result.value);
    } else {
      console.error("Error fetching estimate:", result.reason);
    }
  }

  return response;
}
