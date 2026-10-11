#!/usr/bin/env python3
"""Batch 6 (part 4): humanmetrics, fullstack-desk.
5 simulations + 4 consoleSims + 7 terminalMissions each (bash-lite profile,
outputs verified with node harness 2026-10-08).
Atomic write (tmp + os.replace), json.load re-validation.
"""
import json, os, re

BASE = '/home/hatch/workspace/cert-bootcamps/site/bootcamps'

# ------------------------------------------------------------- humanmetrics
HUM_SIMS = [
 {"id":"hum-sim-1","title":"The 51/49 split","kind":"troubleshoot",
  "domain_id":"humanmetrics","difficulty":2,"points":100,
  "brief":"A candidate scores 51/49 on Extraversion/Introversion and the hiring manager wants a label. Hold the line on honesty.",
  "steps":[
   {"symptom":"A candidate scores 51% Extraversion / 49% Introversion. The hiring manager wants a label.",
    "evidence":[["result","E 51 / I 49, preference clarity: slight"]],
    "options":["Report a slight preference for Extraversion \u2014 near-ties are the instrument saying 'unclear', not a type verdict",
               "Label them Extravert",
               "Label them Introvert",
               "Retest until it is 70/30"],
    "correct":0,
    "explain":"Humanmetrics reports preference clarity for a reason: 51/49 is within the instrument's noise. Honest reporting says 'slight' and moves on."},
   {"symptom":"The manager still wants one letter for the org chart.",
    "evidence":[["request","one letter, no nuance"]],
    "options":["Refuse the false precision: give the full profile with clarity bands \u2014 the chart can carry four letters with qualifiers",
               "Give them E",
               "Flip a coin",
               "Make up a stronger score"],
    "correct":0,
    "explain":"Collapsing a near-tie to a letter manufactures certainty the data does not contain. The ethical move is the full, qualified profile."},
   {"symptom":"How do you use a 51/49 result in coaching?",
    "evidence":[["coaching","working-style conversation"]],
    "options":["Treat it as flexibility: the person draws on both modes \u2014 coach the range, not the label",
               "Coach them as an extravert",
               "Coach them as an introvert",
               "Ignore the dimension"],
    "correct":0,
    "explain":"Near-ties are information: this person flexes. Coaching the range beats coaching the label."}],
  "debrief":"Close scores are the instrument being honest: report the clarity, refuse false precision, coach the range."},
 {"id":"hum-sim-2","title":"Type is not a trait score","kind":"troubleshoot",
  "domain_id":"humanmetrics","difficulty":2,"points":100,
  "brief":"A manager turns a Thinking preference into a character verdict, then into a hiring filter. Correct both errors.",
  "steps":[
   {"symptom":"A manager says 'She scored 90% Thinking, so she has no empathy.' Correct the category error.",
    "evidence":[["result","T 90 (very clear)"]],
    "options":["Thinking/Feeling is about decision criteria (logic vs values), not capacity for empathy \u2014 the inference is invalid",
               "Agree with the manager",
               "Retest her",
               "Move her off the team"],
    "correct":0,
    "explain":"Jungian preferences describe preferred decision-making, not ability or character. T-preference people feel deeply; they just decide differently."},
   {"symptom":"The manager now wants to use types for hiring filters.",
    "evidence":[["proposal","only hire INTJs for engineering"]],
    "options":["Refuse: the instrument was not validated for selection, and type-based hiring is both unethical and legally exposed",
               "Implement the filter",
               "Use it quietly",
               "Ask HR to approve"],
    "correct":0,
    "explain":"Humanmetrics-style instruments lack the validity evidence selection requires, and filtering by type invites adverse-impact liability. Development yes; selection no."},
   {"symptom":"Where does the instrument legitimately help?",
    "evidence":[["use cases","team workshops, coaching, communication"]],
    "options":["Self-knowledge and team communication: a shared vocabulary for working-style differences",
               "Hiring",
               "Promotion",
               "Termination"],
    "correct":0,
    "explain":"The instrument's valid home is development: understanding yourself and adapting to others. Every selection use is out of scope."}],
  "debrief":"Know what the instrument is: a preferences lens for growth \u2014 never a hiring filter, never a character verdict."},
 {"id":"hum-sim-3","title":"Staff the on-call rotation","kind":"troubleshoot",
  "domain_id":"humanmetrics","difficulty":3,"points":100,
  "brief":"Build a 4-person on-call rotation from type profiles. Use types to inform \u2014 and know exactly where their authority ends.",
  "steps":[
   {"symptom":"Build a 4-person on-call rotation from type profiles. What do you optimize for?",
    "evidence":[["team","mixed E/I, S/N, T/F, J/P"]],
    "options":["Coverage of working styles across the rotation: pairing detail-oriented with big-picture, structured with adaptable",
               "All Judgers for discipline",
               "All Perceivers for flexibility",
               "Random"],
    "correct":0,
    "explain":"Diverse rotations catch more failure modes: the S notices the anomaly, the N sees the pattern, the J follows the runbook, the P improvises."},
   {"symptom":"Two Sensors want the same holiday week. Resolve it with type-awareness, not favoritism.",
    "evidence":[["conflict","both planned around the holiday months ago"]],
    "options":["A transparent rotation rule decided in advance (seniority/alternation) \u2014 type-awareness explains the clash, the rule resolves it",
               "Give it to the louder one",
               "Manager picks favorites",
               "Cancel both leaves"],
    "correct":0,
    "explain":"Type language diagnoses (both plan concretely, far ahead); it must not decide. Pre-agreed rules decide \u2014 personality never allocates scarce goods."},
   {"symptom":"The rotation is live. How do you review it?",
    "evidence":[["metrics","page counts, ack times, burnout survey"]],
    "options":["Review outcomes (load fairness, response quality), not types \u2014 the roster is judged by results",
               "Review by type balance",
               "Never review",
               "Ask who is happiest"],
    "correct":0,
    "explain":"Staffing decisions are validated by operational outcomes. Type diversity is a hypothesis; page-load fairness is the measurement."}],
  "debrief":"Types inform team design; outcomes judge it. Never let a preference label allocate, and always measure the result."},
 {"id":"hum-sim-4","title":"From type to career map","kind":"troubleshoot",
  "domain_id":"humanmetrics","difficulty":2,"points":100,
  "brief":"An INTP analyst asks what roles fit. Map preferences to work modes \u2014 and honor the life that contradicts the map.",
  "steps":[
   {"symptom":"An INTP analyst asks what roles fit. Map the preferences, not the stereotype.",
    "evidence":[["profile","I 80, N 75, T 90, P 65 \u2014 all clear"]],
    "options":["Map each preference to work modes: I\u2192deep solo work, N\u2192systems and patterns, T\u2192logic-driven decisions, P\u2192exploratory scope \u2014 then match roles to the modes",
               "Say 'data scientist' and stop",
               "Say 'avoid people'",
               "Refuse to advise"],
    "correct":0,
    "explain":"The honest mapping is preferences \u2192 work modes \u2192 roles. Stereotype-matching ('INTPs do X') skips the reasoning and bakes in bias."},
   {"symptom":"They love their current support-desk role despite the 'wrong' type. Response?",
    "evidence":[["reality","thriving on the desk for 2 years"]],
    "options":["Celebrate it: the instrument describes preferences, not permissions \u2014 lived fit beats predicted fit",
               "Tell them to quit",
               "Retest them",
               "Explain they are mistyped"],
    "correct":0,
    "explain":"Reality outranks the model. If someone thrives where the type says they shouldn't, the type description was incomplete \u2014 not the person."},
   {"symptom":"They ask for one practice to grow. What do you prescribe?",
    "evidence":[["growth","non-preferred modes"]],
    "options":["Deliberate practice in the non-preferred mode (structured facilitation) \u2014 type development is range, not prison",
               "Stay in the comfort zone",
               "Change type",
               "Ignore growth"],
    "correct":0,
    "explain":"Type theory's own growth story is developing the non-preferred functions. Range is the goal; the label is the starting line."}],
  "debrief":"Career mapping is preferences \u2192 modes \u2192 roles, and lived fit always outranks the prediction."},
 {"id":"hum-sim-5","title":"The retest wobble","kind":"troubleshoot",
  "domain_id":"humanmetrics","difficulty":2,"points":100,
  "brief":"INTJ becomes INTP on retest. Explain the wobble with clarity bands \u2014 and refuse to narrate identity from noise.",
  "steps":[
   {"symptom":"A candidate retests after 6 months: INTJ \u2192 INTP. The J/P flipped. Is the instrument broken?",
    "evidence":[["scores","J 55 \u2192 P 58, others stable"]],
    "options":["No \u2014 near-tie dimensions wobble; the 55/58 flip is the same slight preference measured twice with noise",
               "Yes, discard it",
               "Average to INXJ",
               "Test a third time and take the majority"],
    "correct":0,
    "explain":"Test-retest reliability is lowest at the middle. A 3-point swing across the line is expected noise, not instrument failure."},
   {"symptom":"Which dimensions should you trust most in this profile?",
    "evidence":[["clarity","I 85, N 80, T 90, P 58"]],
    "options":["The high-clarity ones (I, N, T) \u2014 clarity bands are the confidence intervals; trust scales with them",
               "All equally",
               "None",
               "Only the flipped one"],
    "correct":0,
    "explain":"Preference-clarity scores are the instrument's own uncertainty bars. Read them as confidence: 90 is a signal, 58 is a shrug."},
   {"symptom":"The candidate asks what changed about them in 6 months.",
    "evidence":[["question","did I change?"]],
    "options":["Probably nothing structural \u2014 the wobble is measurement noise on a near-tie; check life context before narrating change",
               "You became a different person",
               "The test was wrong the first time",
               "Mood explains everything"],
    "correct":0,
    "explain":"Do not narrate identity change from a 3-point swing. Ask about life context first; the numbers alone say 'noise'."}],
  "debrief":"Retest wobbles are clarity-band physics: trust high-clarity dimensions, shrug at near-ties, and never narrate identity from noise."}
]

