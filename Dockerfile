FROM node:20-alpine

WORKDIR /app

# Copy root manifests and server files
COPY package*.json ./
COPY vercel.json ./
COPY mcp-server ./mcp-server
COPY data ./data
COPY scripts ./scripts

# Install dependencies
RUN cd mcp-server && npm install --production

# Run the MCP server over stdio
CMD ["node", "mcp-server/server.js"]
