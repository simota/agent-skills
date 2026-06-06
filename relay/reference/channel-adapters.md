# Channel Adapter Patterns

## Adapter Interface

```typescript
interface ChannelAdapter<TPlatformMessage, TPlatformConfig> {
  readonly platform: PlatformType;

  // Lifecycle
  initialize(config: TPlatformConfig): Promise<void>;
  shutdown(): Promise<void>;
  healthCheck(): Promise<HealthStatus>;

  // Inbound: Platform → Unified
  normalizeMessage(raw: TPlatformMessage): UnifiedMessage;
  normalizeEvent(raw: unknown): UnifiedEvent;

  // Outbound: Unified → Platform
  adaptMessage(unified: UnifiedMessage): TPlatformMessage;
  send(channelId: string, message: UnifiedMessage): Promise<SendResult>;

  // Platform capabilities
  supports(feature: PlatformFeature): boolean;
}

type PlatformType = 'slack' | 'discord' | 'telegram' | 'whatsapp' | 'line' | 'teams';

type PlatformFeature =
  | 'threads'
  | 'reactions'
  | 'rich_embeds'
  | 'buttons'
  | 'file_upload'
  | 'voice'
  | 'video'
  | 'ephemeral'
  | 'scheduled_messages'
  | 'message_editing'
  | 'message_deletion';
```

## Unified Message Format

```typescript
// Discriminated union for message types
type UnifiedMessage =
  | TextMessage
  | RichMessage
  | InteractiveMessage
  | FileMessage
  | SystemMessage;

interface BaseMessage {
  id: string;
  timestamp: Date;
  channelId: string;
  userId: string;
  platform: PlatformType;
  threadId?: string;
  metadata: Record<string, unknown>;
}

interface TextMessage extends BaseMessage {
  type: 'text';
  content: string;
  mentions: Mention[];
}

interface RichMessage extends BaseMessage {
  type: 'rich';
  blocks: MessageBlock[];
  fallbackText: string;
}

interface InteractiveMessage extends BaseMessage {
  type: 'interactive';
  components: InteractiveComponent[];
  callbackId: string;
}

interface FileMessage extends BaseMessage {
  type: 'file';
  files: FileAttachment[];
  caption?: string;
}

interface SystemMessage extends BaseMessage {
  type: 'system';
  event: SystemEventType;
  data: Record<string, unknown>;
}
```

## SDK Comparison Matrix

| Platform | SDK | Package | Stars | Strengths | Weaknesses |
|----------|-----|---------|-------|-----------|------------|
| Slack | Bolt.js v4 | `@slack/bolt` | 2.7k+ | Official, event-driven, middleware, AI agent features (v4.7+) | Slack-only, opinionated |
| Slack | WebClient | `@slack/web-api` | - | Low-level control | Manual event handling |
| Discord | discord.js | `discord.js` | 25k+ | Feature-rich, well-maintained, Components V2 support | Large dependency |
| Discord | Eris | `eris` | 1.4k | Lightweight | Less features, slower Components V2 adoption |
| Telegram | grammY | `grammy` | 2k+ | TypeScript-first, middleware | Telegram-only |
| Telegram | node-telegram-bot-api | `node-telegram-bot-api` | 8k+ | Simple, popular | Callback-based |
| WhatsApp | Baileys | `@whiskeysockets/baileys` | 4k+ | Reverse-engineered, full access | Unofficial, risk of breakage |
| WhatsApp | Cloud API | `whatsapp-business-api` | - | Official, stable | Limited features, cost |
| LINE | LINE SDK | `@line/bot-sdk` | 400+ | Official, LIFF v2.28+ (requestFriendship, 2026) | Limited ecosystem |
| Teams | Bot Framework | `botbuilder` | 4k+ | Microsoft official, Adaptive Cards support | Complex, heavy; new multi-tenant bot registrations discontinued after July 31, 2025 |