HUM_CONSOLES = [
 {"id":"hum-console-1","title":"Configure the assessment","console":"generic-web",
  "domain_id":"humanmetrics","difficulty":1,
  "brief":"Set up the cohort's assessment record in the program form.",
  "tasks":[
   {"id":"hum-c1-t1","instruction":"Set the cohort name field (site_name) to humanmetrics-cohort-3.",
    "validate":{"action":"set-field","params":{"id":"site_name","value":"humanmetrics-cohort-3"}},
    "hint":"Set field site_name to humanmetrics-cohort-3."},
   {"id":"hum-c1-t2","instruction":"Set the coach contact field (admin_email) to coach@example.com.",
    "validate":{"action":"set-field","params":{"id":"admin_email","value":"coach@example.com"}},
    "hint":"Set field admin_email to coach@example.com."},
   {"id":"hum-c1-t3","instruction":"Set the timezone field to UTC.",
    "validate":{"action":"set-field","params":{"id":"timezone","value":"UTC"}},
    "hint":"Set field timezone to UTC."},
   {"id":"hum-c1-t4","instruction":"Submit the configuration.",
    "validate":{"action":"submit-form","params":{}},
    "hint":"Press Submit settings."}],
  "debrief":"Assessments start with administration: cohort, coach, timezone \u2014 filed before anyone answers a question."},
 {"id":"hum-console-2","title":"Query the team matrix","console":"sql-studio",
  "domain_id":"humanmetrics","difficulty":2,
  "brief":"The working-style team matrix is a table. Build it and query it in the SQL workbench.",
  "tasks":[
   {"id":"hum-c2-t1","instruction":"Create table team_types with columns id INTEGER, type TEXT.",
    "validate":{"action":"create-table","params":{"name":"team_types","columns":"id INTEGER, type TEXT"}},
    "hint":"Create table team_types (id INTEGER, type TEXT)."},
   {"id":"hum-c2-t2","instruction":"Index the type column.",
    "validate":{"action":"create-index","params":{"table":"team_types","column":"type"}},
    "hint":"Create an index on team_types.type."},
   {"id":"hum-c2-t3","instruction":"Run a query selecting types from team_types.",
    "validate":{"action":"run-query","params":{"match":"team_types"}},
    "hint":"Run any SELECT that mentions the team_types table."}],
  "debrief":"Team matrices are data: record the types, index the lookup, query the mix."},
 {"id":"hum-console-3","title":"Store the results","console":"db-admin",
  "domain_id":"humanmetrics","difficulty":2,
  "brief":"Stand up the assessments database with a least-privilege coach role.",
  "tasks":[
   {"id":"hum-c3-t1","instruction":"Create the database assessments.",
    "validate":{"action":"create-database","params":{"name":"assessments"}},
    "hint":"Create database assessments."},
   {"id":"hum-c3-t2","instruction":"Create the database user coach.",
    "validate":{"action":"create-user","params":{"name":"coach"}},
    "hint":"Create user coach."},
   {"id":"hum-c3-t3","instruction":"Grant SELECT on assessments to coach.",
    "validate":{"action":"grant-priv","params":{"db":"assessments","user":"coach","priv":"SELECT"}},
    "hint":"Grant SELECT on assessments to coach."}],
  "debrief":"Assessment data is sensitive: its own database, a reader role, SELECT and nothing more."},
 {"id":"hum-console-4","title":"Triage the coaching request","console":"ticketing",
  "domain_id":"humanmetrics","difficulty":1,
  "brief":"A candidate requests a career-mapping session. File it, route it to the coach, and record completion of the assessment.",
  "tasks":[
   {"id":"hum-c4-t1","instruction":"Create a P3 ticket titled 'Career mapping session request'.",
    "validate":{"action":"create-ticket","params":{"title":"Career mapping session request","priority":"P3"}},
    "hint":"New ticket tab \u2192 title 'Career mapping session request', priority P3."},
   {"id":"hum-c4-t2","instruction":"Assign the new ticket INC-9002 to coach.",
    "validate":{"action":"assign-ticket","params":{"id":"INC-9002","assignee":"coach"}},
    "hint":"Assign INC-9002 to coach."},
   {"id":"hum-c4-t3","instruction":"Add a note to INC-9002: candidate completed the assessment.",
    "validate":{"action":"add-note","params":{"id":"INC-9002","text":"Candidate completed the assessment."}},
    "hint":"Add the completion note to INC-9002."}],
  "debrief":"Coaching operations are tickets too: request, owner, and the facts on record."}
]

