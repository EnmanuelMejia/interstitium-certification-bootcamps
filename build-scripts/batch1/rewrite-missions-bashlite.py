#!/usr/bin/env python3
"""Batch 1 fix: rewrite all acad terminalMissions to bash-lite-safe commands.

Engine reality (verified in _engine/terminal.js): acad-* slugs route to
bashLiteProfile, which implements ONLY: echo, whoami, id, date, ls (static),
uname, pwd, hostname (+ help/clear/history/exit). The earlier missions used
cat/grep/sha256sum/head/tail/ps/wc/dig/ping, which return 'command not found'
there and could never validate. New missions use only commands that exist in
BOTH bash-lite and the full bash profile, with expect_contains values verified
against exact engine outputs. Precedent: Batch 4 did the same (56/56 checks
fidelity-tested) and was accepted.
"""
import json, os, re

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')

def M(mid, title, domain, difficulty, brief, objectives, checks, success):
    return {"id": mid, "title": title, "domain_id": domain, "difficulty": difficulty,
            "brief": brief, "objectives": objectives, "checks": checks,
            "success_message": success}

def C(pattern, contains, hint):
    return {"command_pattern": pattern, "expect_contains": contains, "hint": hint}

MISSIONS = {
# ---------------- acad-cyber ----------------
'acad-cyber': [
    M('acad-cyber-mission-1', 'Identify yourself to the SOC', 'acad-cyber', 1,
      'Every incident starts with identity. Print your username — the SOC needs to know who is on the keyboard.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is operating this station?')],
      'Identity confirmed: candidate. Attribution starts with knowing who acted.'),
    M('acad-cyber-mission-2', 'Confirm your station', 'acad-cyber', 1,
      'Verify which machine you are on. Print the hostname — incident reports must name the host.',
      ['Print the hostname'],
      [C('^hostname$', 'interstitium', 'Run: hostname — confirm your station.'),
       C('^echo\\s+.*station.*$', 'station', 'Run: echo with a confirmation naming your station (e.g. echo "on station interstitium").')],
      'Station confirmed. Reports name the host, always.'),
    M('acad-cyber-mission-3', 'Inventory the workstation', 'acad-cyber', 1,
      'Before you touch anything, know what is here. List the home directory.',
      ['List the home directory'],
      [C('^ls$', 'notes.txt', 'Run: ls — inventory the workstation. What study material is here?')],
      'Workstation inventoried. Situational awareness before action — always.'),
    M('acad-cyber-mission-4', 'Declare the incident', 'acad-cyber', 2,
      'A phishing report just landed. Declare it on the channel with echo — declarations must be explicit and visible, never assumed.',
      ['Declare the security incident'],
      [C('^echo\\s+.*[Ii][Nn][Cc][Ii][Dd][Ee][Nn][Tt].*$', 'INCIDENT',
         'Run: echo with an incident declaration (e.g. echo "SECURITY INCIDENT DECLARED").')],
      'Incident declared. If nobody says it, nobody owns it.'),
    M('acad-cyber-mission-5', 'Verify your identity token', 'acad-cyber', 2,
      'Access reviews check the full identity string, not just the name. Print your identity record.',
      ['Print your full identity record'],
      [C('^id$', 'uid=1000', 'Run: id — read the full identity string.')],
      'Identity verified: uid=1000. Reviews check the whole record, not the username.'),
    M('acad-cyber-mission-6', 'Check the platform build', 'acad-cyber', 2,
      'Know your platform: print the full system information. Vulnerability management starts with knowing what you run.',
      ['Print full system information'],
      [C('^uname\\s+-a$', '6.8.0-ilb', 'Run: uname -a — read the platform build string.')],
      'Platform identified. You cannot protect what you cannot name.'),
    M('acad-cyber-mission-7', 'Confirm your operating position', 'acad-cyber', 3,
      'Print your working directory, then attest with echo that your position is confirmed — two independent confirmations, like any good control.',
      ['Print working directory', 'Attest your position'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — where are you operating from?'),
       C('^echo\\s+.*confirmed.*$', 'confirmed',
         'Run: echo with a confirmation (e.g. echo "position confirmed").')],
      'Position confirmed twice. Defense in depth applies to verification too.'),
],
# ---------------- acad-cloud ----------------
'acad-cloud': [
    M('acad-cloud-mission-1', 'Name your region', 'acad-cloud', 1,
      'Every cloud resource lives in a region. Print this machine\'s hostname — its region codename for this drill.',
      ['Print the region codename'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name your region.')],
      'Region named. Resources without regions are just hopes.'),
    M('acad-cloud-mission-2', 'Who is deploying', 'acad-cloud', 1,
      'Deployments are attributed to identities. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is deploying?')],
      'Deployer identified. Every change has an owner.'),
    M('acad-cloud-mission-3', 'List the migration staging area', 'acad-cloud', 1,
      'Before migrating anything, map the territory. List the home directory.',
      ['List the staging area'],
      [C('^ls$', 'logs/', 'Run: ls — map the staging area.')],
      'Territory mapped. Migrations fail when people move things they never inventoried.'),
    M('acad-cloud-mission-4', 'Confirm the working directory', 'acad-cloud', 2,
      'Cloud consoles are context-sensitive — the wrong directory means the wrong deployment. Print yours.',
      ['Print working directory'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — confirm your context.')],
      'Context confirmed. Deploy from the wrong directory and you deploy the wrong thing.'),
    M('acad-cloud-mission-5', 'State the migration wave', 'acad-cloud', 2,
      'Migrations move in waves. Announce the current wave with echo — status must be stated, not assumed.',
      ['Announce the migration wave'],
      [C('^echo\\s+.*wave.*$', 'wave',
         'Run: echo with the wave status (e.g. echo "wave 1 complete").')],
      'Wave stated. Silent migrations are how cutovers surprise people.'),
    M('acad-cloud-mission-6', 'Verify the platform', 'acad-cloud', 2,
      'Instance types matter. Print the full system information to confirm the platform architecture.',
      ['Print platform architecture'],
      [C('^uname\\s+-a$', 'x86_64', 'Run: uname -a — confirm the architecture.')],
      'Platform verified. Right-size from facts, not guesses.'),
    M('acad-cloud-mission-7', 'Attest the deploy identity', 'acad-cloud', 3,
      'Print your full identity record, then attest it with echo — the deploy bot gets the same identity hygiene as humans.',
      ['Print identity record', 'Attest the identity'],
      [C('^id$', 'uid=1000', 'Run: id — read the full identity string.'),
       C('^echo\\s+.*attested.*$', 'attested',
         'Run: echo with an attestation (e.g. echo "identity attested").')],
      'Identity attested. Every deploy identity — human or machine — gets verified.'),
],
# ---------------- acad-command ----------------
'acad-command': [
    M('acad-command-mission-1', 'Who has the conn', 'acad-command', 1,
      'An incident commander first establishes who is present. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is on the bridge?')],
      'Presence established. You cannot assign roles to people you have not accounted for.'),
    M('acad-command-mission-2', 'Name the command post', 'acad-command', 1,
      'Name the machine you are commanding from. Print the hostname.',
      ['Print the command post name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name your command post.')],
      'Command post named. Incidents get locations, not vibes.'),
    M('acad-command-mission-3', 'Survey the bridge', 'acad-command', 1,
      'Survey your instruments before the crisis. List the home directory.',
      ['Survey the workspace'],
      [C('^ls$', 'app.py', 'Run: ls — survey the bridge.')],
      'Bridge surveyed. Commanders study the terrain before the battle.'),
    M('acad-command-mission-4', 'Declare incident command', 'acad-command', 2,
      'The IC for this drill is M. Reyes. Announce it with echo — if nobody says "I am the IC," nobody is.',
      ['Announce the incident commander'],
      [C('^echo\\s+.*Reyes.*$', 'Reyes',
         'Run: echo with the declaration (e.g. echo "IC: M. Reyes has command").')],
      'Command declared. Explicit beats assumed, every time.'),
    M('acad-command-mission-5', 'Confirm your station', 'acad-command', 2,
      'Print your working directory — a commander knows exactly where they stand.',
      ['Print working directory'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — confirm your station.')],
      'Station confirmed. Clarity of position is clarity of command.'),
    M('acad-command-mission-6', 'Verify credentials', 'acad-command', 2,
      'Authority must be verifiable. Print your full identity record.',
      ['Print identity record'],
      [C('^id$', 'groups=1000', 'Run: id — verify your credentials.')],
      'Credentials verified. Authority you cannot verify is authority you should not claim.'),
    M('acad-command-mission-7', 'Sound the all-clear', 'acad-command', 3,
      'The incident is resolved. Announce the all-clear with echo, then print the platform string for the after-action record.',
      ['Announce all-clear', 'Record the platform'],
      [C('^echo\\s+.*all-clear.*$', 'all-clear',
         'Run: echo with the all-clear (e.g. echo "all-clear, incident resolved").'),
       C('^uname\\s+-a$', 'Linux', 'Run: uname -a — record the platform.')],
      'All-clear sounded and recorded. Every incident ends with a clear statement, not a fade-out.'),
],
# ---------------- acad-data ----------------
'acad-data': [
    M('acad-data-mission-1', 'Who is the analyst', 'acad-data', 1,
      'Analyses are attributed. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is analyzing?')],
      'Analyst identified. Every number has an author.'),
    M('acad-data-mission-2', 'Name the warehouse host', 'acad-data', 1,
      'Data lives somewhere. Print the hostname of this machine.',
      ['Print the host name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name the host.')],
      'Host named. Lineage starts with location.'),
    M('acad-data-mission-3', 'List the datasets', 'acad-data', 1,
      'Profile before you analyze: list what data is available here.',
      ['List available data'],
      [C('^ls$', 'logs/', 'Run: ls — what datasets are here?')],
      'Datasets listed. Never analyze data you have not inventoried.'),
    M('acad-data-mission-4', 'State the sample size', 'acad-data', 2,
      'The dataset holds 6 records. State the sample size with echo — conclusions scale with n, so n gets stated.',
      ['State the sample size'],
      [C('^echo\\s+.*6.*$', '6',
         'Run: echo with the sample size (e.g. echo "n=6 records").')],
      'Sample size stated. A number without its n is a rumor.'),
    M('acad-data-mission-5', 'Confirm the working directory', 'acad-data', 2,
      'Reproducibility starts with context. Print your working directory.',
      ['Print working directory'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — record your context.')],
      'Context recorded. Reproducible work states where it ran.'),
    M('acad-data-mission-6', 'Check the platform', 'acad-data', 2,
      'Print the full system information — the platform is part of the methodology section.',
      ['Print platform information'],
      [C('^uname\\s+-a$', '6.8.0-ilb', 'Run: uname -a — record the platform.')],
      'Platform recorded. Methods sections include the machine.'),
    M('acad-data-mission-7', 'Publish the finding', 'acad-data', 3,
      'State your headline finding with echo (the error rate is 33%), then print your identity record to sign the analysis.',
      ['State the finding', 'Sign the analysis'],
      [C('^echo\\s+.*33.*$', '33',
         'Run: echo with the finding (e.g. echo "error rate 33 percent").'),
       C('^id$', 'uid=1000', 'Run: id — sign your work.')],
      'Finding published and signed. Honest numbers, named author.'),
],
# ---------------- acad-forge ----------------
'acad-forge': [
    M('acad-forge-mission-1', 'Who is shipping', 'acad-forge', 1,
      'Shipped work has an author. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is shipping?')],
      'Author identified. Ship under your name, proudly.'),
    M('acad-forge-mission-2', 'Name the build machine', 'acad-forge', 1,
      'Builds are reproducible from a known machine. Print the hostname.',
      ['Print the build machine name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name the build machine.')],
      'Build machine named. "Works on my machine" starts with naming the machine.'),
    M('acad-forge-mission-3', 'List the project', 'acad-forge', 1,
      'Before you build, know what you have. List the project directory.',
      ['List the project'],
      [C('^ls$', 'app.py', 'Run: ls — list the project.')],
      'Project listed. You cannot build on what you have not looked at.'),
    M('acad-forge-mission-4', 'Confirm the workspace', 'acad-forge', 2,
      'Print your working directory — builds run from a known place.',
      ['Print working directory'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — confirm the workspace.')],
      'Workspace confirmed. Known place, known build.'),
    M('acad-forge-mission-5', 'Tag the release', 'acad-forge', 2,
      'Releases get names. Tag this one with echo: v2.14.0.',
      ['Tag the release'],
      [C('^echo\\s+.*v2\\.14\\.0.*$', 'v2.14.0',
         'Run: echo with the release tag (e.g. echo "release v2.14.0").')],
      'Release tagged. Named releases are retrievable releases.'),
    M('acad-forge-mission-6', 'Verify the builder identity', 'acad-forge', 2,
      'Signed releases come from verified builders. Print your full identity record.',
      ['Print builder identity'],
      [C('^id$', 'uid=1000', 'Run: id — verify the builder.')],
      'Builder verified. Ship under a verified name.'),
    M('acad-forge-mission-7', 'Announce the release', 'acad-forge', 3,
      'Announce the release with echo, then print the platform string for the release notes.',
      ['Announce the release', 'Record the platform'],
      [C('^echo\\s+.*live.*$', 'live',
         'Run: echo with the announcement (e.g. echo "v2.14.0 is live").'),
       C('^uname\\s+-a$', 'x86_64', 'Run: uname -a — record the build platform.')],
      'Release announced and documented. Shipping is a verb with a record.'),
],
# ---------------- acad-hermetica ----------------
'acad-hermetica': [
    M('acad-hermetica-mission-1', 'Who is observing', 'acad-hermetica', 1,
      'The observer is part of the system. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — name the observer.')],
      'Observer named. You are in the system you are studying.'),
    M('acad-hermetica-mission-2', 'Name the system', 'acad-hermetica', 1,
      'Name the thing you are thinking about. Print the hostname.',
      ['Print the system name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name the system.')],
      'System named. Unnamed systems cannot be discussed.'),
    M('acad-hermetica-mission-3', 'Map the components', 'acad-hermetica', 1,
      'Map the territory as it is. List the home directory.',
      ['Map the components'],
      [C('^ls$', 'README.md', 'Run: ls — map the components.')],
      'Components mapped. Models built on unmapped territory are fiction.'),
    M('acad-hermetica-mission-4', 'Name the pattern', 'acad-hermetica', 2,
      'Unnamed patterns cannot be discussed. State the pattern you have been studying with echo — use the word "reinforcing".',
      ['Name the pattern'],
      [C('^echo\\s+.*reinforcing.*$', 'reinforcing',
         'Run: echo naming the pattern (e.g. echo "a reinforcing feedback loop").')],
      'Pattern named. What gets named gets noticed.'),
    M('acad-hermetica-mission-5', 'Locate yourself in the system', 'acad-hermetica', 2,
      'Print your working directory — know where you stand inside the system.',
      ['Print your position'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — locate yourself.')],
      'Position located. The map includes the mapmaker.'),
    M('acad-hermetica-mission-6', 'Check the substrate', 'acad-hermetica', 2,
      'Every system runs on a substrate. Print the full system information.',
      ['Print the substrate'],
      [C('^uname\\s+-a$', 'Linux', 'Run: uname -a — check the substrate.')],
      'Substrate checked. Abstractions rest on something — know what.'),
    M('acad-hermetica-mission-7', 'State the whole', 'acad-hermetica', 3,
      'State the core principle with echo ("the map is not the territory"), then print your identity record — the observer signs the map.',
      ['State the principle', 'Sign the map'],
      [C('^echo\\s+.*territory.*$', 'territory',
         'Run: echo with the principle (e.g. echo "the map is not the territory").'),
       C('^id$', 'candidate', 'Run: id — sign the map.')],
      'Principle stated, map signed. Hold models lightly; verify the territory.'),
],
# ---------------- acad-math ----------------
'acad-math': [
    M('acad-math-mission-1', 'Who is calculating', 'acad-math', 1,
      'Calculations have authors. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is calculating?')],
      'Calculator identified. Numbers have authors.'),
    M('acad-math-mission-2', 'List the data files', 'acad-math', 1,
      'Quantitative work starts with the data at hand. List the home directory.',
      ['List available data'],
      [C('^ls$', 'notes.txt', 'Run: ls — list the data files.')],
      'Data listed. Measure what is here before estimating what is not.'),
    M('acad-math-mission-3', 'State the estimate', 'acad-math', 2,
      'Fermi estimate: 60 VMs at ~$50/month = $3,000/month compute. State the number with echo — estimates get stated, not mumbled.',
      ['State the Fermi estimate'],
      [C('^echo\\s+.*3000.*$', '3000',
         'Run: echo with the estimate (e.g. echo "estimate 3000 per month").')],
      'Estimate stated. A stated number can be checked; a mumbled one cannot.'),
    M('acad-math-mission-4', 'State the base rate', 'acad-math', 2,
      'Two errors in six log lines: the base rate is ~33%. State it with echo — base rates get written down.',
      ['State the base rate'],
      [C('^echo\\s+.*33.*$', '33',
         'Run: echo with the base rate (e.g. echo "base rate 33 percent").')],
      'Base rate stated. The first thing people forget and the last thing that matters.'),
    M('acad-math-mission-5', 'Name the host', 'acad-math', 2,
      'Even math runs somewhere. Print the hostname.',
      ['Print the host name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name the host.')],
      'Host named. Context is part of the calculation.'),
    M('acad-math-mission-6', 'Verify the platform', 'acad-math', 2,
      'Print the full system information — the instrument gets calibrated.',
      ['Print platform information'],
      [C('^uname\\s+-a$', '6.8.0-ilb', 'Run: uname -a — calibrate the instrument.')],
      'Instrument calibrated. Know what you compute on.'),
    M('acad-math-mission-7', 'Sign the proof', 'acad-math', 3,
      'Conclude with QED via echo, then print your identity record — the prover signs the proof.',
      ['State QED', 'Sign the proof'],
      [C('^echo\\s+.*QED.*$', 'QED',
         'Run: echo QED — conclude the proof.'),
       C('^id$', 'uid=1000', 'Run: id — sign the proof.')],
      'QED, signed. A proof without a prover is just a rumor with notation.'),
],
# ---------------- acad-systems ----------------
'acad-systems': [
    M('acad-systems-mission-1', 'Who is operating', 'acad-systems', 1,
      'Systems have operators. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is operating?')],
      'Operator identified. Every command has an author.'),
    M('acad-systems-mission-2', 'Name this host', 'acad-systems', 1,
      'Name the machine you are responsible for. Print the hostname.',
      ['Print the host name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name this host.')],
      'Host named. You operate what you can name.'),
    M('acad-systems-mission-3', 'Survey the filesystem', 'acad-systems', 1,
      'Survey the ground you stand on. List the home directory.',
      ['Survey the filesystem'],
      [C('^ls$', 'logs/', 'Run: ls — survey the filesystem.')],
      'Filesystem surveyed. Operators work from maps, not memory.'),
    M('acad-systems-mission-4', 'Print your position', 'acad-systems', 2,
      'Print your working directory — know exactly where you are before you act.',
      ['Print working directory'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — print your position.')],
      'Position known. The most dangerous command is the one run in the wrong directory.'),
    M('acad-systems-mission-5', 'Show your identity', 'acad-systems', 2,
      'Print your full identity record — permissions flow from identity.',
      ['Print identity record'],
      [C('^id$', 'uid=1000(candidate)', 'Run: id — show your identity.')],
      'Identity shown. In systems, who you are determines what you may do.'),
    M('acad-systems-mission-6', 'Identify the kernel', 'acad-systems', 2,
      'Print the full system information — know the kernel you are talking to.',
      ['Print kernel information'],
      [C('^uname\\s+-a$', '6.8.0-ilb', 'Run: uname -a — identify the kernel.')],
      'Kernel identified. Beneath every abstraction, a specific kernel.'),
    M('acad-systems-mission-7', 'Report system status', 'acad-systems', 3,
      'Report status with echo ("all systems nominal"), then confirm the host with hostname — status reports name the reporter and the machine.',
      ['Report status', 'Confirm the host'],
      [C('^echo\\s+.*nominal.*$', 'nominal',
         'Run: echo with the status (e.g. echo "all systems nominal").'),
       C('^hostname$', 'interstitium', 'Run: hostname — confirm the reporting host.')],
      'Status reported. Good news travels with the host name attached.'),
],
# ---------------- acad-theory ----------------
'acad-theory': [
    M('acad-theory-mission-1', 'Who is reasoning', 'acad-theory', 1,
      'Arguments have authors. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is reasoning?')],
      'Reasoner identified. Claims need claimants.'),
    M('acad-theory-mission-2', 'List the axioms', 'acad-theory', 1,
      'Every proof starts from givens. List what is available here.',
      ['List the givens'],
      [C('^ls$', 'app.py', 'Run: ls — list the givens.')],
      'Givens listed. State your axioms before your theorems.'),
    M('acad-theory-mission-3', 'State the complexity class', 'acad-theory', 2,
      'A loop with a constant bound is constant time. State the class with echo: O(1).',
      ['State the complexity class'],
      [C('^echo\\s+O\\(1\\)$', 'O(1)',
         'Run: echo O(1) — name the class.')],
      'O(1) stated. Name the class; do not just feel it.'),
    M('acad-theory-mission-4', 'Name the machine', 'acad-theory', 2,
      'Computation happens on machines. Print the hostname.',
      ['Print the machine name'],
      [C('^hostname$', 'interstitium', 'Run: hostname — name the machine.')],
      'Machine named. Abstract machines still run somewhere.'),
    M('acad-theory-mission-5', 'Locate the observer', 'acad-theory', 2,
      'Print your working directory — the observer has a position.',
      ['Print your position'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — locate the observer.')],
      'Observer located. Even pure reason runs from somewhere.'),
    M('acad-theory-mission-6', 'Sign the proof', 'acad-theory', 3,
      'Conclude with QED via echo, then print your identity record — the prover signs the proof.',
      ['State QED', 'Sign the proof'],
      [C('^echo\\s+QED$', 'QED', 'Run: echo QED — conclude.'),
       C('^id$', 'uid=1000', 'Run: id — sign the proof.')],
      'QED, signed. Verify, do not trust.'),
    M('acad-theory-mission-7', 'Identify the platform', 'acad-theory', 3,
      'Print the full platform string, then your username — the proof records its machine and its author.',
      ['Print platform', 'Print author'],
      [C('^uname\\s+-a$', 'x86_64', 'Run: uname -a — record the platform.'),
       C('^whoami$', 'candidate', 'Run: whoami — record the author.')],
      'Platform and author recorded. Reproducibility is a virtue, even in theory.'),
],
# ---------------- acad-career ----------------
'acad-career': [
    M('acad-career-mission-1', 'Who is applying', 'acad-career', 1,
      'Careers have owners. Print your username.',
      ['Print your username'],
      [C('^whoami$', 'candidate', 'Run: whoami — who is applying?')],
      'Applicant identified. Own the search.'),
    M('acad-career-mission-2', 'Inventory your assets', 'acad-career', 1,
      'A career is a portfolio of assets. List what you have to work with.',
      ['Inventory your assets'],
      [C('^ls$', 'README.md', 'Run: ls — inventory your assets.')],
      'Assets inventoried. You cannot position what you have not catalogued.'),
    M('acad-career-mission-3', 'Write your headline', 'acad-career', 1,
      'Every profile needs a one-line headline. Write yours with echo — it must contain "DevSecOps".',
      ['Write your headline'],
      [C('^echo\\s+.*DevSecOps.*$', 'DevSecOps',
         'Run: echo with your headline (e.g. echo "DevSecOps engineer").')],
      'Headline written. If you cannot say it in one line, you do not own it yet.'),
    M('acad-career-mission-4', 'Confirm your home base', 'acad-career', 2,
      'Outreach starts from a known base. Print the hostname.',
      ['Print your home base'],
      [C('^hostname$', 'interstitium', 'Run: hostname — confirm your home base.')],
      'Home base confirmed. Network from somewhere, not nowhere.'),
    M('acad-career-mission-5', 'Confirm your base of operations', 'acad-career', 2,
      'Print your working directory — the job hunt runs from a known place.',
      ['Print working directory'],
      [C('^pwd$', '/home/candidate', 'Run: pwd — confirm your base.')],
      'Base confirmed. Run the search like an operation, not a hope.'),
    M('acad-career-mission-6', 'Verify your professional identity', 'acad-career', 2,
      'Print your full identity record — know exactly how you present.',
      ['Print identity record'],
      [C('^id$', 'uid=1000', 'Run: id — verify your identity.')],
      'Identity verified. Present yourself precisely.'),
    M('acad-career-mission-7', 'Announce your availability', 'acad-career', 3,
      'Announce you are open to work with echo, then print the platform string for the record — visibility is a strategy.',
      ['Announce availability', 'Record the platform'],
      [C('^echo\\s+.*open to work.*$', 'open to work',
         'Run: echo with your announcement (e.g. echo "open to work").'),
       C('^uname\\s+-a$', 'Linux', 'Run: uname -a — record the platform.')],
      'Availability announced. The candidate who is visible is the candidate who gets found.'),
],
}

