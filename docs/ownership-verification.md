# Ownership Verification Mechanism

## How Creator Information is Stored

### For Project Issues

Creator information is stored in a **hidden HTML comment** at the end of the issue body:

```markdown
### New Project Proposal
...

<!-- Creator: vlad-exply -->
```

**Where to find it:**
- GitHub UI: Not visible (HTML comments are hidden)
- GitHub API: Visible in `issue.body`
- Raw markdown: Visible when editing

### For Expert Profiles

Creator information is stored in a **hidden HTML comment** at the end of the MD file:

```markdown
# John Doe - Full-Stack Engineer

...

<!-- Creator: john-doe -->
```

**File location:** `exply-dev-public-experts/experts/john-doe.md`

## How Identification Works When User Returns

### Problem
ChatGPT doesn't persist user identity between sessions automatically. When a user opens "Свой GPT" again, we need to identify them.

### Solution: Two Methods

#### Method 1: GitHub Token (Preferred - More Secure)
1. User provides GitHub Personal Access Token in GPT Actions configuration
2. Token is sent in `Authorization: Bearer ghp_...` header
3. System verifies token → gets GitHub username
4. Compares with stored `<!-- Creator: username -->`
5. If matches → allows update

**Pros:**
- ✅ Secure (token verification)
- ✅ Cannot be spoofed
- ✅ Works automatically once configured

**Cons:**
- ❌ User must configure token in GPT Actions
- ❌ Token management complexity

#### Method 2: GitHub Username (Fallback - Works Without Token)
1. User provides GitHub username during creation
2. Username is stored in metadata
3. When updating, user provides username again
4. System verifies username exists via GitHub API (public)
5. Compares with stored creator
6. If matches → allows update

**Pros:**
- ✅ Works without token configuration
- ✅ Simple for users (just username)
- ✅ No security tokens to manage

**Cons:**
- ⚠️ Less secure (anyone can claim a username)
- ⚠️ User must provide username each time

## Current Implementation

### When Creating Resource

**For Projects:**
1. Agent asks for GitHub username (if not provided)
2. Calls `create_project_issue` with `githubUsername` parameter
3. Backend stores: `<!-- Creator: username -->` in issue body

**For Expert Profiles:**
1. Agent extracts username from GitHub profile link (if provided)
2. If not, asks: "What is your GitHub username?"
3. Calls `create_expert_profile` with `githubUsername` parameter
4. Backend stores: `<!-- Creator: username -->` in MD file

### When Updating Resource

**Backend checks ownership:**
1. Looks for `Authorization` header (token)
   - If present: verifies token → gets username
2. Else looks for `githubUsername` in request body
   - If present: verifies username exists
3. Reads resource (issue/profile)
4. Extracts `<!-- Creator: username -->`
5. Compares username with creator
6. Allows update only if match

## Limitations

**Current limitation:**
ChatGPT doesn't remember user identity between sessions. Each time user opens GPT:
- Option 1: User must have configured their GitHub PAT in Actions (shared for all users)
- Option 2: Agent must ask for username again

**Future improvement:**
- Store username in GPT's conversation context (if possible)
- Or implement OAuth flow through GitHub App
- Or use ChatGPT's built-in user identification (if available)

## Verification Flow Diagram

```
Create Resource:
  User → Agent → API (with githubUsername)
              → Store: <!-- Creator: username -->

Update Resource:
  User → Agent → API (with token OR githubUsername)
              → Read resource
              → Extract <!-- Creator: username -->
              → Compare with provided username
              → Allow/Deny
```

## Security Notes

- **Hidden comments** are not visible in GitHub UI (HTML comments)
- **Username verification** checks that username exists (via GitHub API)
- **Token verification** is more secure (cannot be spoofed)
- **Public resources** are readable by anyone, but only creators can update