HUM_MISSIONS = [
 {"id":"hum-mission-1","title":"Roll call","domain_id":"humanmetrics","difficulty":1,
  "brief":"Prove the sandbox answers before the self-knowledge work begins.",
  "objectives":["Print your username","Print the working directory","Print the hostname"],
  "checks":[
   {"command_pattern":"^whoami$","expect_contains":"candidate","hint":"Type exactly: whoami"},
   {"command_pattern":"^pwd$","expect_contains":"/home/candidate","hint":"Type exactly: pwd"},
   {"command_pattern":"^hostname$","expect_contains":"interstitium","hint":"Type exactly: hostname"}],
  "success_message":"Roll call complete \u2014 the sandbox is yours."},
 {"id":"hum-mission-2","title":"Survey the library","domain_id":"humanmetrics","difficulty":1,
  "brief":"Recon the practice workspace like a new library.",
  "objectives":["List the workspace","Confirm the logs directory exists","Mark the library mapped"],
  "checks":[
   {"command_pattern":"^ls$","expect_contains":"logs/","hint":"Type exactly: ls"},
   {"command_pattern":"^ls$","expect_contains":"README.md","hint":"Type exactly: ls"},
   {"command_pattern":"^echo 'library mapped'$","expect_contains":"library mapped","hint":"Type exactly: echo 'library mapped'"}],
  "success_message":"Library surveyed \u2014 every instrument has a shelf."},
 {"id":"hum-mission-3","title":"Know thyself","domain_id":"humanmetrics","difficulty":1,
  "brief":"The theme is self-knowledge; start with the machine's.",
  "objectives":["Print your user identity","Print the kernel name","Print full system info"],
  "checks":[
   {"command_pattern":"^id$","expect_contains":"uid=1000","hint":"Type exactly: id"},
   {"command_pattern":"^uname$","expect_contains":"Linux","hint":"Type exactly: uname"},
   {"command_pattern":"^uname -a$","expect_contains":"x86_64","hint":"Type exactly: uname -a"}],
  "success_message":"Environment read \u2014 now turn inward."},
 {"id":"hum-mission-4","title":"Clarity drill","domain_id":"humanmetrics","difficulty":2,
  "brief":"Drill the three honesty rules for reading results.",
  "objectives":["State the reporting rule","State the near-tie rule","State the coaching rule"],
  "checks":[
   {"command_pattern":"^echo 'report the clarity, not just the letter'$","expect_contains":"report the clarity, not just the letter","hint":"Type exactly: echo 'report the clarity, not just the letter'"},
   {"command_pattern":"^echo '51/49 is a shrug, not a verdict'$","expect_contains":"51/49 is a shrug, not a verdict","hint":"Type exactly: echo '51/49 is a shrug, not a verdict'"},
   {"command_pattern":"^echo 'coach the range, not the label'$","expect_contains":"coach the range, not the label","hint":"Type exactly: echo 'coach the range, not the label'"}],
  "success_message":"Clarity drilled \u2014 honesty before labels."},
 {"id":"hum-mission-5","title":"Scope drill","domain_id":"humanmetrics","difficulty":2,
  "brief":"Drill what the instrument is for \u2014 and what it is not.",
  "objectives":["State the selection rule","State the permission rule","State the fit rule"],
  "checks":[
   {"command_pattern":"^echo 'development yes, selection no'$","expect_contains":"development yes, selection no","hint":"Type exactly: echo 'development yes, selection no'"},
   {"command_pattern":"^echo 'preferences are not permissions'$","expect_contains":"preferences are not permissions","hint":"Type exactly: echo 'preferences are not permissions'"},
   {"command_pattern":"^echo 'lived fit beats predicted fit'$","expect_contains":"lived fit beats predicted fit","hint":"Type exactly: echo 'lived fit beats predicted fit'"}],
  "success_message":"Scope drilled \u2014 a lens, not a filter."},
 {"id":"hum-mission-6","title":"Team drill","domain_id":"humanmetrics","difficulty":2,
  "brief":"Drill the team-design rules.",
  "objectives":["State the authority rule","State the allocation rule","State the measurement rule"],
  "checks":[
   {"command_pattern":"^echo 'types inform, outcomes judge'$","expect_contains":"types inform, outcomes judge","hint":"Type exactly: echo 'types inform, outcomes judge'"},
   {"command_pattern":"^echo 'personality never allocates scarce goods'$","expect_contains":"personality never allocates scarce goods","hint":"Type exactly: echo 'personality never allocates scarce goods'"},
   {"command_pattern":"^echo 'diversity is a hypothesis, fairness is the measurement'$","expect_contains":"diversity is a hypothesis, fairness is the measurement","hint":"Type exactly: echo 'diversity is a hypothesis, fairness is the measurement'"}],
  "success_message":"Team drilled \u2014 inform, never allocate."},
 {"id":"hum-mission-7","title":"Closing","domain_id":"humanmetrics","difficulty":1,
  "brief":"Close with the ancient instruction: date, host, self-knowledge.",
  "objectives":["Print the current date","Confirm the hostname","State the instruction"],
  "checks":[
   {"command_pattern":"^date$","expect_contains":"GMT","hint":"Type exactly: date"},
   {"command_pattern":"^hostname$","expect_contains":"interstitium","hint":"Type exactly: hostname"},
   {"command_pattern":"^echo 'know thyself, then adapt'$","expect_contains":"know thyself, then adapt","hint":"Type exactly: echo 'know thyself, then adapt'"}],
  "success_message":"Work complete \u2014 know thyself, then adapt."}
]

