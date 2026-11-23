# CryptoCasinoMedia Newsroom & Operations MCP Server

[![thomashjkim/Cryptocasinomedia MCP server](https://glama.ai/mcp/servers/thomashjkim/Cryptocasinomedia/badges/score.svg)](https://glama.ai/mcp/servers/thomashjkim/Cryptocasinomedia)
[![Smithery](https://smithery.ai/badge/@thomashjkim/Cryptocasinomedia)](https://smithery.ai/server/@thomashjkim/Cryptocasinomedia)
[![MCP](https://img.shields.io/badge/MCP-Standard%202025--12--11-blue)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Model Context Protocol (MCP) server for **CryptoCasinoMedia** (`https://cryptocasinomedia.com`). Connect your AI assistants (Claude, Cursor, Antigravity, Windsurf) directly to live crypto casino & iGaming journalism datasets, search engines, editorial health verification, and wire dispatch pipelines.

---

## 🛠️ Provided Tools

1. **`get_newsroom_metrics`**
   - Returns real-time newsroom statistics: total master articles, 24h & 48h publication counts, category distributions, and repository sync state.
2. **`search_articles`**
   - Instant search across 244+ verified news stories, regulatory filings, and guides by query, company name, category, or topic tags.
3. **`get_article_details`**
   - Retrieves full article body, editorial metadata, high-resolution wire photo URI, dateline, and category classifications by slug or article ID.
4. **`verify_site_health`**
   - Runs pre-flight site verification suite (`scripts/verify_site.py`), including article deduplication, image integrity, canonical URL audits, and schema checks.
5. **`trigger_daily_publish`**
   - Triggers the automated daily wire publishing workflow, building new feeds, sitemaps, and triggering edge deployment on demand.

---

## 🚀 Quickstart & Installation

### Option 1: Smithery CLI (Fastest)

```bash
npx -y @smithery/cli install @thomashjkim/Cryptocasinomedia
```

### Option 2: Claude Desktop Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cryptocasinomedia-newsroom": {
      "command": "node",
      "args": ["/Users/thomaskim/Cryptocasinomedia/mcp-server/server.js"]
    }
  }
}
```

### Option 3: Cursor / Windsurf Configuration

In `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "cryptocasinomedia-newsroom": {
      "command": "node",
      "args": ["/Users/thomaskim/Cryptocasinomedia/mcp-server/server.js"]
    }
  }
}
```

---

## 📄 License
MIT © [CryptoCasinoMedia](https://cryptocasinomedia.com)
