from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "public" / "garunavi" / "index.html"
WORKFLOW = ROOT / ".github" / "workflows" / "apply_garunavi_final.yml"
SELF = Path(__file__).resolve()
ASSETS = ROOT / "public" / "garunavi" / "assets" / "android"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly 1 marker, actual={count}")
    return text.replace(old, new, 1)


def assert_png(path: Path) -> None:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError(f"{path.name}: expected PNG signature")
    if len(data) < 24:
        raise RuntimeError(f"{path.name}: PNG is too short")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (539, 903):
        raise RuntimeError(
            f"{path.name}: unexpected dimensions {(width, height)}, expected (539, 903)"
        )


history_src = ASSETS / "history_update.webp"
clip_src = ASSETS / "clip_update.webp"
assert_png(history_src)
assert_png(clip_src)
history_dst = ASSETS / "history_update.png"
clip_dst = ASSETS / "clip_update.png"
if history_dst.exists() or clip_dst.exists():
    raise RuntimeError("destination screenshot already exists")
history_src.rename(history_dst)
clip_src.rename(clip_dst)

html = HTML.read_text(encoding="utf-8")

html = replace_once(
    html,
    '<meta name="description" content="がるなびは、ガールズちゃんねる（がるちゃん）を快適に読むための無料のがるちゃんアプリ・ブラウザです。iOS・Android・Windows・macOSに対応。検索、クリップ、下書きなど長いトピを読むための機能を備えています。">',
    '<meta name="description" content="がるなびは、ガールズちゃんねる（がるちゃん）を快適に読むための無料のがるちゃんアプリ・ブラウザです。一度開いたトピックのコメントを端末に保存し、次回はすぐ表示。履歴やクリップの更新チェック、検索、下書きなど長いトピを読むための機能を備えています。">',
    "meta description",
)
html = replace_once(
    html,
    '<meta property="og:description" content="がるちゃんを快適に読むための無料のがるちゃんアプリ・ブラウザ。iOS・Android・Windows・macOS対応。">',
    '<meta property="og:description" content="一度読んだトピックは待たずにすぐ読める、無料のがるちゃんアプリ・ブラウザ。履歴やクリップの更新もまとめて確認できます。">',
    "og description",
)
html = replace_once(
    html,
    '    "description": "ガールズちゃんねる（がるちゃん）をiPhone・AndroidスマホやPCで快適に閲覧できる無料のがるちゃんアプリ・ブラウザ。"',
    '    "description": "ガールズちゃんねる（がるちゃん）を快適に閲覧できる無料のがるちゃんアプリ・ブラウザ。一度開いたトピックのコメントを端末に保存し、履歴やクリップの更新もまとめて確認できます。"',
    "structured data description",
)
html = replace_once(
    html,
    '          がるなびは、ガールズちゃんねる（がるちゃん）をiPhone・AndroidスマホやPCで快適に閲覧できる無料の<strong>がるちゃんアプリ・ブラウザ</strong>です。トピックやコメントを保存し、カテゴリ分けやメモもできます。',
    '          がるなびは、ガールズちゃんねる（がるちゃん）をiPhone・AndroidスマホやPCで快適に閲覧できる無料の<strong>がるちゃんアプリ・ブラウザ</strong>です。<strong>一度開いたトピックのコメントは端末に保存され、次に開くときは待たずにすぐ読めます。</strong>履歴やクリップの更新もまとめてチェックできます。検索、クリップ、下書きなど、長いトピを読むための機能も備えています。',
    "hero description",
)
html = replace_once(
    html,
    '<p class="section-lead">Android版の実際の画面といっしょに、がるなびの機能を紹介します。</p>',
    '<p class="section-lead">Android版の実際の画面といっしょに、がるなびならではの便利な機能を紹介します。</p>',
    "feature lead",
)

scroll_marker = '''    <article class="feature-row">
      <div class="feature-copy">
        <span class="feature-category">スクロール画面</span>
        <h3 class="feature-heading">爆速スクロール</h3>'''
new_sections = '''    <article class="feature-row">
      <div class="feature-copy">
        <span class="feature-category">読み返し</span>
        <h3 class="feature-heading">一度読んだトピは、すぐ開ける</h3>
        <p class="feature-description">一度開いたトピックのコメントは端末に自動で保存。<br>次に開くときは読み込みを待たずに表示します。<br>保存済みのコメントは、通信できない場所でも読み返せます。</p>
      </div>
      <div class="feature-visual">
        <div class="screens">
          <img class="phone-shot" src="./assets/android/history.png" alt="Android版の履歴画面" loading="lazy">
          <img class="phone-shot" src="./assets/android/detail.png" alt="Android版の保存済みトピック詳細画面" loading="lazy">
        </div>
      </div>
    </article>

    <article class="feature-row reverse">
      <div class="feature-copy">
        <span class="feature-category">履歴機能</span>
        <h3 class="feature-heading">履歴の新着をまとめてチェック</h3>
        <p class="feature-description">履歴に入れたトピックの新着をまとめて確認。<br>どのトピに何件増えたか、一覧でひと目でわかります。</p>
      </div>
      <div class="feature-visual">
        <div class="screens">
          <img class="phone-shot single" src="./assets/android/history_update.png" alt="Android版の履歴一括更新画面" loading="lazy">
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
          <img class="phone-shot single" src="./assets/android/clip_update.png" alt="Android版のクリップ一括更新画面" loading="lazy">
        </div>
      </div>
    </article>

'''
html = replace_once(html, scroll_marker, new_sections + scroll_marker, "scroll section")

html = replace_once(
    html,
    '      <li>インターネット接続が必要です（初回起動時および画像読み込み時）。</li>',
    '      <li>新しいトピック・コメントの取得や画像の読み込みにはインターネット接続が必要です。保存済みのコメントは通信なしでも読み返せます。</li>',
    "network requirement",
)
faq_marker = '''    <details class="faq">
      <summary>iOS版のアップデート方法は？</summary>'''
offline_faq = '''    <details class="faq">
      <summary>通信なしでもトピックを読めますか？</summary>
      <p>一度開いて端末に保存されたコメントは、通信できない場所でも読み返せます。新しいトピックやコメントの取得、画像の読み込みにはインターネット接続が必要です。</p>
    </details>
'''
html = replace_once(html, faq_marker, offline_faq + faq_marker, "FAQ marker")

style_marker = '    .feature-row:nth-child(5) .feature-visual { background: #fff6e9; }'
style_new = '''    .feature-row:nth-child(5) .feature-visual { background: #fff6e9; }
    .feature-row:nth-child(6) .feature-visual { background: #eef5ff; }
    .feature-row:nth-child(7) .feature-visual { background: #fff2f6; }
    .feature-row:nth-child(8) .feature-visual { background: #eef9f3; }'''
html = replace_once(html, style_marker, style_new, "feature colors")

for required in (
    "history_update.png",
    "clip_update.png",
    "一度読んだトピは、すぐ開ける",
    "履歴の新着をまとめてチェック",
    "クリップしたコメントの反応をまとめて確認",
    "通信なしでもトピックを読めますか？",
):
    if html.count(required) != 1:
        raise RuntimeError(f"post-patch validation failed for {required!r}: count={html.count(required)}")

HTML.write_text(html, encoding="utf-8")

# Remove one-shot transport files from the final diff.
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
