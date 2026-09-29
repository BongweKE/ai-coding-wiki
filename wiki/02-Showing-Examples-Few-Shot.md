> **Section 02 · Lesson 3** · Level: intermediate · ~12 min · Prereq: [Structuring instructions](02-Structuring-Instructions)

## Why this matters

Describing a format in prose takes a paragraph and still leaves room for interpretation. One worked example pins it down in four lines. Few-shot prompting — showing the model examples of the behaviour you want — is the cheapest way to move an agent from "roughly right" to "the same shape every time".

## One example beats three paragraphs

Compare these two ways to ask for a code review:

```text
Review the diff. Be concise. Report real bugs only.
```

```text
Review the diff. Format every finding like this example:

<example>
File: src/routes/invoices.ts line 42
Issue: query filters by id only; a merchant can read another merchant's invoice
Fix: add merchant_id to the WHERE clause
Severity: high
</example>
```

The second prompt gets findings that name a file, a line, a problem and a fix, because that is what the example shows. Anthropic's context-engineering guidance calls examples "the pictures worth a thousand words" and recommends curating a small set of canonical ones rather than stuffing in every rule.

## Choose examples that cover the edge, not the happy path

The natural instinct is to show the easy case. The model already handles the easy case; the example is there to define the boundary.

- Reviewing code? Use a finding that is subtle — a missing ownership check, not a typo.
- Writing tests? Show a test with a boundary input (empty list, zero amount), not the third happy path.
- Formatting errors? Show the message you want for an unknown account, not a generic 500.

Keep examples consistent with each other. Two review examples that use different severity words teach the model that the vocabulary is optional.

## Negative examples are for review and formatting

When the task is "do not do this", a negative example with a reason is often clearer than a rule.

```text
<bad_example>
"Great work! You might want to consider adding some tests."
</bad_example>

Why this is bad: no file, no line, no action. You cannot fix it.
```

Marking examples as good and bad explicitly matters. If you only label the good ones, the model reads the bad one as a second style to imitate — which is exactly the kind of quiet failure that shows up as "the reviewer keeps giving vague feedback".

Use negative examples in review prompts, formatters, commit-message drafting, and anywhere the difference between acceptable and unacceptable is a judgement call. Use them sparingly in generation tasks: a bad example of code is a bad example of code.

## Where examples belong long-term

An example pasted into a chat dies with the session. Compaction may drop it. A teammate never sees it.

![Prompt anatomy](https://raw.githubusercontent.com/BongweKE/ai-coding-wiki/main/assets/02-prompt-anatomy.png)

Two homes for examples that matter:

- **The rules file** for anything short and universal — the review format, the commit-message shape, the naming convention. One example, two lines.
- **A skill** for anything procedural that comes with more material — the test-writing skill with its three worked tests and its bundled fixtures. See [What are Agent Skills?](04-What-Are-Agent-Skills) and [Writing good skills](04-Writing-Good-Skills).

The rules of thumb: an example you have rewritten by hand in two sessions belongs in the repo. An example that needs a paragraph of explanation belongs in a skill, where it loads only when relevant.

## Try it

1. Pick a task where you keep correcting the output's shape — a review, a changelog entry, a PR description.
2. Take the last good output the agent produced and paste it as a labelled `<example>` in your prompt.
3. Add one negative example drawn from a real bad output, with one line on why it is bad.
4. Run the prompt twice on different inputs and check the shapes match.
5. Move the pair into `AGENTS.md` (short) or a skill (long) and delete it from your scratch file.

## Common mistakes

- **Happy-path-only examples.** You teach the format but not the judgement. Include the awkward case.
- **Examples the model copies literally.** If your example uses `INV-001` and `KES 250`, some outputs will too. Use placeholder-looking values and say "these are examples, use the real values from the input".
- **Inconsistent examples.** Different severity labels, different heading styles, different lengths — the model averages them into mush.
- **Showing a bad example without labelling or explaining it.** The model imitates what it sees. Label it `<bad_example>` and give the reason in one line.
- **A laundry list of edge cases.** Twenty examples of corner cases crowd out the actual task. Three diverse canonical examples beat twenty exhaustive ones.
- **Leaving examples in chat history.** They vanish from the next session and from your teammate's view. Put them in the repo.

## Key takeaways

- One worked example beats a paragraph of description; format is easier to show than to describe.
- Curate a few diverse canonical examples instead of every edge case you can think of.
- Cover the awkward case — the happy path is not what you are teaching.
- Negative examples need an explicit label and a one-line reason, or they read as more style to copy.
- Examples that survive belong in the rules file or a skill, not in a chat window.

## Further learning

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — guidance on curating examples and keeping context high-signal.
- [Anthropic's prompt engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — dedicated chapters on giving the model examples and structuring outputs.
- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — pointing an agent at existing patterns in your own codebase as examples.
