export default async (request, context) => {
  const response = await context.next();
  const url = new URL(request.url);
  
  // Apply noindex headers to all staging, branch deploy, and preview hosts
  const host = url.hostname.toLowerCase();
  if (host !== "cryptocasinomedia.com" && host !== "www.cryptocasinomedia.com" && host !== "localhost" && host !== "127.0.0.1") {
    response.headers.set("X-Robots-Tag", "noindex, nofollow");
    console.log(`[SEO-GUARD] Host "${host}" detected. Injected X-Robots-Tag: noindex, nofollow`);
  }
  
  return response;
};
