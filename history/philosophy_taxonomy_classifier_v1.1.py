#!/usr/bin/env python3
"""
philosophy_taxonomy_classifier_v1.1.py
Version 1.1 — Full 16-category edition

Complete XNOR-style classifier covering all 16 possible answer combinations
for distinguishing Philosophy vs Sophistry and their meta-variants.

Designed for direct use in substance_lens v0.5.6 pipelines,
Recursive Self-Exposure, Epistemic Lens Grinder, and Sophistry Detector.

New in v1.1:
- All 16 patterns now explicitly mapped (no more "Unclassified")
- 8 new categories for performative contradictions and mixed-priority cases
- Improved recursive second-pass logic for contradiction detection
- Updated category metadata (contradiction_type field support)

Usage:
    from philosophy_taxonomy_classifier_v1.1 import PhilosophyTaxonomyClassifier
    classifier = PhilosophyTaxonomyClassifier()
    result = classifier.classify_from_answers('A', 'A', 'A', 'B')  # SelfUnderminingClaim
    print(result)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json


@dataclass
class Category:
    id: int
    name: str
    description: str
    core_intent: str
    tools: str
    level: str
    honest_intent: bool
    pattern: str
    contradiction_type: Optional[str] = None


@dataclass
class DecisionQuestion:
    id: str
    question: str
    optionA: str
    optionB: str


class PhilosophyTaxonomyClassifier:
    def __init__(self, data_path: Optional[str] = None):
        if data_path:
            with open(data_path, 'r') as f:
                data = json.load(f)
            self._load_from_dict(data)
        else:
            self._load_default_v1_1()

    def _load_default_v1_1(self):
        self.name = "philosophy_taxonomy_xnor_classifier"
        self.version = "1.1"
        self.description = "Complete 16-category system covering all 2^4 answer combinations."

        self.categories: Dict[int, Category] = {
            # === Original 8 coherent categories (v1.0) ===
            1: Category(1, "Philosophy",
                "The genuine pursuit of truth using reason, evidence, and logical consistency, with willingness to be proven wrong.",
                "Truth-seeking", "Reason, logic, evidence", "Object-level", True, "AAAA"),
            2: Category(2, "Metaphilosophy",
                "The honest, self-reflective study of the nature, methods, strengths, and limits of philosophy itself.",
                "Truth-seeking", "Philosophical analysis", "Meta-level", True, "AABA"),
            3: Category(3, "Sophilosophy",
                "The skillful use of rhetoric, style, and persuasion in genuine service of making truth clearer, more compelling, and harder to evade.",
                "Truth-seeking", "Persuasion + truth-seeking", "Object-level", True, "ABAA"),
            4: Category(4, "Metasophilosophy",
                "The deliberate, self-aware use of persuasive skill to strengthen the boundary between genuine philosophy and sophistry.",
                "Truth-seeking", "Persuasive meta-rhetoric", "Meta-level", True, "ABBA"),
            5: Category(5, "Sophistry",
                "The use of rhetoric, fallacies, and linguistic tricks to win arguments or persuade, while being indifferent or hostile to truth.",
                "Persuasion/Victory", "Fallacies, emotional appeals", "Object-level", False, "BBAB"),
            6: Category(6, "Philosophistry",
                "Actively weaponizing philosophical concepts, terminology, and methods specifically to advance deceptive or self-serving goals.",
                "Persuasion/Victory", "Philosophical jargon + self-interest", "Object-level", False, "BAAB"),
            7: Category(7, "Metaphilosophistry",
                "Using philosophy to deliberately blur or erase the distinction between truth-seeking and deception, making the two appear equivalent.",
                "Persuasion/Victory", "Relativist collapse, boundary erasure", "Meta-level", False, "BABB"),
            8: Category(8, "Metasophistry",
                "The strategic use of sophisticated rhetorical techniques to defend sophistry and attack attempts to distinguish it from philosophy.",
                "Persuasion/Victory", "Sophisticated meta-rhetoric", "Meta-level", False, "BBBB"),

            # === New in v1.1: Performative contradictions (Q1=A + Q4=B) ===
            9: Category(9, "SelfUnderminingClaim",
                "Claims truth-seeking orientation while engaging in deceptive practices at the object level using philosophical tools. A performative contradiction.",
                "Truth-seeking (claimed) / Deceptive (practiced)", "Philosophical", "Object-level", False, "AAAB",
                "Performative contradiction (Q1=A + Q4=B)"),
            10: Category(10, "SelfUnderminingMeta",
                "Engages in meta-level philosophical reflection while maintaining deceptive intent. Often appears as sophisticated skepticism that exempts itself.",
                "Truth-seeking (claimed) / Deceptive (practiced)", "Philosophical", "Meta-level", False, "AABB",
                "Performative contradiction (Q1=A + Q4=B)"),
            11: Category(11, "DeceptiveSophilosophy",
                "Uses rhetorical skill while claiming truth-seeking, but with underlying deceptive intent. Rhetoric becomes a tool for winning rather than clarifying.",
                "Truth-seeking (claimed) / Deceptive (practiced)", "Rhetorical", "Object-level", False, "ABAB",
                "Performative contradiction (Q1=A + Q4=B)"),
            12: Category(12, "DeceptiveMetasophilosophy",
                "Deploys meta-rhetorical skill to defend truth-seeking while actually serving deceptive goals. Often blurs boundaries under the guise of sophistication.",
                "Truth-seeking (claimed) / Deceptive (practiced)", "Rhetorical (meta)", "Meta-level", False, "ABBB",
                "Performative contradiction (Q1=A + Q4=B)"),

            # === New in v1.1: Mixed priority (Q1=B + Q4=A) ===
            13: Category(13, "InstrumentalPhilosophy",
                "Uses philosophical tools and reason primarily to achieve victory or persuasion, while maintaining honest (non-deceptive) intent. Pragmatic but not purely truth-seeking.",
                "Persuasion/Victory (primary) / Honest (secondary)", "Philosophical", "Object-level", True, "BAAA",
                "Mixed priority (Q1=B + Q4=A)"),
            14: Category(14, "InstrumentalMetaphilosophy",
                "Applies meta-philosophical analysis with a primary goal of winning arguments or advancing a position, while remaining honest in method.",
                "Persuasion/Victory (primary) / Honest (secondary)", "Philosophical (meta)", "Meta-level", True, "BABA",
                "Mixed priority (Q1=B + Q4=A)"),
            15: Category(15, "DialecticalPragmatism",
                "Employs rhetorical skill and persuasion techniques with honest intent, but oriented toward winning or effective advocacy rather than pure truth-seeking.",
                "Persuasion/Victory (primary) / Honest (secondary)", "Rhetorical", "Object-level", True, "BBAA",
                "Mixed priority (Q1=B + Q4=A)"),
            16: Category(16, "StrategicMetasophilosophy",
                "Uses sophisticated meta-rhetoric and boundary-drawing with honest intent but a primary orientation toward persuasion or victory.",
                "Persuasion/Victory (primary) / Honest (secondary)", "Rhetorical (meta)", "Meta-level", True, "BBBA",
                "Mixed priority (Q1=B + Q4=A)"),
        }

        self.questions: List[DecisionQuestion] = [
            DecisionQuestion("Q1", "Primary Orientation?",
                "Truth-seeking (evidence-driven, open to correction)",
                "Persuasion/Victory (winning or self-interest matters more than truth)"),
            DecisionQuestion("Q2", "Primary Tools/Method?",
                "Philosophical (reason, logic, concepts, evidence)",
                "Rhetorical (style, persuasion, linguistic tricks)"),
            DecisionQuestion("Q3", "Level of Operation?",
                "Object-level (applying directly to claims/topics)",
                "Meta-level (about philosophy or sophistry itself)"),
            DecisionQuestion("Q4", "Underlying Intent?",
                "Honest/Genuine (aligns with stated goal)",
                "Deceptive/Self-serving"),
        ]

        self.mapping: Dict[str, Dict[str, Any]] = {
            "AAAA": {"mode": "Philosophy", "category_id": 1},
            "AABA": {"mode": "Metaphilosophy", "category_id": 2},
            "ABAA": {"mode": "Sophilosophy", "category_id": 3},
            "ABBA": {"mode": "Metasophilosophy", "category_id": 4},
            "AAAB": {"mode": "SelfUnderminingClaim", "category_id": 9},
            "AABB": {"mode": "SelfUnderminingMeta", "category_id": 10},
            "ABAB": {"mode": "DeceptiveSophilosophy", "category_id": 11},
            "ABBB": {"mode": "DeceptiveMetasophilosophy", "category_id": 12},
            "BAAA": {"mode": "InstrumentalPhilosophy", "category_id": 13},
            "BABA": {"mode": "InstrumentalMetaphilosophy", "category_id": 14},
            "BBAA": {"mode": "DialecticalPragmatism", "category_id": 15},
            "BBBA": {"mode": "StrategicMetasophilosophy", "category_id": 16},
            "BBAB": {"mode": "Sophistry", "category_id": 5},
            "BAAB": {"mode": "Philosophistry", "category_id": 6},
            "BABB": {"mode": "Metaphilosophistry", "category_id": 7},
            "BBBB": {"mode": "Metasophistry", "category_id": 8},
        }

        self.recursive_rule = (
            "Always feed the final classification back through the same 4 questions at least once. "
            "The second pass is especially important for patterns 9–16 (contradictions and mixed priorities), "
            "as the specific type of inconsistency often only becomes visible upon re-examination of the justification."
        )

    def _load_from_dict(self, data: dict):
        self.name = data.get("name", "philosophy_taxonomy_xnor_classifier")
        self.version = data.get("version", "1.1")
        self.description = data.get("description", "")

        self.categories = {}
        for cid, cat_data in data.get("categories", {}).items():
            self.categories[int(cid)] = Category(
                id=int(cid),
                name=cat_data["name"],
                description=cat_data["description"],
                core_intent=cat_data["core_intent"],
                tools=cat_data["tools"],
                level=cat_data["level"],
                honest_intent=cat_data["honest_intent"],
                pattern=cat_data.get("pattern", ""),
                contradiction_type=cat_data.get("contradiction_type")
            )

        self.questions = []
        for q in data.get("decision_tree", {}).get("questions", []):
            self.questions.append(DecisionQuestion(
                id=q["id"], question=q["question"],
                optionA=q["optionA"], optionB=q["optionB"]
            ))

        self.mapping = data.get("mapping", {})
        self.recursive_rule = data.get("recursive_rule", "")

    def get_pattern(self, q1: str, q2: str, q3: str, q4: str) -> str:
        def norm(x: str) -> str:
            x = x.strip().upper()
            if x in ("A", "1", "TRUE", "YES", "LEFT", "FIRST"):
                return "A"
            if x in ("B", "2", "FALSE", "NO", "RIGHT", "SECOND"):
                return "B"
            raise ValueError(f"Invalid answer: {x}. Use 'A' or 'B'.")
        return f"{norm(q1)}{norm(q2)}{norm(q3)}{norm(q4)}"

    def classify_from_answers(self, q1: str, q2: str, q3: str, q4: str,
                              recursive: bool = True) -> Dict[str, Any]:
        pattern = self.get_pattern(q1, q2, q3, q4)

        if pattern not in self.mapping:
            # Should no longer happen in v1.1
            result = {
                "pattern": pattern,
                "mode": "ERROR - Pattern not in mapping",
                "category_id": None,
                "warning": "This should not occur in v1.1. Check input."
            }
            return result

        entry = self.mapping[pattern]
        cat = self.categories[entry["category_id"]]

        result = {
            "pattern": pattern,
            "mode": entry["mode"],
            "category_id": entry["category_id"],
            "category": cat.name,
            "description": cat.description,
            "core_intent": cat.core_intent,
            "tools": cat.tools,
            "level": cat.level,
            "honest_intent": cat.honest_intent,
            "contradiction_type": cat.contradiction_type,
            "recursive_note": self.recursive_rule if recursive else None
        }

        if recursive:
            result["second_pass"] = self._perform_recursive_pass(result, pattern)

        return result

    def _perform_recursive_pass(self, first_pass_result: Dict[str, Any], original_pattern: str) -> Dict[str, Any]:
        mode = first_pass_result.get("mode", "")
        honest = first_pass_result.get("honest_intent")
        contradiction = first_pass_result.get("contradiction_type")

        second_pass = {
            "applied_to": "first_classification_and_justification",
            "detected_masquerade_risk": False,
            "detected_contradiction": bool(contradiction),
            "notes": []
        }

        if contradiction:
            second_pass["notes"].append(f"Detected {contradiction}. Second pass recommended on justification trace.")

        if mode in ["SelfUnderminingClaim", "SelfUnderminingMeta", "DeceptiveSophilosophy", "DeceptiveMetasophilosophy"]:
            second_pass["detected_masquerade_risk"] = True
            second_pass["notes"].append("High risk of performative contradiction. Examine whether the stated truth-seeking goal is consistent with observed behavior.")

        if mode in ["InstrumentalPhilosophy", "InstrumentalMetaphilosophy", "DialecticalPragmatism", "StrategicMetasophilosophy"]:
            second_pass["notes"].append("Mixed priority mode. Clarify whether persuasion or truth-seeking is the actual primary goal.")

        if not second_pass["notes"]:
            second_pass["notes"].append("Second pass stable. No additional contradictions detected.")

        return second_pass

    def classify_text_prompt(self, text: str) -> str:
        q_str = "\n".join(
            f"{q.id}: {q.question}\n  A: {q.optionA}\n  B: {q.optionB}"
            for q in self.questions
        )
        return f"""You are an expert epistemic classifier using the Philosophy vs Sophistry Taxonomy (v1.1 - Full 16 categories).

