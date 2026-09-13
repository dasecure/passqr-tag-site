# tag.passqr.com

Marketing site for **PassQR Tag** — the anonymous contact tag. A coded sticker that lets a
stranger reach the owner of a car, gate or piece of kit without either side holding an
identifier for the other.

Static, no framework. `index.html` is the whole site; everything else is assets. Same house
system as `loyalty.passqr.com` (Fraunces display / Instrument Sans body, the same token
names, buttons, cards and band rhythm) with the Tag palette — pine `#0A4F45`, teal
`#0E7C6B`, ink `#101D1A`, paper `#F5F8F6` — in place of the café espresso/amber.

## Files

| | |
|---|---|
| `index.html` | The entire landing page — markup, CSS and the one inline script |
| `404.html` | Branded not-found page (without it, Pages serves `index.html` at status 200 for every unknown path) |
| `og.png` | 1200×630 social card |
| `favicon.svg`, `apple-touch-icon.png` | Icons |
| `robots.txt`, `sitemap.xml` | Indexing |
| `_headers` | Cloudflare Pages response headers |
| `tools/make-images.py` | Regenerates `og.png` and `apple-touch-icon.png` |

## Deploy

Cloudflare Pages, git-connected to this repo — **a push to `main` deploys production.**
No environment variables, no secrets.

The "build" is a copy step that stages only the public files, so `tools/` and `README.md`
are never served:

```
mkdir -p _site && cp index.html 404.html og.png favicon.svg apple-touch-icon.png robots.txt sitemap.xml _headers _site/
```

Output directory is `_site`. **If you add a public file, add it to that command**
(Pages dashboard → Settings → Builds & deployments) or it will not ship.

## The two PNGs cannot be pushed through the GitHub MCP

The MCP's file-write tool stores whatever string it is given as **text**, so a base64 PNG
lands in the repo as a base64 text file with a `.png` name — it looks committed and serves
as garbage. Both binaries must be committed from a real git client. Regenerate them with
`tools/make-images.py` and commit from the Mac.

## This is not the relay

`t.passqr.com` is the relay: it is `TAG_HOST`, the host inside every sticker QR, and the
`applinks:`/`appclips:` domain in the app's `project.yml`. **Nothing here may ever answer on
that host.** `tag.passqr.com` has never resolved before — as of 11 Sep 2026 it was removed
from the ZapQR IdP client row (`zq_WJSXhlnHFB1w`) precisely because it was dead — so this
site is free to take it, and taking it does not disturb the relay, the stickers, the app's
universal links or the OAuth redirect.

## The call to action

Every "Ask for a tag" button is repointed at runtime from one constant near the bottom of
`index.html`:

```js
var BETA_URL = "mailto:hello@passqr.com?subject=PassQR%20Tag%20beta";
```

The `href` attributes in the markup carry the same value, so the links still work with
JavaScript off. **When the iPhone app is approved**, swap that constant for the App Store
URL and change the five button labels to match — a button says what happens when it is used,
so "Ask for a tag" should not open the App Store.

## The patent-pending chip

One component, `.pp`, used in four places: under the hero trustline, after the
presence note, on the sticker mock, and in the footer. Drop it anywhere:

```html
<span class="pp" title="Two U.S. provisional patent applications filed">
  <svg viewBox="0 0 20 24" fill="none" aria-hidden="true">
    <path d="M10 1.7 2.9 4.7v7c0 4.9 3 8.3 7.1 9.6 4.1-1.3 7.1-4.7 7.1-9.6v-7Z"
          stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
    <rect x="7.3" y="8.1" width="5.4" height="5.4" rx="1.4" stroke="currentColor" stroke-width="1.7"/>
  </svg>Patent pending
</span>
```

| Variant | Use on |
|---|---|
| `pp` | `--paper` and `.band-paper` |
| `pp on-dark` | `.band-dark` and the footer |
| `pp quiet` | white cards, or anywhere it would compete with a heading |

The glyph is a shield around the PassQR finder square, so the chip reads as part
of the mark rather than as a stock badge.

Three rules for anyone editing it:

1. **The words stay "Patent pending."** It is a legal-notice term of art. Do not
   inflate it to "Patented", and do not shorten it to "Pat. pend."
2. **The application numbers stay off the page.** They live in the tooltip only as
   a count. Provisionals are unpublished; there is nothing to point a reader at.
3. **It comes off the day the provisionals lapse** unless a non-provisional has
   been filed. The deadline is **02 Sep 2027** from the earlier filing and does not
   move. Marking a product patent pending when nothing is pending is a false
   marking problem, not a copy problem.

## Claims on this page are checked, not aspirational

The status table in `section#status` is load-bearing. As of 12 Sep 2026:

| Claim on the page | Why it is true |
|---|---|
| Relay + browser scan page live | Live on `t.passqr.com`, in daily use |
| Two-way thread, voice notes both directions | Shipped; browser side is ahead of the native sender surface |
| Wallet / push / SMS owner alerts, second contact by invitation | Shipped |
| iPhone app "with Apple for review" | 0.9.0 (3) submitted 12 Sep, Waiting for Review |
| Android "browser only for now" | No Android client exists |
| "Two provisionals filed" | 64/146,350 (02 Sep 2026) and 64/148,948 (05 Sep 2026) |
| Retention "2 days by default, 1–30, no keep-forever" | `sweepPurge()`, `tag.owners.purge_days` |

Deliberately **not** claimed, because it is not shipped: saving a copy of a conversation
(the keep endpoints exist but no UI reaches them), NFC tap as a presence signal, and any
App Store availability. The privacy policy at `www.passqr.com/privacy` makes the same
omissions — keep the two in step.

The presence section names the signals but publishes **no weights or thresholds**. That is
on purpose: the scoring is the subject of the provisionals, and a published table is a
recipe for gaming the score.

## Illustrative content

The sticker mock in the credential section shows code `K7MD · 4QXA`, which is not a real
tag. The QR drawn inside it is decorative and does not decode — unlike the loyalty site's,
which is a real scannable code. If a scannable QR is ever wanted here, it must point at a
tag that exists and is owned by us, never at a personal one.
