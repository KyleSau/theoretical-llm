# 17. Risks and open questions

[Back to the overview](../README.md) · Previous: [16. Timeline](16-timeline.md) · Next: [18. Glossary](18-glossary.md)

The rest of this plan describes the best case. This chapter lists what would break it, how you would know early, and what the plan does about each. It ends with the questions that paper cannot answer.

## 17.1 The five that matter most

| # | Risk | Why it is at the top |
|---|---|---|
| 1 | **Power arrives late** | Everything else can be bought faster with money. A gigawatt of firm power cannot. A year's slip on interconnection or turbines moves the whole program a year |
| 2 | **The model crosses a dangerous-capability threshold before safeguards or security are ready** | The framework's answer is to pause. That is the correct outcome, and it can cost months |
| 3 | **The weights are stolen** | It removes every run-time safeguard and hands the investment to someone else, permanently |
| 4 | **Scale does not pay off as predicted** | The scaling law is an extrapolation two orders of magnitude past where it was measured. If a 10T model is only slightly better than a 1T model, the economics collapse |
| 5 | **The legal ground under training data shifts** | An adverse appellate ruling or a regulator's order could remove a large part of the corpus or attach a large price to it |

## 17.2 Risk register

Likelihood and impact are rated low (L), medium (M) or high (H) for the best-case plan.

### Power, site and construction

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Grid interconnection slips | H | H | Utility study milestones missed | On-site generation sized to carry the full load; second candidate site kept warm until month 4 |
| Turbine, transformer or switchgear lead times | H | H | Factory slot dates | Order in month 1, before the site is final; accept mixed equipment; batteries to cover gaps |
| Permits, local opposition, moratoria | M | H | Hearing calendar, press | Closed-loop cooling with near-zero water draw, noise limits, local hiring, community benefit agreement, published emissions plan |
| Skilled-trade shortage | H | M | Bid coverage, overtime rates | Travelling crews, on-site housing, apprenticeship program from month 1 |
| Coolant leak or cooling-loop failure takes out a hall | M | M | Leak sensors, pressure trends | Leak detection at every rack, isolation valves, N+1 pumps and heat exchangers, drip management, tested emergency shutdown |
| Training-load power swings stress generators or the grid | M | H | Measured oscillation during pilot runs | Rack-level energy buffers, site batteries, software ramp limits, agreed limits with the utility |
| Battery or fuel fire | L | H | Thermal monitoring | Separation distances, suppression, emergency planning with local responders |

### Supply chain

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Accelerator allocation shortfall or delay | M | H | Vendor delivery schedule | Contracted allocation with penalties; accept one generation older for early halls; second-source evaluation |
| Memory, optics or liquid-cooling parts shortage | M | M | Integrator lead times | Forward purchase; qualify two suppliers per part |
| Export controls, tariffs, sanctions | M | M | Policy tracking | Site and supplier choices that stay inside one trade bloc |
| Hardware obsolescence | H | M | Vendor roadmaps | Expected: the next rack generation roughly doubles performance per watt. Halls are built for higher density than the first racks need; the first-generation racks move to inference |

### Training and model

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Instability at unprecedented scale (divergence, loss spikes, expert collapse) | M | H | Loss curves, gradient statistics, router load balance | Scaling ladder of pilots; conservative optimizer settings early; frequent checkpoints; automatic rollback |
| Silent data corruption in hardware | H | M | Checksum mismatches, replica disagreement | Periodic recomputation on a second device, checksummed checkpoints, quarantine of suspect nodes |
| Low-precision arithmetic harms quality | M | M | Comparison against 16-bit reference runs at small scale | Mixed precision with sensitive layers kept at higher precision; fall back at a known compute cost |
| Fault tolerance falls short and uptime is under 85% | M | M | Hours lost per week | Elastic data-parallel groups, hot spares, in-memory checkpoint replicas ([chapter 8](08-training-stack-and-run.md)) |
| Scaling returns are smaller than predicted | M | H | Pilot results at 100B and 1T against the fitted curve | Decision point after the pilot: proceed, resize, or redirect compute to post-training |
| Data quality ceiling: the web is filling with machine-written text | H | M | Quality-classifier yield per crawl month | Weight toward pre-2023 archives, licensed and human-commissioned data; machine-text detection |
| Reward hacking in reinforcement learning | H | M | Gap between training reward and held-out graders | Held-out graders, human audits, tamper penalties |
| Evaluations saturate or leak | H | M | Scores at ceiling; canary strings found | Private, rotating evaluation sets |

### Data and legal

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Adverse copyright ruling or statute | M | H | Appellate dockets, legislative calendars | Provenance ledger for every token; licensed-first posture; ability to rebuild the corpus without any given source class |
| Licensing costs escalate | H | M | Deal terms across the industry | Long-term agreements signed early; a mix that does not depend on any one licensor |
| Opt-out wave shrinks the open web | H | M | Blocked share of crawl attempts | Pay-per-crawl budget; direct publisher agreements |
| Privacy enforcement | M | M | Regulator guidance | Privacy filtering before training; regional processing rules; a deletion path |
| Data poisoning | M | H | Anomaly detection; backdoor scans on checkpoints | Source trust tiers, per-domain caps, behavioral scans |

