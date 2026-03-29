# skillPre

Claude Code 前提の実行依存を排除し、Gemini API + FastAPI + Streamlit で動作する最小構成に移行したサンプルです。

## `.claude` で始まるディレクトリは必要？

不要です。この実装では `.claude` 配下の設定・コマンド・権限モデルに依存しません。

- 実行基盤は `backend/` に集約
- UI は `frontend/`
- 再利用可能な skill 資産は `skills/portable/` に配置

## 全体構成

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
│       └── task-planning/SKILL.md
├── docs/
│   └── migration-plan.md
└── .env.example
```

## 目的

- Claude 固有の runtime/tool 依存を排除
- SKILL.md をポータブルな instruction asset として再利用
- API キーを UI に持たせず backend 経由で Gemini を実行
- 今後 skill 追加しても破綻しにくい構成

## セットアップ

### 1. 環境変数

`.env.example` を `.env` にコピーして値を設定します。

```bash
cp .env.example .env
```

最低限、`GEMINI_API_KEY` を設定してください。

### 2. backend 起動

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. frontend 起動

別ターミナルで以下を実行します。

```bash
source .venv/bin/activate
pip install -r frontend/requirements.txt
streamlit run frontend/app.py --server.port 8501
```

## 使い方

1. Streamlit UI で入力フォームに要望を記載
2. 必要なら skill 名を指定（省略時は backend 側で選択）
3. 実行ボタンを押す
4. 実行ログ / 最終出力 / エラーを UI 上で確認

## API

### `GET /health`
- ヘルスチェック

### `POST /run`
リクエスト:

```json
{
  "user_input": "リファクタリング計画を作って",
  "skill_name": "task-planning"
}
```

レスポンス:

```json
{
  "status": "success",
  "selected_skill": "task-planning",
  "logs": ["request accepted", "..."],
  "output": "...",
  "error": null
}
```

## Skill 追加方法

- `skills/portable/<new-skill>/SKILL.md` を追加
- frontmatter の `name` と `description` を設定
- 本文に「いつ使うか / 禁止事項 / 入出力 / 実行手順」を定義

backend は `SKILLS_DIR` 配下を再帰走査して `SKILL.md` を自動ロードします。

## 今後の拡張候補

- Interactions API への切替（`backend/app/gemini_client.py` を置換）
- ストリーミング応答
- skill のランキング・タグベース選択
- 実行履歴の永続化
