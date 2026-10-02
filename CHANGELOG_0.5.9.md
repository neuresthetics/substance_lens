# substance_lens v0.5.9 — CHANGELOG

**Date:** 2026-10-01 (PT) · **Previous:** 0.5.8 (archived at `history/substance_lens_v0.5.8.json`)  
**Source credit:** absorbed from geometric_fallacy_engine v0.1.0, formerly run by Smc.

## Summary

- New top-level `fallacyScanPass`: an extra scan pass. Of Smc's 80 catalog entries, **67 kept**, **6 dropped** (already covered by a v0.5.8 rule) and **7 merged** (duplicates). 67 + 6 + 7 = 80.
- **Pipeline position:** main scan at Stage 2.5 (after the Geometric Constructor, before the Conflict Analyzer), with a re-scan at Stage 5.5 (after the Evidence Validator, before the Invariant Reducer). The `classicPipeline` array itself is unchanged.
- **Both sides by default:** every check runs on the claim AND its counter/steel-man side, with matched budgets. If no counter-case is supplied, one is built first.
- **Honesty (I10/D6/D7):** the `break` wording is the engine's graph metaphor. No argument checker is implemented, so every flag is model or human judgment unless code actually ran. Kept entries are labelled: code-checkable 9, partial 10, judgment 48.
- A flag removes warrant from the flagged edge. It does not show the conclusion is false.
- New `openItems` (OI-001: verse 64 genome claim, owned by freedom_of_necessity) and `patch_0_5_9`. Every v0.5.8 section is unchanged apart from `version`.

## KEPT

Legend: [C] code-checkable once formalized · [P] partial (has a mechanical sub-check) · [J] judgment only

### Relevance (16)

- F001 Ad Hominem [J]
- F002 Straw Man [P]
- F003 Red Herring [J]
- F004 Appeal to Authority [P]
- F005 Appeal to Popularity [J] (absorbs F006)
- F007 Appeal to Emotion [J] (absorbs F008, F009)
- F024 Tu Quoque [J]
- F025 Guilt by Association [J]
- F026 Poisoning the Well [J]
- F027 Genetic Fallacy [J]
- F028 Appeal to Tradition [J]
- F029 Appeal to Novelty [J]
- F043 Misleading Vividness [J]
- F075 Appeal to Consequences [J]
- F076 Wishful Thinking [J]
- F077 Fallacy of Relative Privation [J]

### Insufficiency (11)

- F010 Appeal to Ignorance [J]
- F011 Hasty Generalization [P] (absorbs F023, F044)
- F012 Slippery Slope [J]
- F036 Suppressed Evidence [J]
- F052 Argument from Incredulity [J]
- F053 Argument from Repetition [P]
- F071 Base Rate Neglect [P]
- F072 Conjunction Fallacy [C]
- F073 McNamara Fallacy [J]
- F074 Prosecutor's Fallacy [P]
- F079 Shotgun Argumentation [J]

### Presumption (12)

- F013 False Dilemma [J]
- F016 Complex Question [J]
- F038 Moving the Goalposts [P]
- F039 No True Scotsman [P]
- F045 Sunk Cost Fallacy [J]
- F048 Middle Ground [J]
- F057 Historian's Fallacy [J]
- F058 Presentism [J]
- F059 Moralistic Fallacy [J]
- F060 Naturalistic Fallacy [J]
- F061 Is-Ought Jump [J] (absorbs F030)
- F080 Nirvana Fallacy [J]

### Ambiguity (15)

- F019 Composition [J]
- F020 Division [J]
- F021 Accent [P]
- F022 Accident [J]
- F040 Loaded Language [J]
- F041 False Equivalence [J]
- F042 False Analogy [J]
- F049 Fallacy of the Beard [J]
- F050 Reification [J]
- F054 Etymological Fallacy [J]
- F055 Ecological Fallacy [J]
- F056 Exception Fallacy [J]
- F062 Masked Man Fallacy [J]
- F063 Quantifier Shift [C]
- F064 Existential Fallacy [C]

### Causal (7)

