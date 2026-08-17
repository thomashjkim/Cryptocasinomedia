export default async (req, context) => {
  const url = new URL(req.url);
  const splat = url.pathname.replace(/^\/image-proxy\/?/, '');
  
  if (!splat || splat.includes('..')) {
    return new Response('Not Found', {
      status: 404,
      headers: {
        'Content-Type': 'text/plain',
        'X-Robots-Tag': 'noindex'
      }
    });
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3500);
    const backendUrl = `http://52.44.113.58:8080/file/${splat}`;
    const res = await fetch(backendUrl, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (res.ok) {
      const contentType = res.headers.get('Content-Type') || 'image/jpeg';
      const cacheControl = splat.startsWith('temp/') ? 'public, max-age=3600' : 'public, max-age=604800';
      return new Response(res.body, {
        status: 200,
        headers: {
          'Content-Type': contentType,
          'Cache-Control': cacheControl,
          'X-Robots-Tag': splat.startsWith('temp/') ? 'noindex' : 'all'
        }
      });
    } else {
      return new Response('Asset Not Found', {
        status: 404,
        headers: {
          'Content-Type': 'text/plain',
          'X-Robots-Tag': 'noindex'
        }
      });
    }
  } catch (err) {
    // Network error, timeout or unreachable backend returns controlled 404, never 500/502
    return new Response('Asset Not Found', {
      status: 404,
      headers: {
        'Content-Type': 'text/plain',
        'X-Robots-Tag': 'noindex'
      }
    });
  }
};
