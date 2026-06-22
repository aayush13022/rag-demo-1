import { NextRequest, NextResponse } from "next/server";

// Allow slow first Railway responses while BGE models load.
export const maxDuration = 60;
export const dynamic = "force-dynamic";

function backendBase(): string {
  const url =
    process.env.API_URL?.trim() ||
    process.env.NEXT_PUBLIC_API_URL?.trim() ||
    "http://localhost:8000";
  return url.replace(/\/$/, "");
}

async function proxy(request: NextRequest, path: string): Promise<NextResponse> {
  const target = `${backendBase()}/${path}${request.nextUrl.search}`;

  const headers = new Headers();
  const contentType = request.headers.get("content-type");
  if (contentType) {
    headers.set("content-type", contentType);
  }

  try {
    const init: RequestInit = {
      method: request.method,
      headers,
      signal: AbortSignal.timeout(120_000),
    };
    if (request.method !== "GET" && request.method !== "HEAD") {
      init.body = await request.text();
    }

    const response = await fetch(target, init);
    const body = await response.text();

    return new NextResponse(body, {
      status: response.status,
      headers: {
        "content-type": response.headers.get("content-type") ?? "application/json",
      },
    });
  } catch (error) {
    console.error("API proxy failed for %s: %s", target, error);
    return NextResponse.json(
      {
        detail:
          "Cannot reach the assistant API. Set API_URL on Vercel to your Railway backend URL, then redeploy.",
      },
      { status: 502 },
    );
  }
}

type RouteContext = { params: Promise<{ path: string[] }> };

async function handler(request: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  return proxy(request, path.join("/"));
}

export const GET = handler;
export const POST = handler;
