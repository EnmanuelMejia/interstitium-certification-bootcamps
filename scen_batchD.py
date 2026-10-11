#!/usr/bin/env python3
"""Batch D content: cybernetics CBT — scenarios, lessons, labs.

Structure:
    SCENARIOS = {"cybernetics": {"<domain-id>": [scenario dicts]}}
    LESSONS   = {"cybernetics": {"<domain-id>": [lesson dicts]}}
    LABS      = {"cybernetics": [lab dicts]}
"""

SCENARIOS = {
    "cybernetics": {
        "cybernetics": [
            {
                "id": "cyb-core-sc1",
                "title": "The Black Box on the Factory Floor",
                "domain_id": "cybernetics",
                "situation": "A packaging machine on your factory line misbehaves intermittently: sometimes it seals cartons, sometimes it crushes them. The vendor manual is lost and the machine's internals are sealed. You can vary the input settings (belt speed, temperature, carton size) and observe the outputs (seal quality, crush rate). Your manager wants the housing cut open for inspection.",
                "prompt": "Applying the cybernetic black-box method, what is your best first move?",
                "choices": [
                    "Systematically vary one input at a time, record input-output pairs, and build a model of the machine's behavior without opening it",
                    "Cut the housing open immediately, since only the internal mechanism explains the fault",
                    "Replace the machine, because intermittent faults in sealed systems cannot be diagnosed",
                    "Increase belt speed to maximum to force the fault to appear continuously, then inspect"
                ],
                "answer": 0,
                "why": "The black-box method treats the system by its observable input-output relations: controlled variation of inputs plus careful recording of outputs lets you infer the transfer behavior and isolate the fault condition without destroying the system. Opening it first risks changing the very behavior you need to explain.",
                "hint": "Ashby's black box: you learn a system by what goes in and what comes out, not by assuming you must see inside.",
                "objectives": ["Apply the black-box method to an unknown system", "Distinguish behavioral modeling from structural inspection"],
                "mins": 12,
                "evidence": ["Describes a controlled input-variation experiment with recorded outputs"]
            },
            {
                "id": "cyb-core-sc2",
                "title": "Requisite Variety in the Control Room",
                "domain_id": "cybernetics",
                "situation": "You supervise a regional power-grid control desk. Disturbances arrive in 12 distinct types (line faults, demand spikes, generator trips, and so on). Your control team currently has 5 standard response procedures. Last quarter, three novel disturbance combinations cascaded into outages because no procedure matched them.",
                "prompt": "Ashby's Law of Requisite Variety says only variety can destroy variety. What does it prescribe here?",
                "choices": [
                    "Reduce the variety of disturbances by disconnecting volatile grid segments, since the regulator cannot match them",
                    "Increase the regulator's variety: add response procedures, cross-train operators, and build adaptive playbooks until control variety matches disturbance variety",
                    "Automate the 5 existing procedures so they execute faster; speed compensates for missing variety",
                    "Centralize all decisions with the shift supervisor to eliminate inconsistent responses"
                ],
                "answer": 1,
                "why": "Requisite variety demands the controller's repertoire be at least as rich as the disturbances it must absorb. Faster execution of 5 procedures cannot handle a 12-type disturbance space; only expanding control variety (more procedures, trained judgment, adaptive playbooks) closes the gap.",
                "hint": "Count the varieties: 12 disturbance types vs 5 responses. Which side must grow?",
                "objectives": ["State Ashby's Law of Requisite Variety", "Apply it to a control-system staffing decision"],
                "mins": 10,
                "evidence": ["Identifies the variety gap (12 vs 5) and prescribes expanding regulator variety"]
            }
        ],
        "systems-anatomy": [
            {
                "id": "cyb-sa-sc1",
                "title": "Anatomy of a Thermostat",
                "domain_id": "systems-anatomy",
                "situation": "A homeowner complains the house swings between chilly and stuffy even though the thermostat is set to 70F. You inspect: the thermostat sensor sits directly above a heat vent, the furnace is oversized for the house, and the thermostat has no anticipator adjustment. The owner asks which single part to replace.",
                "prompt": "Reading the thermostat as a sensor-comparator-effector loop, where is the structural fault?",
                "choices": [
                    "The sensor placement: sitting above the vent, it samples hot air instead of room air, so the comparator acts on false feedback",
                    "The furnace: oversizing means it heats too fast, so replace it with a smaller unit",
                    "The setpoint dial: 70F is simply the wrong target for this house",
                    "The homeowner's expectations: some swing is normal and no fix is needed"
                ],
                "answer": 0,
                "why": "In loop anatomy, the sensor feeds the comparator; a sensor sampling the wrong variable (vent air, not room air) corrupts every downstream decision, producing oscillation. Relocating the sensor repairs the feedback path itself, which is the structural fault — the furnace size is secondary.",
                "hint": "Trace the loop: sensor -> comparator -> effector. Which link is lying?",
                "objectives": ["Decompose a control loop into sensor, comparator, and effector", "Diagnose oscillation from sensor placement"],
                "mins": 10,
                "evidence": ["Names the sensor-comparator-effector chain and locates the fault at the sensor"]
            },
            {
                "id": "cyb-sa-sc2",
                "title": "Anatomy of Homeostasis",
                "domain_id": "systems-anatomy",
                "situation": "During a winter hike, a companion starts shivering violently, then the shivering stops even though the cold continues. An hour later they become confused and drowsy. A fellow hiker says the stopped shivering means the body has adapted and they are fine now.",
                "prompt": "As a homeostatic feedback system, what does the stopped shivering actually signal?",
                "choices": [
                    "Successful adaptation: the setpoint has shifted and the body no longer needs to generate heat",
                    "Effector exhaustion: the shivering mechanism (heat production) has failed while the disturbance continues, so core temperature is now falling unchecked",
                    "Sensor failure: the skin thermoreceptors have gone numb, which is harmless on its own",
                    "A secondary loop taking over: sweating will begin to compensate for the cold"
                ],
                "answer": 1,
                "why": "Shivering is the effector in the thermoregulatory loop; when it ceases while the cold disturbance persists, the loop has lost its corrective arm, not reached its goal. Confusion and drowsiness confirm core temperature is dropping — a loop failure, not adaptation. This is a medical emergency pattern.",
                "hint": "An effector that quits while the disturbance continues is loop failure, not success.",
                "objectives": ["Map physiological regulation onto feedback-loop anatomy", "Distinguish loop success from effector failure"],
                "mins": 10,
                "evidence": ["Identifies shivering as the effector and its cessation as loop failure"]
            },
            {
                "id": "cyb-sa-sc3",
                "title": "Anatomy of a PID Controller",
                "domain_id": "systems-anatomy",
                "situation": "Your team's delivery drone oscillates in altitude: it climbs past the target, dives below it, climbs again. The flight controller is a PID loop. Telemetry shows the oscillation period is steady and the amplitude is not decaying. A teammate proposes cranking up the proportional gain to force it onto target faster.",
                "prompt": "Reading the PID anatomy, what is the disciplined diagnosis and first tuning move?",
                "choices": [
                    "Increase proportional gain: stronger correction always reduces steady oscillation",
                    "The loop is underdamped and oscillating; increase derivative gain (damping) first, and re-check integral windup, before touching proportional gain",
                    "Disable the integral term permanently: integrators cause all oscillation",
                    "Add a feedforward term and ignore the oscillation: feedforward overrides feedback problems"
                ],
                "answer": 1,
                "why": "Steady, non-decaying oscillation is the signature of an underdamped loop with insufficient derivative (damping) action; more proportional gain typically worsens it. The disciplined move is to add damping first, then verify the integrator is not wound up, keeping the P-I-D anatomy balanced.",
                "hint": "P pushes, I remembers, D brakes. Which one brakes oscillation?",
                "objectives": ["Explain the P, I, and D roles in loop anatomy", "Choose a tuning move from oscillation symptoms"],
                "mins": 12,
                "evidence": ["Diagnoses underdamping and prescribes derivative action before proportional changes"]
            },
            {
                "id": "cyb-sa-sc4",
                "title": "Anatomy of Organizational Feedback",
                "domain_id": "systems-anatomy",
                "situation": "A software company runs quarterly performance reviews, but product quality keeps sliding. Engineers say reviews measure lines of code and ticket counts; customer-escape defects are tracked by a different team and never enter the review. Managers say they are giving plenty of feedback.",
                "prompt": "Where is the organizational feedback loop anatomically broken?",
                "choices": [
                    "The comparator: reviews compare engineers against the wrong reference (output volume instead of outcome quality), so correction pushes the wrong behavior",
                    "The effector: managers are not delivering the reviews forcefully enough",
                    "The setpoint: quarterly is too infrequent; reviews should be monthly",
                    "The sensor: engineers are not listening during review meetings"
                ],
                "answer": 0,
                "why": "The loop's comparator judges performance against its reference signal; here the reference is volume metrics while the true goal is quality, so the 'correction' actively rewards the wrong behavior. Frequency and delivery style cannot fix a comparator aimed at the wrong target.",
                "hint": "Feedback is only as good as the reference it compares against. What is being compared to what?",
                "objectives": ["Map sensor-comparator-effector anatomy onto a management process", "Diagnose a mis-aimed comparator"],
                "mins": 10,
                "evidence": ["Locates the fault at the comparator/reference and names the mis-aimed metric"]
            },
            {
                "id": "cyb-sa-sc5",
                "title": "Anatomy of an Ecosystem Loop",
                "domain_id": "systems-anatomy",
                "situation": "A lake's algae blooms have worsened for five years. Data: fertilizer runoff (input) rose steadily; zooplankton that eat algae declined after a pesticide entered the water; dead algae decay consumes oxygen, killing fish that eat zooplankton. The town council proposes banning fertilizer outright as the single fix.",
                "prompt": "Reading the lake as coupled feedback loops, how should you advise the council?",
                "choices": [
                    "Support the fertilizer ban alone: cutting the input starves the bloom, and single causes need single fixes",
                    "Advise a loop-level view: the bloom is driven by a reinforcing cycle (algae -> decay -> oxygen loss -> fewer grazers -> more algae) plus weakened negative feedback (pesticide killing zooplankton); intervene at multiple loop points, not just the input",
                    "Stock more fish: predators always restore balance in food webs",
                    "Do nothing: ecosystems self-correct and the bloom will collapse on its own"
                ],
                "answer": 1,
                "why": "The lake is coupled loops, not a single input-output pipe: a reinforcing loop amplifies the bloom while the pesticide has cut the negative-feedback grazing arm. Effective intervention must weaken the reinforcing cycle and restore the negative feedback together; an input ban alone leaves the loop structure intact.",
                "hint": "Find the reinforcing loop and the damaged negative-feedback arm before prescribing.",
                "objectives": ["Identify coupled reinforcing and balancing loops in an ecosystem", "Argue for multi-point intervention from loop structure"],
                "mins": 12,
                "evidence": ["Names the reinforcing cycle and the weakened grazing feedback, prescribing multi-point action"]
            },
            {
                "id": "cyb-sa-sc6",
                "title": "Conversation as a Feedback System",
                "domain_id": "systems-anatomy",
                "situation": "Two co-founders argue weekly about product direction. Founder A states a position; Founder B hears criticism and defends; A hears defensiveness as closed-mindedness and pushes harder; B withdraws further. Each leaves believing the other will not listen. A coach suggests they prepare better arguments.",
                "prompt": "Applying Bateson's view of communication as a feedback system, what is the actual pathology and the leverage point?",
                "choices": [
                    "Weak arguments: whoever argues better will break the cycle, so invest in rhetoric training",
                    "A symmetrical schismogenesis: each response amplifies the other's stance in a runaway positive-feedback loop; the leverage point is changing the pattern of response, not the content of arguments",
                    "A personality mismatch: the partnership is structurally unworkable and should be dissolved",
                    "Missing information: they need a shared dashboard so facts replace opinions"
                ],
                "answer": 1,
                "why": "Bateson named this symmetrical schismogenesis — a runaway positive-feedback loop where each party's move escalates the other's. Better arguments feed the loop (more push, more withdrawal). The intervention must target the response pattern itself: e.g., structured turn-taking that breaks the amplification circuit.",
                "hint": "When each move makes the next move worse, the pattern — not the people or the points — is the problem.",
                "objectives": ["Recognize symmetrical schismogenesis as positive feedback", "Choose a pattern-level intervention over a content-level one"],
                "mins": 12,
                "evidence": ["Names schismogenesis and prescribes changing the response pattern"]
            },
            {
                "id": "cyb-sa-sc7",
                "title": "Anatomy of the Watt Governor",
                "domain_id": "systems-anatomy",
                "situation": "You are restoring an 1880s steam engine with its original centrifugal (Watt) governor: two flyballs spin with the engine, rise with speed, and close the steam valve as they rise. During testing the engine hunts — speed surges and sags rhythmically. The restoration team debates adding a modern electronic controller.",
                "prompt": "Diagnosing the governor as a feedback loop, what explains the hunting and what is the minimal faithful fix?",
                "choices": [
                    "The flyballs are too light for this engine; replace them with heavier modern equivalents",
                    "Hunting is loop oscillation: the correction lags or overshoots (friction, play in the linkage, or excessive valve gain); the faithful fix is to reduce the loop gain or add damping in the linkage, preserving the original mechanism",
                    "The setpoint is wrong: adjust the spring tension until the hunting stops, ignoring the linkage",
                    "Install the electronic controller: 19th-century governors cannot hold speed on restored engines"
                ],
                "answer": 1,
                "why": "Hunting is the classic symptom of an underdamped feedback loop — delay or excess gain makes correction overshoot the setpoint rhythmically. The Watt governor already contains the full loop anatomy (sensor: flyballs, comparator: linkage geometry, effector: steam valve); the minimal fix tunes gain/damping in the existing loop rather than replacing its architecture.",
                "hint": "Hunting means the loop overshoots. Do you need a new loop, or a calmer one?",
                "objectives": ["Analyze a historical mechanism as a complete feedback loop", "Distinguish tuning fixes from architectural replacement"],
                "mins": 10,
                "evidence": ["Diagnoses hunting as underdamped oscillation and prescribes gain/damping adjustment"]
            }
        ],
        "origins": [
            {
                "id": "cyb-origins-sc1",
                "title": "Designing a Macy-Style Team",
                "domain_id": "origins",
                "situation": "Your company is forming a task force on algorithmic hiring bias. The proposed roster is six machine-learning engineers. HR suggests adding a labor sociologist, an employment lawyer, and a former job applicant who experienced the system. Engineering leadership objects: outsiders will slow the technical work.",
                "prompt": "What lesson from the Macy Conferences (1946-1953) settles this roster debate?",
                "choices": [
                    "The Macy lesson is specialization: keep the team purely technical so feedback concepts stay rigorous",
                    "The Macy breakthrough came from enforced interdisciplinarity — engineers, anthropologists, psychologists, and mathematicians in one room, sharing the language of feedback and information; the mixed roster is the method, not a concession",
                    "The Macy lesson is hierarchy: put the engineers in charge and consult outsiders only at the end",
                    "The Macy conferences failed precisely because of disciplinary mixing, so keep the team narrow"
                ],
                "answer": 1,
                "why": "The Macy Conferences deliberately assembled radically different disciplines around the shared concepts of circular causality, feedback, and information — and that collision produced cybernetics itself. A hiring-bias task force needs the same structure: the sociologist, lawyer, and affected applicant are not overhead, they are the feedback channels the engineers lack.",
                "hint": "Cybernetics was born when disciplines collided in one room. What does that imply for the roster?",
                "objectives": ["Explain the Macy Conferences' interdisciplinary method", "Apply it to a modern team-design decision"],
                "mins": 10,
                "evidence": ["Cites enforced interdisciplinarity as the Macy method and defends the mixed roster"]
            },
            {
                "id": "cyb-origins-sc2",
                "title": "Circular Causality in a Family Business",
                "domain_id": "origins",
                "situation": "In a family-run distributor, the founder micromanages his daughter, the operations lead. She responds by withholding bad news; he responds to surprises by tightening control; she withholds more. A consultant's report blames her communication skills and recommends training for her alone.",
                "prompt": "The Macy circle would reject linear blame here. What is the cybernetically sound reframing?",
                "choices": [
                    "Accept the consultant's finding: the daughter's withholding is the root cause, and training fixes root causes",
                    "Reframe as circular causality: control provokes withholding which provokes control — each behavior is both cause and effect; intervene in the circuit (e.g., structured reporting rituals) rather than fixing one person",
                    "Blame the founder instead: reverse the linear blame to the true root cause",
                    "Remove family members from reporting lines: the only fix is structural separation"
                ],
                "answer": 1,
                "why": "The Macy core insight is circular causality: in a feedback circuit there is no first cause, only a pattern that sustains itself. Training one node leaves the circuit intact; the intervention must change the circuit — e.g., a weekly reporting ritual that makes withholding unnecessary and control redundant.",
                "hint": "In a loop, who started it is the wrong question. What sustains it is the right one.",
                "objectives": ["Apply circular causality to an interpersonal conflict", "Reject linear blame in favor of circuit intervention"],
                "mins": 10,
                "evidence": ["Describes the control-withholding circuit and proposes a circuit-level intervention"]
            },
            {
                "id": "cyb-origins-sc3",
                "title": "Wiener vs von Bertalanffy on the Startup",
                "domain_id": "origins",
                "situation": "Two advisors assess a struggling logistics startup. Advisor W says: map every feedback loop — dispatch, driver incentives, customer complaints — and tune the control mechanisms. Advisor B says: treat the firm as an open system exchanging matter, energy, and information with its environment; study its boundaries, inputs, and growth dynamics before touching any loop.",
                "prompt": "Which advisor channels Wiener and which channels von Bertalanffy, and what is the productive synthesis?",
                "choices": [
                    "W is von Bertalanffy (feedback) and B is Wiener (open systems); pick W because feedback is the whole of systems science",
                    "W is Wiener (feedback, control, communication mechanisms) and B is von Bertalanffy (open systems, boundaries, wholeness); the synthesis is to bound the open system first, then tune its internal feedback loops",
                    "Both are Wiener: von Bertalanffy never wrote about organizations",
                    "Both are von Bertalanffy: Wiener's cybernetics applies only to machines, not firms"
                ],
                "answer": 1,
                "why": "Wiener's cybernetics centers control and communication through feedback; von Bertalanffy's General Systems Theory centers open systems, boundaries, and wholeness. They are complements: Bertalanffy tells you what the system is open to and where its boundaries lie; Wiener tells you how its internal loops regulate it. Diagnose the open system first, then tune the loops.",
                "hint": "Wiener = feedback and control; Bertalanffy = open systems and wholeness. They answer different questions.",
                "objectives": ["Contrast Wiener's cybernetics with von Bertalanffy's GST", "Synthesize both framings on one case"],
                "mins": 12,
                "evidence": ["Correctly attributes each advisor and orders the diagnosis: boundaries first, loops second"]
            },
            {
                "id": "cyb-origins-sc4",
                "title": "Equifinality in Market Entry",
                "domain_id": "origins",
                "situation": "Two rival food-delivery firms reach the same dominant city share by opposite routes: one burned venture capital on rider subsidies, the other built slowly through restaurant partnerships. Your strategy team insists there must be one best-practice playbook and wants to copy the subsidy route because it was faster.",
                "prompt": "Von Bertalanffy's principle of equifinality speaks directly to this debate. What does it say?",
                "choices": [
                    "Equifinality proves the faster route is the optimal one; copy the subsidies",
                    "Equifinality states that open systems can reach the same final state from different initial conditions and by different paths; there is no single mandatory playbook — the team should match the path to its own resources and environment",
                    "Equifinality applies only to biological organisms, not companies",
                    "Equifinality means all strategies converge on failure; exit the market"
                ],
                "answer": 1,
                "why": "Equifinality — a signature von Bertalanffy concept for open systems — holds that the same end state can be reached via different trajectories. Copying the subsidy playbook ignores that the rival's path depended on its capital; the team's own resource base may favor the partnership path to the same outcome.",
                "hint": "Same destination, different roads. What does that imply about 'best practice'?",
                "objectives": ["Define equifinality", "Use it to challenge playbook-copying in strategy"],
                "mins": 10,
                "evidence": ["States equifinality and argues for path-resource fit over copying"]
            },
            {
                "id": "cyb-origins-sc5",
                "title": "Bateson's Difference That Makes a Difference",
                "domain_id": "origins",
                "situation": "An operations dashboard shows 40 real-time metrics, all green, yet the warehouse keeps missing ship targets. Managers stare at the wall of numbers daily and change nothing. The analytics vendor proposes adding 20 more metrics and an AI summary layer.",
                "prompt": "Bateson defined information as 'a difference that makes a difference.' What does that prescribe for the dashboard?",
                "choices": [
                    "Add the 20 metrics: more differences measured means more information by definition",
                    "Cut the dashboard to the few differences that actually change decisions — a metric is information only if it makes a difference to action; the rest is noise regardless of volume",
                    "Keep all 40 but color-code them: presentation, not selection, is the problem",
                    "Replace the dashboard with the AI summary: automation resolves the overload"
                ],
                "answer": 1,
                "why": "Bateson's definition is pragmatic: a difference counts as information only insofar as it makes a difference — to the system that receives it. Forty green metrics that change no decision carry no information; the fix is subtractive, selecting the differences that trigger action, not additive.",
                "hint": "If no decision changes, was any information transmitted?",
                "objectives": ["Apply Bateson's definition of information", "Prescribe subtractive dashboard design"],
                "mins": 10,
                "evidence": ["Quotes the difference criterion and recommends cutting non-actionable metrics"]
            },
            {
                "id": "cyb-origins-sc6",
                "title": "The Double Bind Memo",
                "domain_id": "origins",
                "situation": "A CEO sends an all-hands memo: 'I want radical candor — challenge every decision openly. But remember, we are a family, and family members do not embarrass each other in public.' Afterwards, engineers who raise concerns in meetings are praised for candor and quietly passed over for promotion. Silence spreads.",
                "prompt": "Bateson's double-bind theory diagnoses this precisely. What is the bind, and what breaks it?",
                "choices": [
                    "There is no bind: employees should simply be more courageous about candor",
                    "The bind is two contradictory injunctions at different levels (speak up / do not embarrass) with punishment for either response and no permitted meta-commentary; it breaks by making the contradiction discussable — legitimizing talk about the talk",
                    "The bind is a compensation problem: pay people more to tolerate the contradiction",
                    "The bind resolves by choosing one injunction: enforce candor and abolish the family metaphor by decree"
                ],
                "answer": 1,
                "why": "Bateson's double bind requires: two conflicting injunctions, punishment whichever is obeyed, and no escape to a meta-level where the contradiction can be named. The memo creates exactly this. Decreeing one side wins does not restore the missing meta-level; only legitimizing discussion of the contradiction itself dissolves the bind.",
                "hint": "Two orders, punished either way, and you are forbidden to mention the contradiction. What is missing?",
                "objectives": ["Identify a double bind in organizational communication", "Prescribe the meta-level escape"],
                "mins": 12,
                "evidence": ["Names the two injunctions and prescribes legitimizing meta-communication"]
            },
            {
                "id": "cyb-origins-sc7",
                "title": "McCulloch-Pitts in the Neural Net Era",
                "domain_id": "origins",
                "situation": "A junior ML engineer dismisses the 1943 McCulloch-Pitts neuron as a historical curiosity: 'Binary threshold units have nothing to do with our transformer models.' Her tech lead disagrees but struggles to articulate the connection in one breath.",
                "prompt": "What is the precise, defensible relevance of McCulloch and Pitts (1943) to modern deep learning?",
                "choices": [
                    "None: transformers abandoned threshold logic entirely, so the paper is only of antiquarian interest",
                    "The paper proved networks of simple threshold units can compute any logical function — establishing the principle that cognition-like computation can emerge from interconnected simple units, the architectural idea every neural network, including transformers, still instantiates",
                    "The paper invented backpropagation, which transformers still use unchanged",
                    "The paper proved binary units are optimal, so modern continuous activations are a mistake"
                ],
                "answer": 1,
                "why": "'A Logical Calculus of the Ideas Immanent in Nervous Activity' showed that networks of idealized binary threshold neurons can realize arbitrary logical functions — the founding demonstration that mind-like computation could arise from simple interconnected units. Transformers differ in scale, training, and continuous activations, but they inherit this exact architectural premise.",
                "hint": "What did the paper prove possible — not how modern nets train, but what networks of simple units can compute?",
                "objectives": ["State the McCulloch-Pitts result accurately", "Connect it to modern neural architectures without overclaiming"],
                "mins": 10,
                "evidence": ["States the logical-completeness result and its architectural legacy"]
            },
            {
                "id": "cyb-origins-sc8",
                "title": "Wiener's Refusal",
                "domain_id": "origins",
                "situation": "Your robotics lab is offered a lucrative defense contract to adapt its warehouse navigation stack for autonomous weapons targeting. The funding would triple the lab's budget. A senior researcher cites Norbert Wiener and argues the lab should decline, even though the work is 'just navigation math.'",
                "prompt": "What is the Wiener precedent, and how does it apply to the 'just math' defense?",
                "choices": [
                    "Wiener had no ethical positions; he accepted all military funding, so there is no precedent",
                    "Wiener, whose wartime anti-aircraft predictor work founded cybernetics, later refused military research funding and warned in 'The Human Use of Human Beings' about ceding human judgment to machines — the precedent is that the mathematician is responsible for foreseeable uses, and 'just math' does not absolve the lab",
                    "Wiener's precedent is that scientists should never consider applications at all",
                    "Wiener supported autonomous weapons, so the precedent favors accepting"
                ],
                "answer": 1,
                "why": "Wiener's trajectory is the point: the founder of cybernetics did the wartime predictor work, then publicly refused further military funding and spent 'The Human Use of Human Beings' warning against dehumanizing automation. The precedent holds that technical neutrality is no defense — responsibility follows foreseeable use.",
                "hint": "The man who built the wartime predictor later refused the war work. What does that say about 'just math'?",
                "objectives": ["Recall Wiener's ethical stance accurately", "Apply it to a dual-use funding decision"],
                "mins": 10,
                "evidence": ["Cites the predictor work, the refusal, and the responsibility principle"]
            }
        ],
        "feedback-systems": [
            {
                "id": "cyb-feedback-sc1",
                "title": "Finding Loops in the Support Org",
                "domain_id": "feedback-systems",
                "situation": "A SaaS company's support queue grows every quarter despite hiring. You map the system: tickets arrive from customers; agents close tickets; management rewards agents per ticket closed; agents, pressed for speed, close tickets with shallow fixes; shallow fixes generate reopened tickets and new complaints; management sees rising volume and hires more agents, who are onboarded with the same speed incentives.",
                "prompt": "Which intervention actually changes the loop structure rather than feeding it?",
                "choices": [
                    "Hire faster: more agents with the same incentives will eventually drain the queue",
                    "Change the reward to reward durable resolution (low reopen rate), breaking the shallow-fix reinforcing loop at its incentive link",
                    "Add a triage layer: more process steps will absorb the volume",
                    "Outsource tier-1 support to cut cost per ticket"
                ],
                "answer": 1,
                "why": "The mapped system is a reinforcing loop: speed incentives -> shallow fixes -> reopens -> more volume -> more speed pressure. Hiring and triage add capacity without touching the loop's gain; only changing what is rewarded alters the loop structure itself, converting a vicious cycle into a balancing one.",
                "hint": "Draw the loop. Which arrow can you actually rewire?",
                "objectives": ["Map reinforcing loops in an organization", "Choose a structural intervention over a capacity one"],
                "mins": 12,
                "evidence": ["Names the speed->shallow-fix->reopen loop and rewires the incentive link"]
            },
            {
                "id": "cyb-feedback-sc2",
                "title": "Designing Negative Feedback for Cloud Spend",
                "domain_id": "feedback-systems",
                "situation": "Your startup's cloud bill tripled in six months. Engineers spin up resources freely; finance sees the bill 30 days later; by the time anyone reacts, the spend is entrenched. The CFO proposes a monthly approval committee for all new resources.",
                "prompt": "Design the cybernetically sound negative-feedback control. What matters most?",
                "choices": [
                    "The monthly committee: human approval is the strongest possible negative feedback",
                    "Shorten the feedback delay and close the loop at the source: real-time spend dashboards per team with automatic alerts and budget guardrails at provisioning time, so deviation corrects before it compounds",
                    "Negotiate a bigger enterprise discount: lower unit cost solves the growth",
                    "Blame engineering culture: the problem is attitudes, not loops"
                ],
                "answer": 1,
                "why": "Negative feedback stabilizes only if the correction arrives while it can still act — a 30-day delay plus a monthly committee lets overshoot compound between corrections. Effective control shortens the loop (real-time visibility) and places the comparator at the decision point (provisioning guardrails), which is the actual negative-feedback design.",
                "hint": "A thermostat that reads the temperature a month late cannot hold the setpoint. Where is the delay?",
                "objectives": ["Design a negative-feedback control for a cost system", "Explain why feedback delay defeats correction"],
                "mins": 10,
                "evidence": ["Proposes real-time visibility plus provisioning-time guardrails, citing delay"]
            },
            {
                "id": "cyb-feedback-sc3",
                "title": "Spotting the Runaway: A Bank Run in Miniature",
                "domain_id": "feedback-systems",
                "situation": "A regional bank faces rumors of insolvency on social media. A few depositors withdraw; local news films the ATM lines; more depositors see the lines and withdraw; the bank, seeing outflows, restricts withdrawals, which confirms the rumor. The bank is actually solvent, with reserves well above requirements.",
                "prompt": "Name the loop dynamics and the correct early intervention.",
                "choices": [
                    "A balancing loop that will self-correct once the rumor fades; do nothing and wait",
                    "A runaway positive-feedback loop (withdrawals -> visible lines -> more withdrawals, amplified by restrictions); the intervention is to break the amplification early — credible, verifiable disclosure of reserves plus visible normal operations before the loop saturates",
                    "A negative-feedback loop: restrictions will stabilize outflows, so tighten them faster",
                    "A linear cause-effect chain: find and punish the rumor's originator to stop it"
                ],
                "answer": 1,
                "why": "Each withdrawal visibly signals danger, recruiting the next withdrawal — positive feedback with no natural ceiling until the bank empties. Withdrawal restrictions act as confirming evidence, adding gain. Only an early counter-signal stronger than the loop's amplification (transparent, verifiable solvency proof while operations look normal) can break it before saturation.",
                "hint": "Does each event make the next event more or less likely? That tells you the loop sign.",
                "objectives": ["Identify runaway positive feedback in a social system", "Prescribe an early amplification-breaking intervention"],
                "mins": 12,
                "evidence": ["Names the positive-feedback loop and prescribes early credible disclosure"]
            },
            {
                "id": "cyb-feedback-sc4",
                "title": "The Hiring Oscillation",
                "domain_id": "feedback-systems",
                "situation": "A logistics firm alternates between frantic hiring binges and layoffs every 18 months. The pattern: a capacity crunch triggers aggressive hiring; recruiting and training take 9 months; by the time new staff are productive, demand has normalized, so the firm is overstaffed; layoffs follow; months later another crunch hits. Management blames 'unpredictable markets.'",
                "prompt": "What is the cybernetic diagnosis, and what breaks the cycle?",
                "choices": [
                    "The market is genuinely unpredictable; the cycle is unavoidable and should be managed with severance planning",
                    "Delay-induced oscillation: the 9-month hiring delay means corrections arrive out of phase with the need, so the firm perpetually overshoots; the fix is to shorten the delay (faster onboarding, flexible staffing buffers) or damp the correction (hire to a moving average, not the peak)",
                    "Managers are incompetent at forecasting; replace them with a forecasting algorithm",
                    "The hiring gain is too low; hire even more aggressively during crunches"
                ],
                "answer": 1,
                "why": "This is the classic delay-oscillation pattern Donella Meadows described: when corrective action lags the signal by a large fraction of the cycle, each correction lands out of phase and overshoots, producing perpetual boom-bust. The cure targets the delay and the gain — faster response, buffered capacity, and hiring to smoothed demand — not better predictions of an 'unpredictable' market.",
                "hint": "Nine months of delay in an 18-month cycle: corrections keep arriving exactly out of phase.",
                "objectives": ["Diagnose delay-induced oscillation", "Prescribe delay-shortening and gain-damping fixes"],
                "mins": 12,
                "evidence": ["Names delay-induced oscillation and proposes buffering plus smoothed hiring targets"]
            },
            {
                "id": "cyb-feedback-sc5",
                "title": "The PID Tuning Decision",
                "domain_id": "feedback-systems",
                "situation": "You are tuning the temperature controller for a chemical reactor. Trial A (high proportional gain): reaches setpoint in 4 minutes but overshoots by 15 degrees, risking a runaway reaction. Trial B (low gain): no overshoot but takes 40 minutes, and a persistent 3-degree offset remains because the integral term is disabled. The batch is worth $200,000 and the safety margin is 10 degrees.",
                "prompt": "What is the correct tuning judgment?",
                "choices": [
                    "Ship Trial A: speed matters most and 15 degrees of overshoot is acceptable risk",
                    "Ship Trial B: safety first, and the 3-degree offset is a minor quality issue",
                    "Reject both: enable the integral term to eliminate the offset in Trial B's safe structure, then add derivative damping and re-test — tune for no overshoot beyond the 10-degree safety margin with zero steady-state error",
                    "Average the two gains: the midpoint of two bad tunings is a good tuning"
                ],
                "answer": 2,
                "why": "Trial A violates the hard safety constraint (15-degree overshoot > 10-degree margin) — unacceptable regardless of speed. Trial B is safe but leaves steady-state error because the integrator is off. The disciplined move is structural: keep the safe low-gain base, enable integral action to kill the offset, add derivative damping against overshoot, and verify against the safety margin. Tuning is constraint-first, not compromise-by-averaging.",
                "hint": "Safety margin is a hard constraint, and the missing integrator has a name for its symptom: steady-state error.",
                "objectives": ["Apply safety-constrained PID tuning judgment", "Explain integral action's role in eliminating offset"],
                "mins": 12,
                "evidence": ["Rejects the unsafe trial, prescribes I-enable plus D-damping within the safety margin"]
            },
            {
                "id": "cyb-feedback-sc6",
                "title": "Feedforward vs Feedback on the Highway Crew",
                "domain_id": "feedback-systems",
                "situation": "A highway maintenance crew is repeatedly caught by flash floods that wash out fresh asphalt. They currently react after each flood (feedback): assess damage, repave, wait for the next storm. A meteorologist offers a paid early-warning feed; the crew chief says warnings are useless because 'you can't control the weather.'",
                "prompt": "What is the cybernetic case for the early-warning feed?",
                "choices": [
                    "There is none: feedback after the event is the only honest control, since the weather is uncontrollable",
                    "Feedforward control: the warning measures the disturbance before it hits, allowing pre-emptive action (cover fresh asphalt, reschedule pours) — it complements feedback by acting on measured disturbance rather than waiting for error",
                    "Replace feedback entirely: with warnings, post-storm assessment becomes unnecessary",
                    "The feed is only useful if it is perfectly accurate; imperfect forecasts add noise"
                ],
                "answer": 1,
                "why": "Feedforward measures the disturbance directly and acts before error appears, while feedback corrects after error appears; they are complements, not rivals. The chief's objection confuses controlling the weather (impossible) with controlling the response to it (the whole point). Even imperfect forecasts beat pure reaction when the cost of being caught unprepared is high.",
                "hint": "Feedback corrects error after it appears. What acts before the error appears?",
                "objectives": ["Distinguish feedforward from feedback control", "Justify feedforward under uncertainty"],
                "mins": 10,
                "evidence": ["Defines feedforward as disturbance-measurement and pairs it with existing feedback"]
            },
            {
                "id": "cyb-feedback-sc7",
                "title": "Nested Loops in the Sales Organization",
                "domain_id": "feedback-systems",
                "situation": "A sales org has two loops: reps adjust daily effort against weekly targets (fast inner loop), and leadership adjusts quarterly quotas and territories against revenue goals (slow outer loop). Lately the outer loop raises quotas every quarter based on last quarter's over-performance, and reps respond by sandbagging deals into the next quarter — total revenue is flat while everyone games the system.",
                "prompt": "Diagnose the nested-loop pathology and fix it.",
                "choices": [
                    "Tighten the inner loop: daily monitoring of rep activity will stop sandbagging",
                    "The outer loop is destabilizing the inner: quota ratcheting punishes over-performance, so the inner loop's rational response is to hide performance; fix the outer loop's reference (e.g., quotas set from market potential, with ratchet caps) so the inner loop can optimize honestly",
                    "Abolish quotas: without targets there is nothing to game",
                    "Speed up the outer loop to monthly quota resets so sandbagging has nowhere to hide"
                ],
                "answer": 1,
                "why": "In nested loops the outer loop sets the reference the inner loop chases; when the outer loop punishes success (ratcheting quotas up after over-performance), the inner loop rationally suppresses its own output — the pathology is in the outer reference, not inner effort. Faster or tighter inner control just intensifies the gaming. The fix re-anchors the outer reference to market potential with anti-ratchet rules.",
                "hint": "The inner loop is behaving rationally given its reference. Who sets that reference?",
                "objectives": ["Analyze nested feedback loops", "Locate pathology in the outer loop's reference signal"],
                "mins": 12,
                "evidence": ["Identifies quota ratcheting as the outer-loop fault and re-anchors quotas to market potential"]
            }
        ],
        "information": [
            {
                "id": "cyb-info-sc1",
                "title": "Entropy of a Biased Coin",
                "domain_id": "information",
                "situation": "A sensor reports a binary status each second. Under normal conditions the reading is 0 with probability 0.75 and 1 with probability 0.25. A vendor proposes compressing the telemetry stream and claims 'each reading carries 1 bit of information, so the stream is incompressible.'",
                "prompt": "What is the actual Shannon entropy per reading, and what does it imply?",
                "choices": [
                    "1 bit, as the vendor says: binary readings always carry exactly 1 bit",
                    "Approximately 0.81 bits: H = -(0.75*log2(0.75) + 0.25*log2(0.25)) ~ 0.81, so the stream is compressible to about 81% of its raw size with ideal coding",
                    "0.5 bits: the minority symbol carries half a bit",
                    "2 bits: uncertainty doubles because the distribution is skewed"
                ],
                "answer": 1,
                "why": "Shannon entropy for this distribution is -(0.75 x log2 0.75 + 0.25 x log2 0.25) = 0.311 + 0.5 = 0.811 bits per symbol — less than 1 because the skewed distribution is partly predictable. The source coding theorem says the stream can be compressed to near 0.81 bits per reading; the vendor's '1 bit always' claim is false.",
                "hint": "Skewed means predictable, and predictable means less surprise per symbol. Compute -sum(p log2 p).",
                "objectives": ["Compute Shannon entropy for a binary source", "Apply the source coding theorem to a compression claim"],
                "mins": 12,
                "evidence": ["Computes ~0.81 bits and concludes the stream is compressible"]
            },
            {
                "id": "cyb-info-sc2",
                "title": "Channel Capacity on a Noisy Link",
                "domain_id": "information",
                "situation": "A remote pipeline monitor must send 50 kbps of sensor data over a radio link with 3 kHz of bandwidth. The link budget gives a signal-to-noise ratio of 30 dB (a power ratio of 1000:1). The radio vendor guarantees 'up to 100 kbps' on this channel.",
                "prompt": "Does the Shannon-Hartley law support the vendor's guarantee for your 50 kbps need?",
                "choices": [
                    "Yes: 100 kbps guaranteed exceeds the 50 kbps need, so deploy with confidence",
                    "No: capacity C = 3000 x log2(1+1000) ~ 29.9 kbps, which is below both the guarantee and your 50 kbps need — the vendor's claim violates the Shannon limit, so you need more bandwidth, better SNR, or less data",
                    "Yes, because 30 dB is a strong signal and strong signals carry unlimited data",
                    "No, but the fix is a better antenna rather than questioning the guarantee"
                ],
                "answer": 1,
                "why": "Shannon-Hartley caps capacity at B x log2(1+S/N) = 3000 x log2(1001) ~= 29.9 kbps — a hard physical ceiling no coding can exceed. The vendor's 100 kbps guarantee is impossible on this channel, and the 50 kbps requirement cannot be met without more bandwidth, higher SNR, or data reduction.",
                "hint": "C = B log2(1 + S/N). Run the numbers before trusting the datasheet.",
                "objectives": ["Apply the Shannon-Hartley capacity formula", "Use it to falsify an impossible vendor claim"],
                "mins": 12,
                "evidence": ["Computes ~30 kbps capacity and rejects the 100 kbps guarantee"]
            },
            {
                "id": "cyb-info-sc3",
                "title": "The Redundancy Decision",
                "domain_id": "information",
                "situation": "A spacecraft team debates its command uplink coding. Option R: heavy redundancy (triple repetition) — extremely reliable but only 1/3 the command rate. Option E: efficient coding near the Shannon limit — full rate but any uncorrected error corrupts a command. The mission phase involves rare, critical, irreversible commands (engine burns).",
                "prompt": "How should information theory guide the coding choice for this phase?",
                "choices": [
                    "Always choose efficiency: Shannon proved we can approach capacity with arbitrarily low error, so redundancy is wasteful",
                    "Match redundancy to the cost of error: for rare, critical, irreversible commands, the price of a corrupted burn dwarfs the bandwidth cost, so spend redundancy heavily here and use efficient coding for routine telemetry",
                    "Always choose triple repetition: reliability is the only metric that matters in space",
                    "Let the ground operators decide per command with no policy: flexibility beats theory"
                ],
                "answer": 1,
                "why": "Information theory frames the trade precisely: redundancy buys error protection at the price of rate. Shannon's limit tells us what is achievable, but the choice of operating point is economic — set by the asymmetry between bandwidth cost and error cost. Irreversible critical commands justify heavy redundancy; bulk routine data justifies efficiency.",
                "hint": "Redundancy is insurance. When is the insured event catastrophic?",
                "objectives": ["Explain the redundancy-rate trade-off", "Set the operating point from error cost"],
                "mins": 10,
                "evidence": ["Justifies heavy redundancy for critical commands from error-cost asymmetry"]
            },
            {
                "id": "cyb-info-sc4",
                "title": "Signal vs Noise in the Incident Channel",
                "domain_id": "information",
                "situation": "A DevOps team's alert channel fires 400 alerts a day; 3 are actionable. Engineers muted the channel months ago. Last week a genuine database-failover alert scrolled past unnoticed and caused a 2-hour outage. The proposed fix is 'smarter alert routing with machine learning.'",
                "prompt": "What is the information-theoretic diagnosis, and the first fix?",
                "choices": [
                    "A routing problem: ML triage will surface the 3 real alerts without changing alert volume",
                    "A signal-to-noise collapse: with 397 noise alerts per 3 signals, the channel's effective capacity for attention is saturated — the first fix is subtractive (kill noisy alerts, alert only on actionable, paged-worthy conditions), because no receiver can extract signal from that noise ratio",
                    "An engineer discipline problem: unmute the channel and mandate attention",
                    "A tooling problem: buy a louder paging system"
                ],
                "answer": 1,
                "why": "Attention is a channel with finite capacity; a 397:3 noise-to-signal ratio means the receiver (the engineer) cannot extract the signal no matter how it is routed — this is Shannon's lesson applied to human attention. The fix must raise the SNR at the source by deleting non-actionable alerts, not by adding smarter plumbing downstream of the noise.",
                "hint": "If 99% of a channel is noise, is the problem the receiver or the transmitter?",
                "objectives": ["Apply signal-to-noise reasoning to alerting", "Prescribe subtractive alert hygiene"],
                "mins": 10,
                "evidence": ["Diagnoses SNR collapse and prescribes deleting non-actionable alerts first"]
            },
            {
                "id": "cyb-info-sc5",
                "title": "Requisite Variety in the Board Pack",
                "domain_id": "information",
                "situation": "A manufacturing board receives a 200-page monthly pack, yet every strategic surprise of the last two years (a supplier failure, a demand collapse, a quality scandal) arrived with no prior signal in the pack. The CFO's solution is a 300-page pack with more detail.",
                "prompt": "Combine Ashby and Shannon: why does more pages not mean more control, and what would?",
                "choices": [
                    "It does mean more control: 300 pages carry more bits, and more bits always improve regulation",
                    "Bits are not the binding constraint — relevant variety is: the pack must carry variety that matches the disturbances that actually threaten the firm (supplier, demand, quality signals), with the noise of routine detail stripped out; a 20-page pack of decision-relevant differences beats a 300-page undifferentiated dump",
                    "The board needs fewer meetings, not better packs",
                    "Surprises are unforeseeable by definition; no pack design helps"
                ],
                "answer": 1,
                "why": "Ashby's law demands the regulator's variety match the disturbance variety that matters — supplier, demand, and quality channels were absent, so no page count could compensate. Shannon adds that a channel stuffed with routine detail has low effective signal. Control improves by selecting the differences that make a difference (Bateson) and giving them a short, fast path to the board.",
                "hint": "The surprises had no signal in the pack. What variety was missing — and what variety was noise?",
                "objectives": ["Combine requisite variety with signal-to-noise reasoning", "Redesign reporting for decision-relevant variety"],
                "mins": 12,
                "evidence": ["Identifies missing disturbance variety and prescribes a short decision-relevant pack"]
            },
            {
                "id": "cyb-info-sc6",
                "title": "Shannon vs Meaning in the Contract Clause",
                "domain_id": "information",
                "situation": "A legal-tech startup advertises 'Shannon-optimal compression of contracts — maximum information density.' A pilot customer compresses a 50-page supply agreement to a dense 5-page symbol stream that no lawyer can read, then discovers a liability clause was 'losslessly preserved but semantically invisible' to every reviewer.",
                "prompt": "What is the precise conceptual error in the startup's claim?",
                "choices": [
                    "The compression was lossy: true Shannon-optimal coding would have preserved readability",
                    "Category error: Shannon information measures surprise/uncertainty reduction, explicitly excluding meaning — 'maximum information density' in Shannon's sense says nothing about semantic accessibility, which is what contracts require; the startup sold a syntactic metric as a semantic guarantee",
                    "The customer needed a bigger screen, not a conceptual correction",
                    "Shannon's theory does not apply to text at all"
                ],
                "answer": 1,
                "why": "Shannon famously bracketed semantics: his theory quantifies uncertainty reduction, deliberately saying nothing about meaning. A 'Shannon-optimal' encoding can be perfectly information-preserving yet semantically opaque. The startup's error is selling a syntactic optimum as if it guaranteed the pragmatic property — human interpretability — that contracts actually need.",
                "hint": "Shannon himself said semantics were irrelevant to the engineering problem. What problem is a contract?",
                "objectives": ["State the scope limit of Shannon information (excludes semantics)", "Diagnose a category error in a product claim"],
                "mins": 10,
                "evidence": ["Names the syntax/semantics category error in the startup's claim"]
            },
            {
                "id": "cyb-info-sc7",
                "title": "How Much Information Does Control Need?",
                "domain_id": "information",
                "situation": "A warehouse deploys robots regulated by a central controller. The controller receives each robot's full 4K video feed (25 Mbps per robot, 40 robots) but issues only simple commands: forward, stop, turn, lift. The network is saturated, commands lag 2 seconds, and robots collide. The vendor proposes upgrading to 8K cameras 'for better control.'",
                "prompt": "What does the cybernetic view of information-for-control prescribe?",
                "choices": [
                    "Upgrade the cameras: better sensing always improves control, and bandwidth can be bought",
                    "The controller needs only the information its commands can act on: 4 discrete commands need a few bits of relevant state (position, obstacle proximity, load status), not gigabits of video — cut sensing to decision-relevant state, move perception to the edge, and the 2-second lag (a feedback delay) disappears with the bandwidth",
                    "Add more central servers: the problem is compute, not information",
                    "Slow the robots down: speed is the only adjustable parameter"
                ],
                "answer": 1,
                "why": "Control requires only the variety the regulator can actually use — Ashby again: a 4-command regulator needs bits of relevant state, not video streams. The 4K feeds are noise relative to the control task, and their bandwidth cost creates the real pathology: 2 seconds of feedback delay. Edge perception plus minimal state reporting fixes both the information mismatch and the delay.",
                "hint": "Four possible commands. How many bits of state does each command actually need?",
                "objectives": ["Apply 'information needed for control' reasoning", "Diagnose feedback delay caused by sensing overload"],
                "mins": 12,
                "evidence": ["Reduces sensing to command-relevant state and moves perception to the edge"]
            }
        ],
        "second-order": [
            {
                "id": "cyb-second-sc1",
                "title": "The Hawthorne Audit",
                "domain_id": "second-order",
                "situation": "A factory pilots a productivity-monitoring program in one hall: output rises 18% in six weeks. Management declares the monitoring system a success and rolls it out plant-wide. In the second hall, output rises only 4% and falls back within two months. An analyst notes the pilot hall knew it was being studied.",
                "prompt": "What is the second-order cybernetic reading of the pilot result?",
                "choices": [
                    "The pilot proves monitoring works; the second hall needs stricter enforcement of the same system",
                    "The 18% likely includes an observer effect — being observed changed the observed (the Hawthorne pattern); the pilot measured the system-plus-observer, not the monitoring tool alone, so rollout on the tool's merits is unjustified without a controlled comparison",
                    "The pilot hall had better workers; the result is a sampling artifact with no observer component",
                    "Productivity cannot be measured at all, so abandon all monitoring"
                ],
                "answer": 1,
                "why": "Second-order cybernetics insists the observer is part of the system: measurement perturbs what it measures. The pilot hall's awareness of being studied is itself an intervention, so the 18% confounds tool effect with observer effect. A valid claim needs the observer's influence isolated — otherwise the rollout exports an illusion.",
                "hint": "Who else was in the pilot hall besides the workers? The watchers.",
                "objectives": ["Explain the observer effect in measurement", "Withhold causal claims from confounded pilots"],
                "mins": 10,
                "evidence": ["Names the observer effect and demands a controlled comparison before rollout"]
            },
            {
                "id": "cyb-second-sc2",
                "title": "Goodhart at the Call Center",
                "domain_id": "second-order",
                "situation": "A support center bonuses agents on low average handle time (AHT). Within a quarter, AHT falls 30% — and customer satisfaction collapses, reopen rates double, and agents report hanging up on complex callers. Leadership's response is to tighten the AHT target further.",
                "prompt": "Apply Goodhart's Law. What happened, and what is the structurally sound response?",
                "choices": [
                    "Agents are gaming the metric: punish the worst offenders and the metric will recover its validity",
                    "When AHT became the target, it ceased to be a good measure — agents optimized the measure instead of the goal (resolved customers), a textbook Goodhart/Campbell effect; the fix is to re-anchor evaluation to outcomes (resolution quality, satisfaction) and treat metrics as fallible indicators, not targets",
                    "The metric is fine but the target was too lax; tightening further will restore discipline",
                    "Abolish all metrics: measurement inherently corrupts service work"
                ],
                "answer": 1,
                "why": "Goodhart's Law: when a measure becomes a target, it ceases to be a good measure. Agents rationally optimized what was rewarded, destroying the metric's validity as an indicator of good service. Punishing gamers or tightening the target intensifies the distortion; the structural fix changes what is targeted — outcomes, with metrics as servants, not masters.",
                "hint": "The agents did exactly what was rewarded. Was the reward aimed at the right thing?",
                "objectives": ["State Goodhart's Law", "Redesign incentives from metric-targets to outcome-anchors"],
                "mins": 10,
                "evidence": ["Names the Goodhart effect and re-anchors evaluation to resolution outcomes"]
            },
            {
                "id": "cyb-second-sc3",
                "title": "Teaching to the Test",
                "domain_id": "second-order",
                "situation": "A school district ties funding to standardized math scores. Scores rise steadily for four years. Meanwhile, independent assessments of problem-solving show no gain, teachers report dropping science projects to drill test formats, and arts periods vanish. The superintendent cites the scores as proof of improvement.",
                "prompt": "A second-order cybernetician evaluating this 'improvement' would argue what?",
                "choices": [
                    "The scores prove real improvement: standardized tests are objective and drill is effective pedagogy",
                    "The measurement system has reconfigured the system it measures (Campbell's Law): the district optimized the indicator, not learning — scores now measure test-preparation, and the superintendent's claim confuses the map (scores) with the territory (education); validate against independent, un-incentivized measures",
                    "The problem is teacher quality: replace the staff and scores will reflect real learning",
                    "More subjects should be tied to funding to spread the incentive evenly"
                ],
                "answer": 1,
                "why": "This is Campbell's Law in the wild: high-stakes indicators get corrupted by the pressures applied to them. The system under observation reorganized itself around the observer's instrument — curriculum narrowed to what the test samples. Scores remain 'true' as measurements of test-taking while becoming false as measurements of learning; only un-incentivized instruments can check the claim.",
                "hint": "The territory (learning) reshaped itself to flatter the map (scores). Which one is the superintendent reading?",
                "objectives": ["Apply Campbell's Law to high-stakes testing", "Distinguish indicator validity from goal achievement"],
                "mins": 12,
                "evidence": ["Names Campbell's Law and demands validation by un-incentivized measures"]
            },
            {
                "id": "cyb-second-sc4",
                "title": "The Self-Reference Survey",
                "domain_id": "second-order",
                "situation": "A company runs an engagement survey asking employees to rate, on a 1-5 scale, 'how much you trust this survey to remain anonymous.' The item scores 2.1. HR reports 'trust in the survey process is low' and commissions a follow-up survey on survey trust, with a cover letter promising anonymity.",
                "prompt": "What is the self-referential trap here, and what breaks it?",
                "choices": [
                    "There is no trap: low trust is a straightforward finding, and more surveying will diagnose it",
                    "The instrument measures its own credibility — a self-referential loop where distrust of the medium contaminates every message it carries, including the distrust reading itself; the escape is not another survey but a change of medium (e.g., trusted third-party interviews, verifiable anonymity mechanisms) that sits outside the loop",
                    "The trap is the 1-5 scale: switch to open text and the paradox dissolves",
                    "HR should simply assert anonymity more forcefully in the next cover letter"
                ],
                "answer": 1,
                "why": "Second-order paradox: the survey asks the system to evaluate the survey, so the reading is entangled with the instrument's own standing — a 2.1 may measure distrust of this survey specifically, or honest reporting through it; the instrument cannot separate the two. Another survey repeats the entanglement. Only an observation channel outside the loop (independent interviewers, structural anonymity guarantees) breaks the self-reference.",
                "hint": "Can a ruler measure its own accuracy? What observes the observer?",
                "objectives": ["Identify self-referential measurement paradoxes", "Prescribe an observation channel outside the loop"],
                "mins": 12,
                "evidence": ["Names the self-referential entanglement and proposes an independent channel"]
            },
            {
                "id": "cyb-second-sc5",
                "title": "The Ethics of the Model",
                "domain_id": "second-order",
                "situation": "A city pilots an algorithm that allocates building-inspection priority from historical violation data. The model sends inspectors overwhelmingly to one neighborhood — the same neighborhood historically over-inspected, hence over-represented in the data. Officials call the model 'objective because it is mathematical.'",
                "prompt": "What is the second-order ethical objection, stated precisely?",
                "choices": [
                    "There is none: mathematics cannot be biased, so the allocation is fair by definition",
                    "The model closes a self-fulfilling loop: past observation intensity shapes the data, the data shapes the model, the model directs future observation to the same places, confirming itself — the 'objectivity' claim hides that the observer's history is baked into the instrument; ethics requires auditing the loop, not just the math",
                    "The objection is only about accuracy: with more data the bias would vanish",
                    "The fix is to remove the neighborhood variable: blindness guarantees fairness"
                ],
                "answer": 1,
                "why": "Second-order cybernetics locates ethics in the observer-system relation: the model is not a neutral mirror but a participant that steers future observations to confirm its own past. 'Objective because mathematical' mistakes the map for the territory while hiding the loop. Removing one variable does not break the feedback; the ethical demand is to make the whole observation-allocation loop visible and contestable.",
                "hint": "Where did the training data come from? Who decided to look there first?",
                "objectives": ["Expose self-confirming observation loops in algorithmic systems", "Argue the ethical locus is the loop, not the equation"],
                "mins": 12,
                "evidence": ["Traces the data->model->inspection->data loop and demands loop-level auditing"]
            },
            {
                "id": "cyb-second-sc6",
                "title": "Participatory Design, Beer's Way",
                "domain_id": "second-order",
                "situation": "A hospital network is designing productivity metrics for nursing wards. The analytics team proposes deriving metrics from EHR timestamps alone. The nurses' union demands co-design of the metrics, citing Stafford Beer's work. The CFO worries co-design will let nurses 'choose easy metrics.'",
                "prompt": "How does second-order cybernetics (and Beer's practice) adjudicate this?",
                "choices": [
                    "Side with the CFO: the observed must not design the observation, or metrics lose objectivity",
                    "Side with the nurses: in second-order cybernetics the distinction between observer and observed is a choice, and viable systems need the measured to participate in defining the measure — Beer's teams built metrics with workers because ownership of the model is what makes regulation work; the safeguard is transparent, jointly-owned definitions, not exclusion",
                    "Compromise: let analysts design the metrics and nurses vote yes/no at the end",
                    "Abandon metrics: nursing cannot be measured without distortion"
                ],
                "answer": 1,
                "why": "Von Foerster's second-order move dissolves the observer/observed split: those inside the system are observers too. Beer put this into practice — viable regulation requires the regulated to own the model, because a metric imposed from outside becomes a target to game (Goodhart), while a jointly-defined metric becomes a shared instrument. The CFO's fear is answered by transparency of definitions, not by excluding the observed.",
                "hint": "Who has to live inside the metric? What happens when they had no hand in it?",
                "objectives": ["Justify participatory metric design from second-order principles", "Connect Beer's practice to Goodhart resistance"],
                "mins": 12,
                "evidence": ["Argues for co-designed, jointly-owned metrics citing observer/observed unity"]
            },
            {
                "id": "cyb-second-sc7",
                "title": "The Therapist in the System",
                "domain_id": "second-order",
                "situation": "A family therapist notices that whenever she asks the parents about their conflict, the teenage son's disruptive behavior spikes in the session — and the parents unite around managing him, dropping their own conflict. Her supervisor suggests the son's pathology is simply 'more severe than assessed.'",
                "prompt": "Apply Bateson's second-order insight to the therapy room itself.",
                "choices": [
                    "Accept the supervisor's view: escalate the son's individual treatment plan",
                    "Recognize the therapist as part of the circuit: her questions are inputs the family system processes — the son's escalation functions as negative feedback stabilizing the parents' conflict by redirecting it; the 'pathology' may be a property of the therapist-inclusive system, so she must vary her own interventions as experiments on the circuit she participates in",
                    "Exclude the son from sessions: remove the disruptive node to treat the parents cleanly",
                    "Record sessions for a second therapist to rate objectively from outside"
                ],
                "answer": 1,
                "why": "Bateson's cybernetic view of therapy treats the family-plus-therapist as one circuit: the son's symptom can be the system's homeostatic correction, triggered by the therapist's own input. There is no outside vantage — even a rater watches a recording of a system that included the first therapist. The disciplined move is to treat her interventions as experiments and read the circuit's response, including her place in it.",
                "hint": "Her question changed the room. What if the symptom is the system's answer to her?",
                "objectives": ["Include the observer in the system being analyzed", "Reframe symptoms as circuit functions"],
                "mins": 12,
                "evidence": ["Places the therapist inside the circuit and reads the symptom as systemic feedback"]
            }
        ],
        "modern-systems": [
            {
                "id": "cyb-modern-sc1",
                "title": "VSM Diagnosis: The Missing System 4",
                "domain_id": "modern-systems",
                "situation": "A 300-person logistics firm runs operations superbly (System 1) and coordinates daily work well (System 2), but strategic planning is just the CEO's gut feel, there is no market-intelligence function, and every 'strategy' is a reaction to the last crisis. Two agile competitors are eating its key accounts.",
                "prompt": "Diagnose with Beer's Viable System Model. What is missing and what is the prescription?",
                "choices": [
                    "System 3 (control) is missing: add more management layers to tighten operational control",
                    "System 4 (intelligence) is missing: the firm has no outward- and future-looking function scanning the environment and modeling futures; prescribe a dedicated intelligence capacity feeding the policy level, closing the 3-4 homeostat between present operations and future adaptation",
                    "System 5 (policy/identity) is missing: the CEO should write a mission statement",
                    "Nothing is missing: gut-feel strategy worked for twenty years, so the competitors' gains are temporary"
                ],
                "answer": 1,
                "why": "In VSM, System 4 looks outward and forward — environment scanning, modeling, future planning — and holds the homeostatic tension with System 3 (present operations). A firm with strong S1/S2 but no S4 is viable today and blind tomorrow: it can only react. The prescription is an institutionalized intelligence function, not a mission statement or more control layers.",
                "hint": "Which VSM system looks outward and forward? Who does that job here?",
                "objectives": ["Identify VSM System 4 and its function", "Diagnose its absence in an organization"],
                "mins": 12,
                "evidence": ["Names missing System 4 and prescribes an intelligence function feeding policy"]
            },
            {
                "id": "cyb-modern-sc2",
                "title": "Emergence at the Intersection",
                "domain_id": "modern-systems",
                "situation": "A city's new 'smart' intersection has perfect sensors, adaptive signals, and per-car optimization. Yet at rush hour a phantom jam forms with no accident, no bottleneck, no single cause — just stop-and-go waves. The vendor blames 'irrational drivers' and proposes stricter per-car control.",
                "prompt": "What is the complexity-thinking diagnosis?",
                "choices": [
                    "The vendor is right: driver irrationality is the residual cause, so control each car more tightly",
                    "The jam is emergent: stop-and-go waves arise from local car-following interactions (small delays amplifying through the platoon), a property of the interaction pattern, not of any car — the fix addresses coupling (e.g., smoothing flow, variable speed harmonization), not individual driver control",
                    "The sensors are miscalibrated: replace them and the waves vanish",
                    "Phantom jams are random and unmanageable; accept them"
                ],
                "answer": 1,
                "why": "Emergence means the pattern exists at the system level and is not present in — or fixable through — the parts: no driver intends a wave, yet waves reliably form from delayed local responses amplifying down the line. Tighter per-car control misunderstands the level of causation; harmonizing the coupling between cars (speed smoothing, consistent headways) targets the level where the pattern lives.",
                "hint": "No one causes the wave, yet the wave always forms. What level is that?",
                "objectives": ["Define emergence with a traffic example", "Target interventions at the interaction level"],
                "mins": 10,
                "evidence": ["Names emergence and prescribes coupling-level intervention"]
            },
            {
                "id": "cyb-modern-sc3",
                "title": "Diagnosing a Non-Viable Startup",
                "domain_id": "modern-systems",
                "situation": "A health-tech startup has brilliant engineers (S1) shipping features weekly, but: teams constantly collide over priorities (no S2), the founders 'control' by shouting in Slack (no S3), nobody studies competitors or regulation (no S4), and each founder has a different vision of what the company is (no S5). Burn rate gives them 8 months.",
                "prompt": "Using VSM viability criteria, what is the verdict and the triage order?",
                "choices": [
                    "Viable: strong S1 engineering is sufficient; the rest is big-company bureaucracy",
                    "Not currently viable: viability requires all five systems with recursive structure; triage by survival logic — first S5 (identity: what are we, decided jointly), then S3/S2 (control and coordination to stop the collisions), then S4 (intelligence before the market moves), while protecting S1 delivery throughout",
                    "Not viable: shut down immediately, since VSM gaps are unfixable in startups",
                    "Viable if they hire a COO: one hire installs S2 through S5 automatically"
                ],
                "answer": 1,
                "why": "Beer is categorical: viability needs all five functions (they can be roles, not departments). The triage order follows dependency: S5 identity must be settled before S3 can control toward anything; S2/S3 stop the internal collisions bleeding cash; S4 must come before the runway ends because adaptation takes time. A COO hire alone does not conjure identity or intelligence functions.",
                "hint": "All five systems are required. Which missing piece makes the others un-aimable?",
                "objectives": ["Apply VSM viability criteria", "Sequence a turnaround by systemic dependency"],
                "mins": 12,
                "evidence": ["Declares non-viability and orders triage S5 -> S3/S2 -> S4"]
            },
            {
                "id": "cyb-modern-sc4",
                "title": "Leverage Points in the River",
                "domain_id": "modern-systems",
                "situation": "An industrial river is polluted. Past interventions: fines for dumping (weakly enforced), a cleanup fund (spent on studies), public awareness ads (no behavior change). A systems team maps the full structure: factory cost incentives, weak monitoring, regulatory capture, and a cultural norm that 'the river has always been dirty.'",
                "prompt": "Using Meadows' leverage-points hierarchy, where is the highest-leverage intervention among the options?",
                "choices": [
                    "Bigger fines: strengthen the existing negative-feedback penalty loop",
                    "More monitoring buoys: improve the information flow about pollution levels",
                    "Change the goal of the system: rewrite discharge permits and the regulatory mandate from 'manage acceptable pollution' to 'restore the river,' enforced by independent monitoring — goals outrank feedback strength and information flow in Meadows' hierarchy",
                    "A larger cleanup fund: more resources for the same structure"
                ],
                "answer": 2,
                "why": "Meadows ranked leverage points: changing system goals outranks tweaking feedback loops, which outranks information flows, which outrank parameters like fine sizes. Fines and funds adjust parameters of a system whose goal tolerates pollution; rewriting the goal to restoration re-aims every loop at once — the deepest practical intervention short of paradigm change.",
                "hint": "Meadows' hierarchy: goals beat loops, loops beat information, information beats parameters. Where do fines sit?",
                "objectives": ["Rank interventions by Meadows' leverage-points hierarchy", "Distinguish goal change from parameter tweaking"],
                "mins": 12,
                "evidence": ["Ranks goal-change above fines/monitoring and prescribes a restoration mandate"]
            },
            {
                "id": "cyb-modern-sc5",
                "title": "Path Dependence in the Keyboard",
                "domain_id": "modern-systems",
                "situation": "Your team designs a chorded keyboard that tests 40% faster than QWERTY with one week of training. Adoption is zero: employers test typing speed on QWERTY, training programs teach QWERTY, and everyone you hire already knows QWERTY. An investor calls the market 'irrational' for rejecting the superior design.",
                "prompt": "What is the systems diagnosis of this 'irrationality'?",
                "choices": [
                    "The market is irrational: superior technology always wins, so persist with marketing",
                    "Path dependence with lock-in: QWERTY's dominance is a self-reinforcing historical equilibrium (installed base -> training -> hiring filters -> installed base), not a live efficiency contest; the superior artifact loses because the system selects for compatibility with its own history, and displacement needs a coordinated transition, not a better device alone",
                    "The product is actually inferior: 40% faster in tests means nothing",
                    "Regulators should ban QWERTY to force the transition"
                ],
                "answer": 1,
                "why": "Complex systems exhibit hysteresis: history constrains the present through reinforcing feedback (every QWERTY typist raises the value of QWERTY training, which produces more QWERTY typists). Calling this 'irrational' mistakes a systems property for a decision error. The leverage is not a better keyboard but a transition path — e.g., dual-mode devices, institutional retraining deals — that unwinds the lock-in loop.",
                "hint": "The system is not choosing keyboards; it is reproducing its own past. What loop does that?",
                "objectives": ["Explain path dependence and lock-in", "Design transition strategies for locked-in systems"],
                "mins": 10,
                "evidence": ["Names the self-reinforcing lock-in loop and prescribes a coordinated transition path"]
            },
            {
                "id": "cyb-modern-sc6",
                "title": "Operational Closure in the Newsroom",
                "domain_id": "modern-systems",
                "situation": "A newspaper's investigative desk keeps producing stories the audience demonstrably wants (high readership, awards), yet the publisher keeps cutting its budget to fund clickbait verticals. The desk chief argues 'the market has spoken' in their favor. The publisher replies that the paper's identity is 'audience scale,' and investigations don't scale.",
                "prompt": "Apply Luhmann/autopoiesis: what is actually deciding here?",
                "choices": [
                    "The market: readership numbers should decide, and the chief is right",
                    "The organization's operational closure: the paper reproduces itself through its own communications (its identity code 'audience scale'), which filters what counts as a valid reason — external facts like awards perturb the system but the system decides what the perturbation means; the fight is over the code, not the facts",
                    "The publisher's personal bias: replace the publisher and the logic changes",
                    "Journalism ethics: investigations are intrinsically more valuable, so fund them regardless"
                ],
                "answer": 1,
                "why": "Autopoietic systems are operationally closed: they process perturbations only through their own internal distinctions. The publisher's 'audience scale' code determines what counts as evidence, so the desk's awards literally cannot register as reasons within that code. The chief's market argument fails because it speaks a distinction the system does not use; change requires contesting the code itself.",
                "hint": "The same facts, two different verdicts. What filter sits between fact and verdict?",
                "objectives": ["Explain operational closure", "Locate organizational conflict at the level of codes, not facts"],
                "mins": 12,
                "evidence": ["Names operational closure and reframes the dispute as a contest over the system's code"]
            },
            {
                "id": "cyb-modern-sc7",
                "title": "Requisite Variety in Regulation",
                "domain_id": "modern-systems",
                "situation": "A financial regulator oversees 40 banks with 12 examiners using a single standardized checklist. Banks innovate rapidly (crypto custody, AI credit models, embedded finance); every recent failure involved a product the checklist never mentioned. The regulator's plan is a longer checklist.",
                "prompt": "What does Ashby prescribe for the regulator's design?",
                "choices": [
                    "A longer checklist: more items equal more regulatory variety",
                    "Requisite variety at the regulator: 12 examiners with one checklist cannot absorb the variety of 40 innovating banks — the regulator needs variety amplifiers (specialist teams, industry secondments, suptech analytics) and cannot get there by lengthening a single list; alternatively it must attenuate bank variety (constrain permitted activities)",
                    "Deregulate: variety matching is impossible, so abandon oversight",
                    "Fine failures harder: deterrence substitutes for understanding"
                ],
                "answer": 1,
                "why": "Ashby gives exactly two moves: amplify regulator variety or attenuate system variety. A longer checklist is neither — it is the same low-variety instrument with more rows. Real amplification means specialist expertise and analytical tooling that generate genuinely new distinctions; real attenuation means narrowing what banks may do. Deterrence and deregulation dodge the variety equation entirely.",
                "hint": "Only variety absorbs variety. Does a longer checklist create new distinctions, or more of the same?",
                "objectives": ["Apply requisite variety to regulatory design", "Distinguish variety amplification from checklist extension"],
                "mins": 12,
                "evidence": ["Prescribes variety amplifiers or activity attenuation, rejecting checklist lengthening"]
            },
            {
                "id": "cyb-modern-sc8",
                "title": "The Intervention That Backfired",
                "domain_id": "modern-systems",
                "situation": "A city, facing a rat problem, pays a bounty per rat tail. Within months, tail submissions soar — and the rat population grows: residents begin breeding rats for the bounty. The program is canceled, the breeders release their stock, and the infestation is worse than before. (The classic 'cobra effect.')",
                "prompt": "What is the systems lesson for designing the next intervention?",
                "choices": [
                    "Bounties never work: abandon incentive-based interventions entirely",
                    "The intervention created a new reinforcing loop (bounty -> breeding -> more tails -> more bounty) that the designers never mapped; the lesson is to model the incentive structure as part of the system — including second-order responses — before intervening, and to pilot with circuit-breakers (caps, verification, sunset clauses)",
                    "The bounty was too low: a higher price would have outbid the breeders",
                    "Residents are dishonest: screen participants for character before the next program"
                ],
                "answer": 1,
                "why": "The designers modeled only the intended loop (bounty -> fewer rats) and ignored the system they were intervening in — rational agents who optimize the reward, not the goal. Every intervention is a perturbation of an adaptive system; the discipline is to map the response loops first, assume the system will find the reward-maximizing path, and build in circuit-breakers. Character screening and price tweaks miss the structural point.",
                "hint": "They paid for tails, not for fewer rats. What did the system optimize?",
                "objectives": ["Explain the cobra effect as unmodeled response loops", "Design interventions with circuit-breakers"],
                "mins": 10,
                "evidence": ["Names the breeding reinforcing loop and prescribes pre-modeled, circuit-broken pilots"]
            }
        ],
        "exam-strategy": [
            {
                "id": "cyb-exam-sc1",
                "title": "Planning the Feedback Essay",
                "domain_id": "exam-strategy",
                "situation": "Your certification exam includes a 45-minute essay: 'Explain how negative and positive feedback differ, using one engineered and one social example of each.' You have read widely but tend to write everything you know in the order you remember it.",
                "prompt": "What essay plan maximizes marks under time pressure?",
                "choices": [
                    "Write continuously from memory: coverage matters more than structure, and planning wastes writing time",
                    "Spend 8 minutes planning a thesis-led structure — definitions with the loop anatomy (sensor-comparator-effector), then a 2x2 grid (negative/positive x engineered/social) with one worked example per cell, then a synthesis paragraph on delays and loop sign; write to the plan",
                    "Open with a long historical preamble on Wiener to demonstrate breadth, then fit examples into remaining time",
                    "List every feedback example you know: examiners reward quantity of examples"
                ],
                "answer": 1,
                "why": "Examiners mark structure, precision, and comparative analysis — a planned 2x2 grid guarantees all four required cells are addressed with the loop anatomy made explicit, while the synthesis paragraph captures higher-order marks. Unplanned writing drifts into preamble and drops cells; example-dumping without analysis scores low on every rubric.",
                "hint": "The question asks for a comparison across two dimensions. What structure guarantees you hit all four cells?",
                "objectives": ["Plan a comparative essay under time constraint", "Use grid structures for multi-dimensional questions"],
                "mins": 10,
                "evidence": ["Produces a timed plan with thesis, 2x2 grid, and synthesis paragraph"]
            },
            {
                "id": "cyb-exam-sc2",
                "title": "Source Analysis: The Wiener Quote",
                "domain_id": "exam-strategy",
                "situation": "The exam gives an unseen source: Wiener (1954) warning that automated systems may 'reduce the human being to the status of a mere relay' if designers cede judgment to machines. The question: 'Analyze this source's argument and its limits.'",
                "prompt": "What does a strong source analysis do with this passage?",
                "choices": [
                    "Summarize it: restate the warning in your own words and agree with it",
                    "Dissect it: identify the claim (automation displaces human judgment), the mechanism Wiener implies (feedback loops that route around operators), the historical context (postwar computing, his AA predictor work), and the limits (Wiener writes before modern HCI safeguards; his warning is about design choices, not technological inevitability) — then evaluate",
                    "Dismiss it: a 1954 source cannot speak to modern systems",
                    "Quote it at length: the source speaks for itself and long quotation shows engagement"
                ],
                "answer": 1,
                "why": "Source analysis marks come from claim-mechanism-context-limits dissection, not summary or quotation. Naming Wiener's implied mechanism (loops routing around operators) and his context (predictor work, early computing) shows understanding; stating the limits (pre-HCI, design-contingent rather than inevitable) shows evaluation. Agreement without analysis scores minimally.",
                "hint": "Claim, mechanism, context, limits — then your evaluation. Which option does all four?",
                "objectives": ["Dissect a primary source into claim, mechanism, context, limits", "Evaluate rather than summarize"],
                "mins": 12,
                "evidence": ["Identifies claim, mechanism, context, and limits of the Wiener passage"]
            },
            {
                "id": "cyb-exam-sc3",
                "title": "Constructing the Argument: Regulation",
                "domain_id": "exam-strategy",
                "situation": "Essay prompt: 'Is more regulation of algorithmic systems always better? Argue your position using cybernetic concepts.' Your instinct is to argue 'yes' with three supporting points and finish.",
                "prompt": "What argument construction earns the top band?",
                "choices": [
                    "Three supporting points for 'yes,' stated forcefully: one-sided conviction impresses examiners",
                    "A dialectical structure: thesis (requisite variety demands regulatory capacity), antithesis (Ashby also permits attenuating system variety; Goodhart warns metrics-based regulation corrupts), synthesis (design regulation as adaptive feedback — requisite variety plus circuit-breakers and sunset clauses — rather than 'more' as a scalar)",
                    "A neutral survey of opinions with no position: balance is safer than argument",
                    "A personal anecdote about an algorithmic harm, extended for the full essay"
                ],
                "answer": 1,
                "why": "Top-band essays argue through objection: the thesis-antithesis-synthesis structure demonstrates that cybernetic concepts cut both ways (variety can be amplified or attenuated; measurement corrupts). The synthesis — adaptive, feedback-designed regulation — is a position earned by surviving counterargument, which is exactly what the rubric rewards over one-sided assertion or fence-sitting.",
                "hint": "The strongest position is the one that has defeated its best objection. Where is the objection?",
                "objectives": ["Build dialectical essay arguments", "Apply cybernetic concepts on both sides of a debate"],
                "mins": 12,
                "evidence": ["Outlines thesis-antithesis-synthesis with cybernetic concepts on both sides"]
            },
            {
                "id": "cyb-exam-sc4",
                "title": "Time Management Across Sections",
                "domain_id": "exam-strategy",
                "situation": "The exam is 3 hours: Section A (10 short answers, 40 marks), Section B (4 scenarios, 40 marks), Section C (1 essay, 20 marks). In mocks you spend 90 minutes perfecting Section A, rush B, and write C in 15 panicked minutes.",
                "prompt": "What is the cybernetically sound time plan — and why is it cybernetic?",
                "choices": [
                    "Work in order and let each section take what it needs: quality on A banks marks early",
                    "Allocate by marks per minute (A: 60 min, B: 80 min, C: 40 min), enforce section deadlines as a negative-feedback control on your own progress, and keep 10 minutes of buffer as damping against overruns — you are regulating a system (yourself) with feedback, not hoping",
                    "Start with C while fresh: the essay needs the best energy regardless of marks",
                    "Skip planning: rigid schedules increase anxiety and lower performance"
                ],
                "answer": 1,
                "why": "Marks per minute is the setpoint; section deadlines are the comparator; moving on when the deadline hits is the negative-feedback correction that keeps the whole exam near target. Your mock pattern is an undamped loop — perfectionism on A is overshoot that starves C. The buffer is damping against disturbances. Self-regulation is applied cybernetics.",
                "hint": "You are a control system with 180 minutes of actuator time. What is your setpoint per section?",
                "objectives": ["Allocate exam time by marks per minute", "Use feedback-control framing for self-regulation"],
                "mins": 8,
                "evidence": ["Produces a marks-weighted schedule with enforced section deadlines and buffer"]
            },
            {
                "id": "cyb-exam-sc5",
                "title": "Interdisciplinary Synthesis: Shannon Meets Bateson",
                "domain_id": "exam-strategy",
                "situation": "Essay prompt: 'Shannon's information theory and Bateson's ecology of mind both claim to be about 'information,' yet they seem incompatible. Discuss.' You understand each thinker separately but have never connected them.",
                "prompt": "What synthesis resolves the apparent incompatibility?",
                "choices": [
                    "Declare one of them wrong: Shannon's mathematics refutes Bateson's metaphors",
                    "Show they answer different questions at different levels: Shannon quantifies syntactic uncertainty-reduction for engineering channels (deliberately excluding meaning); Bateson theorizes pragmatic difference-that-makes-a-difference in living systems — the synthesis is hierarchical: Shannon's measure operates within channels that Bateson's differences select as relevant, and cybernetics needs both levels",
                    "Claim they say the same thing in different words: information is information",
                    "Avoid the comparison: discuss each in separate paragraphs with no connection"
                ],
                "answer": 1,
                "why": "The incompatibility dissolves once levels are distinguished: Shannon's theory is syntactic and engineering-scoped by design; Bateson's is pragmatic and ecological. They are not rivals but layered — Bateson's differences determine which signals are worth sending through Shannon's channels. The synthesis paragraph that states this hierarchy is where the synthesis marks live; parallel summaries without connection score low.",
                "hint": "Syntax vs pragmatics; engineering channel vs living system. Are these competitors or layers?",
                "objectives": ["Synthesize two thinkers across disciplinary levels", "Resolve apparent contradictions via level distinction"],
                "mins": 12,
                "evidence": ["States the syntactic/pragmatic layering and the channel-selection synthesis"]
            },
            {
                "id": "cyb-exam-sc6",
                "title": "Defining Terms Precisely",
                "domain_id": "exam-strategy",
                "situation": "A short-answer question asks: 'Define negative feedback.' You write: 'Negative feedback is when a system gets bad feedback and corrects itself.' The mock marker gives 1 of 4 marks with the comment 'colloquial.'",
                "prompt": "What definition earns full marks, and why did yours fail?",
                "choices": [
                    "Yours was fine: the marker was harsh, and 'bad feedback' is standard usage",
                    "Full marks need the technical anatomy: 'Negative feedback is a control arrangement in which a sensed output is compared against a reference (setpoint) and the resulting error signal drives an effector to oppose the deviation, stabilizing the system near the reference.' Yours failed because 'bad feedback' uses the colloquial sense of feedback (criticism) instead of the cybernetic sense (return of output to input)",
                    "Add an example: 'like a thermostat' — examples substitute for definitions",
                    "Make it longer: length correlates with marks"
                ],
                "answer": 1,
                "why": "Technical definitions must name the mechanism: sensed output, reference comparison, error-driven correction opposing deviation. Your version imported the everyday meaning of 'feedback' as criticism ('bad feedback'), which is precisely the colloquialism markers penalize. In cybernetics exams, every key term must be defined in loop-anatomy language, with examples illustrating, never substituting.",
                "hint": "In cybernetics, 'feedback' is not criticism. What is it, mechanically?",
                "objectives": ["Write technical definitions in loop-anatomy language", "Avoid colloquial senses of technical terms"],
                "mins": 8,
                "evidence": ["Produces a sensor-comparator-effector definition of negative feedback"]
            },
            {
                "id": "cyb-exam-sc7",
                "title": "Compare and Contrast: Wiener vs von Bertalanffy",
                "domain_id": "exam-strategy",
                "situation": "Prompt: 'Compare Wiener's cybernetics with von Bertalanffy's General Systems Theory.' Your draft lists five facts about Wiener, then five facts about von Bertalanffy, in two separate blocks.",
                "prompt": "How do you convert this into a genuine comparison?",
                "choices": [
                    "It is already a comparison: placing two accounts side by side is what 'compare' means",
                    "Restructure around comparative axes, with both thinkers addressed on each axis: (1) central concept — feedback/control vs open systems/wholeness; (2) system boundary — closed-loop regulation vs environmental exchange; (3) method — mechanism modeling vs holism and equifinality; (4) relation — complementary, with GST bounding the system cybernetics regulates; conclude with the synthesis, not two summaries",
                    "Pick a winner: argue Wiener's framework supersedes von Bertalanffy's",
                    "Add more facts to each block: depth of coverage is what matters"
                ],
                "answer": 1,
                "why": "Examiners distinguish description (two blocks) from comparison (shared axes with both thinkers evaluated on each). The axis structure forces relational judgments — where they converge, diverge, and complement — which is where analysis marks are awarded. The synthesis conclusion (GST bounds the system; cybernetics regulates it) converts comparison into insight.",
                "hint": "Two blocks describe. What structure forces you to relate them, point by point?",
                "objectives": ["Structure compare-and-contrast answers on shared axes", "Conclude comparisons with synthesis"],
                "mins": 10,
                "evidence": ["Reorganizes the answer into comparative axes with a synthesis conclusion"]
            },
            {
                "id": "cyb-exam-sc8",
                "title": "Self-Testing Like a Cybernetician",
                "domain_id": "exam-strategy",
                "situation": "Two weeks before the exam, you have reread all your notes three times and feel fluent. A study partner suggests closing the notes and doing timed past-paper scenarios instead. Rereading feels productive; blank-page recall feels awful.",
                "prompt": "What does the cybernetic view of learning prescribe?",
                "choices": [
                    "Keep rereading: fluency indicates the knowledge is stored and ready",
                    "Switch to retrieval practice: rereading is open-loop (no error signal), while blank-page recall closes the feedback loop — each attempt generates an error signal (what you could not produce) that directs the next study correction; fluency during rereading is a sensor illusion, like a thermostat reading vent air",
                    "Split the difference: alternate pages of rereading with glances at past papers",
                    "Memorize model answers: reproduction is what exams test"
                ],
                "answer": 1,
                "why": "Learning is a control loop: rereading provides no error signal, so the system cannot correct — fluency is the feeling of recognition, not the capacity for production (the sensor reads the wrong variable). Retrieval practice closes the loop: failed recall is the error signal that tells the next study session what to fix. The discomfort is the loop working.",
                "hint": "Which study method gives you an error signal? A loop without error feedback cannot correct.",
                "objectives": ["Justify retrieval practice via feedback-loop reasoning", "Distinguish recognition fluency from recall capacity"],
                "mins": 8,
                "evidence": ["Explains rereading as open-loop and prescribes closed-loop retrieval practice"]
            }
        ],
        "cybernetics-in-tech": [
            {
                "id": "cyb-tech-sc1",
                "title": "Gradient Descent as a Feedback Loop",
                "domain_id": "cybernetics-in-tech",
                "situation": "Your ML team trains a vision model. Training loss falls smoothly; validation loss falls, then rises while training loss keeps falling. The team celebrates the low training loss and ships the model. In production, accuracy is poor on new images.",
                "prompt": "Read training as nested feedback loops. What went wrong structurally?",
                "choices": [
                    "Nothing: low training loss is the objective, and production data is just harder",
                    "The team optimized the inner loop (training loss) while ignoring the outer loop's error signal (validation loss rising = overfitting): the validation loop is the negative feedback that checks generalization, and shipping overrode it — the fix is to let the outer loop govern (early stopping, regularization) rather than celebrating the inner loop's number",
                    "The learning rate was wrong: retune it and the problem disappears",
                    "More training data is the only fix: overfitting is purely a data-volume problem"
                ],
                "answer": 1,
                "why": "Training is nested loops: gradient descent minimizes training loss (inner), while validation monitors generalization (outer). A rising validation loss is the outer loop's error signal — the model memorizing rather than learning. Treating the inner loop's number as success while the outer loop alarms is exactly the nested-loop pathology: the reference that matters (generalization) was overridden by the one that flatters (training loss).",
                "hint": "Two loops, two error signals. Which one measures what production will see?",
                "objectives": ["Map ML training onto nested feedback loops", "Use validation as the governing outer loop"],
                "mins": 12,
                "evidence": ["Identifies validation loss as the outer-loop error signal and prescribes early stopping"]
            },
            {
                "id": "cyb-tech-sc2",
                "title": "Autoscaling: Control Theory in DevOps",
                "domain_id": "cybernetics-in-tech",
                "situation": "Your autoscaler adds servers when CPU exceeds 70% and removes them below 30%, checking every 5 minutes. During a flash sale, servers thrash: added, removed, added — each cycle takes 8 minutes to warm up, so capacity oscillates and checkout latency spikes. The team proposes checking every 30 seconds for 'faster control.'",
                "prompt": "What is the control-theoretic diagnosis and fix?",
                "choices": [
                    "Faster checks: 30-second polling tightens the loop and will stabilize it",
                    "Delay-induced oscillation: the 8-minute warmup delay means corrections arrive out of phase, and faster polling without accounting for in-flight capacity just adds gain to an already oscillating loop — fix with hysteresis (wider deadband), cooldown periods that respect the warmup delay, and predictive (feedforward) scaling from the sale schedule",
                    "Disable downscaling: never remove servers and oscillation is impossible",
                    "The thresholds are wrong: 70/30 should be 90/10"
                ],
                "answer": 1,
                "why": "This is the hiring-oscillation pattern in silicon: actuation delay (warmup) makes fast corrections arrive out of phase, and 30-second polling increases loop gain without fixing the phase problem — classic recipe for worse oscillation. The control-theoretic fixes are damping (hysteresis, cooldowns matched to the delay) and feedforward (scale from the known sale schedule before the disturbance hits).",
                "hint": "Eight-minute warmup vs five-minute checks: corrections keep landing out of phase. Does polling faster fix phase?",
                "objectives": ["Diagnose delay-induced oscillation in autoscaling", "Apply hysteresis and feedforward as fixes"],
                "mins": 12,
                "evidence": ["Names delay-induced oscillation and prescribes cooldowns plus feedforward scaling"]
            },
            {
                "id": "cyb-tech-sc3",
                "title": "TCP Congestion Control: The Internet's Thermostat",
                "domain_id": "cybernetics-in-tech",
                "situation": "A junior engineer asks why TCP uses 'additive increase, multiplicative decrease' (AIMD): growing the send window by 1 packet per round trip, but halving it on packet loss. 'Why not just probe aggressively and back off a little?'",
                "prompt": "Explain AIMD as a feedback control design. Why is the asymmetry correct?",
                "choices": [
                    "It is historical accident: aggressive probing would work just as well",
                    "AIMD is a distributed negative-feedback loop: gentle probing (additive increase) avoids overshooting shared capacity, while sharp backoff (multiplicative decrease) corrects congestion fast when the error signal (loss) appears — the asymmetry matches the costs: overshoot harms everyone sharing the link, so exploration is cautious and correction is decisive; this yields fairness and stability without central control",
                    "Halving is too timid: back off by 10% for efficiency",
                    "Increase should be multiplicative too: symmetric control is mathematically cleaner"
                ],
                "answer": 1,
                "why": "Packet loss is the error signal in TCP's decentralized control loop; every sender runs the same loop with no coordinator. Additive increase probes for available capacity without violent overshoot; multiplicative decrease sheds load fast enough to drain queues before collapse. Symmetric or aggressive variants oscillate or starve — AIMD's asymmetry is what makes thousands of independent loops converge on fair, stable sharing.",
                "hint": "Loss is the error signal. Should you explore gently or violently when the resource is shared?",
                "objectives": ["Explain AIMD as decentralized negative feedback", "Justify the increase/decrease asymmetry"],
                "mins": 10,
                "evidence": ["Describes loss as error signal and justifies cautious probing with decisive backoff"]
            },
            {
                "id": "cyb-tech-sc4",
                "title": "Observability as Organizational Nervous System",
                "domain_id": "cybernetics-in-tech",
                "situation": "A platform team has exhaustive metrics, logs, and traces — yet incidents still take 45 minutes to detect because nobody watches the dashboards, alerts route to a mailing list nobody reads, and postmortems are filed unread. Leadership proposes buying a more powerful observability platform.",
                "prompt": "What is the cybernetic diagnosis of this observability failure?",
                "choices": [
                    "Tooling insufficiency: a more powerful platform with AI insights will close the gap",
                    "The sensing exists but the loop is open: data with no comparator (alert thresholds tied to user-facing objectives), no effector (a responder with authority and a runbook), and no learning arm (postmortems that change the system) is not feedback — it is unprocessed variety; the fix wires sensor->comparator->effector->learning before buying anything",
                    "Engineers need dashboard-watching shifts: the problem is staffing, not loops",
                    "45 minutes is acceptable: distributed systems are inherently slow to diagnose"
                ],
                "answer": 1,
                "why": "Cybernetically, observation is only the sensor arm; feedback requires the full loop — comparator (thresholds against service objectives), effector (empowered responders), and a learning loop (postmortems that alter the system). Unwatched dashboards are open-loop sensing: variety collected, none of it regulating. A new platform adds sensors to a loop that was never closed.",
                "hint": "Sensors without comparators and effectors are just expensive thermometers. Where does the signal go?",
                "objectives": ["Distinguish sensing from closed-loop observability", "Wire the full detect-decide-act-learn loop"],
                "mins": 10,
                "evidence": ["Diagnoses an open loop and prescribes comparator, effector, and learning arms"]
            },
            {
                "id": "cyb-tech-sc5",
                "title": "The Recommender's Positive Feedback",
                "domain_id": "cybernetics-in-tech",
                "situation": "A video platform's recommender optimizes watch time. Analytics show users' feeds narrowing over months: each click trains the model toward similar content, which crowds out alternatives, which makes future clicks even more concentrated. Creators complain the system 'decides what succeeds.' The PM says the algorithm 'just reflects user preferences.'",
                "prompt": "What is the precise cybernetic objection to 'just reflects preferences'?",
                "choices": [
                    "There is none: revealed preferences are preferences, and optimization is neutral",
                    "The system is a runaway positive-feedback loop, not a mirror: clicks -> training signal -> narrower recommendations -> narrower clicks — the 'preference' being measured is partly produced by the measurement instrument itself (second-order effect), so the loop amplifies its own outputs and calls them user choice; the PM confuses a self-confirming circuit with a neutral reflection",
                    "The problem is insufficient data: more diverse training data would fix it without loop analysis",
                    "Users should take responsibility for their clicks: the system is fine"
                ],
                "answer": 1,
                "why": "A mirror does not change what it reflects; this loop does — each recommendation shapes the click distribution that trains the next recommendation, so 'preferences' are co-produced by the observer (the algorithm). Positive feedback then concentrates the distribution until the system converges on a narrow attractor. Calling this neutral reflection misses that the instrument manufactures the phenomenon it claims to measure.",
                "hint": "Does the recommendation change the clicks it will later learn from? Then it is not a mirror.",
                "objectives": ["Identify positive feedback in recommender systems", "Expose the second-order co-production of 'preferences'"],
                "mins": 12,
                "evidence": ["Traces the clicks->model->recommendations->clicks loop and rejects the mirror claim"]
            },
            {
                "id": "cyb-tech-sc6",
                "title": "Canary Deploys as Controlled Experiment",
                "domain_id": "cybernetics-in-tech",
                "situation": "Your team deploys a rewritten payment service to 100% of traffic at once. It fails under a traffic pattern staging never produced, and rollback takes 40 minutes of lost revenue. The postmortem proposes 'more staging environments.'",
                "prompt": "What is the cybernetic case for canary deployment instead?",
                "choices": [
                    "Canaries are just slower: the real fix is better staging that perfectly mirrors production",
                    "Ashby's variety argument: staging can never contain production's full variety, so the canary treats production as the experiment — a small, reversible probe (1% traffic) with tight feedback (error-rate comparator) and a fast effector (automatic rollback) turns deployment into a controlled feedback loop instead of an open-loop bet",
                    "Canaries double the infrastructure cost, so they are only for large companies",
                    "The team should deploy at low-traffic hours instead: timing replaces experimentation"
                ],
                "answer": 1,
                "why": "No staging environment can match production's variety (Ashby: only variety absorbs variety), so big-bang deploys are open-loop — full commitment with no error signal until damage is done. The canary closes the loop: minimal exposure as the probe, real user traffic as the sensor, error budgets as the comparator, automated rollback as the effector. 'More staging' tries to perfect the model; the canary instruments reality instead.",
                "hint": "Staging is a model of production. What does Ashby say about a low-variety model regulating a high-variety reality?",
                "objectives": ["Justify canary deploys via requisite variety", "Design deployment as a closed feedback loop"],
                "mins": 10,
                "evidence": ["Frames the canary as probe-sensor-comparator-effector loop against staging's variety gap"]
            },
            {
                "id": "cyb-tech-sc7",
                "title": "Feature Flags and Requisite Variety",
                "domain_id": "cybernetics-in-tech",
                "situation": "A SaaS product serves hospitals, schools, and factories from one codebase. Each customer segment demands different behavior, and the release train ships one-size-fits-all updates that anger two segments at a time. Engineering proposes maintaining three separate forks.",
                "prompt": "How do feature flags answer this with cybernetic reasoning?",
                "choices": [
                    "They don't: three forks are cleaner, and flags create technical debt",
                    "Requisite variety: one release pipeline (low regulator variety) cannot absorb three segments' behavioral variety without either forking (tripling maintenance variety-cost) or flags — flags amplify the single pipeline's variety by making behavior conditional at runtime, matching segment variety without multiplying codebases",
                    "Flags are only for A/B testing: using them for segmentation is misuse",
                    "The segments should adapt to the product: reduce customer variety instead"
                ],
                "answer": 1,
                "why": "Ashby's law frames it exactly: the deployable system's behavioral variety must match the environment's demand variety. Forks buy variety at the cost of triplicated maintenance; one-size-fits-all starves variety and angers segments. Feature flags are a variety amplifier — one artifact, many behaviors — achieving requisite variety at far lower cost than forks.",
                "hint": "Three segments, one pipeline. How do you multiply the pipeline's behavioral variety without multiplying the codebase?",
                "objectives": ["Apply requisite variety to release engineering", "Justify feature flags as variety amplifiers"],
                "mins": 10,
                "evidence": ["Frames flags as variety amplifiers matching segment variety"]
            },
            {
                "id": "cyb-tech-sc8",
                "title": "Chaos Engineering as Variety Injection",
                "domain_id": "cybernetics-in-tech",
                "situation": "A fintech's disaster-recovery plan has never been tested; the runbook assumes the failover database is current and the team remembers the procedure. The CTO calls chaos engineering 'reckless sabotage' and prefers the untested plan. Last quarter a real outage exposed a stale failover and the runbook failed at step 3.",
                "prompt": "What is the cybernetic defense of chaos engineering here?",
                "choices": [
                    "There is none: deliberately breaking production is never defensible",
                    "Controlled variety injection: an untested recovery plan is a regulator whose variety is assumed, not demonstrated — chaos experiments inject measured disturbances in controlled conditions, generating the error signals that prove (or disprove) the recovery loop before reality does it catastrophically; the 'reckless' option is trusting an open-loop assumption",
                    "It is only defensible with a full staging replica: never in production",
                    "The runbook just needs clearer writing: documentation quality was the failure"
                ],
                "answer": 1,
                "why": "A recovery plan is a feedback loop that has never received feedback — its corrective capacity is a hypothesis. Chaos engineering closes that loop deliberately: injected faults are test disturbances, and the recovery response is the measured output. The blast radius is controlled precisely so the error signal arrives in safe conditions. Trusting the untested plan is the genuinely open-loop gamble, as the quarter's outage demonstrated.",
                "hint": "A recovery loop that has never run is a hypothesis. How do you test a hypothesis safely?",
                "objectives": ["Defend chaos engineering as feedback-loop testing", "Distinguish controlled disturbance from recklessness"],
                "mins": 10,
                "evidence": ["Frames chaos experiments as test disturbances validating the recovery loop"]
            }
        ],
        "case-studies": [
            {
                "id": "cyb-case-sc1",
                "title": "Three Mile Island: The Light That Lied",
                "domain_id": "case-studies",
                "situation": "On March 28, 1979, a pilot-operated relief valve at Three Mile Island stuck open after a routine shutdown. In the control room, the indicator light for the valve showed only that the close command had been sent (solenoid de-energized) — not the valve's actual position. Operators, trusting the light, believed the valve was shut while coolant escaped for over two hours; they throttled emergency cooling because a pressurizer level gauge misleadingly read high.",
                "prompt": "Analyze this through cybernetic lenses. What failed?",
                "choices": [
                    "Operator incompetence: better-trained operators would have ignored the misleading instruments",
                    "A feedback architecture failure: the control room's sensors reported commands, not states — the loop's feedback path carried the system's intentions rather than reality, so the comparator (operators) corrected against a false model; compounded by a mental model (pressurizer level = coolant inventory) that the actual physics violated",
                    "Insufficient automation: the plant needed fully automatic control with no operators",
                    "Bad luck: stuck valves are unforeseeable, so no systemic lesson applies"
                ],
                "answer": 1,
                "why": "Cybernetically, the operators were a comparator fed by corrupt sensors: the valve light signaled the command, not the state — feedback about intention, not reality. Their corrective actions (throttling emergency cooling) were rational given the false feedback and the wrong mental model of what pressurizer level meant. The lesson is architectural: feedback must report actual state, and operators need models of the system's true physics, not its indicators.",
                "hint": "The light reported what was commanded, not what was. What does a comparator do with false feedback?",
                "objectives": ["Analyze TMI as a feedback-architecture failure", "Distinguish command-reporting from state-reporting sensors"],
                "mins": 15,
                "evidence": ["Identifies the command-vs-state sensor flaw and the false-model comparator"]
            },
            {
                "id": "cyb-case-sc2",
                "title": "Toyota's Andon Cord: Designed Negative Feedback",
                "domain_id": "case-studies",
                "situation": "In Toyota's production system, any worker can pull the andon cord to stop the line when spotting a defect — halting dozens of workers and idling expensive equipment. Conventional mass-production logic calls this insane: never stop the line. Yet Toyota's defect rates became the industry's lowest.",
                "prompt": "Explain the andon cord cybernetically. Why does stopping the line improve the line?",
                "choices": [
                    "It doesn't really: Toyota's quality came from Japanese work culture, not the cord",
                    "The cord is a fast negative-feedback loop: it converts a defect (error signal) into immediate line-wide correction at the moment of cheapest intervention, preventing defect propagation downstream — short delay, high gain, local authority as the effector; mass production instead lets errors compound through long, slow feedback paths",
                    "It works by frightening workers into perfection through the threat of stopping everyone's work",
                    "It is a positive-feedback mechanism: stopping amplifies attention, which amplifies quality"
                ],
                "answer": 1,
                "why": "The andon cord closes the quality loop at the point of origin with minimal delay: error detected -> line stops -> root cause fixed -> restart. This is negative feedback with short delay and empowered effectors (the workers themselves). Conventional lines detect defects at final inspection — a long-delay loop that lets errors multiply through every downstream station. Toyota's advantage is loop architecture, not culture mystique.",
                "hint": "Where is the defect cheapest to fix — at the station where it occurs, or at final inspection?",
                "objectives": ["Explain andon as negative feedback design", "Contrast short-delay vs long-delay quality loops"],
                "mins": 12,
                "evidence": ["Describes the cord as a short-delay negative-feedback loop with worker effectors"]
            },
            {
                "id": "cyb-case-sc3",
                "title": "Ant Colonies: Stigmergy and Emergence",
                "domain_id": "case-studies",
                "situation": "Argentine ants reliably find the shortest path between nest and food with no leader, no map, and no ant understanding the colony's foraging strategy. Mechanism: ants lay pheromone trails (positive feedback amplifying successful paths) while pheromones evaporate (negative feedback pruning stale paths).",
                "prompt": "What does the ant colony demonstrate about control, and what is its lesson for human organizations?",
                "choices": [
                    "That central control is always superior: the colony succeeds despite having no leader, not because of it",
                    "Stigmergic coordination: global optimization emerges from local rules plus environmental feedback (the pheromone field as shared memory) — positive feedback amplifies what works, evaporation (negative feedback) forgets what doesn't; the organizational lesson is to design environments where local actions leave traces others can build on, rather than routing all coordination through hierarchy",
                    "That pheromones are a chemical curiosity with no organizational analogue",
                    "That emergence requires millions of agents: small teams cannot use this"
                ],
                "answer": 1,
                "why": "The colony is existence proof that sophisticated coordination needs no central controller: coupled positive feedback (trail reinforcement) and negative feedback (evaporation) plus a shared medium compute the shortest path. For organizations, the analogue is stigmergic infrastructure — visible work traces (boards, logs, shared docs) that let local actors coordinate without managerial routing — balancing amplification of success with forgetting of the stale.",
                "hint": "No ant knows the shortest path, yet the colony finds it. Where is the 'knowledge' stored?",
                "objectives": ["Explain stigmergy and coupled feedback in ant foraging", "Derive organizational design lessons"],
                "mins": 12,
                "evidence": ["Names trail-reinforcement and evaporation as coupled loops; proposes stigmergic infrastructure"]
            },
            {
                "id": "cyb-case-sc4",
                "title": "The Immune System: Learning by Feedback",
                "domain_id": "case-studies",
                "situation": "The adaptive immune system generates millions of random antibody variants, selects those that bind invaders (clonal selection), multiplies them, and — critically — deletes variants that bind the body's own tissues during training in the thymus (negative selection). Autoimmune disease is what happens when this fails.",
                "prompt": "Read the immune system as a cybernetic learner. What is its architecture, and what does autoimmunity reveal?",
                "choices": [
                    "It is a simple negative-feedback loop like a thermostat, and autoimmunity is sensor noise",
                    "It is a generate-and-test learning architecture: massive variety generation (requisite variety against pathogen variety), positive-feedback amplification of successes (clonal expansion), and negative selection as the comparator that defines self vs non-self — autoimmunity is comparator failure, the system attacking its own reference; the lesson is that learning systems need both amplification of hits and a trained discriminator",
                    "It is purely feedforward: antibodies are pre-programmed, so no learning occurs",
                    "Autoimmunity proves feedback architectures are inherently unsafe"
                ],
                "answer": 1,
                "why": "The immune system implements Ashby's variety principle (generate more antibody variety than pathogen variety), selectionist learning (amplify what binds), and a trained comparator (negative selection defining 'self'). Autoimmune disease is precisely comparator failure — the reference corrupted, so correction attacks the system itself. Any learning organization needs the same three arms: variety generation, success amplification, and a calibrated discriminator.",
                "hint": "Generation, amplification, discrimination — which arm fails in autoimmunity?",
                "objectives": ["Map clonal/negative selection onto cybernetic learning", "Interpret autoimmunity as comparator failure"],
                "mins": 12,
                "evidence": ["Names variety generation, clonal amplification, and negative selection as the three arms"]
            },
            {
                "id": "cyb-case-sc5",
                "title": "Chernobyl: Positive Feedback Unleashed",
                "domain_id": "case-studies",
                "situation": "On April 26, 1986, operators ran a test on Chernobyl's Reactor 4 with safety systems disabled. The RBMK design had a positive void coefficient: falling coolant increased reactivity, which boiled more coolant — a physical positive-feedback loop. When power surged, the SCRAM button's graphite-tipped rods initially added reactivity before absorbing it, spiking power beyond containment.",
                "prompt": "What is the cybernetic autopsy?",
                "choices": [
                    "Pure operator error: the test procedure was violated, so the physics is irrelevant",
                    "A compound failure: an inherently positive-feedback physical design (void coefficient) whose stabilizing negative-feedback arms (safety systems, SCRAM) were deliberately disabled by operators following institutional pressure to complete the test — the system was left with amplification and no correction, and the SCRAM design added a perverse transient; both the loop architecture and the organizational loops that disabled safeguards must be indicted",
                    "A maintenance failure: the rods were simply worn out",
                    "An unforeseeable act of nature: no design could have contained it"
                ],
                "answer": 1,
                "why": "Cybernetically, Chernobyl combined a positive-feedback core (void coefficient) with the systematic removal of every negative-feedback arm — disabled safety systems, plus a SCRAM mechanism that briefly amplified before correcting. The operators' decision itself emerged from organizational loops (production pressure overriding safety signals). The autopsy must span both levels: physical loop design and the institutional circuits that stripped its protections.",
                "hint": "Positive feedback plus disabled negative feedback equals what? And who disabled the safeguards?",
                "objectives": ["Analyze Chernobyl as positive feedback with removed stabilizers", "Span physical and organizational loop levels"],
                "mins": 15,
                "evidence": ["Indicts the void-coefficient loop, the disabled safeguards, and the organizational pressure circuit"]
            },
            {
                "id": "cyb-case-sc6",
                "title": "The Flash Crash: Algorithms Closing the Loop",
                "domain_id": "case-studies",
                "situation": "On May 6, 2010, the Dow lost nearly 1,000 points in minutes, then recovered. Investigations found high-frequency trading algorithms reacting to each other's sell signals: one algorithm's selling triggered others' stop-losses, which triggered more selling — machine-speed positive feedback with human overseers unable to intervene in time. A large fundamental sell order was the initial disturbance.",
                "prompt": "What does the Flash Crash teach about feedback in automated systems?",
                "choices": [
                    "That algorithms are inherently unstable and should be banned from markets",
                    "That tightly coupled automated feedback loops operate faster than human supervisory loops can correct: the HFT algorithms formed a machine-speed positive-feedback circuit with no damping (no coordinated circuit-breakers at the time) and no human in the loop at relevant timescales — the lesson is to design damping (breakers, kill switches, speed bumps) into automated loops proportional to their speed, since supervision must match loop velocity",
                    "That the initial sell order was illegal and caused everything alone",
                    "That markets are random and no lesson applies"
                ],
                "answer": 1,
                "why": "The crash was positive feedback at machine timescale: each algorithm's output became the next algorithm's input, amplifying the initial disturbance with no countervailing loop fast enough to matter. Human oversight existed at human timescale — irrelevant to a millisecond circuit. The cybernetic lesson is timescale matching: supervisory and damping mechanisms must operate at the speed of the loops they govern, built in as circuit-breakers rather than hoped-for human intervention.",
                "hint": "The loop ran in milliseconds; the humans watched in minutes. What timescale must the damping live at?",
                "objectives": ["Analyze the Flash Crash as machine-speed positive feedback", "Prescribe timescale-matched damping"],
                "mins": 12,
                "evidence": ["Names the HFT positive-feedback circuit and prescribes built-in, speed-matched circuit-breakers"]
            },
            {
                "id": "cyb-case-sc7",
                "title": "The Millennium Bridge Wobble",
                "domain_id": "case-studies",
                "situation": "London's Millennium Bridge opened in June 2000 and closed two days later: pedestrians' footsteps synchronized with the bridge's slight lateral sway, and each synchronized step amplified the sway, recruiting more pedestrians into step — until the deck moved alarmingly. Engineers had tested for vertical loads, not lateral synchronous feedback.",
                "prompt": "What is the cybernetic structure of the wobble, and what fixed it?",
                "choices": [
                    "A structural defect: the bridge was under-engineered and needed rebuilding",
                    "Pedestrian-structure positive feedback: sway -> synchronized stepping -> amplified sway, a coupled loop between crowd and structure that the designers never modeled because their tests excluded the human-structure interaction; the fix was damping (retrofitted tuned dampers absorbing the lateral energy), breaking the loop's gain rather than rebuilding the bridge",
                    "Pedestrian misbehavior: signage instructing people to walk out of step would have sufficed",
                    "Wind resonance: the wobble was purely aerodynamic"
                ],
                "answer": 1,
                "why": "The wobble is textbook coupled positive feedback: the bridge's motion organized pedestrian stepping, which fed energy back into the motion. The design failure was boundary choice — the 'system' was modeled as structure-only, excluding the crowd it would carry. Dampers fixed it by absorbing energy faster than the crowd could add it, lowering loop gain below the instability threshold without rebuilding.",
                "hint": "The bridge moved people, and the people moved the bridge. Where was the loop boundary drawn — and where should it have been?",
                "objectives": ["Identify coupled human-structure positive feedback", "Explain damping as loop-gain reduction"],
                "mins": 10,
                "evidence": ["Names the pedestrian-structure loop and the damper retrofit as gain reduction"]
            },
            {
                "id": "cyb-case-sc8",
                "title": "Biosphere 2: The Closed System That Breathed Wrong",
                "domain_id": "case-studies",
                "situation": "Biosphere 2 (1991-93) sealed eight people inside a 3-acre artificial ecosystem. Within months, oxygen fell from 21% to 14%: soil microbes respired faster than plants photosynthesized, and exposed concrete absorbed CO2, starving plants further — interacting loops the designers had not closed in their models. Oxygen had to be injected; the crew split into factions.",
                "prompt": "What does Biosphere 2 demonstrate about modeling closed systems?",
                "choices": [
                    "That closed ecological systems are impossible and should never be attempted",
                    "That unmodeled couplings dominate: the designers closed the material boundary but left causal loops open in their models — microbial respiration, concrete carbonation, and plant photosynthesis formed interacting feedbacks whose net effect (oxygen drain) no single-discipline model predicted; the lesson is that closure must be causal, not just physical, and complex systems demand cross-domain loop mapping before sealing the lid",
                    "That the crew's psychological conflicts caused the oxygen decline",
                    "That more concrete would have fixed the carbonation problem"
                ],
                "answer": 1,
                "why": "Biosphere 2 sealed matter and energy flows but not the causal understanding: soil microbiology, concrete chemistry, and plant physiology interacted through loops invisible to each discipline alone. The oxygen crash was an emergent property of coupled feedbacks, not a single failure. The lesson generalizes: in complex systems, the boundary that matters is the causal one — every loop crossing your model boundary is a surprise waiting to happen.",
                "hint": "They sealed the building. Did they seal their understanding of the loops inside it?",
                "objectives": ["Explain Biosphere 2's oxygen decline via coupled loops", "Argue for causal (not just physical) closure in modeling"],
                "mins": 12,
                "evidence": ["Names the microbe-concrete-plant loop interaction and demands causal closure"]
            }
        ]
    }
}

