# Claude notes

Working notes for Claude on this repo. Every comment that isn't something a
plain, no-frills dev would leave in the code lives here instead — usage
instructions, rationale, gotchas — so the code files themselves stay short
and easy to read. Also tracks standing instructions from Jeffrey that should
keep applying to future changes, not just the request they came from.

## Standing rules

- No comments in code files (HTML/CSS/JS/Python) — none at all, not even
  a plain section divider, a file-header banner, or a one-line docstring.
  Every code file should read as if nobody ever needed to explain any of
  it. Anything that would've been a comment — rationale, a gotcha, usage
  instructions, what a function does, what a stylesheet section covers —
  goes here instead (Sep 2: swept the whole repo for the first time under
  this rule; see "Comment sweep" below for what moved). The one exception
  is a shebang line (`#!/usr/bin/env python3`) — that's an interpreter
  directive, not documentation, so it stays.
- No images embedded as base64/data URIs in HTML. Every image is its own
  file in the repo root, referenced with a normal relative `src`/`href`.
- Every page shares the same header (pfp + "Originalboy2" h1) and footer
  (just the Originalboy2 copyright line — no zuki.awu/pfp credit line
  anywhere anymore, see "Footer copyright cleanup" below). Sub-pages
  (socials/projects/blog/404) follow the same layout order: header, then
  back-btn ("< index"), then the page's content box, with a 0.75rem gap
  between the back-btn and that box (same as the 0.75rem gap between
  rows within a list).
- Favicon is ogb2.ico (not something Claude should re-touch).

## How to add a blog post (from build_blog.py)

1. Create a file in `posts/`, e.g. `posts/my-new-post.md`:

   ```
   ---
   title: My New Post
   date: 2026-09-05
   summary: One line describing the post, shown on the blog index row.
   ---

   Body goes here, written in a small subset of markdown: blank lines
   separate paragraphs, # / ## make headings, **bold**, *italic*, `code`,
   and [link text](https://example.com) all work.
   ```

   For a video post (a YouTube link embedded on the post page instead of
   written body text), add a `video:` line with the video's URL — the
   body/markdown underneath is ignored:

   ```
   ---
   title: My New Post
   date: 2026-09-05
   summary: One line, used for this post's <meta description> tag only —
     video posts don't show a summary on the blog list row.
   video: https://www.youtube.com/watch?v=XXXXXXXXXXX
   ---
   ```

   Optionally add a `thumbnail:` line to override the auto-derived
   `https://i.ytimg.com/vi/<id>/hqdefault.jpg` used on the blog list row.

2. Run `python3 build_blog.py`. It (re)writes `blog.html` and every
   `blog-<slug>.html` page.
3. Commit and push as usual.

Re-running is always safe — every post page and `blog.html` are fully
regenerated from `posts/` each time, so nothing drifts out of sync.

## Implementation notes