# ------------------------------------------------------------- fullstack-desk
FSD_SIMS = [
 {"id":"fsd-sim-1","title":"The 3 AM page","kind":"troubleshoot",
  "domain_id":"fullstack-desk","difficulty":2,"points":100,
  "brief":"Paged at 3 AM: checkout 500s, cache refusing connections, retry storm backing up the queue. Contain it.",
  "steps":[
   {"symptom":"Paged at 3 AM: checkout API returning 500s. Cache connection refused; the app retries forever and the queue backs up.",
    "evidence":[["log","ERROR connection refused: cache:6379"],["metric","p99 latency 30s, queue depth 12k"]],
    "options":["Fail fast with a circuit breaker and serve degraded (stale cache / direct DB) \u2014 retries without bound are the outage",
               "Keep retrying; the cache will come back",
               "Restart the app servers",
               "Page the cache vendor"],
    "correct":0,
    "explain":"Unbounded retries turn a cache blip into a full outage via queue backup. Break the circuit, degrade gracefully, recover fast."},
   {"symptom":"Circuit broken, degraded mode on. The cache is back \u2014 when do you close the circuit?",
    "evidence":[["health","cache responding, error rate falling"]],
    "options":["Half-open with a probe: let a trickle through, and close only when probes succeed consistently",
               "Close immediately at the first success",
               "Wait an hour",
               "Never close; stay degraded"],
    "correct":0,
    "explain":"Half-open probing prevents flapping: a trickle validates recovery before full traffic returns. One success is not a trend."},
   {"symptom":"Recovered. The postmortem asks for the one systemic fix.",
    "evidence":[["root","no timeout on cache calls; retries unbounded"]],
    "options":["Timeouts, bounded retries with backoff, and circuit breakers as defaults on every dependency call",
               "More cache servers",
               "A bigger queue",
               "An apology email"],
    "correct":0,
    "explain":"The systemic fix is defensive defaults: every external call gets a timeout, a retry budget, and a breaker. The outage was a missing-defaults outage."}],
  "debrief":"Outages are dependency failures with amplification: bound the retries, break the circuit, degrade \u2014 then make the defaults systemic."},
 {"id":"fsd-sim-2","title":"The runaway job","kind":"troubleshoot",
  "domain_id":"fullstack-desk","difficulty":2,"points":100,
  "brief":"A nightly job is burning CPU at noon. Work the runbook in order: schedule, lock, kill \u2014 then fix the lock.",
  "steps":[
   {"symptom":"A background job meant to run nightly is consuming 100% CPU at noon. The runbook says: check the schedule, then the lock.",
    "evidence":[["runbook","1. verify schedule 2. check singleton lock 3. kill and alert"]],
    "options":["Follow the runbook: confirm it is off-schedule, check whether the singleton lock is held, then kill per procedure",
               "Kill it immediately",
               "Let it finish",
               "Ignore it until tonight"],
    "correct":0,
    "explain":"Runbooks exist so 3 AM you makes the same decisions as 3 PM you. Diagnose in order; the lock tells you whether it is a duplicate or a zombie."},
   {"symptom":"The lock is stale \u2014 the job died mid-run yesterday and the lock never released. Today's run spawned alongside the orphan.",
    "evidence":[["lock","lock file dated yesterday, PID dead"]],
    "options":["Kill both, clear the stale lock, and add lock expiry/heartbeats so it cannot happen again",
               "Clear the lock and walk away",
               "Kill one and hope",
               "Disable the job"],
    "correct":0,
    "explain":"Stale locks are a design bug: locks need expiry or heartbeats. Clear it now, fix the mechanism so it cannot recur."},
   {"symptom":"Stable. The interviewer asks what the runbook gains you.",
    "evidence":[["team","5 engineers, rotating on-call"]],
    "options":["Consistent response regardless of who is paged \u2014 runbooks transfer judgment, not just steps",
               "Nothing; seniors know this",
               "Slower response",
               "Paperwork"],
    "correct":0,
    "explain":"A runbook is institutional memory: the diagnosis order, the kill criteria, the alert threshold \u2014 decided once, executed the same every time."}],
  "debrief":"Background jobs fail in predictable ways: follow the runbook, fix the lock mechanism, and write down what you learned."},
 {"id":"fsd-sim-3","title":"Severity call","kind":"troubleshoot",
  "domain_id":"fullstack-desk","difficulty":2,"points":100,
  "brief":"Two incidents, one free engineer. Classify by customer impact, reclassify as facts change, and teach it by precedent.",
  "steps":[
   {"symptom":"Two incidents at once: checkout 500s for 10% of users, and the internal admin dashboard is slow. One engineer free. Classify.",
    "evidence":[["A","checkout 500s, 10% of users, revenue impact"],["B","admin dashboard slow, internal only"]],
    "options":["A is P1 (customer-facing revenue), B is P3 (internal degradation) \u2014 severity follows customer impact, and the engineer goes to A",
               "Both P1",
               "B first; it is easier",
               "Alternate"],
    "correct":0,
    "explain":"Severity is customer impact, not technical interest. Revenue-path failures outrank internal slowness every time."},
   {"symptom":"While fixing A, the admin dashboard goes fully down. Reclassify?",
    "evidence":[["B now","admin dashboard 100% down; support cannot refund users affected by A"]],
    "options":["Escalate B to P2: it now blocks the response to the P1 \u2014 severity is dynamic, reassess as facts change",
               "Keep B at P3",
               "Drop A",
               "Page everyone"],
    "correct":0,
    "explain":"Severity follows current impact: B now amplifies A's damage by blocking refunds. Reclassify on new facts, not on first impressions."},
   {"symptom":"Both resolved. What goes in the severity definitions doc?",
    "evidence":[["doc","needs examples"]],
    "options":["Customer-impact thresholds with examples from these incidents \u2014 definitions are taught by precedent",
               "Vague principles",
               "Technical metrics only",
               "Nothing; everyone knows"],
    "correct":0,
    "explain":"Severity definitions stick when they carry real examples. 'P1: checkout down (Oct 8)' teaches faster than any abstract rubric."}],
  "debrief":"Severity is customer impact, reassessed as facts change, and taught by precedent."},
 {"id":"fsd-sim-4","title":"Correlate the logs","kind":"troubleshoot",
  "domain_id":"fullstack-desk","difficulty":3,"points":100,
  "brief":"'The app is slow': frontend 504s, backend timeouts, a 28s query. Find the root by causality, fix it, prove it, monitor it.",
  "steps":[
   {"symptom":"Users report 'the app is slow'. Frontend shows 504s on /api/report; backend shows 30s timeouts; DB shows a 28s query. Where is the fault?",
    "evidence":[["frontend","504 on /api/report"],["backend","timeout after 30s"],["db","SELECT ... 28s, full table scan"]],
    "options":["The database query: the 28s full scan causes the backend timeout which causes the frontend 504 \u2014 correlate timestamps, fix the query",
               "The frontend",
               "The network",
               "All three independently"],
    "correct":0,
    "explain":"Correlate by timestamp and causality: the slowest layer with the earliest start is the root. The 504s are symptoms of the 28s scan."},
   {"symptom":"The query lacks an index on the filter column. Fix and verify.",
    "evidence":[["query","WHERE created_at > X \u2014 no index"]],
    "options":["Add the index in a migration, then replay the slow query and confirm sub-second \u2014 verify with EXPLAIN",
               "Add the index live without testing",
               "Cache the report",
               "Increase the timeout"],
    "correct":0,
    "explain":"Index, then prove it: EXPLAIN before and after, replay the exact query. 'Probably faster' is not a verification."},
   {"symptom":"Fixed. What monitoring prevents the sequel?",
    "evidence":[["gap","no slow-query alerting"]],
    "options":["Slow-query alerting with a threshold plus a dashboard on p99 per endpoint \u2014 the next 28s scan pages before users notice",
               "More logs",
               "Bigger DB",
               "Hope"],
    "correct":0,
    "explain":"Every incident buys a monitor: alert on the symptom (slow queries) and the user-facing signal (p99) so the next one is caught early."}],
  "debrief":"Log correlation is causality with timestamps: find the earliest slow layer, fix it, prove it, monitor it."},
 {"id":"fsd-sim-5","title":"The blameless postmortem","kind":"troubleshoot",
  "domain_id":"fullstack-desk","difficulty":2,"points":100,
  "brief":"Facilitate the postmortem for the 3 AM outage. Keep it blameless, keep the actions alive, and refuse the naming.",
  "steps":[
   {"symptom":"Facilitate the postmortem for the 3 AM outage. An engineer says 'I should have caught the missing timeout.' Redirect.",
    "evidence":[["room","the on-call engineer, their manager, you facilitating"]],
    "options":["Redirect to the system: 'What allowed a dependency call with no timeout to ship?' \u2014 blameless means fixing systems, not people",
               "Agree and move on",
               "Skip the postmortem",
               "Blame the vendor"],
    "correct":0,
    "explain":"Blameless is a method, not kindness: human error is the starting point of the investigation, never the conclusion."},
   {"symptom":"The group lists five action items. How do you keep them from dying?",
    "evidence":[["items","5 actions, no owners"]],
    "options":["One owner and one date per item, tracked like any other work \u2014 action items without owners are wishes",
               "Trust the team",
               "More items",
               "File them away"],
    "correct":0,
    "explain":"Postmortem value is entirely in the follow-through: named owners, dates, and the same tracking as feature work."},
   {"symptom":"A manager asks to name the engineer in the public report. Answer?",
    "evidence":[["request","name and shame for accountability"]],
    "options":["Refuse: naming chills future honesty and teaches engineers to hide \u2014 accountability is in the fixed system",
               "Comply",
               "Name them privately",
               "Skip the report"],
    "correct":0,
    "explain":"Public blame optimizes for the appearance of accountability while destroying the reporting culture that prevents the next outage."}],
  "debrief":"Blameless postmortems fix systems: ask what allowed it, assign every action, and never trade honesty for the appearance of accountability."}
]

