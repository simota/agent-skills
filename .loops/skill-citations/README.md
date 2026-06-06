# skill-citations — citation-application loop

22 個のスキルに対し、`skill-update` ループの IMPROVE pass で挙がった Source citation MID 提案を実際に SKILL.md / reference/*.md に適用する小ループ。

## 仕組み

- Input: `citations-todo.md`(`skill-update/reports/improvements.md` から抽出した citation 提案)
- Per iter: 4 スキル × `claude --print` で WebFetch → URL 確認 → Source citation 追加
- Per fetch: `_common/WEB_FETCH_SAFETY.md` 検査(strong indicator はソース破棄)
- Per iter 後: skill-update の verify.sh を借りて AC1/AC2/AC4 dead count を計測、悪化したらバッチをロールバック

## 運用

```bash
cd /Users/simota/.claude/skills/.loops/skill-citations

bash bootstrap.sh                       # 初期化(skills-pending.txt に 22 件)
bash run-loop.sh                        # 1 iter ずつ手動実行
bash run-all.sh --unattended            # 無人モード(opt-in)で全部
bash verify.sh all                      # C1-C4 検証
bash recover.sh --diagnose              # 状態確認
```

想定総時間: 6 iter × 5-10 分 = **30-60 分**

## ファイル

| File | 役割 |
|---|---|
| `goal.md` | 目的・スコープ・C1-C4 受入基準 |
| `citations-todo.md` | 22 件の citation 提案(skill 名 → 提案文) |
| `bootstrap.sh` | citations-todo.md を読んで skills-pending.txt 生成 |
| `run-loop.sh` | 1 iter ぶんの citation 適用 |
| `verify.sh` | C1-C4 自動検証 |
| `recover.sh` | --diagnose / --reset-circuit / --clear-lock 等(skill-update から流用) |
| `run-all.sh` | DONE まで自動継続(skill-update から流用) |

## ロールバック

iter 後に AC1/AC2/AC4 dead count が悪化したら `git checkout HEAD -- <skill>/SKILL.md <skill>/references` でバッチ編集を破棄して BLOCKED 終了。手動巻戻しは:

```bash
git -C /Users/simota/.claude/skills diff --stat   # 何が変わったか
git -C /Users/simota/.claude/skills restore .     # 全部破棄
```
