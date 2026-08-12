export default async (request, context) => {
  const url = new URL(request.url);
  const pathname = url.pathname.toLowerCase();

  // 1. Immediately return HTTP 410 Gone for known garbage / malformed URLs like /script%3E, /author/, /team/
  if (pathname.includes("script%") || pathname.includes("script>") || pathname.startsWith("/author/") || pathname.startsWith("/team/") || pathname.startsWith("/wp-")) {
    return new Response("410 Gone - Malformed or Obsolete URL", {
      status: 410,
      headers: {
        "Content-Type": "text/plain; charset=UTF-8",
        "X-Robots-Tag": "noindex, nofollow"
      }
    });
  }

  const response = await context.next();
  
  // 2. Apply noindex headers to all staging, branch deploy, and preview hosts
  const host = url.hostname.toLowerCase();
  if (host !== "cryptocasinomedia.com" && host !== "www.cryptocasinomedia.com" && host !== "localhost" && host !== "127.0.0.1") {
    response.headers.set("X-Robots-Tag", "noindex, nofollow");
  }
  
  return response;
};
