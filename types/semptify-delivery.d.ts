// semptify-delivery.d.ts
export type DeliveryStatus = "CREATED" | "PENDING" | "PARTIAL_COMPLETED" | "COMPLETED" | "FAILED" | "CANCELLED";
export type MethodType = "USPS" | "EMAIL" | "CERTIFIED_PRINT" | "TEXT" | "HAND_DELIVERED" | "SERVICE_IN_PERSON" | "FEDEX" | "COURT_SERVER" | "OTHER";
export type MethodStatus = "PENDING" | "ATTEMPTED" | "CONFIRMED" | "FAILED";

export interface DeliveryJob {
  id: string;
  caseId: string;
  createdBy: string;
  createdAt: string; // ISO timestamp
  methods: DeliveryMethod[];
  priorityOrder: string[]; // method ids in order
  status: DeliveryStatus;
  history: DeliveryHistory[];
  notes?: string;
}

export interface DeliveryMethod {
  id: string;
  type: MethodType;
  recipientName?: string;
  recipientContact?: RecipientContact;
  scheduledAt?: string; // ISO timestamp
  serviceProvider?: string;
  trackingNumber?: string;
  certifiedNumber?: string;
  proofFiles?: string[]; // file ids
  instructions?: string;
  costEstimate?: number;
  currency?: string;
  requiredFields?: string[]; // e.g. ["recipientContact.email"]
  status: MethodStatus;
}

export interface RecipientContact {
  email?: string;
  phone?: string;
  address?: string; // single-line or structured address string
}

export interface DeliveryHistory {
  id: string;
  deliveryMethodId: string;
  event: string;
  actor: string; // userId or system
  timestamp: string; // ISO
  metadata?: Record<string, unknown>;
}

export interface AttemptPayload {
  actor: string;
  attemptAt: string; // ISO
  providerResponse?: string;
  trackingNumber?: string;
  proofFileIds?: string[];
}

export interface ConfirmPayload {
  actor: string;
  confirmedAt: string; // ISO
  proofFileIds?: string[];
}