FSD_CONSOLES = [
 {"id":"fsd-console-1","title":"Triage the outage ticket","console":"ticketing",
  "domain_id":"fullstack-desk","difficulty":2,
  "brief":"The checkout outage has a ticket: INC-9001, open and unassigned. Take it, start it, and log the diagnosis.",
  "tasks":[
   {"id":"fsd-c1-t1","instruction":"Assign ticket INC-9001 to on-call.",
    "validate":{"action":"assign-ticket","params":{"id":"INC-9001","assignee":"on-call"}},
    "hint":"Assign INC-9001 to on-call."},
   {"id":"fsd-c1-t2","instruction":"Move INC-9001 to in-progress.",
    "validate":{"action":"update-status","params":{"id":"INC-9001","status":"in-progress"}},
    "hint":"Update INC-9001 status to in-progress."},
   {"id":"fsd-c1-t3","instruction":"Add a note to INC-9001: cache refused connections; circuit breaker engaged.",
    "validate":{"action":"add-note","params":{"id":"INC-9001","text":"Cache refused connections; circuit breaker engaged."}},
    "hint":"Add the diagnosis note to INC-9001."}],
  "debrief":"Outage tickets move fast and stay factual: owned, in-progress, and the diagnosis on record."},
 {"id":"fsd-console-2","title":"Work the unusual-outbound alert","console":"siem-dashboard",
  "domain_id":"fullstack-desk","difficulty":2,
  "brief":"Unusual outbound volume from the backup server. Work ALT-103 in the simulated SIEM: acknowledge, assign, escalate.",
  "tasks":[
   {"id":"fsd-c2-t1","instruction":"Acknowledge alert ALT-103.",
    "validate":{"action":"acknowledge-alert","params":{"id":"ALT-103"}},
    "hint":"Acknowledge alert ALT-103."},
   {"id":"fsd-c2-t2","instruction":"Assign ALT-103 to analyst soc-tier1.",
    "validate":{"action":"assign-alert","params":{"id":"ALT-103","analyst":"soc-tier1"}},
    "hint":"Assign ALT-103 to soc-tier1."},
   {"id":"fsd-c2-t3","instruction":"Escalate ALT-103.",
    "validate":{"action":"escalate","params":{"id":"ALT-103"}},
    "hint":"Escalate ALT-103."}],
  "debrief":"SIEM triage is acknowledge-assign-escalate: the alert is never just stared at."},
 {"id":"fsd-console-3","title":"Debug the handler","console":"code-editor",
  "domain_id":"fullstack-desk","difficulty":1,
  "brief":"A request handler misbehaves. Walk it with breakpoints and inspection in the simulated editor.",
  "tasks":[
   {"id":"fsd-c3-t1","instruction":"Open app.py in the Explorer.",
    "validate":{"action":"open-file","params":{"name":"app.py"}},
    "hint":"Explorer tab \u2192 Open app.py."},
   {"id":"fsd-c3-t2","instruction":"Set a breakpoint at app.py line 4.",
    "validate":{"action":"toggle-breakpoint","params":{"file":"app.py","line":4}},
    "hint":"Click line 4 in the editor to toggle a breakpoint."},
   {"id":"fsd-c3-t3","instruction":"Run to the breakpoint.",
    "validate":{"action":"run-to-breakpoint","params":{}},
    "hint":"Press Run to breakpoint."},
   {"id":"fsd-c3-t4","instruction":"Inspect the variable s.",
    "validate":{"action":"inspect-variable","params":{"name":"s"}},
    "hint":"Use Inspect with variable name s."}],
  "debrief":"Handlers are debugged like everything else: open, break, run, inspect \u2014 read state before guessing."},
 {"id":"fsd-console-4","title":"Protect the logs","console":"linux-desktop",
  "domain_id":"fullstack-desk","difficulty":2,
  "brief":"Lock down the app log and open an incident directory for the postmortem notes.",
  "tasks":[
   {"id":"fsd-c4-t1","instruction":"Set /var/log/app.log to owner/group read, others none (mode 640).",
    "validate":{"action":"chmod","params":{"path":"/var/log/app.log","mode":"640"}},
    "hint":"chmod 640 on /var/log/app.log."},
   {"id":"fsd-c4-t2","instruction":"Create the incident directory /home/user/incidents.",
    "validate":{"action":"create-dir","params":{"path":"/home/user/incidents"}},
    "hint":"Create directory /home/user/incidents."},
   {"id":"fsd-c4-t3","instruction":"Create the postmortem file /home/user/incidents/postmortem-1008.txt.",
    "validate":{"action":"create-file","params":{"path":"/home/user/incidents/postmortem-1008.txt"}},
    "hint":"Create file /home/user/incidents/postmortem-1008.txt."}],
  "debrief":"Incident hygiene is file hygiene: logs permissioned, postmortems filed where the team finds them."}
]

