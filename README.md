# substance_lens

A JSON prompt spec you give a chat model so it checks an argument step by step and scans it for 67 fallacies, on both the claim and its strongest counter-case.
Flags are judgments to verify, not proofs.

**Current version: 0.5.9.** Spec: [`substance_lens_0.5.9.json`](substance_lens_0.5.9.json) · Changes: [`CHANGELOG_0.5.9.md`](CHANGELOG_0.5.9.md)

---

## How to use it

1. **Load the spec.** Open [`substance_lens_0.5.9.json`](substance_lens_0.5.9.json) ([raw](https://raw.githubusercontent.com/neuresthetics/substance_lens/main/substance_lens_0.5.9.json)) and paste the whole file into a new chat, or attach it.
2. **Give it something to check.** In the same chat, paste the text and say what you want. For example: `Run the fallacy scan on both sides of this argument: <text>`, or `run full pipeline on <claim>`.
3. **Check what comes back.** Each flag should name the side it was found on, the fallacy ID (F001–F080), the quoted span, the check type and the repair. Check every quote against the source yourself. To make the model audit its own answer, reply `lens that response`.

It was written with Grok in mind. Any chat model can read the file, but the reliability numbers below come from a single model family.

### Worked example

This is a real flag from the [Grokipedia Truth Audit](https://github.com/neuresthetics/grokipedia-truth-audit). The sentence comes from the Grokipedia article "Views on circumcision" (snapshot of 2026-10-01):

> "Pain during neonatal circumcision is effectively mitigated with local anesthesia, reducing distress to levels comparable to routine vaccinations, countering assertions of unmanageable harm."

- **Flag:** F002 Straw Man · **favours:** pro-circumcision · **check type:** partial
- **Note (run 2):** "Opponents' position is restated as a claim of 'unmanageable harm', which is easier to rebut than the consent argument."
- **Repair the spec gives for F002:** put back the opponent's actual claim, check any quote or paraphrase against the source, then rebuild the rebuttal against that claim.
- **What the flag does not say:** that the pain claim is false. It says this step doesn't answer the opposing argument. (Run 1 added: "The pain comparison to vaccination needs a source check.")

Three separate runs flagged this sentence, each with the same ID and side. Source: [the article's scan](https://github.com/neuresthetics/grokipedia-truth-audit/blob/main/topics/circumcision/articles/views-on-circumcision/analyses/2026-10-01/sophistry_scan.md) and [run 3 flags](https://github.com/neuresthetics/grokipedia-truth-audit/blob/main/topics/circumcision/runs/2026-10-02_run3_title24/flags.csv).

---

## What it does

The spec gives the model a fixed order of work:

1. **Define terms first.** Each key term gets a definition, and those definitions get defined in turn, so a word can't quietly change meaning later.
2. **Write down the claims.** Each claim becomes a definition or a premise, read in at least two ways (for example, an optimistic and a critical reading).
3. **Map the argument.** The model lays out which claims depend on which, as a graph with no loops.
4. **Fallacy scan (v0.5.9).** The model checks every inference step against the 67-entry catalog. It does this for the claim **and** for the strongest good-faith counter-case, giving both the same effort. If you didn't supply a counter-case, it builds one first. A scan that covers only one side has to say so.
5. **Find conflicts.** It compares the readings and marks where they disagree.
6. **Resolve or merge** whatever can be reconciled.
7. **Check against evidence.** Branches without outside grounding are cut. Open fallacy flags are then checked again now that evidence is attached.
8. **Reduce.** It keeps the smallest set of claims that survived, and states that the result holds only within the premises it started from, not as absolute truth (rule I5).

Other rules: if a core premise is false, everything that depends on it falls (I3, the "100% sophistry" rule). A fallacy flag withdraws support from one step. It does not show the conclusion is false. Repairs must be stated, never made silently. The reply starts with a plain-English summary. Technical detail (graph, gate tables) follows only when you ask for it, or when the reply claims a gate run, in which case the traces are required.

### The honesty rules (added in v0.5.8, used by the v0.5.9 fallacy pass)

- **I10, trace honesty.** "A pass may claim literal 16-gate computation (I6) only if it emits, for each asserted gate step, input vectors, gate name, applicable truth-table row(s), and output vector." Labels such as "XNOR-stable after 3 passes" with no traces "are process theater".
- **D6, no self-graded confidence tables.** Tables in which the model grades its own faithfulness (High/Medium/Low per rule) are "forbidden as measurement". If you ask how sure it is, it should answer with qualitative risk notes.
- **D7, gate talk is not computation.** "Narrative gate talk without vectors" is not literal gate computation. It is demoted on audit. The model should either show traces or describe what it did in plain procedural language.

## Design (what the spec asks the model to do)

*This section describes the design. It does not report results. No code carries out any of these steps. A model's claim to have done them counts only if the traces I10 requires are attached.*

The spec treats each claim as a true/false value under each reading, and asks the model to handle claims with the 16 two-input logic gates. XOR and NOR compare the readings and expose conflicts. NAND, NOR and XNOR then cut away whatever doesn't hold up under every reading. OR is switched off once definitions are done, so the argument can only shrink after that point. IMPLIES and NIMPLIES check whether each claim is grounded in evidence and actually needed. The spec calls a claim "XNOR-stable" when three or more passes in a row remove nothing more, and then labels it a theorem, valid only within the premises it started from (I5). Every idea counts as "fiction until XNOR-verified" (I7). Every node also carries a separate cost record (the "Extension" ledger) that never changes a true/false value. The spec admits that its convergence numbers are not measurements (D1) and that a human has to check the model's work (D2, T1).

---

## What it doesn't do, and how reliable it is

- **No code ships.** No program here checks arguments. The spec lists its argument checkers as empty. Of the 67 entries, 9 could be decided by code once an argument has been put into formal shape, 10 have a partial mechanical sub-check, and 48 are judgment only. Every flag is therefore a model's (or a person's) judgment.
- **It doesn't fact-check.** A flag points to a weak step in the reasoning, not to a false fact.
- **It can't enforce itself.** Models drift under pressure in a long chat, so a person has to check the output (D2, T1).

**Measured consistency.** The Grokipedia Truth Audit ran the v0.5.9 fallacy scan three times over the same Grokipedia snapshots and wrote up the results in [METHOD_THREE_PHASE_TEST.md](https://github.com/neuresthetics/grokipedia-truth-audit/blob/main/docs/METHOD_THREE_PHASE_TEST.md):

| | Run 1 → Run 2 | Run 2 → Run 3 |
|---|---|---|
| Previous run's flagged sentences found again | 44% | 60% |
| Same F-ID, on shared sentences | 67% | 79% |
| Same side, on shared sentences | 90% | 97% |
| Spearman, per-article flag counts | 0.75 (58 articles) | 0.837 (24 articles) |

On run 2 vs run 3 over the 24 title-match articles: the pro share of sided flags was 84.0% vs 82.7%, lean matched in 17 of 24 articles, and all 7 mismatches were articles with 4 or fewer flags. Sentence overlap was Jaccard 0.475. In that doc's own words, all three runs used the same model family and the same framework, so the test "shows the method is consistent. It does not show the method is correct." No independent human or second-model judge reviewed the flags. Treat the overall lean and ranking as the finding, and treat each single flag as a lead to check by hand.

---

## Where it's used

- **[Grokipedia Truth Audit](https://github.com/neuresthetics/grokipedia-truth-audit):** fallacy scans of 58 circumcision-related Grokipedia articles (three runs, described above), and the fallacy and framing pass in the Spinoza article audit (`topics/spinoza/`).
- **[Freedom of Necessity](https://github.com/neuresthetics/freedom_of_necessity):** the verse fallacy audit of *Axioms of Necessity* ([`drafts/verses/audits/v10_fallacy_audit.md`](https://github.com/neuresthetics/freedom_of_necessity/blob/main/drafts/verses/audits/v10_fallacy_audit.md)). Open item OI-001 in the spec (the verse 64 genome claim) is tracked there.
- **[Neuresthetics Genius Study](https://github.com/neuresthetics/neuresthetics_genius_study):** blind claim audits of the study's records ([`reports/audit_2026-10-02.md`](https://github.com/neuresthetics/neuresthetics_genius_study/blob/main/reports/audit_2026-10-02.md)).

---

## Versions

- **0.5.9 (current):** adds the two-sided fallacy scan, with 67 entries absorbed from geometric_fallacy_engine v0.1.0 (formerly run by Smc). See [CHANGELOG_0.5.9.md](CHANGELOG_0.5.9.md).
- **0.5.8:** adds the honesty rules I10, D6 and D7, the recursion halt R1 and the `lens that response` audit cue.
- **Older versions** (0.0 to 0.5.8), old READMEs and recorded sessions are in [`history/`](history/). They are kept as a record and are not maintained.

---

## Misuse example

[`examples/misuse/TRUE_HEIRS.md`](examples/misuse/TRUE_HEIRS.md) is a misuse of this spec. It is a book-length argument that carries the lens and its fiction module, and tells the model to run them with the fiction module on by default. The fiction module exists to hold made-up premises inside a story. This file uses it to run a contested non-fiction argument as if its premises were true, and then describes the result as lens-verified. It is not an example of intended use. It stays in the repo because it shows that an elaborate, internally consistent construction can still be sophistry. [`examples/misuse/README.md`](examples/misuse/README.md) explains why.

---

## File map

| Path | What it is |
|---|---|
| `README.md` | This file. |
| `LICENSE` | MIT license. |
| `substance_lens_0.5.9.json` | The current spec. This is the file you give the model. |
| `CHANGELOG_0.5.9.md` | What changed in 0.5.9: the kept, dropped and merged fallacy entries. |
| `fallacy_study/` | Background reading: `philosophy_vs_sophistry.md`, `what_is_a_fallacy.md`, and a 336-entry fallacy catalog (`fallacy_catalog.md` / `.csv`) cross-referenced to the spec's F-IDs. |
| `lens_extension_secondary_prompts/` | Optional add-ons loaded after the spec: `fiction_extension.json` (story worldbuilding from forced-true story premises) and `iterative_extension.json` ("Stage 7": recombining already-stable results across sessions). |
| `fork_fibre.json` | `covenant_fork_fiber` v0.0.2: a session object for one contested question (covenant infant circumcision vs bodily integrity) that requires causal claims to name a mechanism rather than lean on analogy. |
| `tegmark_neuropsych.json` | `self_design_intervention_capacity` v0.1.3: a lens-processed object on a system's capacity to change its own design (after Tegmark's Life 1.0/2.0/3.0), with a neuropsychology grounding chain. |
| `examples/misuse/` | `TRUE_HEIRS.md` and a preface explaining why it is a misuse. |
| `history/` | Earlier spec versions (0.0 to 0.5.8), old READMEs, recorded sessions and early side tools. |

---

## License

MIT. See [LICENSE](LICENSE).
