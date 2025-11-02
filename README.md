# Exply.dev Public Documentation

Public documentation and API specifications for exply.dev platform services.

## 📚 Structure

- **`api/`** - OpenAPI specifications for public APIs
- **`docs/`** - General documentation and guides

## 🔌 Available APIs

### Exply Project Proposals API

HTTP API for managing project proposals in the `exply-dev/exply-dev-public-projects` repository.

**OpenAPI Specification (REST API):**
- **File:** [`api/exply-project-proposals-api.json`](api/exply-project-proposals-api.json)
- **Raw URL:** https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-project-proposals-api.json
- **Service URL:** https://exply-github-proxy-kwftltj4yq-uc.a.run.app

**Usage in ChatGPT/Custom GPTs:**
1. Go to your GPT configuration → Actions
2. Add the OpenAPI schema URL:
   ```
   https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/api/exply-project-proposals-api.json
   ```
3. The GPT will automatically discover available operations

**Available Operations:**
- `create_project_issue` - Create a new project proposal
- `update_project_issue` - Update an existing project proposal (title, body, or state)
- `get_project_issue` - Retrieve details of a specific project proposal issue
- `list_project_issues` - List all project proposal issues (with filters for state, label, and limit)
- `get_labels` - Retrieve all repository labels
- `create_label` - Create a new repository label (with duplicate checking)

## 📖 Documentation

See [`docs/`](docs/) directory for detailed guides and documentation.

## 🔗 Related Repositories

- **Project Proposals:** [exply-dev/exply-dev-public-projects](https://github.com/exply-dev/exply-dev-public-projects)
- **Specifications:** [exply-dev/exply-dev-specs](https://github.com/exply-dev/exply-dev-specs)

## 📝 License

Public documentation - use freely for integration purposes.

## 🔒 Privacy Policy

Our Privacy Policy explains how we handle information when you use exply.dev services:
- [Privacy Policy](PRIVACY.md)
- [Raw URL](https://raw.githubusercontent.com/exply-dev/exply-dev-public-docs/main/PRIVACY.md)

Use this URL when configuring GPT Actions that require a privacy policy link.
