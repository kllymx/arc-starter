[Return to Amp](https://ampcode.com/)

[Chronicle](https://ampcode.com/chronicle)//\[News\] Custom Agents

June 19, 2026

# Custom Agents

You can now create custom agents in Amp with plugins.

You can use these custom agents as your main Amp agent, or as subagents. You can
use them as a small part of a tool pipeline that you invoke with `amp -x`. Or
you can spawn 25 custom worker agents, then switch between them.

Each custom agent comes with a custom orb color.

Here is how you define a custom agent in an Amp plugin:

```ts
// .amp/plugins/focused-reviewer-agent.ts
import type { PluginAPI } from '@ampcode/plugin'

export default function (amp: PluginAPI) {
	// Create the agent
	const reviewer = amp.createAgent({
		name: 'focused-reviewer',
		model: 'openai/gpt-5.5',
		instructions: [\
			'You are a focused code-review subagent.',\
			'Inspect only the files and concerns named by the caller.',\
			'Return concise findings with severity, evidence, and suggested fixes.',\
		].join(' '),
		tools: 'all',
		display: { label: 'reviewer', color: '#d97706' },
	})

	// Register a tool. This agent acts as a subagent
	amp.registerTool({
		name: 'focused_review',
		description: 'Run a focused code-review subagent.',
		inputSchema: {
			type: 'object',
			properties: {
				request: { type: 'string' },
			},
			required: ['request'],
		},

		async execute(input, ctx) {
			// Run a one-shot agent turn
			const result = await reviewer.run(input, {
				parentThreadID: ctx.thread.id,
			})
			return result.text
		},
	})

	// Or register the agent as a selectable main thread mode
	amp.registerAgentMode({
		key: 'focused-reviewer',
		description: 'Code Review Expert',
		agent: reviewer.definition,
	})
}
```

## Threads

Once you have defined an agent, you can create threads:

```ts
// Spawn a new thread
const thread = await reviewer.createThread({
	// Tell the UI switch to this thread
	show: true,
})

// Get an existing thread
const thread = amp.threads.get(input.threadID)
```

The `Thread` object lets you interact with a thread in many different ways, and
is where the real power comes in.

### Send a message to a Thread

Add a new user message to a thread by calling `thread.appendUserMessage()`. The
call returns as soon as Amp has accepted the message; it does not wait for
inference to complete before returning.

```ts
await thread.appendUserMessage({
	type: 'user-message',
	content: 'Review the auth changes in this branch.',
})
```

### Wait for the Agent's response

When you do want to wait, call `waitForResponse()` on the thread. It resolves
with the next assistant message after the agent finishes its turn.

```ts
const reply = await thread.waitForResponse()
```

## Example: Spawn an async thread that responds to the main thread

These are just a few primitives provided by the Plugin API. Together, they
compose into unique workflows. An example used on the Amp team: spawn an agent
in an asynchronous thread, and give it the tools it needs to respond to the
parent when it needs to.

```ts
amp.registerTool({
	name: 'start_async_review',
	description: 'Start a review in a background thread.',
	inputSchema: { type: 'object', properties: {} },
	async execute(_input, ctx) {
		const thread = await reviewer.createThread({
			parentThreadID: ctx.thread.id,
		})

		await thread.appendUserMessage({
			type: 'user-message',
			content: [\
				'Review the auth changes in this branch.',\
				`When you are done, call send_to_thread with threadID ${ctx.thread.id}`,\
				'and include your review in the message.',\
			].join(' '),
		})

		return `Started background review in ${thread.id}.`
	},
})
```

Full documentation is [in the manual](https://ampcode.com/manual/plugin-api). Happy Hacking.

- [All Systems Operational](https://ampcodestatus.com/)
- [Security](https://ampcode.com/security)
- [Privacy Policy](https://ampcode.com/privacy-policy)
- [Terms of Service](https://ampcode.com/terms)

### Product

- [Get Started](https://ampcode.com/auth/sign-up)
- [Sign In](https://ampcode.com/auth/sign-in)
- [Owner's Manual](https://ampcode.com/manual)
- [Models](https://ampcode.com/models)

### Resources

- [Chronicle](https://ampcode.com/chronicle)
- [Pricing](https://ampcode.com/pricing)
- [Podcast](https://ampcode.com/podcast)
- [Press Kit](https://ampcode.com/press-kit)

### Guides

- [How to Build an Agent](https://ampcode.com/how-to-build-an-agent)
- [Context Management](https://ampcode.com/guides/context-management)

### Community

- [𝕏 @ampcode](https://x.com/ampcode)
- [Amp Insiders](https://ampcode.com/insiders)
- [YouTube](https://www.youtube.com/@Sourcegraph/videos)