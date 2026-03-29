# Claude Code 依存から Gemini 実行基盤への移行計画

## 1. 現状分析（2026-03-29 時点）

このリポジトリを実ファイルベースで調査した結果、アプリケーションコードは存在せず、`README.md` のみが配置されていました。

### 調査コマンド
- `pwd`
- `find . -maxdepth 3 -type f`
- `sed -n '1,240p' README.md`

### 検出されたファイル
- `README.md`（タイトルのみ）
- `.git/*`（Git メタデータ）

## 2. Claude Code 依存箇所の洗い出し

リポジトリ内には Claude Code 実装が存在しないため、**コードとしての依存箇所は 0 件**でした。
ただし移行対象の観点では、以下の 3 区分で扱います。

### A. instruction asset として再利用できる部分
- `SKILL.md` という資産フォーマット自体
- 「業務知識」「判断基準」「作業手順」の記述方式
- Skill のメタデータ（name/description）と手順本文の分離

### B. runtime / tool / permissions / directory convention として置換が必要な部分
- Claude 固有ランタイム呼び出し
- Claude 向け slash command 記法
- `.claude/` 配下前提のディレクトリ慣習
- Claude 固有の tool / permission 設定

### C. 完全に削除してよい部分
- Claude 専用文言で、他 Agent では意味を持たない規約
- Claude 固有 CLI 実行手順

## 3. `.claude` ディレクトリを作るべきか

結論: **不要**。今回の移行後アーキテクチャでは `.claude` を運用ディレクトリとして使いません。

- 実行ロジックは `backend/`
- UI は `frontend/`
- 再利用可能 skill は `skills/portable/`

## 4. 目標アーキテクチャ

「まず動く最小構成（MVP）」として、以下を採用します。

- **Frontend:** Streamlit（1画面）
- **Backend:** FastAPI
- **LLM Provider:** Gemini（Google GenAI SDK）
- **Skill 実行:** Backend に集約（UI は入力/表示に専念）

### 4.1 コンポーネント責務

1. `frontend/app.py`
   - 入力フォーム
   - 実行ボタン
   - 実行ログ表示
   - 最終出力表示
   - エラー表示

2. `backend/app/main.py`
   - `/health` と `/run` を提供
   - リクエスト受理後に Skill 解決と Gemini 推論を実行

3. `backend/app/gemini_client.py`
   - Google GenAI SDK 呼び出しを隠蔽
   - 既定モデルを設定値で差し替え可能にし、ハードコードを回避

4. `backend/app/skills/*`
   - Skill 一覧を走査
   - `SKILL.md` の frontmatter を解析
   - name / description / body を実行時コンテキスト化

## 5. ディレクトリ構成（目標）

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── gemini_client.py
│   │   └── skills/
│   │       ├── loader.py
│   │       └── orchestrator.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── skills/
│   └── portable/
│       └── task-planning/
│           └── SKILL.md
├── docs/
│   └── migration-plan.md
├── .env.example
└── README.md
```

## 6. 非機能・拡張方針

- モデル名は `GEMINI_MODEL` 環境変数で切替可能
- API キーは backend 側の `GEMINI_API_KEY` のみで管理
- Skill 追加時は `skills/portable/<skill-name>/SKILL.md` を増やすだけで自動検出
- 将来的に Interactions API へ差し替える場合も `gemini_client.py` 内の実装置換に閉じ込める

## 7. 未対応事項（次フェーズ）

- Skill の優先度ルール（複数マッチ時のランキング）
- 実行履歴の永続化（DB）
- SSE/WebSocket によるストリーミングログ
- 認証・監査ログ
