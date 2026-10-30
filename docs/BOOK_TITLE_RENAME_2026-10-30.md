# Canonical book-title migration — 2026-10-30

## Founder directive

- **New canonical book title (exact wording):** `jason - the rabbit hole in my head`.
- **Book title component:** `jason` (lowercase).
- **Book subtitle:** `the rabbit hole in my head` (lowercase).
- This replaces the *book title* `.json — the rabbit hole in my head`. It does **not** automatically rename the `.json Studio` production platform, Jira project key `JSON`, social handles, labels, chapter slugs or existing assets.
- Do not modify the founder-approved text of memoir chapters, historic posts/captions, previously approved video masters, visual artwork or platform settings during this naming migration.

## Implemented in this proposed change

- `book.json` sets `title` to `jason`; existing subtitle and chapter/edition structure stay the same.
- `README.md` project heading uses the new canonical book title.
- `shared/web/index.html` updates browser metadata and visible HTML brand/book labels to `jason`.
- Public `book.json.public_url` and reader deep links intentionally remain at the **currently deployed** slug until URL-migration acceptance. No redirect is assumed or invented.

## Requires a separate, verified URL migration

1. Change GitHub repo name to the founder-selected target only when it is available and migration is ready; current GitHub API reports the new target 404. Previously existing instruction: Change GitHub repo name from `jasonthedataguy/json-the-rabbit-hole-in-my-head` to **`jasonthedataguy/json-rabbit-hole-in-my-head`** using GitHub repository Settings when approved; confirm that name is free. The connector currently cannot rename repositories.
2. Check GitHub Pages publication under the new name, including the home reader and `/read/com-nguoi/` chapter alias on mobile and within Instagram.
3. Preserve old public links with an independently verified working redirect or stable custom domain before replacing any public CTA. Do **not** assume old `github.io/<old-repo>/` URL redirects automatically when a repository is renamed.
4. Once tested, update `book.json.public_url`, social bios, Jira active link destinations, GitHub links, QR codes, sites, publishing templates and campaign CTAs as a **separate approved cutover**. Historic publication URLs remain historical evidence.
5. Update book-cover/ring art or embedded logo text only after visual design review; source manuscripts and release-approved images are not rewritten.
6. Check repository code search for old title/slug and align copy in build outputs and other repositories, keeping backward-compatible identifiers where required.

## Current boundaries

- This is **title/copy preparation only**, not a publication, redeployment, social reschedule, automation change or new domain purchase.
- `.json Studio`, Jira keys and existing publishing connections are preserved.

## Founder slug correction — 2026-10-31 (authoritative target)

- Book: `jason - the rabbit hole in my head`.
- **Repository target:** `https://github.com/jasonthedataguy/json-rabbit-hole-in-my-head` (`json-rabbit-hole-in-my-head`, not `jason-the-rabbit-hole-in-my-head`).
- **Website target:** `https://jasonthedataguy.github.io/json-rabbit-hole-in-my-head/`, Cold Rice target `https://jasonthedataguy.github.io/json-rabbit-hole-in-my-head/read/com-nguoi/`.
- Verification: Connected GitHub currently returns the old repository; the new repository responds 404, and new Pages deployment could not be confirmed. Record this as founder-declared intended identity, not a verified live endpoint.
- Preserve current public links, historical Jira evidence and `book.json.public_url` until the new site and deep links are confirmed working. No publishing settings or automations changed.
