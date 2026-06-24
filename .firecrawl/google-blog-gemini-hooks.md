[![Google for Developers](https://storage.googleapis.com/gweb-developer-goog-blog-cms-assets/site/20260519-162827/images/g-dev.svg)](https://developers.google.com/)

[Community/Events](https://developers.google.com/community)

[Learn](https://developers.google.com/solutions/catalog)

[Blog](https://developers.googleblog.com/)

[YouTube](https://www.youtube.com/user/GoogleDevelopers)

Search


[![Google for Developers](https://storage.googleapis.com/gweb-developer-goog-blog-cms-assets/site/20260519-162827/images/g-dev.svg)](https://developers.google.com/)

- [Community/Events](https://developers.google.com/community)
- [Learn](https://developers.google.com/solutions/catalog)
- [Blog](https://developers.googleblog.com/)
- [YouTube](https://www.youtube.com/user/GoogleDevelopers)

# Tailor Gemini CLI to your workflow with hooks

JAN. 28, 2026

[Edi Palencia](https://developers.googleblog.com/search/?author=Edi+Palencia) Software Engineer

[Jack Wotherspoon](https://developers.googleblog.com/search/?author=Jack+Wotherspoon) Developer Advocate

[Abhi Patel](https://developers.googleblog.com/search/?author=Abhi+Patel) Software Engineer

Share

- [Facebook](https://www.facebook.com/sharer/sharer.php?u=https://developers.googleblog.com/tailor-gemini-cli-to-your-workflow-with-hooks/ "Share on Facebook")
- [Twitter](https://twitter.com/intent/tweet?text=https://developers.googleblog.com/tailor-gemini-cli-to-your-workflow-with-hooks/ "Share on Twitter")
- [LinkedIn](https://www.linkedin.com/shareArticle?url=https://developers.googleblog.com/tailor-gemini-cli-to-your-workflow-with-hooks/&mini=true "Share on LinkedIn")
- [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20https://developers.googleblog.com/tailor-gemini-cli-to-your-workflow-with-hooks/ "Send via Email")
- [Get shareable link](https://developers.googleblog.com/tailor-gemini-cli-to-your-workflow-with-hooks/# "Get shareable link")

![Gemini CLI Hooks hero image](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemini_CLI_Hooks_hero_image.original.png)

## Tailor Gemini CLI to your workflow with hooks

Efficiency in the age of agents isn't just about writing code faster; it's about building custom tools that adapt to your specific environment. Whether you need to inject custom project context, enforce strict security policies, or automate testing workflows, a one-size-fits-all agent often falls short.

That’s why we’re introducing **Gemini CLI hooks**, a powerful new way to _control_ and _customize_ the agentic loop, allowing you to tailor the behavior of Gemini CLI without ever having to touch its source code.

Sorry, your browser doesn't support playback for this video

## What are hooks?

Hooks are scripts or programs that Gemini CLI executes at specific, predefined points in its lifecycle. Think of them as "middleware" for your AI assistant. With hooks you can easily add custom logic that runs synchronously within the agent loop, giving you the ability to:

- **Add context:** Inject relevant information (like recent git commits, Jira tickets, or local documentation) before the model processes a request.
- **Validate actions:** Review and block potentially dangerous operations before they are executed. Continue iterating until specific requirements are met, improving model performance.
- **Enforce policies:** Implement organization-wide security and compliance requirements automatically.
- **Log and optimize:** Track tool usage and dynamically adjust tool selection to improve model accuracy and reduce token costs.
- **Notifications:** Get updates when Gemini CLI is idle, awaiting input or requires a tool confirmation.

By configuring hooks, you can customize Gemini CLI to your specific project. When an event fires, the CLI waits for your hook to complete before continuing, ensuring your custom logic is always respected. This opens the door for you to build on top of Gemini CLI in any way you see fit.

## A compelling example: Automated secret scanning

One of the most practical uses for hooks is creating a security safety net. With a **`BeforeTool`** hook, you can prevent the AI from accidentally writing sensitive data, like API keys or passwords, into your codebase.

To see all the available hook event types in Gemini CLI, reference the [official documentation](https://geminicli.com/docs/hooks/#hook-events).

**The hook script (.gemini/hooks/block-secrets.sh):**

```shell

```

Shell


Copied

**The configuration (.gemini/settings.json):**

```json

```

JSON


Copied

Now, whenever Gemini attempts to write or edit a file, the hooks script validates the content first. If a secret is detected, the operation is blocked, and the agent receives a clear explanation of why it was denied, allowing it to self-correct.

## Best practices for hooks

To ensure your hooks enhance your workflow without slowing you down, we recommend following a few key guidelines:

- **Keep hooks fast:** Because they run synchronously, any delay in your script will delay the agent’s response; use parallel operations and caching for expensive tasks.
- **Use specific matchers:** Instead of running a hook for every single tool, use the **`matcher`** property (e.g., **`"matcher": "write_file|replace"`**) to limit execution to relevant events.
- **Security first:** Hooks execute with your user privileges, so always review the source of project-level hooks before enabling them.

**Leverage the tooling:** Use the **`/hooks`** command to show all hooks and their status.

![Gemini CLI Hooks panel](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemini_CLI_Hooks_panel.original.png)

## Hooks in Gemini CLI extensions

The power of hooks isn't limited to your local configuration. [Gemini CLI extensions](https://geminicli.com/docs/extensions) now come with full support for hooks. Extension authors can bundle hooks directly within their extension, allowing users to install them with a single command and no manual configuration. See the [extensions documentation on hooks](https://geminicli.com/docs/extensions/#hooks) to learn more on how to add hooks to your extension.

Hooks support brings a new wave of what is possible with Gemini CLI extensions. One example being the [Ralph extension](https://github.com/gemini-cli-extensions/ralph), which implements the viral "Ralph loop” technique. By leveraging an **`AfterAgent`** hook, the extension intercepts the agent's completion signal and forces it into a continuous, iterative loop.

This allows Gemini CLI to persistently continue away at difficult tasks while automatically refreshing its context between attempts to prevent the context rot that often plagues long sessions. It transforms Gemini CLI from a reactive assistant into a tireless, autonomous worker that doesn't stop until the job is done.

Another example of an extension with hooks is a Gemini CLI team member's evolution of the “Ralph loop” technique which follows a more rigid, iterative software development lifecycle process (with a bit of character and humor). [View the extension here](https://geminicli.com/extensions/?name=galz10pickle-rick-extension).

## Get started

Hooks are enabled by default in Gemini CLI as of **v0.26.0+**. Update to the latest version by running:

```plaintext

```

Plain text


Copied

To dive deeper and start building your first hook, check out our official documentation:

- [**Introduction to hooks**](https://geminicli.com/docs/hooks/): An overview of the core concepts and events.
- [**Writing Your First hook**](https://geminicli.com/docs/hooks/writing-hooks): A comprehensive example.
- [**Hooks Technical Reference**](https://geminicli.com/docs/hooks/reference): Detailed input and output schemas for every event type.
- [**Best Practices & Security**](https://geminicli.com/docs/hooks/best-practices): Performance optimization and threat mitigation strategies.

Try it out today and let us know how you're tailoring Gemini CLI to your workflow on our [GitHub repository](https://github.com/google-gemini/gemini-cli) or on socials!

You can also follow [Gemini CLI on X](https://x.com/geminicli) to stay up to date with the latest news and announcements.

posted in:


- [AI](https://developers.googleblog.com/search/?technology_categories=AI)
- [Announcements](https://developers.googleblog.com/search/?content_type_categories=Announcements)
- [Learn](https://developers.googleblog.com/search/?tag=Learn)

[Previous](https://developers.googleblog.com/beyond-the-chatbot-a-blueprint-for-trustable-ai/) Previous

Next [Next](https://developers.googleblog.com/litert-the-universal-framework-for-on-device-ai/)

Related Posts

[![Build Cross-Language Multi-Agent Team with Google’s Agent Development Kit and A2A](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/banner.2e16d0ba.fill-800x400.jpg)\\
\\
AICloudAnnouncementsBest Practices\\
\\
Build Cross-Language Multi-Agent Team with Google’s Agent Development Kit and A2A\\
\\
JUNE 22, 2026](https://developers.googleblog.com/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/) [![How A2A is Building a World of Collaborative Agents](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/image2.original_6xqVyTd.2e16d0ba.fill-800x400.jpg)\\
\\
AICloudCase StudiesAnnouncements\\
\\
How A2A is Building a World of Collaborative Agents\\
\\
JUNE 18, 2026](https://developers.googleblog.com/how-a2a-is-building-a-world-of-collaborative-agents/) [![Measuring What Matters with Jules](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Measuring_What_Matters_with_Jules_.2e16d0ba.fill-800x400.png)\\
\\
WebAICase StudiesLearn\\
\\
Measuring What Matters with Jules\\
\\
JUNE 22, 2026](https://developers.googleblog.com/measuring-what-matters-with-jules/)

- Connect
   - [Blog](https://googledevelopers.blogspot.com/)
  - [Bluesky](https://goo.gle/3FReQXN)
  - [Instagram](https://goo.gle/googlefordevs)
  - [LinkedIn](https://goo.gle/gdevs-li)
  - [X (Twitter)](https://goo.gle/gdevs-tw)
  - [YouTube](https://goo.gle/developers)
- Programs
   - [Google Developer Program](https://developers.google.com/program)
  - [Google Developer Groups](https://developers.google.com/community/gdg)
  - [Google Developer Experts](https://developers.google.com/community/experts)
  - [Accelerators](https://developers.google.com/community/accelerators)
  - [Women Techmakers](https://www.womentechmakers.com/)
  - [Google Cloud & NVIDIA](https://developers.google.com/community/nvidia)
- Developer consoles
   - [Google API Console](https://console.developers.google.com/)
  - [Google Cloud Platform Console](https://console.cloud.google.com/)
  - [Google Play Console](https://play.google.com/apps/publish)
  - [Firebase Console](https://console.firebase.google.com/)
  - [Actions on Google Console](https://console.actions.google.com/)
  - [Cast SDK Developer Console](https://cast.google.com/publish)
  - [Chrome Web Store Dashboard](https://chrome.google.com/webstore/developer/dashboard)
  - [Google Home Developer Console](https://console.home.google.com/)

[![Google for Developers](https://storage.googleapis.com/gweb-developer-goog-blog-cms-assets/site/20260519-162827/images/g-dev.svg)](https://developers.google.com/)

- [Android](https://developer.android.com/)
- [Chrome](https://developer.chrome.com/home)
- [Firebase](https://firebase.google.com/)
- [Google Cloud Platform](https://cloud.google.com/)
- [All products](https://developers.google.com/products)
- Manage cookies


- [Terms](https://developers.google.com/terms/site-terms)
- [Privacy](https://policies.google.com/privacy)