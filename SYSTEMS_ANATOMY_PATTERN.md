# Systems Anatomy Pattern — Sitewide Integration Guide

## Origin
Inspired by an interactive 3D jet engine visualization (Instagram @aialchemists, Oct 2026): "A textbook diagram shows you one part. This shows you how all of it moves together."

## Core Principle
Teach complex systems as **living, moving assemblies** — not static diagrams. Every technical concept should be explorable as:
1. **Whole in context** — See the system where it lives
2. **Cut open** — Reveal internal layers/components  
3. **Step through** — Walk the process in sequence
4. **Pull apart** — Exploded view with labeled pieces

## Implementation Template

### 1. Domain Structure (content.json)
Each course should have a `systems-anatomy` domain (or equivalent) with:
- **3 lessons** following the pattern: Concept → Deep Dive → Applied
- **2 scenarios** requiring systems-thinking troubleshooting
- Lessons must include `example.walkthrough` narrating the journey
- Scenarios must have `evidence` showing system state at each layer

### 2. Interactive Explorer (visuals/systems-anatomy-explorer.html)
Reusable HTML component with:
- System selector buttons (4-6 systems per course)
- Step-through flow with active/done states
- Detail panels showing protocol-level data
- "Interview Insight" revealed on completion
- Mobile-responsive, keyboard-accessible

**To adapt for a new course:**
1. Copy `systems-anatomy-explorer.html`
2. Replace the `systems` JS object with course-specific flows
3. Each system needs: title, insight, steps[] (title, desc, detail)
4. Update the system selector buttons

### 3. Lesson Content Pattern
```json
{
  "title": "Anatomy of [System]: [Subtitle]",
  "concepts": [
    "[System] is a [N]-step [process]: [step1] → [step2] → [step3]",
    "See it as a journey: [start] → [middle] → [end], with [artifacts] as the physical tokens",
    "[Critical dependency] matters because [reason] — [failure mode]",
    "[Course-specific] relevance: [how this connects to the job role]"
  ],
  "example": {
    "code": "[Step-by-step trace with arrows showing the journey]",
    "walkthrough": "Use the [Explorer] in Visuals. Click through each step and watch [artifacts] move."
  }
}
```

### 4. Scenario Content Pattern
Scenarios must require **systems tracing**, not memorization:
- **Situation**: Symptom that misleads (e.g., "wrong password" when it's clock skew)
- **Evidence**: System state at different layers (logs, configs, outputs)
- **Correct answer**: The one that traces the full journey
- **Why**: Explains the living system, not just the fix

## Courses to Integrate (Priority Order)
1. ✅ tl-infra-assessment-prep (DONE — 23 domains, 95 lessons)
2. tl-interview (ThreatLocker product focus)
3. All certification bootcamps (A+, Network+, Security+, CCNA)
4. All university courses (interstitiumlabs.dev/university/)

## Verification Checklist
- [ ] Domain appears in Learn path with correct lesson/scenario counts
- [ ] Explorer HTML loads without JS errors
- [ ] All step-through buttons work (Prev/Next/Reset/System switch)
- [ ] Mobile responsive (test at 390×844)
- [ ] Interview Insight appears on final step
- [ ] Lessons auto-complete on correct knowledge check
- [ ] Scenarios show correct letter after shuffle

## References
- Source inspiration: https://www.instagram.com/reel/DeBXPzPj6au/
- Live implementation: https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/visuals/systems-anatomy-explorer.html
- CBT domain: systems-anatomy (23rd domain in tl-infra-assessment-prep)
