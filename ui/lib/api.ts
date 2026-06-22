export interface ChatResponse {
  answer: string;
  source_url: string | null;
  last_updated_from_sources: string | null;
  disclaimer: string;
  refused: boolean;
  educational_link?: string | null;
}

// Prefer same-origin proxy (/api → Railway) to avoid browser CORS issues.
// Set API_URL on Vercel (server-side). NEXT_PUBLIC_API_URL overrides for direct calls.
const API_BASE = (
  process.env.NEXT_PUBLIC_API_URL?.trim() || "/api"
).replace(/\/$/, "");

function formatFetchError(error: unknown): string {
  if (error instanceof TypeError) {
    return "Cannot reach the assistant API. Check that API_URL is set on Vercel and the Railway backend is running.";
  }
  if (error instanceof Error && error.message.trim()) {
    return error.message;
  }
  return "Something went wrong. Please try again.";
}

export async function postChat(message: string): Promise<ChatResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
  } catch (error) {
    throw new Error(formatFetchError(error));
  }

  if (!response.ok) {
    const raw = await response.text();
    let detail = raw || `Request failed with status ${response.status}`;
    try {
      const payload = JSON.parse(raw) as { detail?: unknown };
      if (typeof payload.detail === "string") {
        detail = payload.detail;
      }
    } catch {
      // Keep raw response text when the body is not JSON.
    }
    throw new Error(detail);
  }

  return response.json();
}