### Safety

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Dangerous-capability threshold crossed before safeguards are ready | M | H | Checkpoint evaluations trending toward a threshold | Safeguard and security work started a year ahead; a pre-agreed pause |
| Universal jailbreak after launch | H | M | Bounty reports, abuse monitoring | Classifier hot-fix within 24 hours; rollback path |
| Serious misalignment found late | L | H | Alignment audits, production anomalies | Evaluation during training; staged release; rollback |
| Agent causes real-world damage | M | M | Incident reports | Permission tiers, confirmation for irreversible actions, sandboxing |
| Over-refusal makes the product unusable | M | M | False-refusal metrics, user feedback | Paired metrics; refusal budget; fast policy iteration |
| Harm to vulnerable users | M | H | Crisis-conversation sampling | Safe-messaging protocol, age assurance, external clinical advisers |

### Security

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Weight theft by a state-level actor | M | H | Egress anomalies, canary triggers | SL4 controls before flagship weights exist ([chapter 13](13-security.md)) |
| Insider theft or sabotage | M | H | Access-pattern analytics | Two-person rule, no plaintext access, separation of duties |
| Supply-chain implant in hardware or software | L | H | Attestation failures, teardown findings | Attestation, vetted integrators, reproducible builds |
| Attack on facility control systems | M | H | Operational-technology network monitoring | Isolated control networks, manual overrides, drills |
| Model extraction through the API | H | M | Harvesting-pattern detection | Rate limits, verification, legal terms |

### People, money and market

| Risk | L | I | Early warning | Mitigation |
|---|---|---|---|---|
| Cannot hire the 50 people who matter | M | H | Offer acceptance rate | Mission, compute access, compensation, a credible safety culture |
| Loss of key staff mid-run | M | M | Attrition signals | Documentation, deputies for every critical role, retention structure |
| Cost overrun | H | M | Monthly variance | 15% contingency; phased halls so spend follows proof |
| Demand falls short or prices collapse | M | H | Preview usage, competitor pricing | Distilled tiers for volume; campus can sell capacity |
| Financing dries up mid-build | L | H | Capital-market conditions | Committed financing before ground-breaking; phase gates |
| New regulation requires redesign | M | M | Consultation papers | Build to the strictest existing regime from day one |

## 17.3 Decision points

The plan is not a single bet. These are the moments where evidence can change it.

| When | Evidence | Options |
|---|---|---|
| Month 4 | Power commitments in writing | Proceed at site A; switch to site B; phase to 500 MW first |
| Month 9 | First working model at about 100B parameters on rented compute | Confirm the recipe; fix the data mix |
| Month 12 | Corpus v1 measured: real token counts and quality | Resize the token budget and therefore the model |
| Month 16 | Pilot model at about 1T parameters: does it sit on the predicted curve? | Proceed to 10T; choose sparse or dense; or stop at a smaller size and invest in post-training |
| Month 20 | Dress rehearsal at quarter scale: uptime and throughput | Start the flagship; or fix fault tolerance first |
| During the flagship run | Checkpoint evaluations against capability thresholds | Continue; add safeguards; pause |
| Month 30 | Safety case for limited preview | Release; restrict; hold |

## 17.4 Open questions

These cannot be settled by planning. Each has an experiment attached.

| Question | What would answer it |
|---|---|
| Does a 10T-parameter model beat a 2T model by enough to justify the cost? | The scaling ladder: 10B, 100B and 1T pilots, extrapolated with error bars |
| Sparse or dense at this scale? | Matched-compute comparison at 100B and 1T |
| How much of final quality comes from post-training? | Hold the base model fixed and vary the reinforcement-learning budget |
| Is video worth 60T tokens of the budget? | Ablation at pilot scale: text-only against multimodal, scored on text tasks |
| Is 8-bit and 4-bit training stable at 10T parameters? | Precision sweeps on the pilot; reference runs at 16-bit |
| Can a single job hold 85% uptime across 155,000 GPUs? | The dress rehearsal |
| Will the grid or the turbines actually arrive on schedule? | Only time; hence two power paths |
| Will the law allow training on the open web in three years? | Court and legislative outcomes; hence provenance and a licensed-first corpus |
| Will the finished model be safe to release at all? | The evaluations in [chapter 11](11-evaluation-and-red-teaming.md). The plan has to be willing to hear "no" |

## 17.5 What this exercise leaves out

- **Algorithmic progress.** Architectures and training methods improve every year. A team starting now would not build exactly this design three years from now.
- **Competition.** Others are building at the same scale. Being second with a better model is fine; being second with the same model is expensive.
- **The downside of success.** A model that crosses the upper thresholds in chapter 10 is a different kind of responsibility from a product launch. The governance in [chapter 14](14-people-and-organization.md) exists for that case.
