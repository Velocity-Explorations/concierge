import { t } from "elysia";

export interface LodgingRequest {
  type: "lodging";
  location: string;
  checkInDate: string;
  checkOutDate: string;
  roomType?: "standard" | "suite";
}

export interface PerDiemRequest {
  type: "per_diem";
  location: string;
  startDate: string;
  endDate: string;
  mealType?: "breakfast" | "lunch" | "dinner" | "full_day";
}

export interface FlightRequest {
  type: "flights";
  origin: string;
  destination: string;
  departureDate: string;
  returnDate?: string;
  passengerCount: number;
  cabinClass?: "economy" | "business" | "first";
}

export interface GroundTransportRequest {
  type: "ground_transport";
  pickupLocation: string;
  dropoffLocation: string;
  date: string;
  vehicleType?: "sedan" | "suv" | "van" | "bus";
  passengerCount: number;
}

export interface TranscriptionRequest {
  type: "transcription";
  language: string;
  duration: number;
  audioQuality?: "standard" | "high";
  turnaroundTime?: "standard" | "rush";
}

export interface InterpretationRequest {
  type: "interpretation";
  sourceLanguage: string;
  targetLanguage: string;
  duration: number;
  interpreterType?: "consecutive" | "simultaneous";
  location: string;
  requiresTravel?: boolean;
}

export interface InterpreterRulesRequest {
  type: "interpreter_rules";
  interpreterCitizenship: string;
  conferenceMode: boolean;
  securityClearance?: "none" | "secret" | "top_secret";
}

export interface VenuePackageRequest {
  type: "venue_package";
  venueType: "conference_room" | "auditorium" | "outdoor";
  attendeeCount: number;
  duration: number;
  requiresAV: boolean;
  requiresHeadsets: boolean;
}

export interface NotaryServicesRequest {
  type: "notary_services";
  documentCount: number;
  serviceType: "acknowledgment" | "jurat" | "copy_certification";
  location?: string;
}

export interface EquipmentRentalRequest {
  type: "equipment_rental";
  equipmentType: "microphone" | "camera" | "projector" | "laptop" | "other";
  quantity: number;
  rentalDuration: number;
  deliveryRequired: boolean;
}

export interface VisaTravelRequest {
  type: "visa_travel";
  country: string;
  visaType: "tourist" | "business" | "transit";
  urgency?: "standard" | "expedited";
}

export type EstimateRequest =
  | LodgingRequest
  | PerDiemRequest
  | FlightRequest
  | GroundTransportRequest
  | TranscriptionRequest
  | InterpretationRequest
  | InterpreterRulesRequest
  | VenuePackageRequest
  | NotaryServicesRequest
  | EquipmentRentalRequest
  | VisaTravelRequest;

export interface EstimateResponse {
  type: EstimateRequest["type"];
  estimatedCost: number;
  confidence: "high" | "medium" | "low";
  breakdown?: {
    baseRate: number;
    fees?: number;
    taxes?: number;
    surcharges?: number;
  };
  notes?: string;
  validUntil?: string;
}

export interface InvoiceRequest {
  estimates: EstimateRequest[];
  clientInfo?: {
    name: string;
    organization: string;
    email: string;
  };
  projectInfo?: {
    name: string;
    description: string;
    deadline: string;
  };
}

export interface InvoiceResponse {
  totalEstimate: number;
  estimates: EstimateResponse[];
  warnings: string[];
  requiresManualReview: boolean;
  estimateId: string;
  createdAt: string;
  validUntil: string;
}

export const requestValidator = t.Object({
  estimates: t.Array(
    t.Union([
      t.Object({
        type: t.Literal("lodging"),
        location: t.String(),
        checkInDate: t.String(),
        checkOutDate: t.String(),
        roomType: t.Optional(
          t.Union([t.Literal("standard"), t.Literal("suite")])
        ),
      }),
      t.Object({
        type: t.Literal("per_diem"),
        location: t.String(),
        startDate: t.String(),
        endDate: t.String(),
        mealType: t.Optional(
          t.Union([
            t.Literal("breakfast"),
            t.Literal("lunch"),
            t.Literal("dinner"),
            t.Literal("full_day"),
          ])
        ),
      }),
      t.Object({
        type: t.Literal("flights"),
        origin: t.String(),
        destination: t.String(),
        departureDate: t.String(),
        returnDate: t.Optional(t.String()),
        passengerCount: t.Number(),
        cabinClass: t.Optional(
          t.Union([
            t.Literal("economy"),
            t.Literal("business"),
            t.Literal("first"),
          ])
        ),
      }),
      t.Object({
        type: t.Literal("ground_transport"),
        pickupLocation: t.String(),
        dropoffLocation: t.String(),
        date: t.String(),
        vehicleType: t.Optional(
          t.Union([
            t.Literal("sedan"),
            t.Literal("suv"),
            t.Literal("van"),
            t.Literal("bus"),
          ])
        ),
        passengerCount: t.Number(),
      }),
      t.Object({
        type: t.Literal("transcription"),
        language: t.String(),
        duration: t.Number(),
        audioQuality: t.Optional(
          t.Union([t.Literal("standard"), t.Literal("high")])
        ),
        turnaroundTime: t.Optional(
          t.Union([t.Literal("standard"), t.Literal("rush")])
        ),
      }),
      t.Object({
        type: t.Literal("interpretation"),
        sourceLanguage: t.String(),
        targetLanguage: t.String(),
        duration: t.Number(),
        interpreterType: t.Optional(
          t.Union([t.Literal("consecutive"), t.Literal("simultaneous")])
        ),
        location: t.String(),
        requiresTravel: t.Optional(t.Boolean()),
      }),
      t.Object({
        type: t.Literal("interpreter_rules"),
        interpreterCitizenship: t.String(),
        conferenceMode: t.Boolean(),
        securityClearance: t.Optional(
          t.Union([
            t.Literal("none"),
            t.Literal("secret"),
            t.Literal("top_secret"),
          ])
        ),
      }),
      t.Object({
        type: t.Literal("venue_package"),
        venueType: t.Union([
          t.Literal("conference_room"),
          t.Literal("auditorium"),
          t.Literal("outdoor"),
        ]),
        attendeeCount: t.Number(),
        duration: t.Number(),
        requiresAV: t.Boolean(),
        requiresHeadsets: t.Boolean(),
      }),
      t.Object({
        type: t.Literal("notary_services"),
        documentCount: t.Number(),
        serviceType: t.Union([
          t.Literal("acknowledgment"),
          t.Literal("jurat"),
          t.Literal("copy_certification"),
        ]),
        location: t.Optional(t.String()),
      }),
      t.Object({
        type: t.Literal("equipment_rental"),
        equipmentType: t.Union([
          t.Literal("microphone"),
          t.Literal("camera"),
          t.Literal("projector"),
          t.Literal("laptop"),
          t.Literal("other"),
        ]),
        quantity: t.Number(),
        rentalDuration: t.Number(),
        deliveryRequired: t.Boolean(),
      }),
      t.Object({
        type: t.Literal("visa_travel"),
        country: t.String(),
        visaType: t.Union([
          t.Literal("tourist"),
          t.Literal("business"),
          t.Literal("transit"),
        ]),
        urgency: t.Optional(
          t.Union([t.Literal("standard"), t.Literal("expedited")])
        ),
      }),
    ])
  ),
  clientInfo: t.Optional(
    t.Object({
      name: t.String(),
      organization: t.String(),
      email: t.String(),
    })
  ),
  projectInfo: t.Optional(
    t.Object({
      name: t.String(),
      description: t.String(),
      deadline: t.String(),
    })
  ),
});