- **Comment sweep (Sep 2):** style.css and build_blog.py were the only
  files with anything left in them — index/404/blog/projects/socials/off
  .html and script.js were already clean. What moved:
  - style.css's old file-header banner just said what the file was for
    ("Originalboy2 — shared site styles, used by index.html, socials.html,
    …") — now just: this file is the shared stylesheet every page links
    to.
  - `--text` (#f8f8f2) and `--text-muted` (#75715e) are Monokai's
    foreground and comment colors respectively — the rest of the palette
    (`--green`/`--cyan`/`--orange`/`--pink`/`--purple`) is Monokai too,
    picked to match.
  - style.css section order, since the `/* ---- name ---- */` dividers
    that used to mark this are gone — top to bottom: `:root` vars, resets,
    body/page-bg (shared backdrop), header, about (index), error-code
    (404), nav buttons, back button, the shared button hover-gif effect,
    social rows, project cards, blog list, individual post page, footer,
    power button, CRT power-off keyframes, small-screens media query.
  - build_blog.py's module docstring said the script generates blog post
    pages and the blog index from markdown files in posts/ — that's the
    "How to add a blog post" section below already, so it wasn't
    duplicated anywhere new.
  - `get_pfp_img_tag()`'s docstring said it returns the `<img class="pfp">`
    tag from index.html — already covered above under pfp/favicon
    extraction.
  - `render_markdown()` had a comment on the plain-paragraph branch noting
    that hard-wrapped lines within one markdown paragraph (no blank line
    between them) get joined into a single line before rendering, so a
    manual line break in a post's source `.md` file doesn't turn into a
    stray line break in the output — paragraphs only break on an actual
    blank line.
- **pfp/favicon extraction (Sep 1):** the profile picture used to be a
  ~375KB base64 blob duplicated inside every page. Extracted once to
  pfp.png. `get_pfp_img_tag()` in build_blog.py pulls the `<img class="pfp">`
  tag straight out of index.html at build time specifically so that one
  file stays the single source of truth — pointing that tag at pfp.png
  fixed every generated page automatically, no other script changes needed.
- **404.html:** matches the same header/back-btn/content-box pattern as
  socials/projects/blog: header, then back-btn, then content. A giant
  `--brand`-colored "404" (`.error-code`, an `<h2>`, not bold) sits
  between the back-btn and the `.about` text box. `.back-btn + .error-code`
  and `.error-code + .about` both bring their gaps down to the standard
  0.75rem in-page gap (same idea as the `.back-btn + .about` rule below —
  `.error-code`'s own base margin-top of 1.1rem is only what applies if
  it's ever used directly under a header instead).
- **`.back-btn + .about` rule (style.css):** `.about` normally sits right
  under the header on index.html (margin-top: 1.1rem, matching the
  header-to-first-element gap used everywhere). On 404.html the back-btn
  sits between the header and the about box instead, so this override
  brings that gap down to the standard 0.75rem "back-btn to content" gap
  used by the other sub-pages.
- **`.blog-empty` margin fix:** it's a bare `<p>`, and browsers give `<p>`
  a default margin the other list items (`<a>` tags) don't have. That
  default margin was stacking on `.blog-list`'s own margin-top, making
  the gap under the blog page's back-btn bigger than every other page's.
  Fixed by zeroing the paragraph's margin.
- **`.back-btn` is `display:block; width:fit-content;`, not
  `inline-block`:** with `inline-block`, the back-btn sat inside an
  anonymous inline formatting context that added ~10px of invisible
  leading below it (from the inherited line-height), making the gap to
  whatever came next visibly bigger than the equivalent gap elsewhere
  (e.g. `.about` to `nav` on index.html) even though both used the same
  0.75rem margin. `display:block` drops the leading; `width:fit-content`
  keeps the button sized to its own text instead of stretching full-width.
  Measured with real pixel values before and after to confirm — was 21.6px
  vs. 12px, now 12px everywhere.
- **script.js removed (Sep 1), reinstated (Sep 2):** originally deleted
  as an empty placeholder with nothing wired to it, along with the
  `<script>` tag on every page and in both build_blog.py templates.
  Recreated Sep 2 for the power-button feature above — only index.html
  has the `<script>` tag back in, since that's the only page with the
  button.
- **`render_inline()` escaping order (build_blog.py):** `html.escape` runs
  before the markdown inline patterns (`**bold**`, `` `code` ``, links) are
  applied, on purpose — escape first, then add markup, so the tags this
  function inserts don't themselves get escaped afterward. If this ever
  gets reordered, quotes/brackets in post text will mangle the generated
  tags.
- **Project accent colors (style.css, `.project-gachastuck`/`.project-genesis`):**
  each project's `--accent` was picked to match that project's own itch.io
  page theme; the Genesis color was sampled directly from its cover art.
- **genesis-cover.png (Sep 2):** Genesis's cover was hotlinked straight
  from itch.io at its native 630x500 (1.26 aspect), while Gachastuck's is
  650x500 (1.3 aspect) — same grid column width on projects.html, but two
  different aspect ratios meant Genesis rendered visibly taller. Downloaded
  it, cropped 15px off the height (7 top / 8 bottom, plain black margin,
  no logo content there) to 630x485 to match Gachastuck's 1.3 aspect, and
  saved it locally as genesis-cover.png rather than re-hosting a modified
  image back on itch.io. `--cover-ratio` for `.project-genesis` updated to
  630/485 to match. Confirmed in a real render both images come out within
  0.2px of the same height.
- **Button hover effect (Sep 2):** `.btn` and `.back-btn` each get a
  `::before` layer showing purple-effect.gif at 25% opacity, only on
  hover/focus. Two non-obvious bits: `overflow:hidden` on the button is
  what crops the gif to the button's shape, and `position:relative` +
  `z-index:0` on the button is required for the pseudo-element's
  `z-index:-1` to stack *behind that button specifically* — without a
  z-index on the button itself, `position:relative` alone doesn't create
  a new stacking context, and the effect renders invisible behind the
  page background instead.
  Each button class gets a different `background-position` so they show
  visually distinct crops rather than all looking like the same diagonal
  stripes (the image is mostly uniform diagonal lines up top and a
  chevron/weave interference pattern lower down, so positions were chosen
  by eye to land on different-looking regions, not just evenly spaced
  corners): `.btn-projects` 0% 0% (stripes), `.btn-blog` 100% 30%
  (crosshatch), `.btn-socials` 20% 100% (chevron), `.back-btn` 100% 100%
  (weave).
  `.back-btn`'s hover state also sets `color:var(--text)` (off-white) —
  its default text/arrow color is `--brand` (purple), which was unreadable
  against the purple-ish gif once it faded in on hover.
- **Power button + CRT-off (Sep 2, index.html only):** `#power-btn` in the
  bottom-right links to off.html. script.js's `playCrtOff()` synthesizes the
  power-down sound with the Web Audio API instead of shipping an audio file:
  a sine oscillator sweeping 1400Hz down to 35Hz over 0.4s (the classic CRT
  degauss/collapse whine) with an exponential gain fade, plus a short burst
  of white noise at the very end for the final relay click. The click
  handler waits for that to finish before navigating to off.html, so the
  sound always plays out even though the link itself is instant. off.html
  has an empty `<body>` and no page-specific CSS — the shared `body{
  background:var(--bg) }` rule alone already renders a full near-black
  viewport, so "just black" needed no new styles, just an empty page.
  script.js was previously deleted from the repo as a dead placeholder (see
  the note below); this is a new, real use of it, not a revert.
- **bg-clouds.png background (Sep 2):** every page except off.html has a
  `<div class="bg-clouds">` as the first thing in `<body>`. It's a real
  element, not a `body` CSS background, on purpose: `.crt-off`'s `transform`
  on `body` only warps things that are part of body's own painted box, and
  a `position:fixed` div is exactly like `.footer`/`.power-btn` above —
  once `body` has a transform it becomes their containing block, so this
  div collapses into the same line they do instead of staying put. A plain
  `background-image` on `body` doesn't reliably get the same treatment
  (mixing `background-attachment:fixed` with a transform on the same
  element is inconsistent across browsers), so it's a div, `position:fixed;
  inset:0; z-index:-1;`, not a background property.
  `body` keeps only `background-color:var(--bg)` (solid black) — with no
  background set on `html`, that color is what propagates to paint the
  actual canvas/viewport behind everything, and the canvas paint is
  untouched by `body`'s transform. So mid-collapse, what's left behind the
  shrinking clouds is that plain static black, not empty/white.
  off.html simply never gets the div (it was never added there), so it's
  just the plain black canvas with nothing else — no override needed.
  `build_blog.py`'s `PAGE_TEMPLATE`/`INDEX_TEMPLATE` both got the div too,
  so future blog builds keep it; blog.html itself was hand-edited to add
  it rather than regenerated, since posts/ is empty right now and
  regenerating would have overwritten the shortened "No posts yet." text
  with the template's longer empty-state line.
- **Images moved into images/ (Sep 2):** all image/gif assets now live under
  `images/`, with the four page-background images further nested in
  `images/bgs/`. Every `src="…"` and CSS `url("…")` pointing at one got the
  new relative path. ogb2.ico stayed at the repo root (favicon, untouched).
  `get_pfp_img_tag()` in build_blog.py just pulls whatever `<img class="pfp">`
  tag is currently in index.html, so pointing that tag at `images/pfp.png`
  was the only change needed for every generated page to pick it up too —
  same reason the original pfp extraction only needed one edit back on Sep 1.
  finlee.gif and ogb2button.png live in images/ but aren't referenced by any
  page currently — left as-is, not part of this pass.
- **Genesis "Play in browser" (Sep 2):** Genesis.html is the game itself
  (a big standalone export, ~16MB), dropped at the repo root. Genesis's
  project card is `.project-card-group.project-genesis`, a plain div with
  two pieces: `.project-cover-wrap` (the cover image plus `.project-play`,
  a small badge absolutely positioned over the bottom-center of the image)
  and a `.project-card` anchor below it for just the title/tagline, still
  going to the itch.io page. The image itself isn't a separate link anymore
  — `.project-play` sits inside `.project-cover-wrap` specifically so its
  `position:absolute` resolves against that wrapper's box (which is exactly
  the image's own rendered size, since `.project-cover-wrap` has nothing
  else in it), and `bottom`/`left` on an absolutely positioned element
  don't need a percentage-of-parent-height calculation the way `top` would
  on a parent whose height isn't fixed — this is what keeps the badge
  correctly anchored to the image at any card width, not just one
  screen size. `--accent`/`--cover-ratio` live on `.project-card-group`
  (an ancestor of both pieces) so both the badge and the title inherit the
  same accent red without repeating it. `align-items:start` on
  `.projects-list` stops CSS Grid's default `stretch` from forcing
  Gachastuck's card to match Genesis's height. `.project-play` also gets
  the same hover-gif treatment as `.btn`/`.back-btn` (own `background-
  position`, `0% 100%`, not reused elsewhere) — needs `z-index:0` in
  addition to `position:absolute` for the same reason `.btn`/`.back-btn`
  need it with `position:relative`: without an explicit z-index the
  element doesn't form its own stacking context, and the `::before`'s
  `z-index:-1` escapes to some ancestor's context and paints behind the
  page instead of just behind this badge.
- **Per-page backgrounds (Sep 2):** renamed the div/class from `bg-clouds`
  to the generic `page-bg` once socials/projects/blog got their own image
  files (blog-bg.png, projects-bg.png, socials-bg.png — each tinted to
  match that section's accent color: cyan, green, orange) instead of all
  sharing bg-clouds.png. `.page-bg-blog`/`-projects`/`-socials` override
  just `background-image` on top of the shared `.page-bg` rule (same
  pattern as `.btn-projects`/`.project-gachastuck` elsewhere — a base
  class plus a per-context modifier). index.html and 404.html have no
  modifier class, so they keep falling back to bg-clouds.png.
- **CRT collapse visual (Sep 2):** `body.crt-off` (added by script.js on
  click, alongside the sound) runs the `crt-off` keyframes: the whole page
  brightens and squashes vertically to a thin line, then that line shrinks
  to nothing and fades — the classic CRT-tube-degaussing look. It's applied
  to `body` rather than just `.wrap` on purpose: a `transform` on `body`
  makes it the containing block for its `position:fixed` descendants too
  (`.footer`, `.power-btn`), so they collapse into the same line instead of
  staying pinned in place while the rest of the page shrinks around them.
  Animation duration (0.48s) and the JS navigation delay (480ms) are the
  same number by design so the page doesn't jump to off.html mid-collapse —
  if one changes, change the other.
- **Minecraft server box (index.html, Sep 3):** `.mc-server` reuses
  `.about`'s surface/padding pattern rather than `.about` itself, since
  `.about` is semantically the intro-text box. `.mc-address` mirrors
  `.error-code`'s look (centered, `--brand` purple, `font-weight:400`) but
  under its own class with a smaller clamp — `.error-code`'s own
  `clamp(5.25rem, 24vw, 9rem)` is sized for "404" filling the whole page
  width, and would overflow an 11-character domain squeezed inside a
  padded box. `.mc-address` uses `clamp(1.75rem, 8vw, 3rem)` instead,
  which keeps the address the clear visual focus of the box without
  wrapping or spilling past the box edges at any width (checked 375px and
  1280px).
- **Matrix row (socials.html, Sep 10):** `href` links to the real Matrix ID
  via `https://matrix.to/#/@ogb2:matrix.org` (matrix.to is the standard
  matrix-URI redirector — opens in whatever Matrix client, e.g. Element,
  the visitor has set up), same as every other row links to the real
  profile URL. The `.handle` text shows the display name "Originalboy2"
  instead of the raw `@ogb2:matrix.org` ID, matching the Spotify row's
  precedent (its `href` is the raw account URL, its `.handle` text is the
  display name, not the URL's opaque user-id slug). Icon is simple-icons'
  official Matrix path (the "[m" bracket mark), same sourcing as every
  other social icon on this page.
- **Video posts (build_blog.py, Sep 12):** added as a second post "kind"
  alongside the original text/markdown kind, picked per-post in `main()`
  by whether frontmatter has a `video:` line (see "How to add a blog
  post" above for the frontmatter). Text posts are unaffected — same
  templates, same behavior. A video post's blog-list row
  (`VIDEO_ROW_TEMPLATE`/`.blog-row-video`) shows a thumbnail instead of
  the usual summary paragraph, since seeing the video's own thumbnail is
  more useful there than repeating text; its post page
  (`VIDEO_PAGE_TEMPLATE`/`.post-video`) embeds the player in place of
  rendered markdown body — `body_md` is simply unused for these posts.
  Embed goes through `youtube-nocookie.com` rather than `youtube.com`
  (YouTube's own privacy-enhanced embed domain — same player, doesn't set
  cookies/tracking until playback starts). `.post-video`/`.blog-thumb`
  both use `aspect-ratio:16/9` rather than a fixed height so they scale
  correctly at any width — same technique as `.project-cover`'s
  `--cover-ratio`. Thumbnail defaults to YouTube's
  `https://i.ytimg.com/vi/<id>/hqdefault.jpg` (always exists for any
  public video, no API key needed) unless a post's frontmatter overrides
  it with `thumbnail:`.
- **Footer copyright cleanup (Sep 12):** the "&copy; zuki.awu 2026 (pfp)"
  line used to appear on every page's footer, copied from index.html when
  each page/template was first built. First pass removed it everywhere
  except index.html (build_blog.py's three templates — `PAGE_TEMPLATE`,
  `VIDEO_PAGE_TEMPLATE`, `INDEX_TEMPLATE` — and socials.html/projects.html/
  404.html all lost the line; index.html's version of it was reworded
  from a `&copy;` statement to "All rights reserved — zuki.awu 2026
  (pfp)" instead). Follow-up same day: removed it from index.html too —
  the line is gone from every page now, footers everywhere are just the
  single "&copy; Originalboy2 2026 (website)" line.
- **Blog-row hover effect + white text (style.css, Sep 12):** `.blog-row`
  now gets the same `::before` purple-effect.gif hover treatment as
  `.btn`/`.back-btn`/`.project-play` (own `background-position: 50% 60%`,
  distinct from the others), which needed the same `position:relative;
  z-index:0; overflow:hidden;` addition those already have. `.blog-title`/
  `.blog-date`/`.blog-summary` (and the title's `.sigil`) all have their
  own explicit colors normally (off-white/cyan/dim-gray), so a plain
  `.blog-row:hover{color:#fff}` wouldn't reach them — those child colors
  win on specificity. Targeted each one directly under `.blog-row:hover`/
  `:focus-visible` instead, forcing pure `#fff` rather than reusing
  `--text` (which is an off-white, #f8f8f2, not literally white).
  Follow-up fix same day: the shared `background-size:280%` (a single
  percentage sizes width *and* height independently, each as 280% of the
  element's own box) was fine on the nav/back/play buttons since they're
  roughly square-ish, but `.blog-row` is much wider than it is tall
  (~592x90 vs. the gif's native 1280x836), so 280% stretched the image
  horizontally to match that lopsided box shape — visibly distorted, not
  just zoomed. Changed the shared rule to `background-size:280% auto`
  (width still scales to 280% of the element, height follows the gif's
  own aspect ratio instead of the element's) so `.btn`/`.back-btn`/
  `.project-play` are never stretched either, just genuinely zoomed.
  Second follow-up same day: even undistorted, `280% auto` on
  `.blog-row` still read as "squished" — mathematically correct but
  visually wrong, because at that zoom the 592x90 crop window only shows
  ~3% of the total (now much larger) image, and a window that
  disproportionately wide/short makes even a correctly-scaled diagonal
  pattern look compressed. `.blog-row::before` now overrides
  `background-size` to `cover` instead of inheriting `280% auto` from
  the shared rule — `cover` picks whichever scale (width-based here,
  since the row is proportionally much wider than the image) makes the
  image just barely span the whole row width, so the full horizontal
  sweep of the pattern shows across the row instead of a small zoomed-in
  fragment of it. `.btn`/`.back-btn`/`.project-play` keep `280% auto` —
  their boxes are close enough to the gif's own aspect ratio that a
  zoomed crop still reads fine; `cover` is specifically a `.blog-row`
  fix for its much more extreme box shape, not a change to the general
  approach.