Analyze the following text/speech/argument rigorously and answer ONLY with the 4-letter pattern (e.g. AAAB or BBAA).

{text}

Decision Questions:
{q_str}

Respond with exactly 4 characters: only A or B for Q1-Q4 in order. No other text.
Example response: ABAA"""

    def get_category_summary(self) -> str:
        lines = ["# Philosophy Taxonomy Classifier v1.1 — All 16 Categories\n"]
        for cid in sorted(self.categories.keys()):
            c = self.categories[cid]
            intent = "Honest" if c.honest_intent else "Deceptive"
            contra = f" | {c.contradiction_type}" if c.contradiction_type else ""
            lines.append(f"**{cid}. {c.name}** ({c.pattern}) — {c.description[:120]}...")
            lines.append(f"   Intent: {c.core_intent} | Level: {c.level} | {intent}{contra}\n")
        return "\n".join(lines)

    def print_decision_tree(self):
        print("4-Question XNOR-Style Decision Tree (v1.1 - Full 16)")
        print("=" * 55)
        for q in self.questions:
            print(f"{q.id}: {q.question}")
            print(f"   A = {q.optionA}")
            print(f"   B = {q.optionB}\n")
        print("All 16 patterns are now mapped. See categories 9-16 for contradictions and mixed priorities.")


# Self-test
if __name__ == "__main__":
    classifier = PhilosophyTaxonomyClassifier()

    print("=== Philosophy Taxonomy Classifier v1.1 Self-Test ===\n")
    classifier.print_decision_tree()

    test_cases = [
        ("AAAA", "Classic Philosophy"),
        ("ABBA", "Metasophilosophy"),
        ("AAAB", "SelfUnderminingClaim (new)"),
        ("AABB", "SelfUnderminingMeta (new)"),
        ("BAAA", "InstrumentalPhilosophy (new)"),
        ("BBBA", "StrategicMetasophilosophy (new)"),
        ("BBBB", "Metasophistry"),
    ]

    for pattern, label in test_cases:
        q1, q2, q3, q4 = pattern[0], pattern[1], pattern[2], pattern[3]
        result = classifier.classify_from_answers(q1, q2, q3, q4)
        print(f"--- {label} ({pattern}) ---")
        print(f"Mode: {result['mode']}")
        if result.get("contradiction_type"):
            print(f"Contradiction: {result['contradiction_type']}")
        print()

    print("=== End Self-Test ===")