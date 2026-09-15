# Auth.md

Registration instructions for AI agents and automated clients connecting to CryptoCasinoMedia.

## Agent Registration

CryptoCasinoMedia provides open access and automated registration metadata for AI agents and LLM clients.

### Registration Endpoint
- Registration URL: https://cryptocasinomedia.com/about/
- Documentation: https://cryptocasinomedia.com/llms.txt

### Supported Identity & Authentication Types
- `public`: Open access to all intelligence content and regulatory guides.
- `bearer`: Bearer token authorization for high-frequency API access.

### Authorization Server
- Issuer: https://cryptocasinomedia.com
- Discovery: https://cryptocasinomedia.com/.well-known/oauth-authorization-server
- Protected Resource: https://cryptocasinomedia.com/.well-known/oauth-protected-resource

### Instructions for Agents
1. Fetch the knowledge catalog from https://cryptocasinomedia.com/.well-known/ai-catalog.json.
2. Access structured LLM markdown data from https://cryptocasinomedia.com/llms.txt.
3. No credentials required for standard public intelligence retrieval.
