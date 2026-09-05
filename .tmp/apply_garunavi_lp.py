from __future__ import annotations

import base64
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp" / "garunavi-assets"
HTML = ROOT / "public" / "garunavi" / "index.html"
ASSETS = ROOT / "public" / "garunavi" / "assets" / "android"
WORKFLOW = ROOT / ".github" / "workflows" / "apply_garunavi_lp.yml"


def decode_asset(prefix: str, parts: int, output: str, expected_len: int, expected_sha256: str) -> None:
    encoded = "".join((TMP / f"{prefix}_{i:02d}.b64").read_text(encoding="utf-8") for i in range(parts))
    data = base64.b64decode(encoded, validate=True)
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if len(data) != expected_len:
        raise RuntimeError(f"{output}: size mismatch: expected={expected_len}, actual={len(data)}")
    if actual_sha256 != expected_sha256:
        raise RuntimeError(f"{output}: sha256 mismatch: expected={expected_sha256}, actual={actual_sha256}")
    (ASSETS / output).write_bytes(data)


decode_asset(
    "history",
    3,
    "history_update.webp",
    18504,
    "69f72fbeca7190a6a06913870493024ff194397b3307837303911e7461e8b35d",
)
decode_asset(
    "clip",
    5,
    "clip_update.webp",
    36408,
    "b9028295bbbbdf35493ab0d5825b48ca33fcd2bbe41b0d6efdba8b5656c8e314",
)

html = HTML.read_text(encoding="utf-8")
lead_old = '<p class="section-lead">Android版の実際の画面といっしょに、がるなびの機能を紹介します。</p>'
lead_new = '<p class="section-lead">Android版の実際の画面といっしょに、がるなびならではの便利な機能を紹介します。</p>'
if html.count(lead_old) != 1:
    raise RuntimeError(f"section lead marker count must be 1, actual={html.count(lead_old)}")
html = html.replace(lead_old, lead_new, 1)

marker = '''    <article class="feature-row reverse">
      <div class="feature-copy">
        <span class="feature-category">スクロール画面</span>
        <h3 class="feature-heading">爆速スクロール</h3>'''
if html.count(marker) != 1:
    raise RuntimeError(f"scroll section marker count must be 1, actual={html.count(marker)}")

new_sections = '''    <article class="feature-row reverse">
      <div class="feature-copy">
        <span class="feature-category">履歴機能</span>
        <h3 class="feature-heading">履歴の新着をまとめてチェック</h3>
        <p class="feature-description">履歴に入れたトピックの新着をまとめて確認。<br>どのトピに何件増えたか、一覧でひと目でわかります。</p>
      </div>
      <div class="feature-visual">
        <div class="screens">
          <img class="phone-shot single" src="./assets/android/history_update.webp" alt="Android版の履歴一括更新画面" loading="lazy">
        </div>
      </div>
    </article>

    <article class="feature-row">
      <div class="feature-copy">
        <span class="feature-category">クリップ機能</span>
        <h3 class="feature-heading">クリップしたコメントの反応をまとめて確認</h3>
        <p class="feature-description">保存したコメントの返信や評価の変化をまとめて確認。<br>気になるコメントのその後を追いかけやすくなります。</p>
      </div>
      <div class="feature-visual">
        <div class="screens">
          <img class="phone-shot single" src="./assets/android/clip_update.webp" alt="Android版のクリップ一括更新画面" loading="lazy">
        </div>
      </div>
    </article>

'''
html = html.replace(marker, new_sections + marker, 1)

for required in (
    "history_update.webp",
    "clip_update.webp",
    "履歴の新着をまとめてチェック",
    "クリップしたコメントの反応をまとめて確認",
):
    if html.count(required) != 1:
        raise RuntimeError(f"post-patch validation failed for {required!r}: count={html.count(required)}")

HTML.write_text(html, encoding="utf-8")

# Temporary transport files and this one-shot workflow must not remain in the PR diff.
shutil.rmtree(ROOT / ".tmp")
if WORKFLOW.exists():
    WORKFLOW.unlink()