> **Deprecation notes (2025-2026):**
> - Slack RTM API: **legacy** — new apps must use Events API or Socket Mode. Source: [docs.slack.dev/legacy/legacy-rtm-api](https://docs.slack.dev/legacy/legacy-rtm-api/)
> - Slack classic apps: discontinued **November 16, 2026**. Legacy custom bots: stopped **March 31, 2025**. Source: [docs.slack.dev/changelog/2024-09-legacy-custom-bots-classic-apps-deprecation](https://docs.slack.dev/changelog/2024-09-legacy-custom-bots-classic-apps-deprecation/)
> - Discord API: current version is **v10**; always target `/api/v10`. Source: [docs.discord.com/developers/reference](https://docs.discord.com/developers/reference)
> - Microsoft Teams: new multi-tenant bot registrations discontinued after **July 31, 2025**. Source: [learn.microsoft.com/microsoftteams/platform](https://learn.microsoft.com/en-us/microsoftteams/platform/)

## SDK Selection Decision Tree

```
Need official support + stability?
├── Yes → Official SDK (Bolt, Cloud API, LINE SDK, Bot Framework)
└── No
    ├── Need maximum features?
    │   ├── Yes → Community SDK (discord.js, Baileys)
    │   └── No → Lightweight SDK (Eris, WebClient)
    └── TypeScript-first priority?
        ├── Yes → grammY (Telegram), discord.js v14+ (Discord)
        └── No → node-telegram-bot-api, simpler options
```

## Platform Feature Matrix

| Feature | Slack | Discord | Telegram | WhatsApp | LINE | Teams |
|---------|-------|---------|----------|----------|------|-------|
| Text messages | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rich formatting | Blocks (Block Kit) | Embeds + Components V2 | HTML/MD | Limited | Flex Message | Adaptive Cards |
| Buttons/Actions | ✅ | ✅ Components V2 | Inline KB | Buttons | Quick Reply | ✅ |
| Threads | ✅ | ✅ | Reply-to | ✅ | ❌ | ✅ |
| Reactions | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| File uploads | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ephemeral msgs | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Slash commands | ✅ | ✅ | Bot commands | ❌ | ❌ | Commands |
| Message editing | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Webhooks inbound | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| WebSocket | ✅ (Socket Mode) | ✅ (Gateway v10) | ❌ (polling) | ❌ | ❌ | ❌ |
| AI/LLM agent support | ✅ (Bolt v4.7+) | ❌ native | ❌ | ❌ | ❌ | ✅ (Copilot) |
| Rate limits | Tier-based (non-Marketplace restricted from Mar 2026) | 50 req/s global + per-route X-RateLimit-Bucket | 30 msg/sec | Varies | 100k/min | Varies |

> **Discord Components V2 (2025):** Use `IS_COMPONENTS_V2` message flag (`1 << 15`) to enable Section, Container, Separator, Text Display components. Up to 40 components per message. When flag is set, `content` and `embeds` fields are disabled. Recommended for all new Discord apps. Source: [docs.discord.com/developers/components/reference](https://docs.discord.com/developers/components/reference)

## Normalization Patterns

### Inbound Normalization (Platform → Unified)

```typescript
// Pattern: Normalizer per platform
class SlackNormalizer implements MessageNormalizer<SlackEvent> {
  normalize(event: SlackEvent): UnifiedMessage {
    switch (event.type) {
      case 'message':
        return this.normalizeTextMessage(event);
      case 'block_actions':
        return this.normalizeInteraction(event);
      case 'file_shared':
        return this.normalizeFile(event);
      default:
        return this.normalizeSystem(event);
    }
  }

  private normalizeTextMessage(event: SlackMessageEvent): TextMessage {
    return {
      id: event.ts,
      type: 'text',
      timestamp: new Date(parseFloat(event.ts) * 1000),
      channelId: event.channel,
      userId: event.user,
      platform: 'slack',
      threadId: event.thread_ts,
      content: this.convertSlackMarkdown(event.text),
      mentions: this.extractMentions(event.text),
      metadata: { raw: event },
    };
  }
}
```

### Outbound Adaptation (Unified → Platform)

```typescript
// Pattern: Adapter per platform
class SlackAdapter implements OutboundAdapter<SlackMessage> {
  adapt(message: UnifiedMessage): SlackMessage {
    switch (message.type) {
      case 'text':
        return { text: this.toSlackMarkdown(message.content) };
      case 'rich':
        return { blocks: this.toSlackBlocks(message.blocks) };
      case 'interactive':
        return { blocks: this.toSlackInteractive(message.components) };
      default:
        return { text: message.fallbackText ?? '[Unsupported message type]' };
    }
  }
}
```

## Multi-Channel Router

```typescript
class MessageRouter {
  private adapters = new Map<PlatformType, ChannelAdapter>();

  register(adapter: ChannelAdapter): void {
    this.adapters.set(adapter.platform, adapter);
  }

  async send(
    targets: { platform: PlatformType; channelId: string }[],
    message: UnifiedMessage,
  ): Promise<Map<string, SendResult>> {
    const results = new Map<string, SendResult>();

    await Promise.allSettled(
      targets.map(async ({ platform, channelId }) => {
        const adapter = this.adapters.get(platform);
        if (!adapter) {
          results.set(`${platform}:${channelId}`, {
            success: false,
            error: `No adapter registered for ${platform}`,
          });
          return;
        }
        const result = await adapter.send(channelId, message);
        results.set(`${platform}:${channelId}`, result);
      }),
    );

    return results;
  }
}
```
