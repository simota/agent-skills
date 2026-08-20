# Bot Framework Patterns

## Command Parser

### Prefix-based Commands

```typescript
interface Command {
  name: string;
  aliases: string[];
  description: string;
  usage: string;
  args: CommandArg[];
  handler: CommandHandler;
}

interface CommandArg {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'user' | 'channel';
  required: boolean;
  description: string;
  default?: unknown;
}

type CommandHandler = (ctx: CommandContext) => Promise<void>;

interface CommandContext {
  message: UnifiedMessage;
  args: Record<string, unknown>;
  reply: (content: string) => Promise<void>;
  platform: PlatformType;
}

class CommandParser {
  private commands = new Map<string, Command>();
  private prefix: string;

  constructor(prefix = '!') {
    this.prefix = prefix;
  }

  register(command: Command): void {
    this.commands.set(command.name, command);
    for (const alias of command.aliases) {
      this.commands.set(alias, command);
    }
  }

  parse(content: string): { command: Command; args: Record<string, unknown> } | null {
    if (!content.startsWith(this.prefix)) return null;

    const parts = content.slice(this.prefix.length).trim().split(/\s+/);
    const commandName = parts[0]?.toLowerCase();
    if (!commandName) return null;

    const command = this.commands.get(commandName);
    if (!command) return null;

    const args = this.parseArgs(parts.slice(1), command.args);
    return { command, args };
  }

  private parseArgs(
    rawArgs: string[],
    argDefs: CommandArg[],
  ): Record<string, unknown> {
    const result: Record<string, unknown> = {};

    for (let i = 0; i < argDefs.length; i++) {
      const def = argDefs[i];
      const value = rawArgs[i];

      if (value === undefined) {
        if (def.required) throw new Error(`Missing required argument: ${def.name}`);
        result[def.name] = def.default;
        continue;
      }

      result[def.name] = this.coerce(value, def.type);
    }

    return result;
  }

  private coerce(value: string, type: CommandArg['type']): unknown {
    switch (type) {
      case 'number': return Number(value);
      case 'boolean': return ['true', '1', 'yes'].includes(value.toLowerCase());
      default: return value;
    }
  }
}
```

### Slash Commands (Discord/Slack Style)

```typescript
interface SlashCommand {
  name: string;
  description: string;
  options: SlashCommandOption[];
  handler: (interaction: Interaction) => Promise<void>;
}

interface SlashCommandOption {
  name: string;
  description: string;
  type: 'string' | 'integer' | 'boolean' | 'user' | 'channel' | 'role';
  required: boolean;
  choices?: { name: string; value: string | number }[];
}

// Registration (Discord example)
const commands: SlashCommand[] = [
  {
    name: 'remind',
    description: 'Set a reminder',
    options: [
      { name: 'message', description: 'Reminder text', type: 'string', required: true },
      { name: 'time', description: 'When (e.g., 30m, 2h)', type: 'string', required: true },
      { name: 'channel', description: 'Where to remind', type: 'channel', required: false },
    ],
    handler: async (interaction) => {
      // Handle slash command
    },
  },
];
```

## Conversation State Machine

```typescript
type ConversationState =
  | 'idle'
  | 'awaiting_input'
  | 'confirming'
  | 'processing'
  | 'completed'
  | 'error';

interface ConversationStep {
  state: ConversationState;
  prompt?: string;
  validate?: (input: string) => boolean;
  onInput: (input: string, ctx: ConversationContext) => Promise<ConversationState>;
  timeout?: number;
}

interface ConversationContext {
  userId: string;
  channelId: string;
  data: Record<string, unknown>;
  currentState: ConversationState;
  startedAt: Date;
  lastActivityAt: Date;
}

class ConversationManager {
  private conversations = new Map<string, ConversationContext>();
  private flows = new Map<string, Map<ConversationState, ConversationStep>>();

  registerFlow(name: string, steps: ConversationStep[]): void {
    const stepMap = new Map<ConversationState, ConversationStep>();
    for (const step of steps) {
      stepMap.set(step.state, step);
    }
    this.flows.set(name, stepMap);
  }

  async handleMessage(userId: string, message: string): Promise<string | null> {
    const conversation = this.conversations.get(userId);
    if (!conversation) return null; // No active conversation

    const flow = this.flows.get(conversation.data._flowName as string);
    if (!flow) return null;

    const step = flow.get(conversation.currentState);
    if (!step) return null;

    // Validate input
    if (step.validate && !step.validate(message)) {
      return `Invalid input. ${step.prompt}`;
    }

    // Process and transition
    const nextState = await step.onInput(message, conversation);
    conversation.currentState = nextState;
    conversation.lastActivityAt = new Date();

    if (nextState === 'completed' || nextState === 'error') {
      this.conversations.delete(userId);
    }

    const nextStep = flow.get(nextState);
    return nextStep?.prompt ?? null;
  }

  startConversation(
    userId: string,
    flowName: string,
    initialData?: Record<string, unknown>,
  ): string | null {
    const flow = this.flows.get(flowName);
    if (!flow) return null;

    this.conversations.set(userId, {
      userId,
      channelId: '',
      data: { ...initialData, _flowName: flowName },
      currentState: 'awaiting_input',
      startedAt: new Date(),
      lastActivityAt: new Date(),
    });

    const firstStep = flow.get('awaiting_input');
    return firstStep?.prompt ?? null;
  }
}
```

