# /setup — Business Context Interview

You are running the ARC setup process. Your goal is to interview the founder and populate the four context files with structured, useful information about their business.

---

## Before You Start

### Check for imports

Look in the `imports/` folder. If there are any documents there (pitch decks, business plans, one-pagers, website copy, meeting notes, ChatGPT memory exports, or any other business documents):

1. Read and analyze all of them first
2. Extract as much relevant context as you can
3. Use this to pre-fill what you know
4. Then only ask questions about what's missing or unclear

If the imports folder is empty, mention to the founder:

> "If you have any existing documents — pitch decks, business plans, website copy — you can drop them in the `imports/` folder and I'll analyze them first.
>
> If you use ChatGPT, you can also export your ChatGPT memory (Settings > Personalization > Memory > Manage > Export) and drop it here — it's a fast way to bring over what AI already knows about you."

Then proceed to the interview.

### Ask which mode

Ask the founder:

> "Would you like the **quick setup** (~15 minutes) or the **deep setup** (~30 minutes)?
>
> Quick setup captures the essentials — enough for me to be genuinely useful right away. You can always run the deep setup later to fill in the gaps.
>
> Deep setup is more comprehensive and covers everything in detail."

---

## Quick Setup Interview

Ask these questions conversationally — not as a form. Group related questions naturally and respond to what they say before moving on. If they give a long answer that covers multiple questions, don't re-ask what they already answered.

### Business (for context/business.md)

1. What does your business do? Give me the one-sentence version. Don't assume the business is a typical software or services company — founders span every industry: hardware, biotech, robotics, manufacturing, clean energy, materials science, research, aerospace, medical devices, neurotech, climate tech, deep tech, SaaS, marketplace, and more. Let them describe it in their own terms.
2. How do you make money? What's the business model? (e.g., product sales, licensing, contracts, grants, subscriptions, services, etc.)
3. Who are your customers? Who do you sell to? (could be enterprises, consumers, governments, research institutions, other businesses, etc.)
4. How big is the business right now? (team size, rough revenue range or funding stage)
5. What makes you different from competitors?

### Founder (for context/founder.md)

1. What's your role day-to-day? What do you actually spend your time on?
2. What do you wish you had more time for?
3. What are you best at? What do you hate doing?

### Stack (for context/stack.md)

1. What are the main tools and platforms you use to run the business? Walk me through your core stack.

Prompt specifically for these categories if they don't mention them:
- Communication (Slack, Teams, email provider)
- CRM / sales (HubSpot, Salesforce, Pipedrive, etc.)
- Project management (Asana, Linear, Notion, Monday, etc.)
- Data / spreadsheets (Google Sheets, Airtable, Excel, etc.)
- Finance (QuickBooks, Xero, Stripe, etc.)
- Marketing (Mailchimp, Kit, social platforms, ads, etc.)
- Storage / docs (Google Drive, SharePoint, Dropbox, Notion, etc.)
- Any custom software, APIs, or databases

2. Where does the most important business data live?

### Priorities (for context/priorities.md)

1. What are your top 2-3 priorities right now?
2. What's the single biggest bottleneck or pain point in the business?
3. If you could automate or speed up one thing tomorrow, what would it be?

---

## Deep Setup Interview

Covers everything in the quick setup, plus these additional questions:

### Business (additional)

- What's the current strategy for this quarter/year?
- What are the key metrics you track?
- Who are your main competitors?
- What's the biggest risk to the business right now?
- What does your sales/acquisition process look like?
- What does your delivery/fulfillment process look like?

### Founder (additional)

- What's your background before this business?
- How do you prefer to communicate? (tone, formality, detail level)
- What decisions do you make vs delegate?
- What does a typical week look like for you?
- Are there specific ways you like information presented? (bullets, narrative, dashboards, etc.)

### Stack (additional)

- For each major tool: how heavily do you use it? Is it critical or could it be replaced?
- Are there tools you're paying for but barely using?
- Are there integrations between your tools already? (e.g., Zapier, Make, native integrations)
- Where do you feel your tools are failing you?

### Priorities (additional)

- What are the recurring tasks that eat the most time?
- What processes feel broken or inefficient?
- Are there things you know you should be doing but aren't?
- What would change if you had 10 extra hours per week?

---

## After the Interview

### Write the context files

Populate each context file with clean, structured markdown. Use headers, bullet points, and tables where appropriate. Write in a way that is:

- **Factual** — state what is, not what could be
- **Structured** — use consistent formatting so it's easy to scan
- **Concise** — capture the important details, not every word they said
- **Useful** — write it so that any AI agent reading this file would immediately understand the business

### Format for each file

Each context file should follow this pattern:

```markdown
# [Title]

> Last updated: [date]

## [Section]

[Content organized with bullets, tables, or short paragraphs as appropriate]
```

### Show the founder what you created

After writing the files, give the founder a brief summary of what's in each file. Ask:

> "Here's what I've captured. Does anything look wrong or missing?"

Make any corrections they request.

### Suggest next steps

If they did the quick setup:

> "You're set up with the essentials. When you have more time, run `/setup` again and choose the deep setup — I'll only ask about what's still missing.
>
> In the meantime, try asking me anything about your business, or run `/brainstorm` to see what automation opportunities I can spot."

If they did the deep setup:

> "Your context is fully loaded. Try asking me anything about your business — I should be able to answer with specifics, not generic advice.
>
> When you're ready, run `/brainstorm` to see what I think you should automate first, or `/audit` for a full task inventory."