FSD_MISSIONS = [
 {"id":"fsd-mission-1","title":"Roll call","domain_id":"fullstack-desk","difficulty":1,
  "brief":"Prove the sandbox answers before the on-call shift starts.",
  "objectives":["Print your username","Print the working directory","Print the hostname"],
  "checks":[
   {"command_pattern":"^whoami$","expect_contains":"candidate","hint":"Type exactly: whoami"},
   {"command_pattern":"^pwd$","expect_contains":"/home/candidate","hint":"Type exactly: pwd"},
   {"command_pattern":"^hostname$","expect_contains":"interstitium","hint":"Type exactly: hostname"}],
  "success_message":"Roll call complete \u2014 the sandbox is yours."},
 {"id":"fsd-mission-2","title":"Survey the stack","domain_id":"fullstack-desk","difficulty":1,
  "brief":"Recon the practice workspace like a new production stack.",
  "objectives":["List the workspace","Confirm the logs directory exists","Mark the stack mapped"],
  "checks":[
   {"command_pattern":"^ls$","expect_contains":"logs/","hint":"Type exactly: ls"},
   {"command_pattern":"^ls$","expect_contains":"README.md","hint":"Type exactly: ls"},
   {"command_pattern":"^echo 'stack mapped'$","expect_contains":"stack mapped","hint":"Type exactly: echo 'stack mapped'"}],
  "success_message":"Stack surveyed \u2014 you know every layer."},
 {"id":"fsd-mission-3","title":"Know your shift","domain_id":"fullstack-desk","difficulty":1,
  "brief":"Read the environment the way you would read the on-call handoff.",
  "objectives":["Print your user identity","Print the kernel name","Print full system info"],
  "checks":[
   {"command_pattern":"^id$","expect_contains":"uid=1000","hint":"Type exactly: id"},
   {"command_pattern":"^uname$","expect_contains":"Linux","hint":"Type exactly: uname"},
   {"command_pattern":"^uname -a$","expect_contains":"x86_64","hint":"Type exactly: uname -a"}],
  "success_message":"Environment read \u2014 shift started."},
 {"id":"fsd-mission-4","title":"Triage drill","domain_id":"fullstack-desk","difficulty":2,
  "brief":"Drill the severity rules every on-call engineer recites.",
  "objectives":["State the severity rule","State the reassessment rule","State the teaching rule"],
  "checks":[
   {"command_pattern":"^echo 'severity follows customer impact'$","expect_contains":"severity follows customer impact","hint":"Type exactly: echo 'severity follows customer impact'"},
   {"command_pattern":"^echo 'reassess as facts change'$","expect_contains":"reassess as facts change","hint":"Type exactly: echo 'reassess as facts change'"},
   {"command_pattern":"^echo 'precedent teaches faster than rubrics'$","expect_contains":"precedent teaches faster than rubrics","hint":"Type exactly: echo 'precedent teaches faster than rubrics'"}],
  "success_message":"Triage drilled \u2014 classify with confidence."},
 {"id":"fsd-mission-5","title":"Runbook drill","domain_id":"fullstack-desk","difficulty":2,
  "brief":"Drill the runbook discipline.",
  "objectives":["State the diagnosis rule","State the lock rule","State the runbook's value"],
  "checks":[
   {"command_pattern":"^echo 'diagnose in order'$","expect_contains":"diagnose in order","hint":"Type exactly: echo 'diagnose in order'"},
   {"command_pattern":"^echo 'locks need expiry or heartbeats'$","expect_contains":"locks need expiry or heartbeats","hint":"Type exactly: echo 'locks need expiry or heartbeats'"},
   {"command_pattern":"^echo 'runbooks transfer judgment'$","expect_contains":"runbooks transfer judgment","hint":"Type exactly: echo 'runbooks transfer judgment'"}],
  "success_message":"Runbook drilled \u2014 3 AM you thanks you."},
 {"id":"fsd-mission-6","title":"Postmortem drill","domain_id":"fullstack-desk","difficulty":2,
  "brief":"Drill the blameless postmortem rules.",
  "objectives":["State the blame rule","State the action rule","State the honesty rule"],
  "checks":[
   {"command_pattern":"^echo 'fix systems, not people'$","expect_contains":"fix systems, not people","hint":"Type exactly: echo 'fix systems, not people'"},
   {"command_pattern":"^echo 'every action gets an owner and a date'$","expect_contains":"every action gets an owner and a date","hint":"Type exactly: echo 'every action gets an owner and a date'"},
   {"command_pattern":"^echo 'honesty prevents the next outage'$","expect_contains":"honesty prevents the next outage","hint":"Type exactly: echo 'honesty prevents the next outage'"}],
  "success_message":"Postmortem drilled \u2014 blameless and effective."},
 {"id":"fsd-mission-7","title":"Closing","domain_id":"fullstack-desk","difficulty":1,
  "brief":"Close with the on-call mantra: date, host, resilience.",
  "objectives":["Print the current date","Confirm the hostname","State the resilience rule"],
  "checks":[
   {"command_pattern":"^date$","expect_contains":"GMT","hint":"Type exactly: date"},
   {"command_pattern":"^hostname$","expect_contains":"interstitium","hint":"Type exactly: hostname"},
   {"command_pattern":"^echo 'bound the retries, break the circuit, degrade'$","expect_contains":"bound the retries, break the circuit, degrade","hint":"Type exactly: echo 'bound the retries, break the circuit, degrade'"}],
  "success_message":"Shift complete \u2014 bound, break, degrade."}
]

