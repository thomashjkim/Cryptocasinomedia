const fs = require("fs");
const path = require("path");

const DATA_DIR = path.join(process.cwd(), "data");
let cachedArticles = null;

function loadArticles() {
  if (cachedArticles) return cachedArticles;
  const masterPath = path.join(DATA_DIR, "articles_master.json");
  const archivePath = path.join(DATA_DIR, "articles_archive_1000.json");

  let master = [];
  let archive = [];
  if (fs.existsSync(masterPath)) {
    master = JSON.parse(fs.readFileSync(masterPath, "utf8"));
  }
  if (fs.existsSync(archivePath)) {
    archive = JSON.parse(fs.readFileSync(archivePath, "utf8"));
  }

  const all = [...master, ...archive];
  all.sort((a, b) => new Date(b.publishedAt || 0) - new Date(a.publishedAt || 0));
  cachedArticles = { master, archive, all };
  return cachedArticles;
}

const TOOLS = [
  {
    name: "get_newsroom_metrics",
    description:
      "Retrieve live CryptoCasinoMedia newsroom metrics including total indexed articles, active editorial count, historical wire archive count, category breakdown, and latest published headlines.",
    inputSchema: {
      type: "object",
      properties: {},
      additionalProperties: false,
    },
  },
  {
    name: "search_articles",
    description:
      "Search across 1,270+ CryptoCasinoMedia editorial reports and PR Newswire / GlobeNewswire iGaming press releases by keyword, company, or category.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Keyword, operator name, topic, or headline phrase to search for.",
        },
        category: {
          type: "string",
          description:
            "Optional category filter (crypto-casinos, sportsbook, regulation, payments, sweepstakes).",
        },
        limit: {
          type: "integer",
          description: "Maximum number of results to return (default 10, max 50).",
          minimum: 1,
          maximum: 50,
        },
      },
    },
  },
  {
    name: "get_article_details",
    description:
      "Retrieve full structured metadata, canonical URL, image attribution, summary, and full body text for a specific CryptoCasinoMedia article by slug.",
    inputSchema: {
      type: "object",
      properties: {
        slug: {
          type: "string",
          description: "Exact article URL slug (e.g., from search_articles).",
        },
      },
      required: ["slug"],
    },
  },
];

function handleToolCall(name, args = {}) {
  const { master, archive, all } = loadArticles();

  if (name === "get_newsroom_metrics") {
    const categoryCounts = {};
    for (const a of all) {
      const cat = a.primaryCategory || "uncategorized";
      categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
    }
    const payload = {
      publisher: "CryptoCasinoMedia",
      website: "https://cryptocasinomedia.com",
      totalArticles: all.length,
      activeEditorialArticles: master.length,
      historicalWireArchiveArticles: archive.length,
      categoryBreakdown: categoryCounts,
      latestHeadlines: all.slice(0, 5).map((a) => ({
        title: a.title,
        slug: a.slug,
        publishedAt: a.publishedAt,
        category: a.primaryCategory,
        url: `https://cryptocasinomedia.com/press-releases/${a.slug}/`,
      })),
    };
    return {
      content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    };
  }

  if (name === "search_articles") {
    const q = (args.query || "").trim().toLowerCase();
    const cat = (args.category || "").trim().toLowerCase();
    const limit = Math.min(Math.max(parseInt(args.limit, 10) || 10, 1), 50);

    let results = all;
    if (cat) {
      results = results.filter(
        (a) =>
          (a.primaryCategory || "").toLowerCase() === cat ||
          (Array.isArray(a.sections) &&
            a.sections.some((s) => String(s).toLowerCase() === cat))
      );
    }
    if (q) {
      results = results.filter((a) => {
        const hay = [
          a.title,
          a.excerpt,
          a.company,
          a.sourceName,
          ...(Array.isArray(a.topics) ? a.topics : []),
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();
        return hay.includes(q);
      });
    }

    const items = results.slice(0, limit).map((a) => ({
      title: a.title,
      slug: a.slug,
      publishedAt: a.publishedAt,
      category: a.primaryCategory,
      company: a.company,
      sourceName: a.sourceName,
      excerpt: a.excerpt,
      url: `https://cryptocasinomedia.com/press-releases/${a.slug}/`,
    }));

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              query: q || null,
              category: cat || null,
              totalMatches: results.length,
              returned: items.length,
              articles: items,
            },
            null,
            2
          ),
        },
      ],
    };
  }

  if (name === "get_article_details") {
    const slug = (args.slug || "").trim().replace(/^\/+|\/+$/g, "");
    const article = all.find((a) => a.slug === slug);
    if (!article) {
      return {
        isError: true,
        content: [{ type: "text", text: `Article not found for slug: ${slug}` }],
      };
    }
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              ...article,
              url: `https://cryptocasinomedia.com/press-releases/${article.slug}/`,
            },
            null,
            2
          ),
        },
      ],
    };
  }

  return {
    isError: true,
    content: [{ type: "text", text: `Unknown tool: ${name}` }],
  };
}

function processRpcMessage(msg) {
  if (!msg || typeof msg !== "object" || msg.jsonrpc !== "2.0") {
    return {
      jsonrpc: "2.0",
      id: msg && msg.id !== undefined ? msg.id : null,
      error: { code: -32600, message: "Invalid JSON-RPC 2.0 Request" },
    };
  }

  const { id, method, params } = msg;

  // Notifications (no id)
  if (id === undefined || id === null) {
    return null;
  }

  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: (params && params.protocolVersion) || "2025-03-26",
        capabilities: {
          tools: { listChanged: false },
        },
        serverInfo: {
          name: "io.github.thomashjkim/cryptocasinomedia-newsroom",
          version: "1.0.0",
        },
      },
    };
  }

  if (method === "ping") {
    return { jsonrpc: "2.0", id, result: {} };
  }

  if (method === "tools/list") {
    return {
      jsonrpc: "2.0",
      id,
      result: { tools: TOOLS },
    };
  }

  if (method === "tools/call") {
    const toolName = params && params.name;
    const toolArgs = (params && params.arguments) || {};
    return {
      jsonrpc: "2.0",
      id,
      result: handleToolCall(toolName, toolArgs),
    };
  }

  return {
    jsonrpc: "2.0",
    id,
    error: { code: -32601, message: `Method not found: ${method}` },
  };
}

module.exports = (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Accept, Mcp-Session-Id");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method === "GET") {
    return res.status(200).json({
      name: "io.github.thomashjkim/cryptocasinomedia-newsroom",
      title: "CryptoCasinoMedia Newsroom & Market Intelligence",
      version: "1.0.0",
      transport: "streamable-http",
      endpoint: "https://cryptocasinomedia.com/api/mcp",
      homepage: "https://cryptocasinomedia.com",
      tools: TOOLS.map((t) => t.name),
    });
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;

    if (Array.isArray(body)) {
      const responses = body.map(processRpcMessage).filter(Boolean);
      if (responses.length === 0) return res.status(202).end();
      return res.status(200).json(responses);
    }

    const response = processRpcMessage(body);
    if (!response) {
      return res.status(202).end();
    }
    return res.status(200).json(response);
  } catch (err) {
    return res.status(400).json({
      jsonrpc: "2.0",
      id: null,
      error: { code: -32700, message: `Parse error: ${err.message}` },
    });
  }
};
