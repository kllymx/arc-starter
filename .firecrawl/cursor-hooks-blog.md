[Skip to content](https://cursor.com/blog/hooks-partners#main)

[Cursor](https://cursor.com/home)

- [Product](https://cursor.com/product) ↓




  - [Agents](https://cursor.com/product)
  - [Cloud](https://cursor.com/cloud)
  - [CLI](https://cursor.com/cli)
  - [Review](https://cursor.com/bugbot)
  - [Tab](https://cursor.com/tab)
  - [Marketplace ↗](https://cursor.com/marketplace)

- [Enterprise](https://cursor.com/enterprise)
- [Pricing](https://cursor.com/pricing)
- [Resources](https://cursor.com/changelog) ↓




  - [Changelog](https://cursor.com/changelog)
  - [Blog](https://cursor.com/blog)
  - [Docs](https://cursor.com/docs)
  - [Community](https://cursor.com/community)
  - [Help ↗](https://cursor.com/help)
  - [Workshops](https://cursor.com/workshops)
  - [Forum ↗](https://forum.cursor.com/)
  - [Careers](https://cursor.com/careers)

- Product →
- [Enterprise](https://cursor.com/enterprise)

- [Pricing](https://cursor.com/pricing)

- Resources →

[Sign in](https://cursor.com/dashboard) [ContactContact sales](https://cursor.com/contact-sales?source=navbar) [Download](https://cursor.com/download)

[Blog](https://cursor.com/blog)/ [product](https://cursor.com/blog/topic/product)

Dec 22, 2025· [product](https://cursor.com/blog/topic/product)

# Hooks for security and platform teams

![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Fmichael-felstein.jpeg&w=48&q=70)

![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Fmichael-scherr.png&w=48&q=70)

![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Ftravis-mcpeak-cropped.jpg&w=48&q=70)

Michael Feldstein, Michael Scherr & Travis McPeak · 2 min read

### Table of Contents

↑

- [Hooks partners](https://cursor.com/blog/hooks-partners#hooks-partners)
- [MCP governance and visibility](https://cursor.com/blog/hooks-partners#mcp-governance-and-visibility)
- [Code security and best practices](https://cursor.com/blog/hooks-partners#code-security-and-best-practices)
- [Dependency security](https://cursor.com/blog/hooks-partners#dependency-security)
- [Agent security and safety](https://cursor.com/blog/hooks-partners#agent-security-and-safety)
- [Secrets management](https://cursor.com/blog/hooks-partners#secrets-management)

Earlier this year, we released [hooks](https://cursor.com/docs/agent/hooks) for organizations to observe, control, and extend Cursor's agent loop using custom scripts. Hooks run before or after defined stages of the agent loop and can observe, block, or modify behavior.

We've seen many of our customers use hooks to connect Cursor to their security tooling, observability platforms, secrets managers, and internal compliance systems.

To make it easier to get started, we're partnering with ecosystem vendors who have built hooks support with Cursor.

## [\#](https://cursor.com/blog/hooks-partners\#hooks-partners) Hooks partners

Our partners cover MCP governance, code security, dependency scanning, agent safety, and secrets management.

### [\#](https://cursor.com/blog/hooks-partners\#mcp-governance-and-visibility) MCP governance and visibility

**MintMCP** uses beforeMCPExecution and afterMCPExecution hooks to build a complete inventory of MCP servers, monitor tool usage patterns, and scan responses for sensitive data before it reaches the AI model.

[Integrate MintMCP with Cursor ↗](https://www.mintmcp.com/blog/mcp-governance-cursor-hooks)

**Oasis Security** extends their Agentic Access Management platform to Cursor, using hooks to enforce least-privilege policies on AI agent actions and maintain full audit trails across enterprise systems.

[Integrate Oasis Security with Cursor ↗](https://www.oasis.security/blog/cursor-oasis-governing-agentic-access)

**Runlayer** uses hooks to wrap MCP tools and integrate with their MCP broker, giving organizations centralized control and visibility over all agent-to-tool interactions.

[Integrate Runlayer with Cursor ↗](https://www.runlayer.com/blog/cursor-hooks)

### [\#](https://cursor.com/blog/hooks-partners\#code-security-and-best-practices) Code security and best practices

**Corridor** provides real-time feedback to the agent on code implementation and security design decisions as code is being written.

[Integrate Corridor with Cursor ↗](https://corridor.dev/blog/corridor-cursor-hooks/)

**Semgrep** automatically scans AI-generated code for vulnerabilities using hooks, giving the agent real-time feedback to regenerate code until security issues are resolved.

[Integrate Semgrep with Cursor ↗](https://semgrep.dev/blog/2025/cursor-hooks-mcp-server)

### [\#](https://cursor.com/blog/hooks-partners\#dependency-security) Dependency security

**Endor Labs** uses hooks to intercept package installations and scan for malicious dependencies, preventing supply chain attacks like typosquatting and dependency confusion before they enter your codebase.

[Integrate Endor Labs with Cursor ↗](https://www.endorlabs.com/learn/bringing-malware-detection-into-ai-coding-workflows-with-cursor-hooks)

### [\#](https://cursor.com/blog/hooks-partners\#agent-security-and-safety) Agent security and safety

**Snyk** integrates Evo Agent Guard with hooks to review agent actions in real-time, detecting and preventing issues like prompt injection and dangerous tool calls.

[Integrate Snyk with Cursor ↗](https://snyk.io/blog/evo-agent-guard-cursor-integration/)

### [\#](https://cursor.com/blog/hooks-partners\#secrets-management) Secrets management

**1Password** uses hooks to validate that all required environment files from 1Password Environments are properly mounted before shell commands execute, enabling just-in-time secrets access without writing credentials to disk.

[Integrate 1Password with Cursor ↗](https://marketplace.1password.com/integration/cursor-hooks)

* * *

To deploy Cursor with enterprise features and priority support, [talk to our team](https://cursor.com/contact-sales?source=hooks-partners-blog).

If you want to submit your hook integration, please [fill out this form](https://docs.google.com/forms/d/e/1FAIpQLSd8iXLQqoUoFXngRrUv7YpBaBVJarKP3pYFY11kmX4BwoyTew/viewform).

Filed under: [product](https://cursor.com/blog/topic/product)

Authors: Michael Feldstein, Michael Scherr & Travis McPeak

## Related posts

[Mar 16, 2026·Product\\
\\
Securing our codebase with autonomous agents\\
\\
![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Ftravis-mcpeak-cropped.jpg&w=48&q=70)\\
\\
Travis McPeak · 5 min read](https://cursor.com/blog/security-agents)

[Feb 12, 2026·Product\\
\\
Expanding our long-running agents research preview\\
\\
![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Favatar-circle-2d-dark.png&w=48&q=70)![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Favatar-circle-2d-white.png&w=48&q=70)\\
\\
Cursor Team · 5 min read](https://cursor.com/blog/long-running-agents)

[Oct 1, 2025·Product\\
\\
Improving Java support in Cursor\\
\\
![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Favatar-circle-2d-dark.png&w=48&q=70)![](https://cursor.com/marketing-static/_next/image?url=https%3A%2F%2Fptht05hbb1ssoooe.public.blob.vercel-storage.com%2Fassets%2Favatars%2Favatar-circle-2d-white.png&w=48&q=70)\\
\\
Cursor Team · 1 min read](https://cursor.com/blog/java)

[View more posts →](https://cursor.com/blog)

### Product

- [Agents](https://cursor.com/en-US/product)
- [Teams](https://cursor.com/en-US/business/teams)
- [Enterprise](https://cursor.com/en-US/enterprise)
- [Pricing](https://cursor.com/en-US/pricing)
- [Code Review](https://cursor.com/en-US/bugbot)
- [Tab](https://cursor.com/en-US/tab)
- [CLI](https://cursor.com/en-US/cli)
- [Cloud Agents](https://cursor.com/agents)
- [Marketplace ↗](https://cursor.com/marketplace)

### Resources

- [Download](https://cursor.com/en-US/download)
- [Changelog](https://cursor.com/en-US/changelog)
- [Docs](https://cursor.com/docs)
- [Learn ↗](https://cursor.com/learn)
- [Forum ↗](https://forum.cursor.com/)
- [Help ↗](https://cursor.com/help)
- [Workshops](https://cursor.com/en-US/workshops)
- [Status ↗](https://status.cursor.com/)

### Company

- [Careers](https://cursor.com/en-US/careers)
- [Blog](https://cursor.com/en-US/blog)
- [Community](https://cursor.com/en-US/community)
- [Students](https://cursor.com/en-US/students)
- [Brand](https://cursor.com/en-US/brand)
- [Future](https://cursor.com/en-US/future)
- [Anysphere ↗](https://anysphere.inc/)

### Legal

- [Terms of Service](https://cursor.com/en-US/terms-of-service)
- [Privacy Policy](https://cursor.com/en-US/privacy)
- [Data Use](https://cursor.com/en-US/data-use)
- [Security](https://cursor.com/en-US/security)

### Connect

- [X ↗](https://x.com/cursor_ai)
- [LinkedIn ↗](https://www.linkedin.com/company/cursorai)
- [YouTube ↗](https://www.youtube.com/@cursor_ai)

© 2026 [Anysphere, Inc.](https://anysphere.inc/)🛡 [SOC 2 Certified](https://cursor.com/en-US/security)

🖥☉☾

🌐English↓

- English✓
- 简体中文
- 日本語
- 繁體中文
- Español
- Français
- Português
- 한국어
- Deutsch
- हिन्दी