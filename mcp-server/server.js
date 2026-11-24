#!/usr/bin/env node

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require("@modelcontextprotocol/sdk/types.js");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const PROJECT_ROOT = path.resolve(__dirname, "..");
const MASTER_JSON = path.join(PROJECT_ROOT, "data", "articles_master.json");
const ARCHIVE_JSON = path.join(PROJECT_ROOT, "data", "articles_archive_1000.json");

function getAllArticles() {
  const master = fs.existsSync(MASTER_JSON) ? JSON.parse(fs.readFileSync(MASTER_JSON, "utf-8")) : [];
  const archive = fs.existsSync(ARCHIVE_JSON) ? JSON.parse(fs.readFileSync(ARCHIVE_JSON, "utf-8")) : [];
  return { master, archive, combined: [...master, ...archive] };
}

const server = new Server(
  {
    name: "cryptocasinomedia-newsroom",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tool schemas
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_newsroom_metrics",
        description: "Returns real-time newsroom publishing statistics, article counts, category breakdowns, and sitemap health.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "search_articles",
        description: "Searches the master database of 240+ articles by keywords, company name, category, or topic.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search keyword or phrase (e.g. 'solana', 'stablecoin', 'ACR Poker', 'CFTC')",
            },
            category: {
              type: "string",
              description: "Optional category filter: 'payments', 'crypto-casinos', 'sportsbook', or 'press-releases'",
              enum: ["payments", "crypto-casinos", "sportsbook", "press-releases"],
            },
            limit: {
              type: "number",
              description: "Maximum number of results to return (default 5)",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "get_article_details",
        description: "Retrieves complete metadata, full body paragraphs, dateline, and photographic assets for a specific article.",
        inputSchema: {
          type: "object",
          properties: {
            slug_or_id: {
              type: "string",
              description: "Article slug (e.g. 'edx-markets-partners-paxos...') or ID (e.g. 'pr-241...')",
            },
          },
          required: ["slug_or_id"],
        },
      },
      {
        name: "verify_site_health",
        description: "Executes the rigorous 7-point site verification suite: image validation, AST JS syntax, zero AI disclosures, checksum immutability, and zero duplicate images.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "trigger_daily_publish",
        description: "Executes the automated wire news publisher pipeline on demand, syncing breaking press releases, pre-rendering HTML, updating sitemaps, and deploying to Vercel.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

// Handle tool executions
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "get_newsroom_metrics") {
      const { master, archive, combined } = getAllArticles();
      const now = new Date();
      const last24h = new Date(now.getTime() - 24 * 60 * 60 * 1000);
      const last48h = new Date(now.getTime() - 48 * 60 * 60 * 1000);

      const recent24h = master.filter(a => new Date(a.publishedAt) >= last24h);
      const recent48h = master.filter(a => new Date(a.publishedAt) >= last48h);

      const catCounts = {};
      combined.forEach(a => {
        const cat = a.primaryCategory || "other";
        catCounts[cat] = (catCounts[cat] || 0) + 1;
      });

      let gitCommit = "unknown";
      try {
        gitCommit = execSync("git log -1 --format='%h - %s (%cr)'", { cwd: PROJECT_ROOT }).toString().trim();
      } catch (e) {}

      const metrics = {
        totalArticles: combined.length,
        activeEditorialArticles: master.length,
        historicalWireArchiveArticles: archive.length,
        articlesLast24h: recent24h.length,
        articlesLast48h: recent48h.length,
        categories: catCounts,
        latestPublishedAt: master[0]?.publishedAt || "none",
        latestTitle: master[0]?.title || "none",
        archiveSitemaps: [
          "https://cryptocasinomedia.com/sitemap-archive-1.xml",
          "https://cryptocasinomedia.com/sitemap-archive-2.xml"
        ],
        latestCommit: gitCommit,
      };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(metrics, null, 2),
          },
        ],
      };
    }

    if (name === "search_articles") {
      const { combined } = getAllArticles();
      const q = (args.query || "").toLowerCase();
      const cat = args.category;
      const limit = args.limit || 5;

      const filtered = combined.filter(a => {
        if (cat && a.primaryCategory !== cat) return false;
        const inTitle = (a.title || "").toLowerCase().includes(q);
        const inSlug = (a.slug || "").toLowerCase().includes(q);
        const inCompany = (a.company || "").toLowerCase().includes(q);
        const inExcerpt = (a.excerpt || "").toLowerCase().includes(q);
        const inTopics = (a.topics || []).some(t => t.toLowerCase().includes(q));
        return inTitle || inSlug || inCompany || inExcerpt || inTopics;
      });

      const results = filtered.slice(0, limit).map(a => ({
        id: a.id,
        slug: a.slug,
        title: a.title,
        publishedAt: a.publishedAt,
        primaryCategory: a.primaryCategory,
        company: a.company,
        url: `https://cryptocasinomedia.com/press-releases/${a.slug}/`,
        excerpt: a.excerpt,
      }));

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ matchCount: filtered.length, returned: results.length, results }, null, 2),
          },
        ],
      };
    }

    if (name === "get_article_details") {
      const { combined } = getAllArticles();
      const target = (args.slug_or_id || "").trim();
      const article = combined.find(a => a.slug === target || a.id === target);

      if (!article) {
        return {
          isError: true,
          content: [
            {
              type: "text",
              text: `Article not found with slug or ID: '${target}'`,
            },
          ],
        };
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(article, null, 2),
          },
        ],
      };
    }

    if (name === "verify_site_health") {
      const output = execSync("python3 scripts/verify_site.py", {
        cwd: PROJECT_ROOT,
        encoding: "utf-8",
      });

      return {
        content: [
          {
            type: "text",
            text: output,
          },
        ],
      };
    }

    if (name === "trigger_daily_publish") {
      const output = execSync("/bin/bash scripts/run_daily_wire_publish.sh", {
        cwd: PROJECT_ROOT,
        encoding: "utf-8",
        timeout: 120000,
      });

      return {
        content: [
          {
            type: "text",
            text: output || "Execution complete. Check logs/daily_wire_cron.log for detailed trace.",
          },
        ],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: "text",
          text: `Error executing ${name}: ${error.message}\n${error.stdout || ""}\n${error.stderr || ""}`,
        },
      ],
    };
  }
});

async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("CryptoCasinoMedia Newsroom MCP Server running on stdio");
}

run().catch((error) => {
  console.error("Fatal error running MCP server:", error);
  process.exit(1);
});