LESSONS = {
    "cybernetics": {
        "cybernetics": [
            {
                "_id": "cyb-extra-core-1",
                "id": "cyb-extra-core-1",
                "title": "Requisite Variety: The Master Law",
                "domain_id": "cybernetics",
                "concepts": [
                    "Ashby's Law of Requisite Variety: only variety can destroy variety — a regulator must be able to assume at least as many distinct states as the disturbances it must counter.",
                    "Variety is measured as the number of distinguishable states; a thermostat with on/off states has 2 states of variety against a continuous temperature disturbance — it copes only because the furnace and room dynamics attenuate the disturbance first.",
                    "Two strategic moves exist: amplify regulator variety (more sensors, more responses, smarter models) or attenuate disturbance variety (constrain inputs, standardize, buffer).",
                    "The law is a hard constraint, not advice: no amount of effort, funding, or good intentions substitutes for missing variety — control fails at the variety gap."
                ],
                "example": {
                    "code": "Disturbances: 12 fault types on a grid. Regulator: 5 procedures. Gap: 7 unhandled types -> outages. Fix options: (a) add 7 procedures + cross-training [amplify], or (b) island volatile segments so only 5 fault types can reach the desk [attenuate].",
                    "walkthrough": "Count both sides in states, not effort. The gap is arithmetic: 12 vs 5. Every control failure you have ever seen was, at bottom, a variety gap — find it, then choose amplify or attenuate deliberately."
                },
                "pitfalls": [
                    "Confusing effort with variety: working harder with the same 5 procedures does not create a 6th response.",
                    "Trying to amplify variety by adding undifferentiated capacity (more staff with identical training) instead of genuinely new distinctions.",
                    "Forgetting attenuation is a legitimate move: sometimes constraining the disturbance is cheaper than matching it."
                ],
                "try_it": "Pick a system you manage. List its disturbance types (count them) and its distinct responses (count them). Name the gap and choose: amplify or attenuate?"
            },
            {
                "_id": "cyb-extra-core-2",
                "id": "cyb-extra-core-2",
                "title": "The Black Box Method",
                "domain_id": "cybernetics",
                "concepts": [
                    "The black box is Ashby's method for studying systems whose internals are unknown or inaccessible: you infer behavior purely from input-output relations under controlled variation.",
                    "Protocol: enumerate manipulable inputs, vary one at a time, record outputs systematically, and build a transfer model (given input X, output Y follows) — the model's validity is judged by prediction, not by resemblance to hidden internals.",
                    "The method is honest about its limits: it yields behavioral equivalence, not structural truth — two different mechanisms can share one black-box model, and the model breaks outside the tested input range.",
                    "Applications span debugging sealed devices, probing organizational behavior, testing ML models, and any diagnosis where opening the box is impossible, destructive, or beside the point."
                ],
                "example": {
                    "code": "Sealed packaging machine crushes cartons intermittently. Experiment: fix temperature, vary belt speed in 5 steps, record crush rate per 100 cartons at each step. Result: crush rate spikes only above speed 7 with small cartons -> hypothesis: timing misalignment at high speed. Prediction test: run speed 8 with large cartons -> no crushing. Model confirmed behaviorally.",
                    "walkthrough": "Notice no housing was opened. The input-output table alone isolated the fault condition and predicted a new case correctly — that is the black box doing its full job."
                },
                "pitfalls": [
                    "Varying multiple inputs at once, which confounds the input-output mapping beyond interpretation.",
                    "Mistaking the behavioral model for the mechanism and then extrapolating beyond tested ranges.",
                    "Opening the box prematurely and destroying the behavior you needed to explain."
                ],
                "try_it": "Choose a system you cannot open (a vendor API, a team habit, an appliance). Design a one-input-at-a-time experiment table and predict one untested case."
            }
        ],
        "systems-anatomy": [
            {
                "_id": "cyb-extra-sa-1",
                "id": "cyb-extra-sa-1",
                "title": "Anatomy of a Control Loop: Sensor, Comparator, Effector",
                "domain_id": "systems-anatomy",
                "concepts": [
                    "Every control loop decomposes into four functional organs: the sensor (measures the controlled variable), the comparator (computes error = reference minus measurement), the effector (acts to reduce error), and the reference or setpoint itself.",
                    "Diagnosis proceeds anatomically: oscillating? suspect sensor delay or excess effector gain. Steady offset? the comparator lacks integral action or the reference is unreachable. No response at all? trace the signal path organ by organ until the dead link appears.",
                    "The reference is part of the anatomy: many 'broken systems' are healthy loops chasing a wrong, conflicting, or unreachable setpoint — the fault is in the goal, not the machinery.",
                    "Feedforward is a fifth organ where present: a disturbance sensor that acts pre-emptively, complementing the error-driven feedback path."
                ],
                "example": {
                    "code": "Room thermostat loop: sensor = bimetallic strip (room temp), comparator = dial mechanism (setpoint 70F vs measured), effector = furnace relay. Fault: strip mounted above heat vent -> sensor reports 78F while room is 66F -> comparator computes negative error -> effector stays off -> room freezes. Fix: relocate sensor. Every organ was healthy; the sensor sampled the wrong variable.",
                    "walkthrough": "Walk the signal: what does the sensor actually sample? What reference does the comparator use? Can the effector physically close the error? Ask in order and the fault locates itself."
                },
                "pitfalls": [
                    "Blaming the effector (weak furnace, lazy team) when the sensor feeds the comparator lies.",
                    "Tuning gain before checking whether the reference is achievable — no loop can hold an impossible setpoint.",
                    "Forgetting delays: a sensor far downstream in time makes even a perfect loop oscillate."
                ],
                "try_it": "Diagram a loop from your own work (a budget control, a quality check, a habit) labeling sensor, comparator, reference, and effector. Identify the weakest organ."
            },
            {
                "_id": "cyb-extra-sa-2",
                "id": "cyb-extra-sa-2",
                "title": "Anatomy of Second-Order Systems: The Observer Included",
                "domain_id": "systems-anatomy",
                "concepts": [
                    "First-order anatomy maps the observed system; second-order anatomy adds one more organ: the observer, with its own sensors (instruments), comparators (theories, expectations), and effectors (interventions, publications, funding).",
                    "The observer's loop couples with the observed loop: measurement perturbs (Hawthorne), models steer (Goodhart), and descriptions re-enter the system they describe (self-fulfilling prophecies).",
                    "Diagnosing second-order systems means tracing two circuits: the object-level loop and the observer-level loop, plus the coupling arrows between them — most 'irrational' behavior lives in the coupling.",
                    "Von Foerster's maxim anchors the anatomy: objectivity is not the absence of the observer but the explicit inclusion of the observer in the account."
                ],
                "example": {
                    "code": "Call-center metric loop (first order): calls -> AHT sensor -> bonus comparator -> agent effector. Observer loop (second order): managers observe AHT -> theory 'AHT measures efficiency' -> intervention 'tighten target' -> agents game metric -> AHT falls, service collapses -> managers observe 'improvement'. Coupling arrow: the theory about the measure changed the measured behavior (Goodhart). Anatomy shows the pathology is in the coupling, not the agents.",
                    "walkthrough": "Draw both loops side by side, then draw the arrows between them: what does observing do to the observed, and what does the observed do to the observer's theories? The fault is usually on a coupling arrow."
                },
                "pitfalls": [
                    "Analyzing only the object loop and treating observer effects as noise or dishonesty.",
                    "Trying to achieve observer-independence instead of observer-explicitness — the former is impossible, the latter is the discipline.",
                    "Locating ethics in the equation rather than in the observer-system relation."
                ],
                "try_it": "Take a metric you are judged by. Draw your loop and your manager's observer loop, then label the coupling arrows. Which arrow distorts the measure?"
            }
        ],
        "origins": [
            {
                "_id": "cyb-extra-origins-1",
                "id": "cyb-extra-origins-1",
                "title": "The Macy Conferences: How Cybernetics Was Born",
                "domain_id": "origins",
                "concepts": [
                    "Ten conferences (1946-1953), funded by the Josiah Macy Jr. Foundation and chaired by Warren McCulloch, assembled mathematicians, engineers, anthropologists, psychologists, and neurophysiologists around two shared ideas: feedback and information.",
                    "The method was the message: a common language (circular causality, signal, noise, feedback) let disciplines trade insights — Wiener's predictor mathematics illuminated Bateson's anthropology and vice versa.",
                    "Key outputs: the legitimation of circular (rather than linear) causality in science, the treatment of communication and control as one subject ('cybernetics'), and the interdisciplinary template itself.",
                    "The lesson for today: breakthrough fields are born at disciplinary intersections when participants share rigorous common concepts, not when they merely meet."
                ],
                "example": {
                    "code": "Macy moment: Julian Bigelow describes the anti-aircraft predictor's feedback mathematics; Gregory Bateson recognizes the same circular pattern in Iatmul ritual behavior he had studied in New Guinea. One formalism, two domains — the predictor's 'hunting' oscillation and the ritual's schismogenesis are the same dynamics. That recognition, repeated across disciplines for seven years, became cybernetics.",
                    "walkthrough": "Notice the direction of insight: engineering math explained anthropology, and anthropological patterns enriched the math. Interdisciplinarity worked because the concepts (feedback, circular causality) were precise enough to travel."
                },
                "pitfalls": [
                    "Romanticizing the Macy meetings as casual brainstorming — they were rigorously chaired, with prepared papers and fierce conceptual policing.",
                    "Treating 'interdisciplinary' as merely inviting diverse people; without shared rigorous concepts, mixing disciplines produces confusion, not cybernetics.",
                    "Forgetting the wartime context: the predictor work that seeded it all was military engineering with ethical shadows Wiener later confronted."
                ],
                "try_it": "Name a problem you face. List three disciplines whose concepts might illuminate it, and one shared concept (like feedback) that could let them talk to each other."
            }
        ],
        "feedback-systems": [
            {
                "_id": "cyb-extra-feedback-1",
                "id": "cyb-extra-feedback-1",
                "title": "Delays: The Hidden Cause of Oscillation",
                "domain_id": "feedback-systems",
                "concepts": [
                    "Delay between sensing and acting (or between acting and effect) shifts correction out of phase with need: by the time the correction lands, the situation has moved on, so the correction overshoots — the signature of delay is oscillation.",
                    "The dangerous ratio: when delay approaches half the system's natural response time, even modest corrective gain produces sustained boom-bust cycles (hiring, inventory, cloud autoscaling, shower temperature).",
                    "Three remedies, in order of power: shorten the delay (faster sensing, closer effectors), damp the gain (smaller corrections, deadbands, cooldowns), or add feedforward (act on predicted disturbance before delay matters).",
                    "Meadows' rule: delays are systematically underestimated and almost always the true cause of 'irrational' cycling in human systems."
                ],
                "example": {
                    "code": "Shower with slow pipes: turn hotter -> nothing for 10s -> turn more -> scalding arrives -> slam to cold -> freezing arrives. Delay ~10s, correction instant and large -> violent oscillation. Fix ranking: (1) shorten delay — impossible in old plumbing; (2) damp gain — tiny adjustments, then wait; (3) feedforward — count seconds and predict. Every frustrated bather rediscovers control theory.",
                    "walkthrough": "Map any oscillation you know onto this template: measure the delay, estimate the gain, check the ratio. Then apply the three remedies in order and watch which one the real system actually needs."
                },
                "pitfalls": [
                    "Blaming the people ('impatient bather,' 'incompetent managers') instead of the delay structure.",
                    "Increasing correction speed or size to fight oscillation — this adds gain to a delay problem and worsens it.",
                    "Assuming digital systems have no delay: network, queueing, and human-approval delays oscillate cloud and organizational loops identically."
                ],
                "try_it": "Find an oscillation in your life or work. Estimate the delay and the correction size. Which of the three remedies is actually available to you?"
            }
        ],
        "information": [
            {
                "_id": "cyb-extra-info-1",
                "id": "cyb-extra-info-1",
                "title": "Entropy, Redundancy, and Meaning",
                "domain_id": "information",
                "concepts": [
                    "Shannon entropy H = -sum(p log2 p) measures the average surprise per symbol: maximum when outcomes are equiprobable (1 bit for a fair coin), lower when skewed (~0.81 bits at 75/25).",
                    "Redundancy is the gap between the raw symbol rate and the entropy: it is what makes error correction possible (repeat the message, survive the noise) and what makes compression possible (remove the predictable part).",
                    "Shannon deliberately excluded meaning: his theory quantifies uncertainty reduction over a channel, saying nothing about semantics — a perfectly transmitted lie and a perfectly transmitted truth carry identical Shannon information.",
                    "Bateson completes the picture pragmatically: information is 'a difference that makes a difference' — the engineer counts bits in the channel; the cybernetician asks which differences change the receiving system's behavior."
                ],
                "example": {
                    "code": "Fair coin: H = 1 bit/symbol, incompressible. Biased 75/25 coin: H ~= 0.81 bits/symbol, compressible to ~81% via Huffman-style coding. Noisy channel (3 kHz, 30 dB SNR): C = 3000*log2(1001) ~= 30 kbps hard ceiling. Dashboard with 40 green metrics nobody acts on: high Shannon throughput, zero Bateson information.",
                    "walkthrough": "Run the three calculations yourself: entropy of a skewed source, capacity of a noisy channel, and then audit one real dashboard — count how many metrics ever change a decision. The first two are Shannon; the third is Bateson. You need both."
                },
                "pitfalls": [
                    "Quoting '1 bit per binary symbol' for skewed sources — entropy depends on the distribution, not the alphabet.",
                    "Treating Shannon capacity as achievable throughput: it is a ceiling requiring ideal coding, not a data-sheet promise.",
                    "Selling syntactic density (compression) as semantic value — the contract-compression fallacy."
                ],
                "try_it": "Compute the entropy of a source you know (e.g., your team's build outcomes: 90% pass, 10% fail). Then list three 'informative' reports you receive and score each on Bateson's test: did it change any decision last month?"
            }
        ],
        "second-order": [
            {
                "_id": "cyb-extra-second-1",
                "id": "cyb-extra-second-1",
                "title": "The Observer Is Always In the System",
                "domain_id": "second-order",
                "concepts": [
                    "First-order cybernetics studies observed systems (thermostats, servomechanisms); second-order cybernetics, named by von Foerster, studies observing systems — the observer is included in the domain of the science.",
                    "Consequences: measurement perturbs (observer effects), models steer what they model (Goodhart/Campbell), and descriptions re-enter systems (self-fulfilling and self-defeating prophecies) — the instrument and the object form one circuit.",
                    "Von Foerster's ethical pivot: objectivity redefined as explicit inclusion of the observer; 'the world as we know it is constructed by our descriptions' — responsibility follows the describer, not just the described.",
                    "Practical disciplines: participatory design (the measured co-own the measure), reflexivity journals (track how your observing changed the field), and loop-aware metrics (assume the system will optimize your indicator)."
                ],
                "example": {
                    "code": "Anthropologist studies a village's fishing practices; villagers, aware of being studied, fish 'traditionally' for the observer while using motors when unobserved. First-order report: 'traditional methods persist.' Second-order correction: the observation apparatus (foreign researcher, notebook, questions) is part of the system producing the observed behavior — the finding describes the observer-village circuit, not the village alone.",
                    "walkthrough": "For any study or metric you trust, ask: how would the observed behave if the observer vanished? The difference between that and what you see is the observer's contribution — name it explicitly instead of pretending it is zero."
                },
                "pitfalls": [
                    "Treating second-order as mysticism: it is rigorous bookkeeping of observer-system coupling, not a denial of reality.",
                    "Overcorrecting into paralysis: including the observer does not forbid measurement, it disciplines it.",
                    "Confusing 'observer included' with 'everything is subjective' — the coupling is itself an objective fact about the circuit."
                ],
                "try_it": "Take one metric you report upward. Write down three ways the act of measuring it changes the behavior it measures. That list is your second-order audit."
            }
        ],
        "modern-systems": [
            {
                "_id": "cyb-extra-modern-1",
                "id": "cyb-extra-modern-1",
                "title": "The Viable System Model in One Lesson",
                "domain_id": "modern-systems",
                "concepts": [
                    "Beer's VSM identifies five necessary functions for viability: S1 operations (the units doing the work), S2 coordination (anti-oscillation between units), S3 control (resource bargaining, accountability), S3* audit (sporadic direct monitoring), S4 intelligence (outward/future scanning), S5 policy (identity, ultimate arbitration).",
                    "Recursion: every viable system contains viable systems — each S1 unit should itself be analyzable as a five-system whole; pathologies often hide one recursion level down.",
                    "The 3-4 homeostat is the heart: S3 (present, inward) and S4 (future, outward) must hold each other in tension under S5 arbitration — collapse this tension and the system either stagnates (S3 wins) or fantasizes (S4 wins).",
                    "Diagnosis is subtractive: list which functions actually exist (not which boxes appear on the org chart); missing functions predict specific failure modes — no S2 means oscillation, no S4 means strategic blindness, no S5 means identity drift."
                ],
                "example": {
                    "code": "Diagnose a 300-person logistics firm: S1 strong (great operations), S2 present (daily coordination), S3 weak (CEO gut-feel control), S3* absent, S4 ABSENT (no market intelligence — competitors eating accounts), S5 weak (no articulated identity). Verdict: viable today, blind tomorrow. Prescription: build S4 first (intelligence function feeding S5), formalize S3 bargaining, add S3* audits. Org chart titles are irrelevant; functions are everything.",
                    "walkthrough": "Run the five-function audit on any organization you know. Be brutal: a 'strategy department' that only reacts to crises is not S4. Name what is actually missing and predict the failure it will cause — then check the prediction against history."
                },
                "pitfalls": [
                    "Mapping VSM systems to departments: they are functions, and one team can carry several (or none).",
                    "Treating S5 as mission-statement writing: policy is the live arbitration of the 3-4 tension and the guardian of identity under pressure.",
                    "Forgetting recursion: diagnosing only the top level while the pathology lives in an S1 unit's missing S2."
                ],
                "try_it": "Audit your own team as a viable system: which of the five functions exist, which are missing, and what failure does each gap predict? Write the predictions down."
            }
        ],
        "exam-strategy": [
            {
                "_id": "cyb-extra-exam-1",
                "id": "cyb-extra-exam-1",
                "title": "Writing the Cybernetics Essay: Structure That Scores",
                "domain_id": "exam-strategy",
                "concepts": [
                    "The rubric rewards four things in order: precise definitions (loop-anatomy language), structured comparison (shared axes, not parallel summaries), application (thinkers' concepts operating on the question's case), and synthesis (a position that survives its best objection).",
                    "The 8-minute plan: thesis in one sentence, 2x2 or axis grid guaranteeing coverage of every question dimension, one worked example per cell, and a reserved final paragraph for synthesis — write to the plan, not from memory.",
                    "Source questions demand claim-mechanism-context-limits dissection: never summarize when you can analyze, never quote at length when you can dissect briefly.",
                    "Time is a control problem: allocate by marks per minute, enforce section deadlines as negative feedback on yourself, and keep buffer as damping — self-regulation is applied cybernetics."
                ],
                "example": {
                    "code": "Question: 'Shannon and Bateson both theorize information — are they compatible?' Plan (8 min): definitions — Shannon syntactic, Bateson pragmatic (2 min). Axis grid: scope (channel vs living system), unit (bit vs difference), meaning (excluded vs central) — both thinkers on each axis (3 min). Examples: noisy channel capacity; dashboard metrics nobody acts on (2 min). Synthesis: hierarchical — Bateson's differences select what Shannon's channels carry (1 min). Then write 35 min to the plan.",
                    "walkthrough": "Notice the plan does the thinking before the writing starts: every rubric band is pre-assigned a paragraph. Under exam pressure, structure is what survives — fluency is not."
                },
                "pitfalls": [
                    "The historical preamble: opening with Wiener's biography burns marks-earning time on unasked context.",
                    "Parallel summaries masquerading as comparison: two blocks describe; only shared axes compare.",
                    "Colloquial definitions ('bad feedback') — every key term must be defined in sensor-comparator-effector language."
                ],
                "try_it": "Take any past essay question. Produce only the 8-minute plan: thesis, grid, examples, synthesis paragraph outline. Do not write the essay — plans are the skill."
            }
        ],
        "cybernetics-in-tech": [
            {
                "_id": "cyb-extra-tech-1",
                "id": "cyb-extra-tech-1",
                "title": "Gradient Descent Is a Feedback Loop",
                "domain_id": "cybernetics-in-tech",
                "concepts": [
                    "Training is nested control loops: the inner loop (gradient descent) minimizes training loss; the outer loop (validation) monitors generalization — the error signal that matters for production.",
                    "Overfitting is inner-loop success with outer-loop failure: training loss falls while validation loss rises means the model memorizes; the outer loop's alarm must govern (early stopping, regularization).",
                    "Hyperparameters are loop tuning: learning rate is gain (too high oscillates/diverges, too low crawls), batch size and momentum shape the dynamics like damping terms.",
                    "The cybernetic discipline: never celebrate the inner loop's number while the outer loop alarms — ship decisions belong to the loop that measures the deployment reality."
                ],
                "example": {
                    "code": "Vision model: epoch 12 — train loss 0.08 (falling), val loss 0.31 (rising since epoch 8). Inner loop says 'keep going'; outer loop says 'memorizing'. Action: early-stop at epoch 8 checkpoint, add augmentation + dropout, retrain. Production accuracy recovers. The team that shipped epoch 12 optimized the wrong loop.",
                    "walkthrough": "Plot both curves before every ship decision. The moment they diverge, the outer loop owns the decision — that single habit prevents the most common ML deployment failure."
                },
                "pitfalls": [
                    "Tuning the learning rate to make training loss fall faster while ignoring the validation curve.",
                    "Treating regularization as optional polish rather than the outer loop's actuator.",
                    "Confusing the map (loss numbers) with the territory (production performance on unseen data)."
                ],
                "try_it": "Sketch train/val curves for a hypothetical run where they diverge at epoch 10. Mark where you would stop and what two regularizers you would apply."
            },
            {
                "_id": "cyb-extra-tech-2",
                "id": "cyb-extra-tech-2",
                "title": "TCP Congestion Control: The Internet's Thermostat",
                "domain_id": "cybernetics-in-tech",
                "concepts": [
                    "TCP's AIMD (additive increase, multiplicative decrease) is a decentralized negative-feedback loop: packet loss is the error signal, window size is the controlled variable, and every sender runs the identical loop with no coordinator.",
                    "The asymmetry is the design: additive increase probes gently for spare capacity (cautious exploration of a shared resource); multiplicative decrease sheds load decisively when congestion signals (fast correction before collapse).",
                    "Fairness emerges: independent AIMD loops converge on roughly equal shares — a global property arising from local rules, the networking analogue of ant-colony stigmergy.",
                    "Modern variants (CUBIC, BBR) retune the loop — BBR even replaces loss with bottleneck-bandwidth estimation as the sensor — but the feedback architecture is unchanged since the 1980s."
                ],
                "example": {
                    "code": "Two flows share a 100 Mbps bottleneck. Both probe +1 packet/RTT; at loss, both halve. Over seconds, windows sawtooth in sync, each averaging ~50 Mbps. No router told them to share — the shared error signal (loss) coupled their loops into fair division. Remove the backoff (aggressive probing) and the link collapses into congestion: the tragedy of the commons, solved by feedback.",
                    "walkthrough": "Trace one packet-loss event through both senders' loops: signal, comparison, halving, re-probing. Then imagine one sender ignoring the signal — that is what congestion collapse looked like in 1986 before Van Jacobson's algorithm."
                },
                "pitfalls": [
                    "Thinking 'faster probing = better throughput' — aggressive increase overshoots shared capacity and collapses the commons.",
                    "Forgetting the loop is decentralized: there is no controller to appeal to, only the shared signal.",
                    "Assuming loss always means congestion (wireless links break this) — sensor validity matters, as TMI taught."
                ],
                "try_it": "On paper, simulate 5 rounds of two AIMD senders sharing a link: start windows 10 and 2, capacity 12, halve both on overshoot. Watch fairness emerge."
            },
            {
                "_id": "cyb-extra-tech-3",
                "id": "cyb-extra-tech-3",
                "title": "Observability as Organizational Nervous System",
                "domain_id": "cybernetics-in-tech",
                "concepts": [
                    "Metrics, logs, and traces are only the sensor arm; observability becomes feedback when wired to a comparator (alert thresholds anchored to user-facing service objectives), an effector (an empowered responder with runbooks), and a learning arm (postmortems that change the system).",
                    "Alert fatigue is sensor degradation by noise: a 397:3 noise-to-signal ratio saturates the human channel, so the first fix is subtractive — delete non-actionable alerts — before any tooling upgrade.",
                    "SLOs are the reference signal: error budgets translate user tolerance into a setpoint the loop regulates against, replacing gut-feel thresholds with a contract.",
                    "The postmortem is the outer learning loop: incidents are disturbances, and the organization that does not update its models from them is open-loop at the slowest, most important timescale."
                ],
                "example": {
                    "code": "Team: 400 alerts/day, 3 actionable, 45-min detection. Loop wiring: (1) comparator — keep only alerts that page on SLO-budget burn; (2) effector — single on-call with runbook authority; (3) sensor hygiene — delete the other 397 or demote to dashboards; (4) learning — blameless postmortem per incident, action items tracked like bugs. Detection drops to 5 minutes with no new platform purchased.",
                    "walkthrough": "Audit your own alerting against the four arms: sensor, comparator, effector, learning. Score each 0-2. The lowest score is your next project — and it is almost never the sensor."
                },
                "pitfalls": [
                    "Buying a shinier platform to fix an open loop — new sensors, same missing comparator.",
                    "Thresholds set from gut feel instead of SLO math: the comparator needs a principled reference.",
                    "Postmortems filed unread: the learning arm severed, so the same disturbance will recur."
                ],
                "try_it": "List your top 5 noisiest alerts. For each, name the user-facing harm it predicts. Any alert with no answer gets deleted or demoted this week."
            },
            {
                "_id": "cyb-extra-tech-4",
                "id": "cyb-extra-tech-4",
                "title": "Recommender Systems and Runaway Positive Feedback",
                "domain_id": "cybernetics-in-tech",
                "concepts": [
                    "The recommender loop: user clicks -> training signal -> narrower recommendations -> narrower future clicks — positive feedback that concentrates the content distribution into an attractor, misread as 'revealed preference.'",
                    "Second-order twist: the instrument co-produces the phenomenon — 'preferences' measured after months of algorithmic shaping are partly the algorithm's own output, so optimizing them is the system chasing its own tail.",
                    "Concentration dynamics: without countervailing variety injection (exploration, diversity objectives, chronological options), the loop collapses onto a narrow slice of content and creators.",
                    "Design responses are loop surgery: add negative-feedback arms (diversity metrics as comparators), inject exploration variety (epsilon-greedy, editorial picks), and measure long-term user thriving, not just immediate engagement."
                ],
                "example": {
                    "code": "Video platform optimizes watch time. Month 1: user watches cooking + woodworking. Loop: clicks train model -> feed narrows to cooking -> woodworking vanishes from options -> clicks concentrate -> model 'learns' user loves only cooking. Intervention: diversity comparator (no more than 60% of feed from one cluster), 10% exploration slots, quarterly 'broadening' metric. Watch time dips 2%, creator diversity and long-term retention rise.",
                    "walkthrough": "Draw the loop for any feed you use daily, then locate yourself in it: which of your 'preferences' were options before the loop narrowed them? That discomfort is the second-order insight landing."
                },
                "pitfalls": [
                    "Calling the output 'user choice' — choice requires options the loop has not yet eliminated.",
                    "Fixing it with 'more data': the loop will concentrate any dataset; the structure, not the volume, is the problem.",
                    "Optimizing engagement while measuring nothing else — single-metric optimization is Goodhart bait."
                ],
                "try_it": "Pick a feed you use. Scroll 20 items and tally topic clusters. Estimate the concentration ratio — then design one negative-feedback arm (a rule) that would broaden it."
            }
        ],
        "case-studies": [
            {
                "_id": "cyb-extra-case-1",
                "id": "cyb-extra-case-1",
                "title": "Case Method: The Five-Lens Dissection",
                "domain_id": "case-studies",
                "concepts": [
                    "Lens 1 — Loop anatomy: decompose the case into sensors, comparators, references, and effectors; name which organ failed or was missing.",
                    "Lens 2 — Loop sign and coupling: identify reinforcing vs balancing loops, their gain, and how loops coupled (did one loop's output become another's input?).",
                    "Lens 3 — Delay and timescale: locate every significant delay; check whether corrections arrived in phase or out of phase, and whether supervision matched loop velocity.",
                    "Lens 4 — Variety: count disturbance variety vs regulator variety (Ashby); find the gap the failure fell through.",
                    "Lens 5 — Observer: place the observers (operators, managers, modelers, you) inside the system; trace how observation perturbed the observed and how models steered behavior."
                ],
                "example": {
                    "code": "Flash Crash through five lenses: (1) sensors reported prices, comparators were stop-loss rules, effectors were sell algorithms — all machine-speed; (2) sell signals coupled into positive feedback across firms; (3) millisecond loops vs minute-scale human oversight — supervision out of phase; (4) regulator variety (human monitors) dwarfed by HFT variety; (5) the algorithms observed each other — the market they 'measured' was their own collective output. Five lenses, one coherent autopsy.",
                    "walkthrough": "Take any case and run the lenses in order, writing one paragraph per lens. The discipline is completeness: the lens you skip is usually the one holding the root cause."
                },
                "pitfalls": [
                    "Stopping at Lens 1: anatomy without sign, delay, variety, and observer misses most real failures.",
                    "Applying lenses as labels rather than analysis — 'this was positive feedback' without tracing the coupling is decoration.",
                    "Excluding yourself: the analyst's own framing is an observer effect on the case (Lens 5 applies to you too)."
                ],
                "try_it": "Pick a failure you witnessed at work. Write one paragraph per lens. Which lens revealed something you had not seen before?"
            },
            {
                "_id": "cyb-extra-case-2",
                "id": "cyb-extra-case-2",
                "title": "Three Mile Island: Anatomy of a Feedback Failure",
                "domain_id": "case-studies",
                "concepts": [
                    "The sensor lie: the relief-valve indicator reported the command (solenoid de-energized) rather than the valve's physical state — feedback about intention masquerading as feedback about reality.",
                    "The model mismatch: operators read pressurizer level as coolant inventory, but the actual physics (a steam bubble forming) broke that mapping — the comparator corrected against a false model of the system.",
                    "Rational action on false feedback: throttling emergency cooling was the correct move given what the instruments said; the failure was architectural, not a competence failure — blame the loop, then fix the loop.",
                    "Design rules extracted: sensors must report state, not commands; operators need training on system physics, not just procedures; and critical loops need independent, diverse sensing (requisite variety in instrumentation)."
                ],
                "example": {
                    "code": "Timeline: 04:00 valve sticks open; light shows 'commanded shut' — operators believe it shut. Coolant escapes 2+ hours; pressurizer level reads HIGH (steam bubble), operators throttle emergency cooling to 'prevent overfill.' Reality: core uncovered, overheating. Every operator action was locally rational given the instruments. Post-accident fixes: valve position sensors reporting actual stem position, upgraded operator training on thermodynamics, symptom-based (not event-based) emergency procedures.",
                    "walkthrough": "Reconstruct the operators' information state minute by minute, not the physical state. The gap between those two timelines is the case: show exactly where false feedback made the wrong action the reasonable one."
                },
                "pitfalls": [
                    "Hindsight bias: judging operators by the physical timeline instead of their instrument timeline.",
                    "Concluding 'automate everything': the lesson is better feedback architecture, and automation with the same false sensors fails identically.",
                    "Treating TMI as only nuclear: command-vs-state sensor confusion exists in every dashboard you have ever used."
                ],
                "try_it": "Find one indicator in your own systems that reports a command ('restart sent') rather than a state ('service healthy'). Redesign it to report state."
            },
            {
                "_id": "cyb-extra-case-3",
                "id": "cyb-extra-case-3",
                "title": "Toyota's Andon Cord: Designing Negative Feedback That Works",
                "domain_id": "case-studies",
                "concepts": [
                    "The andon cord is negative feedback with minimal delay: defect detected -> line stops -> root cause addressed at the station -> restart — correction applied where the error is cheapest to fix.",
                    "Empowered effectors: any worker can pull the cord — the corrective authority sits at the sensor location, eliminating the delay and distortion of escalation hierarchies.",
                    "Jidoka (autonomation) generalizes it: machines that detect their own abnormalities and stop — the loop closed in hardware, not just in culture.",
                    "Contrast with inspection-at-the-end: long-delay feedback lets defects compound through every downstream station, making the eventual correction orders of magnitude more expensive — the andon economics are delay economics."
                ],
                "example": {
                    "code": "Two plants, one defect type (mis-torqued bolt). Plant A (andon): worker spots it, pulls cord, line stops 4 minutes, torque wrench recalibrated, 3 cars affected. Plant B (final inspection): defect found after full assembly, 400 cars need rework bays, 2 days of chaos. Same defect, different loop delay — cost ratio roughly 100:1. Toyota's quality lead is, arithmetically, a delay lead.",
                    "walkthrough": "Price the delay in any quality process you know: cost of fixing at detection vs at final inspection. The ratio is the business case for moving the comparator upstream — compute it before arguing about culture."
                },
                "pitfalls": [
                    "Copying the cord without the response system: a stop mechanism with no rapid root-cause machinery just stops the line repeatedly.",
                    "Attributing Toyota's results to culture alone: the loop architecture does calculable work regardless of culture.",
                    "Pulling the cord on everything: the comparator still needs calibration — stop for defects, not for trivia."
                ],
                "try_it": "Identify your team's 'final inspection' — the late point where defects surface. Design the andon equivalent: who detects, who can stop, and what happens in the first 5 minutes?"
            },
            {
                "_id": "cyb-extra-case-4",
                "id": "cyb-extra-case-4",
                "title": "The Flash Crash: When Algorithms Close the Loop",
                "domain_id": "case-studies",
                "concepts": [
                    "Machine-speed positive feedback: HFT algorithms' outputs (sell orders) became other algorithms' inputs (stop-loss triggers) in milliseconds — a coupled circuit with no human-timescale participant.",
                    "The initial disturbance was ordinary (a large fundamental sell order); the catastrophe was the loop's gain, not the trigger — positive feedback amplifies whatever enters it.",
                    "Missing damping: no coordinated circuit-breakers operated at the relevant timescale in 2010; supervision existed at human speed, which is no supervision at all for millisecond loops.",
                    "The design principle: every automated loop needs damping proportional to its velocity — breakers, kill switches, speed bumps — built into the loop, because post-hoc human intervention cannot catch a loop that outruns human reaction time by six orders of magnitude."
                ],
                "example": {
                    "code": "May 6, 2010: Dow -998 points in ~20 minutes, then mostly recovered. Chain: large E-mini sell -> HFT momentum algorithms sell -> stop-losses trigger -> more selling -> liquidity vanishes as market-makers withdraw (their own risk loops) -> prices gap down absurdly (Accenture at $0.01) -> breakers finally trip -> humans catch up -> recovery. Post-crash reforms: limit-up/limit-down bands, single-stock circuit breakers — damping installed at machine timescale.",
                    "walkthrough": "Draw the 2010 loop with timescales labeled on every arrow: milliseconds for algorithm arrows, minutes for human arrows. The diagram convicts the architecture by itself — no narrative needed."
                },
                "pitfalls": [
                    "Blaming the initial seller: triggers are interchangeable; the loop's gain is the story.",
                    "Concluding algorithms are ungovernable: they are governable by damping designed at their own timescale.",
                    "Assuming your domain is exempt: any automated decision loop faster than its oversight has a Flash Crash waiting."
                ],
                "try_it": "Name the fastest automated loop in your organization (deploy pipeline, trading, bidding, scaling). What damps it, and at what timescale does the damping operate? If nothing does, design the breaker."
            }
        ]
    }
}

