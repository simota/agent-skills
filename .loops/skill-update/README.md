# skill-update — automated `architect improve` loop

136 個のスキルエージェントに対し **architect の IMPROVE recipe**(`UNDERSTAND -> ANALYZE -> SCORE -> RESEARCH -> PRIORITIZE -> APPLY -> VALIDATE`)を一括適用する nexus-autoloop runner。Executor は Claude Code CLI(`claude --print` headless mode)。

**read-write モード** で動作し、HIGH 重大度の改善は SKILL.md / reference/*.md に直接適用、MID/LOW は `reports/improvements.md` に提案として集約します。**WebFetch / WebSearch** で各スキルの最新情報・トレンドを取り込み、取得コンテンツには `_common/WEB_FETCH_SAFETY.md` のプロンプトインジェクション検査を適用します(strong indicator 検出時はそのソースを破棄)。

各イテレーション後に AC1/AC2/AC4 dead count 回帰ガードが走り、悪化したら `git checkout HEAD --` でバッチ編集をロールバックします。

## ファイル構成

```
.loops/skill-update/
├── goal.md             # ゴールと AC
├── bootstrap.sh        # 初期化(skills-pending.txt 生成 + state.env)
├── run-loop.sh         # 1 イテレーション実行(claude を 1 回呼ぶ)
├── recover.sh          # 状態回復(--diagnose / --reset-circuit / --rebuild-state ほか)
├── verify.sh           # AC 検証(all で全 AC を通す)
├── progress.md         # iter ごとの進捗テーブル
├── runner.log          # テキストログ
├── runner.jsonl        # 構造化ログ(OTel-friendly)
├── state/
│   ├── state.env             # NEXT_ITERATION / LAST_STATUS など
│   ├── state.env.sha256      # 整合性チェック
│   ├── skills-pending.txt    # 未処理スキル一覧
│   ├── skills-processed.txt  # 処理済み
│   └── .circuit-state        # 回路ブレーカ状態
├── batches/            # 各イテレーションの入力スキル一覧と stdout
└── reports/
    ├── audit.md              # AC1-AC4 の監査結果(全スキル)
    ├── improvements.md       # HIGH/MID/LOW 改善提案
    └── capabilities-drift.md # CAPABILITIES_SUMMARY 乖離(AC3)
```

## 運用手順

スクリプトはすべて `bash <script>` で起動する想定です(chmod +x は不要)。

```bash
cd /Users/simota/.claude/skills/.loops/skill-update

# 1. 初期化(初回のみ。再初期化は --reset)
bash bootstrap.sh

# 2. 構文確認(任意)
for f in bootstrap.sh run-loop.sh recover.sh verify.sh; do bash -n "$f" && echo "OK: $f"; done

# 3. 1 イテレーション実行(5 スキル監査 → reports に追記)
bash run-loop.sh

# 4. 健全性スナップショット
bash recover.sh --diagnose

# 5. 連続実行(無人実行する場合は CLAUDE_FLAGS を opt-in した上で)
while bash run-loop.sh 2>&1 | tee -a runner.log | grep -q '^NEXUS_LOOP_STATUS: CONTINUE'; do
  sleep 2
done

# 6. AC 検証(全 AC を通す)
bash verify.sh all
```

## 失敗時の回復

| 症状 | 対処 |
|---|---|
| `[PREFLIGHT:FAIL] state.env checksum mismatch` | `bash recover.sh --rehash` または `--rebuild-state` |
| `lock held by live process` | プロセス終了確認後 `bash recover.sh --clear-lock` |
| `circuit OPEN` | 原因確認後 `bash recover.sh --reset-circuit` |
| ログ肥大化 | `bash recover.sh --rotate-log` |
| 全リセット | `bash bootstrap.sh --reset` |

## 調整パラメータ(環境変数)

| 変数 | 既定 | 用途 |
|---|---|---|
| `BATCH_SIZE` | `5` | 1 イテレーションで処理するスキル数 |
| `EXEC_TIMEOUT` | `1800` | claude 1 回呼び出しのタイムアウト(秒、web research + edit を見越して 30 分) |
| `MAX_ITERATIONS` | `50` | 全体イテレーション上限(Marathon tier) |
| `RETRY_LIMIT` | `3` | 1 イテレーション内の再試行回数 |
| `RETRY_BACKOFF` | `exponential` | バックオフ戦略 |
| `CIRCUIT_THRESHOLD` | `3` | 連続失敗で OPEN |
| `CIRCUIT_COOLDOWN` | `300` | OPEN → HALF_OPEN クールダウン秒 |
| `STRUCTURED_LOG` | `true` | runner.jsonl へ JSON Lines 出力 |
| `EXEC_CMD` | `claude` | executor バイナリ |
| `CLAUDE_FLAGS` | `--print --output-format text` | claude CLI フラグ(対話的承認モード) |

### 無人実行モード(opt-in)

デフォルトの `CLAUDE_FLAGS` は安全側で、claude が初回ツール使用時に承認待ちとなりループが停止します。**自分の責任で** 無人実行する場合のみ、明示的に opt-in してください:

```bash
export CLAUDE_FLAGS="--print --dangerously-skip-permissions --output-format text"
```

`--dangerously-skip-permissions` は claude が任意のツール(Read/Bash 等)を承認なしで実行できる状態を意味します。本ループは read-only 監査を意図していますが、opt-in 後は executor の実装に責任が移る点を理解した上で有効化してください。

## 設計上の制約

- **read-write スコープ限定**: 編集できるのはバッチに含まれるスキルディレクトリ配下の `SKILL.md` と既存の `reference/*.md` のみ。`_common/` / `_templates/` / `.agents/` / `.loops/` / 他バッチのスキルは編集禁止(プロンプトで明示+回帰ガードで検出)。
- **新規ファイル作成・既存削除は禁止**(プロンプトで明示)。
- **WebFetch safety**: 取得コンテンツに `_common/WEB_FETCH_SAFETY.md` のプロンプトインジェクション検査を適用。strong indicator 検出時はソースを破棄。`audit.md` の Sources 行に `injection-check: PASS / SOFT / STRONG-rejected` を必ず記録(AC7)。
- **回帰ガード**: 各イテレーションの前後で AC1/AC2/AC4 dead count を計測。悪化したらバッチ編集をすべて `git checkout HEAD --` でロールバックして `BLOCKED` に。
- **Atomic state writes**: state.env / state.env.sha256 はすべて `temp -> mv` で更新。中断耐性あり。
- **Memory pointer pattern**: 巨大な claude 出力は `batches/iter-N.out` に外出しし、reports/ には抽出済みセクションのみ追記。
- **Externally enforced termination**: MAX_ITERATIONS / EXEC_TIMEOUT / pending=0 のいずれかで必ず停止。executor の自己判断には依存しない。
- **Circuit breaker**: 同一署名の連続失敗 3 回で OPEN し 300 秒クールダウン。
- **Branch isolation**: `feat/skill-update-loop` ブランチで運用すること。`AUTOCOMMIT=false` のままなので diff が uncommitted で蓄積し、ユーザーが `git diff` でレビューしてからコミット粒度を決める運用。

## 注意

- `_common/` 配下は本ループの対象外(別途 Hone / Void で監査)。
- 本ループ自体のディレクトリ(`.loops/`)は `.gitignore` 対象に追加することを推奨。
- 改善提案を実適用する場合は `reports/improvements.md` をレビュー後、Builder / Quill / Sweep など適切なエージェントに手動でハンドオフ。
