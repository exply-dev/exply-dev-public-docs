# Exply.dev Public Documentation

Public documentation and API specifications for exply.dev platform services.

## 📚 Structure

- **`api/`** - OpenAPI specifications for public APIs
- **`docs/`** - General documentation and guides

## 🔌 Available APIs

### Exply GitHub Proxy MCP API

HTTP API for managing project proposals in the `exply-dev/exply-dev-public-projects` repository.

**OpenAPI Specification:**
- **File:** [`api/exply-github-proxy-api.json`](api/exply-github-proxy-api.json)
- **Raw URL:** https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-github-proxy-api.json
- **Service URL:** https://exply-github-proxy-kwftltj4yq-uc.a.run.app

**Usage in ChatGPT/Custom GPTs:**
1. Go to your GPT configuration → Actions
2. Add the OpenAPI schema URL:
   ```
   https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-github-proxy-api.json
   ```
3. The GPT will automatically discover available operations

**Available Operations:**
- `create_project_issue` - Create a new project proposal
- `update_project_issue` - Update an existing project proposal
- `get_project_issue` - Get details of a project proposal
- `list_project_issues` - List all project proposals

## 📖 Documentation

See [`docs/`](docs/) directory for detailed guides and documentation.

## 🔗 Related Repositories

- **Project Proposals:** [exply-dev/exply-dev-public-projects](https://github.com/exply-dev/exply-dev-public-projects)
- **Specifications:** [exply-dev/exply-dev-specs](https://github.com/exply-dev/exply-dev-specs)

## 📝 License

Public documentation - use freely for integration purposes.