# Engine-verified outputs for BOTH profiles (bash-lite static == full-bash ~ listing)
ENGINE = {
    'whoami': 'candidate',
    'hostname': 'interstitium',
    'pwd': '/home/candidate',
    'id': 'uid=1000(candidate) gid=1000(candidate) groups=1000(candidate)',
    'ls': 'README.md   app.py   logs/   notes.txt',
    'uname -a': 'Linux interstitium 6.8.0-ilb x86_64 GNU/Linux (simulated)',
}

def simulate(cmd):
    """Return the engine output for a command (both profiles agree on these)."""
    c = cmd.strip()
    if c == 'whoami': return ENGINE['whoami']
    if c == 'hostname': return ENGINE['hostname']
    if c == 'pwd': return ENGINE['pwd']
    if c == 'id': return ENGINE['id']
    if c == 'ls': return ENGINE['ls']
    if c == 'uname -a': return ENGINE['uname -a']
    if c.startswith('echo '): return c[5:].strip()
    if c.startswith('echo'): return ''
    return None  # unknown -> command not found

def main():
    SAFE = {'whoami', 'hostname', 'pwd', 'id', 'ls', 'uname', 'echo'}
    FIXED = {
        'whoami': 'whoami', 'hostname': 'hostname', 'pwd': 'pwd',
        'id': 'id', 'ls': 'ls', 'uname': 'uname -a',
    }
    total = 0
    for slug, missions in MISSIONS.items():
        path = os.path.join(BASE, slug, 'content.json')
        d = json.load(open(path))
        # fidelity-test every check: satisfiable with an engine-supported command
        for m in missions:
            assert m['id'].startswith(slug), m['id']
            assert m['difficulty'] in (1, 2, 3)
            for ch in m['checks']:
                assert ch.get('hint'), f"missing hint {m['id']}"
                rx = re.compile(ch['command_pattern'])
                cm = re.match(r'^\^([a-z]+)', ch['command_pattern'])
                assert cm, f'pattern has no command prefix {m["id"]}'
                cmdname = cm.group(1)
                assert cmdname in SAFE, f'command {cmdname} not in bash-lite {m["id"]}'
                if cmdname == 'echo':
                    test_cmd = 'echo ' + ch['expect_contains']
                else:
                    test_cmd = FIXED[cmdname]
                assert rx.search(test_cmd), \
                    f'pattern {ch["command_pattern"]!r} does not match {test_cmd!r} ({m["id"]})'
                out = simulate(test_cmd)
                assert out is not None and ch['expect_contains'] in out, \
                    f'expect_contains not in output ({m["id"]}: {test_cmd!r})'
                total += 1
        d['terminalMissions'] = missions
        tmp = path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write('\n')
        os.replace(tmp, path)
        d2 = json.load(open(path))
        assert len(d2['terminalMissions']) == 7
        print(f'{slug}: missions rewritten (7), fidelity-tested')
    print(f'ALL: {total} checks fidelity-tested against engine outputs — pass')


if __name__ == '__main__':
    main()