LABS = {
    "cybernetics": [
        {
            "_id": "cyb-lab-extra1",
            "id": "cyb-lab-extra1",
            "title": "Map a Feedback Loop in Your Organization",
            "domain_id": "feedback-systems",
            "objective": "Diagram one real reinforcing or balancing loop in your workplace, labeling every sensor, comparator, reference, effector, and delay.",
            "steps": [
                "Choose a recurring pattern: a metric that keeps moving the wrong way, a chronic firefight, or a process that oscillates.",
                "List the variables involved as nouns with direction (e.g., 'backlog size,' not 'backlog problems').",
                "Draw the causal arrows between variables, marking each link + (same direction) or - (opposite direction).",
                "Label the loop organs: which variable is sensed, what reference it is compared against, who/what acts as effector, and where the delays sit.",
                "Determine the loop sign by counting - links (odd = balancing, even = reinforcing) and predict the loop's long-term behavior.",
                "Propose one structural intervention: which single arrow would you rewire, and what would change?"
            ],
            "checks": [
                {"command": "State the loop sign and the behavior it predicts", "output": "e.g., 'Reinforcing: backlog grows exponentially because each delay increases future backlog'", "hint": "Count the '-' links: odd = balancing, even = reinforcing."},
                {"command": "Name the weakest loop organ (sensor, comparator, reference, effector)", "output": "e.g., 'Comparator: the target is ticket count, not resolution quality'", "hint": "Ask which organ, if fixed, would change the loop's behavior most."},
                {"command": "Describe your one-arrow intervention", "output": "e.g., 'Rewire the bonus from tickets-closed to reopen-rate; the reinforcing loop becomes balancing'", "hint": "The best interventions rewire structure, not people."}
            ],
            "debrief": "You turned a vague complaint into a testable loop diagram with named organs and a predicted behavior. Most organizational problems become solvable once drawn this way — the diagram is the diagnosis, and the rewired arrow is the prescription."
        },
        {
            "_id": "cyb-lab-extra2",
            "id": "cyb-lab-extra2",
            "title": "PID Tuning Thought Experiment",
            "domain_id": "feedback-systems",
            "objective": "Tune a hypothetical PID loop on paper, predicting the effect of each term change before 'applying' it.",
            "steps": [
                "Set the scene: a water-tank level controller. The tank drains unpredictably (disturbance), a pump fills it (effector), a float sensor reads level with a 5-second lag.",
                "Start with P-only control at moderate gain. Predict: what happens to steady-state error when the drain rate changes? What happens if you double the gain?",
                "Add integral action. Predict: what happens to the steady-state error? What new risk appears (hint: the 5-second sensor lag)?",
                "Add derivative action. Predict: how does it interact with the sensor lag and with measurement noise?",
                "Introduce integral windup: the pump saturates at max while the level stays low. Predict the overshoot when the drain stops, then design the anti-windup fix.",
                "Write your final tuning (P/I/D settings described qualitatively: low/medium/high) and justify each choice against the lag, the disturbance, and the saturation."
            ],
            "checks": [
                {"command": "Predict P-only behavior under changing drain", "output": "'Proportional leaves steady-state error that grows with drain rate; doubling gain halves error but risks oscillation via the 5s lag'", "hint": "P corrects proportional to current error only — it cannot eliminate persistent error."},
                {"command": "Name the risk integral adds with a laggy sensor", "output": "'Overshoot and oscillation: the integrator keeps accumulating during the 5s blind period'", "hint": "What does the integrator do while the sensor hasn't caught up?"},
                {"command": "State your anti-windup design", "output": "e.g., 'Freeze integration while the pump is saturated'", "hint": "Windup is the integrator accumulating error it cannot act on."}
            ],
            "debrief": "You reasoned through P, I, and D as distinct organs with distinct failure modes, and confronted the two classic PID pathologies — lag-induced oscillation and integral windup. Real tuning is this thought experiment plus patience: predict first, then touch the knobs."
        },
        {
            "_id": "cyb-lab-extra3",
            "id": "cyb-lab-extra3",
            "title": "Calculate Channel Capacity",
            "domain_id": "information",
            "objective": "Compute Shannon entropy and Shannon-Hartley capacity for three realistic cases, and use the results to judge a vendor claim.",
            "steps": [
                "Case A: a binary alarm that fires (1) 10% of the time and is silent (0) 90% of the time. Compute H = -(0.1*log2(0.1) + 0.9*log2(0.9)).",
                "Case B: a 4-symbol sensor code with probabilities 0.5, 0.25, 0.125, 0.125. Compute its entropy and compare with the 2 bits/symbol a fixed code would use.",
                "Case C: a 20 kHz radio channel at 20 dB SNR (power ratio 100). Compute C = 20000 * log2(101).",
                "A vendor claims their modem pushes 200 kbps through the Case C channel. Judge the claim against your computed capacity.",
                "For Case A, design the ideal coding insight: how many bits per alarm reading does the source coding theorem say you need, and what does that imply for a year's worth of readings?",
                "Write a two-sentence verdict a manager could understand: what the math allows, and what it forbids."
            ],
            "checks": [
                {"command": "Report Case A entropy", "output": "'H ~= 0.469 bits per reading (0.1*3.32 + 0.9*0.152)'", "hint": "-sum(p*log2(p)); log2(0.1) ~= -3.32, log2(0.9) ~= -0.152."},
                {"command": "Report Case C capacity and the vendor verdict", "output": "'C ~= 133 kbps; the 200 kbps claim violates the Shannon limit'", "hint": "log2(101) ~= 6.66; 20000 * 6.66 = ?"},
                {"command": "State the Case B compression opportunity", "output": "'H = 1.75 bits/symbol vs 2 fixed — ~12.5% compressible'", "hint": "0.5*1 + 0.25*2 + 0.125*3 + 0.125*3 = ?"}
            ],
            "debrief": "You computed entropy as surprise-per-symbol and capacity as a hard physical ceiling, then used the ceiling to falsify an impossible claim. That is the whole practical power of Shannon: numbers that say 'no' to datasheets."
        },
        {
            "_id": "cyb-lab-extra4",
            "id": "cyb-lab-extra4",
            "title": "Trace Information Flow",
            "domain_id": "information",
            "objective": "Audit how decision-relevant information actually travels through your team, and find where signal dies.",
            "steps": [
                "Pick one recurring decision (e.g., weekly prioritization, incident response, release go/no-go).",
                "Map the information path: who senses what, through which channel, to whom, with what delay — draw it as a chain.",
                "For each link, estimate the signal-to-noise ratio: how much of what arrives is decision-relevant vs noise?",
                "Apply Bateson's test to each report or dashboard on the path: did it change any decision in the last month? Mark the ones that failed.",
                "Find the narrowest point: the link with the worst SNR or the longest delay — that is your channel bottleneck.",
                "Propose one flow redesign: what gets cut, what gets a faster path, and what new signal the decision actually needs (requisite variety check)."
            ],
            "checks": [
                {"command": "Name the decision and its current information path", "output": "e.g., 'Release go/no-go: QA report -> Slack -> engineer skim -> gut-feel vote; 3-day delay'", "hint": "Follow one real recent decision, not the documented process."},
                {"command": "List reports that failed Bateson's test", "output": "e.g., 'The 40-metric dashboard: zero decisions changed in 6 weeks'", "hint": "If no decision changed, it carried no information — regardless of bit count."},
                {"command": "State your one flow redesign", "output": "e.g., 'Kill the dashboard; pipe the 3 decision metrics to the release channel with a 1-hour SLA'", "hint": "Cut noise, shorten the path, match variety to the decision."}
            ],
            "debrief": "You traced information as it actually flows — not as the org chart says — and applied both Shannon (SNR, delay, bottleneck) and Bateson (did it make a difference?). The redesign you proposed is an information-theoretic intervention, not just a process tweak."
        },
        {
            "_id": "cyb-lab-extra5",
            "id": "cyb-lab-extra5",
            "title": "Run a VSM Diagnosis",
            "domain_id": "modern-systems",
            "objective": "Audit a real organization against Beer's five systems and deliver a viability verdict with triage order.",
            "steps": [
                "Choose an organization you know well (your employer, a client, a volunteer group).",
                "Identify S1: list the operational units that directly do the work and serve the environment.",
                "Identify S2: find what coordinates the S1 units day-to-day (schedules, standards, shared protocols) — note oscillation where S2 is absent.",
                "Identify S3/S3*: find who bargains resources and holds accountability (S3), and whether anyone audits reality directly, bypassing reports (S3*).",
                "Identify S4 and S5: find the outward/future-scanning function (S4) and the identity-arbitration function (S5) — be brutal about whether they exist or are merely titled.",
                "Deliver the verdict: viable / viable-with-gaps / non-viable, the missing functions, the failure each gap predicts, and the triage order with reasons."
            ],
            "checks": [
                {"command": "List S1 through S5 as found (or missing)", "output": "e.g., 'S1 strong; S2 weak; S3 gut-feel; S3* absent; S4 absent; S5 nominal'", "hint": "Functions, not departments — a titled 'strategy team' that only reacts is not S4."},
                {"command": "State the viability verdict and one predicted failure", "output": "e.g., 'Viable today, blind tomorrow: missing S4 predicts strategic surprise within 18 months'", "hint": "Each missing function predicts a specific failure mode."},
                {"command": "Give the triage order", "output": "e.g., 'S5 identity first, then S3/S2, then S4 — because control needs a target before intelligence matters'", "hint": "Order by dependency: what must exist before the next fix can aim at anything?"}
            ],
            "debrief": "You performed Beer's viability audit: functions instead of boxes, recursion-aware, verdict-first. The triage order is the real skill — viability is not a score, it is a sequence of repairs ordered by what depends on what."
        },
        {
            "_id": "cyb-lab-extra6",
            "id": "cyb-lab-extra6",
            "title": "Build a Causal Loop Diagram",
            "domain_id": "modern-systems",
            "objective": "Construct a multi-loop causal diagram of a complex problem, finding at least one reinforcing and one balancing loop plus a delay.",
            "steps": [
                "Choose a persistent problem: customer churn, technical debt growth, burnout cycles, or traffic congestion.",
                "Brainstorm 8-12 variables as measurable nouns (e.g., 'overtime hours,' 'defect rate') — no vague nouns like 'problems.'",
                "Connect variables with causal arrows, labeling each + or - and noting the evidence or reasoning for each link.",
                "Find closed loops: trace around until you return to the start. Identify at least one reinforcing (even number of - links) and one balancing loop (odd number).",
                "Mark every significant delay with a double-hash on the arrow, and note which loop dominates under current conditions.",
                "Write the story the diagram tells in three sentences, then name the highest-leverage intervention (Meadows: prefer goals and loop structure over parameters)."
            ],
            "checks": [
                {"command": "Name one reinforcing and one balancing loop from your diagram", "output": "e.g., 'R: overtime -> fatigue -> defects -> rework -> more overtime; B: overtime -> hiring pressure -> new staff -> less overtime (delayed)'", "hint": "Trace closed paths; count the '-' links on each."},
                {"command": "Mark the dominant loop and the key delay", "output": "e.g., 'R dominates: the hiring delay (6 months) lets the burnout loop run unchecked'", "hint": "The loop with the shortest delay usually dominates early."},
                {"command": "State the highest-leverage intervention", "output": "e.g., 'Cap overtime (loop structure) rather than wellness posters (parameter)'", "hint": "Meadows: change the loop or the goal, not the poster."}
            ],
            "debrief": "You built a genuine multi-loop model with delays and dominance — the core artifact of systems thinking. The three-sentence story is the test: if the diagram cannot be narrated, it is decoration; if it can, it is a decision tool."
        },
        {
            "_id": "cyb-lab-extra7",
            "id": "cyb-lab-extra7",
            "title": "Design a Negative Feedback Intervention",
            "domain_id": "cybernetics-in-tech",
            "objective": "Design a complete autoscaling policy as a control loop: sensor, comparator, effector, delays, damping, and feedforward.",
            "steps": [
                "Define the controlled variable and its reference: what exactly are you holding stable (e.g., p99 latency < 300ms, or CPU ~60%)? Write the setpoint explicitly.",
                "Design the sensor: what metric, sampled how often, smoothed over what window — and what is the measurement delay?",
                "Design the comparator: scale-up and scale-down thresholds with a deadband (hysteresis) between them; justify the deadband width against the warmup delay.",
                "Design the effector and its limits: step size per action, cooldown periods matched to the warmup delay, min/max instance bounds.",
                "Add feedforward: what predictable disturbances (deploy schedules, marketing events, cron jobs) can you scale for before they hit?",
                "Stress-test on paper: a 10x traffic spike in 2 minutes with an 8-minute warmup — trace what your loop does minute by minute and find where it still oscillates or saturates."
            ],
            "checks": [
                {"command": "State sensor, comparator, and effector with numbers", "output": "e.g., 'Sensor: p99 latency, 1-min avg; comparator: scale up >400ms, down <150ms; effector: +2/-1 instances, 10-min cooldown'", "hint": "Every organ needs numbers: sample window, thresholds, step sizes, cooldowns."},
                {"command": "Justify the deadband and cooldown against the warmup delay", "output": "e.g., 'Cooldown 10 min > 8-min warmup so in-flight capacity is counted before the next decision'", "hint": "Corrections must wait for prior corrections to take effect."},
                {"command": "Describe the 10x-spike trace outcome", "output": "e.g., 'Feedforward pre-scales from the event calendar; feedback handles the residual; saturation at max bound triggers the page'", "hint": "No loop handles everything — name what saturates and what happens then."}
            ],
            "debrief": "You designed autoscaling as control theory, not as config YAML: explicit setpoint, deadband against delay, cooldowns respecting actuation lag, and feedforward for the predictable. The paper stress-test is the difference between a policy and a hope."
        },
        {
            "_id": "cyb-lab-extra8",
            "id": "cyb-lab-extra8",
            "title": "Audit an ML Training Loop",
            "domain_id": "cybernetics-in-tech",
            "objective": "Audit a model training setup as nested feedback loops and write the ship/no-ship decision rule.",
            "steps": [
                "Draw the inner loop: gradient descent minimizing training loss — label the error signal, the gain (learning rate), and the actuator (weight updates).",
                "Draw the outer loop: validation monitoring generalization — label its error signal (val loss / val metric) and its actuators (early stopping, regularization, data changes).",
                "Define divergence criteria: exactly what pattern in the two curves means 'memorizing, not learning'?",
                "Write the ship rule: the precise conditions under which the outer loop permits deployment (e.g., 'val metric within 2% of best for 3 evals, train-val gap < 5%').",
                "Add the production loop: what post-deployment signal (drift detection, live accuracy sampling) continues the outer loop after shipping, and what triggers rollback or retraining?",
                "Red-team your rule: describe a scenario where all your gates pass but the model still fails in production — what loop is missing?"
            ],
            "checks": [
                {"command": "State the inner and outer loop error signals", "output": "'Inner: training loss gradient; outer: validation loss/metric trend'", "hint": "Each loop needs its own error signal and its own actuator."},
                {"command": "Write the ship rule precisely", "output": "e.g., 'Ship iff val metric >= best-2% for 3 consecutive evals AND train-val gap < 5%'", "hint": "A rule you cannot evaluate mechanically is not a rule."},
                {"command": "Name the red-team failure mode", "output": "e.g., 'Training-serving skew: validation data no longer matches production distribution'", "hint": "The outer loop is only as good as its sensor — validation data."}
            ],
            "debrief": "You separated the loop that optimizes from the loop that judges, wrote a mechanical ship rule, and extended the loop into production. The red-team step is the cybernetic habit: every loop has a sensor blind spot — name it before reality does."
        },
        {
            "_id": "cyb-lab-extra9",
            "id": "cyb-lab-extra9",
            "title": "Dissect a Historical Failure",
            "domain_id": "case-studies",
            "objective": "Apply the five-lens case method to Three Mile Island and produce a one-page autopsy.",
            "steps": [
                "Lens 1 — anatomy: list TMI's sensors, comparators, references, and effectors in the control room; mark which reported commands vs states.",
                "Lens 2 — loops: identify the physical positive-feedback risk (core heat vs coolant) and the operators' balancing intent; show how false feedback inverted the intended correction.",
                "Lens 3 — delay/timescale: note the 2+ hour duration of the stuck-open valve vs the operators' mental model of a transient event.",
                "Lens 4 — variety: count the disturbance (a novel plant state) against the operators' trained response repertoire; find the gap.",
                "Lens 5 — observer: describe the operators' information state minute by minute vs the physical state; show where false feedback made the wrong action reasonable.",
                "Write the one-page autopsy: verdict, the single most important architectural fix, and one lesson that transfers to your own field."
            ],
            "checks": [
                {"command": "Name the command-vs-state sensor confusion", "output": "'Valve light reported solenoid command, not stem position; pressurizer level reported bubble-distorted level, not inventory'", "hint": "Two instruments, two lies — find both."},
                {"command": "State the architectural fix", "output": "'Sensors must report physical state; add diverse, independent sensing on safety-critical variables'", "hint": "Fix the loop, not the operators."},
                {"command": "Transfer one lesson to your field", "output": "e.g., 'Our deploy dashboard shows \"restart sent,\" not \"service healthy\" — same confusion'", "hint": "The pattern generalizes; find your instance."}
            ],
            "debrief": "You ran a full five-lens autopsy and extracted a transferable design rule. The discipline — reconstructing the actors' information state rather than judging from hindsight — is what makes case study a method instead of a story."
        },
        {
            "_id": "cyb-lab-extra10",
            "id": "cyb-lab-extra10",
            "title": "Compare Two Cases: Toyota vs Three Mile Island",
            "domain_id": "case-studies",
            "objective": "Contrast a feedback success (Toyota's andon) with a feedback failure (TMI) on shared axes to extract portable design principles.",
            "steps": [
                "Set the comparative axes: (1) sensor truthfulness, (2) feedback delay, (3) effector authority, (4) operator mental models, (5) response to the unexpected.",
                "Score TMI on each axis in one sentence per axis, citing the case facts.",
                "Score Toyota's andon system on each axis in one sentence per axis, citing the case facts.",
                "Identify the axis where the two cases differ most sharply, and explain why that axis dominates the outcomes.",
                "Synthesize: write three portable design principles that hold across both cases (e.g., 'Feedback must report state, not intention').",
                "Apply: take one principle and sketch how you would implement it in a system you work with this month."
            ],
            "checks": [
                {"command": "State the sharpest axis of difference", "output": "e.g., 'Sensor truthfulness: andon senses the actual defect; TMI's light sensed the command'", "hint": "Which single axis, if swapped, would most change each outcome?"},
                {"command": "List your three portable principles", "output": "e.g., '1. Sense state, not commands. 2. Shorten delay before adding authority. 3. Train models of physics, not just procedures.'", "hint": "Principles must survive translation to a different domain."},
                {"command": "Sketch one implementation for your own system", "output": "e.g., 'Replace deploy \"success\" messages with health-check-verified state before marking green'", "hint": "Concrete, this month, one system."}
            ],
            "debrief": "Comparison on shared axes turned two stories into engineering principles. The andon/TMI pair is ideal because they are near-mirror images: same loop anatomy, opposite truthfulness — which is why the principles you extracted will travel."
        },
        {
            "_id": "cyb-lab-extra11",
            "id": "cyb-lab-extra11",
            "title": "Identify Goodhart Cases",
            "domain_id": "second-order",
            "objective": "Hunt down three live Goodhart/Campbell effects in your environment and redesign one metric to resist corruption.",
            "steps": [
                "List five metrics you are judged by (or that judge others): KPIs, OKRs, ratings, scores, counts.",
                "For each, ask: if someone optimized this metric ruthlessly while harming the underlying goal, what would they do? Write the gaming strategy explicitly.",
                "Score each metric 1-5 on corruptibility: how easily does the gaming strategy succeed, and how invisible is it?",
                "Pick the most corruptible metric. Diagnose the loop: what is the measure, what is the goal, and where does the measure diverge from the goal?",
                "Redesign it using Goodhart resistance: pair it with a counter-metric, rotate or randomize measurement, measure outcomes not activities, or return judgment to informed human review.",
                "Write the before/after: the old metric, its gaming strategy, and why your redesign is harder to game without doing the real work."
            ],
            "checks": [
                {"command": "Name three metrics and their gaming strategies", "output": "e.g., 'Tickets closed -> close with shallow fixes; lines of code -> verbose code; NPS -> beg for 10s'", "hint": "Be the adversary: how would you cheat each metric while looking good?"},
                {"command": "Diagnose the worst one: measure vs goal divergence", "output": "e.g., 'AHT measures speed; the goal is resolution — they diverge on complex calls'", "hint": "The divergence point is where the redesign must aim."},
                {"command": "State the redesigned metric and its resistance logic", "output": "e.g., 'Replace AHT with resolution-rate + sampled call review; gaming requires actually resolving'", "hint": "A good redesign makes cheating equivalent to doing the job."}
            ],
            "debrief": "You learned to see metrics as adversarial interfaces: every number you publish is an optimization target for someone. The redesign skill — making the metric hard to game without doing the work — is second-order cybernetics applied to management."
        },
        {
            "_id": "cyb-lab-extra12",
            "id": "cyb-lab-extra12",
            "title": "Model a Black Box",
            "domain_id": "second-order",
            "objective": "Build a behavioral model of an opaque system using only controlled input variation, and state the model's limits honestly.",
            "steps": [
                "Choose a black box: a vendor API, a colleague's approval process, a smart appliance, a recommendation feed — anything whose internals you cannot see.",
                "Enumerate the inputs you can manipulate and the outputs you can observe. Fix all inputs but one.",
                "Vary that input across at least 5 distinct values, recording the output each time in a table. Repeat for a second input.",
                "Look for the transfer pattern: thresholds, proportional regions, saturation, delays, hysteresis — describe it in plain language plus a sketch.",
                "Make one prediction about an untested input combination, then test it. Record whether the model held.",
                "Write the model's charter of limits: the input ranges tested, the conditions not tested, and where you expect the model to break (second-order honesty: your probing may have changed the box, e.g., rate limits, learning effects)."
            ],
            "checks": [
                {"command": "Present your input-output table (5+ values, two inputs)", "output": "e.g., 'API latency vs payload size: 1KB->80ms, 10KB->95ms, 100KB->400ms, 1MB->timeout...'", "hint": "One input at a time; everything else fixed."},
                {"command": "State your prediction and the test result", "output": "e.g., 'Predicted timeout above 500KB; tested 750KB -> timeout confirmed'", "hint": "A model that cannot predict is a diary, not a model."},
                {"command": "Write two limits of your model", "output": "e.g., 'Untested under concurrent load; my probing may have triggered rate limiting, changing the box'", "hint": "The observer clause: did your experiment perturb the system?"}
            ],
            "debrief": "You did Ashby's black-box method end to end: controlled variation, transfer pattern, prediction, and an honest charter of limits including your own observer effect. That last clause is what separates cybernetic modeling from curve-fitting."
        }
    ]
}