CONTENT = {
 "humanmetrics": {"simulations": HUM_SIMS, "consoleSims": HUM_CONSOLES, "terminalMissions": HUM_MISSIONS},
 "fullstack-desk": {"simulations": FSD_SIMS, "consoleSims": FSD_CONSOLES, "terminalMissions": FSD_MISSIONS},
}
PREFIX = {"humanmetrics": "hum-", "fullstack-desk": "fsd-"}

def validate(slug, data, added):
    errs = []
    ids = []
    for key in ("simulations", "consoleSims", "terminalMissions", "labs"):
        for item in data.get(key) or []:
            ids.append(item["id"])
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids: " + str([i for i in ids if ids.count(i) > 1]))
    for s in added["simulations"]:
        for req in ("id", "title", "kind", "domain_id", "difficulty", "brief", "steps", "debrief", "points"):
            if req not in s: errs.append(s["id"] + " missing " + req)
        if s["kind"] != "troubleshoot": errs.append(s["id"] + " bad kind")
        for st in s["steps"]:
            for req in ("symptom", "evidence", "options", "correct", "explain"):
                if req not in st: errs.append(s["id"] + " step missing " + req)
            if not (0 <= st["correct"] < len(st["options"])): errs.append(s["id"] + " bad correct index")
    for c in added["consoleSims"]:
        for req in ("id", "title", "console", "domain_id", "difficulty", "brief", "tasks", "debrief"):
            if req not in c: errs.append(c["id"] + " missing " + req)
        for t in c["tasks"]:
            if not t.get("hint"): errs.append(c["id"] + "/" + t.get("id", "?") + " missing hint")
            v = t.get("validate") or {}
            if "action" not in v or "params" not in v: errs.append(c["id"] + "/" + t.get("id", "?") + " bad validate")
    for m in added["terminalMissions"]:
        for req in ("id", "title", "domain_id", "difficulty", "brief", "objectives", "checks", "success_message"):
            if req not in m: errs.append(m["id"] + " missing " + req)
        if not m["id"].startswith(PREFIX[slug]): errs.append(m["id"] + " not slug-prefixed")
        for ch in m["checks"]:
            if not ch.get("hint"): errs.append(m["id"] + " check missing hint")
            try: re.compile(ch["command_pattern"])
            except Exception: errs.append(m["id"] + " bad regex")
            if "expect_contains" not in ch: errs.append(m["id"] + " missing expect_contains")
    return errs

def main():
    for slug, added in CONTENT.items():
        p = os.path.join(BASE, slug, "content.json")
        data = json.loads(open(p, encoding="utf-8").read())
        before = {k: v for k, v in data.items() if k not in ("simulations", "consoleSims", "terminalMissions")}
        counts_before = {k: len(data.get(k) or []) for k in ("simulations", "consoleSims", "terminalMissions")}
        assert counts_before == {"simulations": 0, "consoleSims": 0, "terminalMissions": 0}, (slug, counts_before)
        for key, items in added.items():
            if key not in data or not isinstance(data[key], list):
                data[key] = []
            data[key].extend(items)
        errs = validate(slug, data, added)
        after = {k: v for k, v in data.items() if k not in ("simulations", "consoleSims", "terminalMissions")}
        assert before == after, slug + ": untouched keys changed!"
        assert not errs, (slug, errs)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, p)
        d2 = json.load(open(p, encoding="utf-8"))
        print(slug, "sims=%d csims=%d missions=%d OK" % (
            len(d2["simulations"]), len(d2["consoleSims"]), len(d2["terminalMissions"])))

if __name__ == "__main__":
    main()
