# Contributing to *Coding With AI in the New Age*

This wiki is a free, technical handbook. Contributions are welcome — especially corrections, real
lessons, and links to sources that are better than the ones we cite.

## How this repository and the wiki relate

- `wiki/*.md` is the **source of truth**. Every page lives in this repository, so changes are
  reviewable, diffable and versioned.
- The GitHub wiki is a **rendering** of those files, synced with `scripts/push_wiki.sh`.
- `WIKI-MANIFEST.md` is the page list (numbered, authoritative). Section index pages, the Home page
  and the sidebar are generated from it.
- `assets/` holds generated infographics; `scripts/build_infographics.py` rebuilds them;
  `tools/` holds the interactive single-file visualisers; `scripts/check_wiki.py` is the gate.

## Before you open a pull request

```bash
python3 scripts/check_wiki.py --strict     # structure, links, assets, mermaid, secrets, banned words
```

Fix every error. Warnings are worth fixing too: they are the checks that catch the mistakes people
actually make.

If you change `scripts/build_infographics.py`, regenerate and commit the PNGs:

```bash
python3 scripts/build_infographics.py assets/
```

## House style, in one screen

The full version is [STYLE.md](STYLE.md); the short version:

1. **No H1.** The wiki renders the page title itself. Start with the metadata blockquote:

   ```
   > **Section 05 · Lesson 3** · Level: beginner · ~12 min · Prereq: [Git essentials](05-Git-Essentials)
   ```

2. **600–1000 words of prose.** Bite-sized beats exhaustive. Split the page instead of sprawling.
3. **Every page has** `## Why this matters`, at least one `## Try it` with a runnable step, a
   `## Common mistakes` list with specific failures, `## Key takeaways`, and `## Further learning`.
4. **Verified links only.** If you have not seen the URL, link the documentation root instead. A
   confident deep link that 404s is worse than no link.
5. **Grounded claims.** Version numbers, prices, quotas and model names change. Say "as of <year>",
   link the source, or leave it out.
6. **No secrets, ever** — not even fake-looking ones. Use `os.environ["SERVICE_API_KEY"]`.
7. **Sanitise.** Lessons may come from real private projects; never publish hostnames, internal URLs,
   credentials, customer data, vendor or client names, or private repo paths. Generalise the example,
   keep the lesson.
8. **Mermaid must render.** Allowed: `flowchart`, `graph`, `sequenceDiagram`, `stateDiagram-v2`,
   `erDiagram`, `classDiagram`, `gantt`, `timeline`, `gitGraph`. No init directives, no click
   handlers, quote labels containing punctuation, and keep diagrams under about twenty nodes.
9. **Write from experience.** A page should contain at least one thing you learned by being wrong.
   Summarising someone else's blog post is not a contribution; a specific failure and its fix is.
10. **Plain voice.** Second person, active, no hype. `check_wiki.py` flags the obvious filler words.

## Adding a page

1. Add it to the manifest source (the build tooling that generates `WIKI-MANIFEST.md`), or open an
   issue describing the page and its place in the numbered sequence.
2. Write `wiki/<NN>-<Title>.md` following the skeleton above.
3. Run the checker, then open a PR. CI runs the same checks plus a regenerated-infographics diff.

## Reporting a mistake

Open an issue with the page name, the sentence, and what is wrong. If you know the correct answer,
include the source. Corrections to *factual* claims are the most valuable contributions this wiki
can receive, because the field moves faster than any page can.

## Licence

Wiki text is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); scripts and tools are MIT
(see [LICENSE](LICENSE)). By contributing you agree to publish your contribution under the same terms.
