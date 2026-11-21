# 1. Scope and assumptions

[Back to the overview](../README.md) · Next: [2. Data sources](02-data-sources.md)

## 1.1 What this is

A written plan for taking an organization from no model to a released frontier model, with every major decision sized: data, model, hardware, campus, training, fine-tuning, safeguards, people, money, time.

It is a thought experiment. Nothing was collected, purchased, built or trained to produce it. It is meant to be read the way an engineering feasibility study is read: to see what the pieces are, how big each one is, and which ones are hard.

## 1.2 The goal

| Aspect | Target |
|---|---|
| Kind of model | General-purpose, multimodal in (text, code, images, audio, video), text and code out |
| Capability | Competitive with the best models of its release year at reasoning, coding and long autonomous tasks |
| Form | A flagship plus two smaller distilled tiers |
| Context window | 1 million tokens |
| Delivery | Served by the lab from its own hardware; weights are not released |
| Safety posture | Published framework with capability thresholds and binding release gates |

## 1.3 Ground rules

1. **Best case means money is not the constraint.** Physics, supply chains, law and the calendar still are.
2. **Technology as of November 2026.** No assumed breakthroughs. The hardware is what is shipping in volume today.
3. **Lawful data only.** Open, licensed, commissioned or synthetic. No pirated libraries, no bypassing access controls ([chapter 2](02-data-sources.md)).
4. **Safety gates are binding.** If an evaluation says stop, the plan stops ([chapter 10](10-safety-guardrails-and-refusals.md)).
5. **One campus.** A single 1 GW site, so that every number can be followed from the wall socket to the token.
6. **Honest derating.** Vendor peak figures are never used as achieved figures.

## 1.4 The assumptions that matter

Confidence is this plan's own rating: high means a published figure from a primary source, medium means a published range or an analyst estimate, low means a judgment call.

| Assumption | Value | Basis | Confidence | If it is wrong |
|---|---|---|---|---|
| IT load | 1,000 MW | Design choice; largest sites today are 0.8 to 1.0 GW | Plan | Everything scales roughly linearly |
| Rack | Vera Rubin NVL72: 72 GPUs, 288 GB each | Vendor product page | High | |
| Power per rack position | 250 kW including network share | Vendor reference design (about 2 MW per 8 racks); analysts put the rack alone at 180 to 227 kW | Medium | Rack count moves by up to 15% |
| **Sustained training rate** | **2.5 PF per GPU** | Chained from measured runs on earlier hardware and the first benchmark of this generation ([chapter 5](05-compute-cluster.md)) | **Low to medium** | At 1.2 PF the flagship run takes five months instead of ten weeks |
| Uptime of the training job | 85% | A published 16,000-GPU run kept over 90% | Medium | Run length scales inversely |
| Scaling law | About 21.6 tokens per parameter; compute = 6 x parameters x tokens | Chinchilla paper's projection table | Medium at this scale | Model size is re-chosen after the pilot |
| **Usable corpus** | **216T tokens** | Sum of sources in chapter 2; four times the largest disclosed training set | **Low to medium** | The model shrinks in proportion |
| Active share of the sparse model | About 16% | Design choice; published models use 3 to 4% | Plan | A dial, set after pilots |
| PUE | 1.15 annual average; 1.3 nameplate ratio | Published modeling value 1.14; built campuses run 1.3 to 1.46 nameplate | Medium | Energy and electrical plant scale with it |
| Electricity price | $68/MWh | 2026 Texas industrial average | Medium | $0.5B to $1.0B a year across US regions |
| Rack price | $8.5M | Analyst range $6M to $9.1M | Medium | Capital moves by -$9B to +$2B |
| Facility cost | $17.5M per MW | Two independent 2026 sources: $16M to $19M | Medium | ±$1.5B |
| Serving throughput | 15% of the dense 4-bit peak; one-third of the memory-bandwidth step rate | Judgment | Low | Cost per token scales inversely |
| Staff | 2,960 | Built bottom-up; leading labs have 4,500 to 5,600 across many products | Medium | People are about 5% of program cost |
| Schedule | 32 months | Every long-lead item on time | Low | 38 to 46 months is the realistic range |

Two of these carry most of the uncertainty: how fast the hardware really trains, and how much good data really exists. Both are settled by measurement early in the program, at the pilot (month 16) and at corpus v1 (month 12).

## 1.5 Units and conventions

| Convention | Meaning |
|---|---|
| T, B, M | Trillion, billion, million |
| FLOPs | A count of operations (the size of a job) |
| FLOP/s, FLOPS | Operations per second (the speed of hardware) |
| PF, EF | PetaFLOPS (10^15) and exaFLOPS (10^18). 1 PF = 1,000 teraFLOPS |
| Dense | Every parameter used for every token |
| Sparse | A mixture-of-experts model; "active" parameters are the ones used for a given token |
| Headline or peak | A vendor's best-case figure |
| Sustained | What a real job achieves while it is running |
| Month N | N months after funding; the illustrative calendar starts January 2027 |
| Dollars | 2026 US dollars |

[Chapter 18](18-glossary.md) defines every term in plain language.

## 1.6 Out of scope

- **A business case.** Revenue, pricing strategy and competition are mentioned only for scale.
- **Financing.** Interest and deal structure are excluded and noted in [chapter 15](15-budget.md).
- **A named site.** Regions are compared; no location is chosen.
- **Research novelty.** The plan uses published techniques. A real lab's edge is in what is not published.
- **Low-level performance engineering.** Kernel and compiler tuning is acknowledged as valuable and left to measurement on real hardware.
- **Geopolitics.** Export controls and trade policy are treated as risks, not modeled.

## 1.7 How the plan was made

| Step | What was done |
|---|---|
| Research | Four passes on 21 November 2026: accelerator hardware; data-center power, cooling and cost; training-data sources and law; model scale, safety practice and regulation. Each returned figures with sources and a verified or reported flag |
| Calculator | [`calc/sizing.py`](../calc/sizing.py) holds every assumption in one block and derives every number in the chapters |
| Correction | The first draft used the vendor's 4-bit headline with an optimistic utilization and a lower rack power. Research replaced both: sustained compute fell by a factor of about 2.7 and the rack count by 10%. The chapters are written on the corrected figures |
| Checks | Diagrams are validated by rendering them; charts are generated from the calculator, not drawn by hand |

## 1.8 What "best case" hides

A best-case plan is a list of things that all have to go right. [Chapter 17](17-risks-and-open-questions.md) lists what goes wrong, and [chapter 16](16-timeline.md) gives the realistic schedule beside the best one. The four assumptions most likely to fail are, in order: firm power on time, the sustained training rate, the size of the lawful corpus, and reaching security level 4 before the weights exist.