- F031 Post Hoc [J]
- F032 Cum Hoc [J]
- F033 Causal Oversimplification [J]
- F034 False Cause [J]
- F035 Texas Sharpshooter [P]
- F046 Gambler's Fallacy [J]
- F047 Hot Hand Fallacy [J]

### Formal (6)

- F065 Illicit Major [C]
- F066 Illicit Minor [C]
- F067 Undistributed Middle [C]
- F068 Exclusive Premises [C]
- F069 Affirming the Consequent [C]
- F070 Denying the Antecedent [C]

## DROPPED (covered by an existing v0.5.8 rule)

- F014 Begging the Question (absorbs F015) → keyRules: Construction DAG is directed acyclic; constructionDAGProperties.cycleDetection
- F017 Equivocation → classicPipeline stage 1 Definition & Axiom Encoder; keyRules: Pre-Stage 0 Recursive Definition Layer; classicPipeline stage 3 Conflict Analyzer; operatorProtocols.lens_that_response
- F018 Amphiboly → classicPipeline stage 1 Definition & Axiom Encoder; classicPipeline stage 3 Conflict Analyzer; coreMotif.operationalMechanicsForAI Step 2
- F037 Special Pleading → coreMotif.mutualAxiomCoherence; operatorProtocols.lens_that_response
- F051 Ipse Dixit → classicPipeline stage 5 Evidence Validator; I7 All ideas are fiction until XNOR-verified
- F078 Kettle Logic → coreMotif.mutualAxiomCoherence; classicPipeline stage 4 Consistency Resolver; explicitGates.NAND

## MERGED (duplicate engine entries)

- F006 Bandwagon Fallacy → F005 Appeal to Popularity. Engine marks F006 'same geometric break as F005' (popularity as warrant); social-pressure cue carried into F005.
- F008 Appeal to Pity → F007 Appeal to Emotion. Pity is listed inside F007's own break (fear/pity/pride/anger). Pity-specific repair carried into F007.
- F009 Appeal to Fear → F007 Appeal to Emotion. Fear is listed inside F007's own break. Fear-specific repair (require risk model) carried into F007.
- F015 Circular Argument → F014 Begging the Question. Engine marks F015 'same as F014' (circularity via synonym Definitions). Merged into F014, which is DROPPED to DAG cycle detection; synonym restatement is also exposed by Pre-Stage 0 recursive definition.
- F023 Converse Accident → F011 Hasty Generalization. Converse accident is the classical name for hasty generalization (Copi & Cohen); engine aka says 'hasty generalization variant'.
- F030 Appeal to Nature → F061 Is-Ought Jump. Appeal to nature has the same break as the is-ought jump (descriptive 'natural' premise -> normative conclusion with no bridge Axiom).
- F044 Anecdotal Fallacy → F011 Hasty Generalization. Anecdotal fallacy is hasty generalization at n=1 (engine relates F011).

## Not absorbed from the engine (non-catalog parts)

- output_contract.header_required method-disclosure header: Conflicts with lens response_style, which starts with a plain-English paragraph. Disclosure is instead covered by I10 and by naming this pass in the output.
- bias_hardening.impartiality_dimensions open scoring: Numeric dimension scores would be cardinal semantic measurements, which D1/T2 forbid. The dual-case and source-balance parts are absorbed.
- optional_consent_audit (M4, default off): Out of scope for a sophistry lens.
- optional_collision (M5): The lens's own Stage 3/4 already does the collision; only its dual-case precondition is absorbed.
- output_contract.forbidden_output_modes 'self-graded faithfulness confidence tables': Already v0.5.8 D6/T5.

## Files

- `substance_lens_v0.5.9.json` (new; also copied to `substance_lens_current.json`)
- `ACTIVE.json` → 0.5.9 (previous 0.5.8)
- `history/substance_lens_v0.5.8.json` + `history/v0.5.8_checkpoint_meta.json`
- `validate_fallacy_pass.py` (structure/traceability validator adapted from Smc's `validate_structure.py`; its only computation is a form-level truth-table test of F069/F070 using the lens's own `explicitGates.IMPLIES`)
