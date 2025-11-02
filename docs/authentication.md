# Authentication & Authorization

This document explains how authentication and authorization work in the Exply.dev Platform API.

## Overview

The API supports **optional authentication** via GitHub tokens. Authentication is:
- **Optional** for creating resources (issues, profiles)
- **Required** for updating resources (only creators can update their own resources)
- **Optional** for reading resources (all public resources are readable)

## Authentication Methods

### Method 1: GitHub Personal Access Token (PAT)

**Recommended for GPT Actions**

1. Get a GitHub Personal Access Token:
   - Go to: https://github.com/settings/tokens
   - Create token with `public_repo` scope
   - Copy the token (starts with `ghp_...`)

2. Configure in GPT Actions:
   - When setting up the action, you can add authentication
   - Use **API Key** type
   - Token format: `ghp_xxxxxxxxxxxxx` or `Bearer ghp_xxxxxxxxxxxxx`

3. Token is sent automatically in `Authorization` header:
   ```
   Authorization: Bearer ghp_xxxxxxxxxxxxx
   ```

### Method 2: OAuth (Future)

Currently in specification but not yet implemented in full. Will support GitHub OAuth flow for web applications.

## Authorization Rules

### Creating Resources

- **Without auth:** Resource is created, creator is set to GitHub issue author (if created via GitHub API directly)
- **With auth:** Resource is created with creator metadata stored in hidden comment: `<!-- Creator: username -->`

### Updating Resources

**Strict ownership check:**
1. User must provide valid GitHub token
2. System verifies token and gets GitHub username
3. System checks if username matches resource creator
4. Update allowed only if creator matches

**Methods of verification:**
- Check GitHub issue creator (`issue.user.login`)
- Check metadata comment in body (`<!-- Creator: username -->`)
- For expert profiles: Check filename matches username or metadata comment

### Reading Resources

- All public resources are readable without authentication
- No authorization checks for read operations

## Ownership Verification

### For Project Issues

1. Check `issue.user.login` (original GitHub creator)
2. Check metadata comment: `<!-- Creator: username -->` in issue body
3. Match against authenticated user's GitHub username

### For Expert Profiles

1. Check metadata comment: `<!-- Creator: username -->` in file content
2. Fallback: Check if filename matches username (e.g., `john-doe.md` → `john-doe`)
3. Match against authenticated user's GitHub username

## Error Responses

### 401 Unauthorized
```
{
  "error": "Invalid or expired authentication token"
}
```

### 403 Forbidden
```
{
  "error": "You don't have permission to update this issue. Only the creator can update it."
}
```

## Security Notes

- **GitHub tokens are never stored** - passed through but not logged
- **Creator metadata is hidden** - stored in HTML comments, not visible in rendered markdown
- **Public resources** - anyone can read, but only creators can update
- **Rate limiting** - follows GitHub API rate limits

## Best Practices

1. **For GPT Actions:**
   - Use API Key authentication method
   - Store token securely (GPT handles this)
   - Token should have minimal required scopes (`public_repo`)

2. **For web applications:**
   - Use OAuth flow (when implemented)
   - Never expose tokens in frontend code
   - Use server-side token exchange

3. **For automated scripts:**
   - Use Personal Access Tokens
   - Store tokens in environment variables
   - Rotate tokens periodically

## Example Flow

1. **Create issue (with auth):**
   ```bash
   POST /create_project_issue
   Authorization: Bearer ghp_xxxxx
   {
     "title": "My Project",
     "body": "Description"
   }
   ```
   → Issue created with `<!-- Creator: username -->` metadata

2. **Update issue (with auth):**
   ```bash
   POST /update_project_issue
   Authorization: Bearer ghp_xxxxx
   {
     "issueNumber": 1,
     "body": "Updated description"
   }
   ```
   → System checks: authenticated user matches creator → Update allowed

3. **Update issue (wrong user):**
   ```bash
   POST /update_project_issue
   Authorization: Bearer ghp_xxxxx  # Different user's token
   {
     "issueNumber": 1,
     "body": "Updated description"
   }
   ```
   → System checks: authenticated user doesn't match creator → **403 Forbidden**