## Middleware Chain

```typescript
type BotMiddleware = (
  ctx: BotContext,
  next: () => Promise<void>,
) => Promise<void>;

interface BotContext {
  message: UnifiedMessage;
  platform: PlatformType;
  reply: (content: string) => Promise<void>;
  state: Record<string, unknown>;
}

class MiddlewareChain {
  private middlewares: BotMiddleware[] = [];

  use(middleware: BotMiddleware): this {
    this.middlewares.push(middleware);
    return this;
  }

  async execute(ctx: BotContext): Promise<void> {
    let index = 0;

    const next = async (): Promise<void> => {
      if (index >= this.middlewares.length) return;
      const middleware = this.middlewares[index++];
      await middleware(ctx, next);
    };

    await next();
  }
}

// Standard middleware stack
const bot = new MiddlewareChain()
  .use(logging)           // Log all messages
  .use(authentication)    // Verify user identity
  .use(rateLimit)         // Per-user rate limiting
  .use(commandParsing)    // Parse commands
  .use(conversationCheck) // Check active conversations
  .use(errorHandling);    // Catch and report errors
```

## Bot Architecture Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| Command Bot | Fixed command set with prefix/slash | Utility bots, admin tools |
| Conversational Bot | Multi-turn with state machine | Onboarding, forms, surveys |
| Reactive Bot | Event-driven responses | Notifications, monitoring |
| Hybrid Bot | Commands + conversation + events | Full-featured assistants |

## Platform-Specific Bot Patterns

### Slack App (Bolt.js v4+)

> **2025-2026 updates:**
> - Bolt for JavaScript v4.7.0 (2026) adds AI agent utilities: thinking status, streaming text, suggested prompts.
> - Slack MCP Server works with Bolt Frameworks.
> - Major agent frameworks (Claude Agent SDK, OpenAI Agents SDK, Pydantic AI, Vercel AI SDK) integrate with Bolt v4+.
> - Requires `agents:read` / `agents:write` scopes for agent features.
> - Source: [docs.slack.dev/tools/bolt-js/concepts/adding-agent-features](https://docs.slack.dev/tools/bolt-js/concepts/adding-agent-features/)

```typescript
import { App } from '@slack/bolt';

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

// Command handler
app.command('/remind', async ({ command, ack, respond }) => {
  await ack();
  await respond(`Reminder set: ${command.text}`);
});

// Message listener
app.message(/hello/i, async ({ message, say }) => {
  await say(`Hello <@${message.user}>!`);
});

// Interactive action
app.action('approve_button', async ({ body, ack, respond }) => {
  await ack();
  await respond('Approved!');
});

// AI agent response with streaming text (Bolt v4.7+)
// app.event('app_mention', async ({ event, client, say }) => {
//   const agent = client.agents.respond({ channel: event.channel, thread_ts: event.ts });
//   await agent.thinking(); // Show thinking indicator
//   const result = await myLLM(event.text);
//   await agent.stream(result); // Stream response tokens
// });
```

### Discord Bot (discord.js — API v10)

> **2025-2026 updates:**
> - Discord API v10 is current; always target `/api/v10`.
> - Components V2 (`IS_COMPONENTS_V2` flag `1 << 15`): enables Section, Container, Separator, Text Display — up to 40 components. Recommended for new apps.
> - Permission splits (Feb 23, 2026): PIN_MESSAGES required to pin; CREATE_EVENTS required for scheduled events.
> - Discord DAVE protocol (E2EE calls) mandatory March 1, 2026.
> - Source: [docs.discord.com/developers/change-log](https://docs.discord.com/developers/change-log)

```typescript
import { Client, GatewayIntentBits, SlashCommandBuilder, MessageFlags } from 'discord.js';

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'ping') {
    await interaction.reply('Pong!');
  }
});

// Components V2 example (recommended for new apps)
// await channel.send({
//   flags: MessageFlags.IsComponentsV2, // 1 << 15
//   components: [
//     { type: ComponentType.TextDisplay, content: 'Hello from Components V2!' },
//   ],
// });
```
