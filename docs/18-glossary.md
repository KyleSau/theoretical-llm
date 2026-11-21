# 18. Glossary

Plain-language definitions for the units and terms used across the plan. Where a term has a number attached in this plan, the number is given so you can see the scale.

[Back to the overview](../README.md) · Previous: [17. Risks and open questions](17-risks-and-open-questions.md) · Next: [19. Sources](19-sources.md)

## Units of compute

| Term | Meaning | In this plan |
|---|---|---|
| FLOP | One floating-point operation: a single add or multiply. | A full training run is counted in total FLOPs. |
| FLOPS (FLOP/s) | FLOPs per second: how fast hardware computes. | Rates for a GPU, a rack, the campus. |
| teraFLOPS (TFLOPS) | 10^12 FLOPS, a trillion operations a second. | A high-end gaming GPU is tens of TFLOPS. |
| petaFLOPS (PF) | 10^15 FLOPS = 1,000 TFLOPS. | One training GPU here is rated in tens of PF. |
| exaFLOPS (EF) | 10^18 FLOPS = 1,000,000 TFLOPS. | One rack is rated in EF. |
| zettaFLOPS (ZF) | 10^21 FLOPS = one billion TFLOPS. | The whole campus is rated in ZF. |
| Headline (peak) FLOPS | The vendor's best-case figure at its lowest-precision number format. | Never achieved in training; see MFU. |
| MFU | Model FLOPs utilization: useful model arithmetic divided by what the hardware could theoretically do. | Real runs report 20 to 55% of the 16-bit peak. |
| Precision (FP4, FP8, BF16, FP32) | How many bits each number uses. Fewer bits is faster and smaller but less exact. | Training mostly at 8 and 16 bits, serving at 4 to 8. |

## Units of model and data

| Term | Meaning | In this plan |
|---|---|---|
| Parameter | One learned number (a weight) in the network. | About 10 trillion in the flagship. |
| Total vs active parameters | In a mixture-of-experts model only some weights are used for each token. Total is what you store; active is what you compute. | About 10T total, 1.6T active. |
| Token | The unit of text a model reads and writes: a word piece, on average about 4 characters or 0.75 English words. Images, audio and video are also cut into tokens. | 216 trillion training tokens. |
| Context window | How many tokens the model can attend to at once. | 1 million tokens at launch. |
| Tokens per second, training | How many tokens the cluster pushes through forward and backward passes each second. | About 41 million for the flagship run. |
| Tokens per second, inference | How fast the finished model writes for one user (per stream), or for everyone at once (throughput). | About 90 per stream; about 120,000 per rack. |
| Epoch | One full pass over a dataset. | Most data is seen once; the best text three times. |
| Checkpoint | A saved copy of the model (and optionally the optimizer state) so training can resume. | About 20 TB weights only, about 100 TB full. |

## Model and training terms

| Term | Meaning |
|---|---|
| Transformer | The neural-network architecture behind modern language models: stacked layers of attention and feed-forward blocks. |
| Decoder-only | A transformer that predicts the next token given all previous ones. The standard design for LLMs. |
| Attention | The mechanism that lets each token look at every earlier token in the context. |
| Mixture of experts (MoE) | A layer design with many feed-forward "experts" where a small router picks a few per token. Capacity grows without growing per-token compute in proportion. |
| Pretraining | The first, largest phase: predict the next token over a vast corpus. Produces a base model that knows a great deal but is not yet an assistant. |
| Post-training | Everything after pretraining that turns a base model into a product: supervised fine-tuning, preference training, reinforcement learning, safety training. |
| Fine-tuning | Continuing training on a narrower dataset to change behavior. |
| SFT | Supervised fine-tuning: train on example conversations that show the wanted behavior. |
| RLHF | Reinforcement learning from human feedback: people compare outputs, a reward model learns their preferences, the model is trained to score well. |
| RL with verifiable rewards | Reinforcement learning where a program checks the answer (tests pass, the proof verifies, the number is right). |
| Distillation | Training a smaller "student" model to imitate a larger "teacher". |
| Quantization | Storing weights in fewer bits for cheaper, faster inference. |
| LoRA / adapters | Small add-on weight matrices that customize a model without retraining all of it. |
| Scaling law | An empirical rule relating model size, data and compute to quality. The "Chinchilla" result says a compute-optimal model wants about 20 training tokens per parameter. |
| `C = 6 N D` | The standard estimate of training compute: FLOPs is about 6 times parameters times tokens. Inference is about 2 N per token. |
| Loss | The number training pushes down: how surprised the model is by the true next token. |
| Optimizer (AdamW) | The algorithm that turns gradients into weight updates. It keeps two extra numbers per weight, which is why a full checkpoint is several times larger than the weights. |
| Parallelism (data, tensor, pipeline, expert) | The ways one model is spread across many GPUs: copies of the model on different data, single matrices split across GPUs, layers split into stages, experts placed on different GPUs. |

## Hardware and data-center terms

| Term | Meaning |
|---|---|
| GPU / accelerator | The chip that does the matrix arithmetic. |
| HBM | High-bandwidth memory stacked next to the GPU. Model weights must fit in it. |
| Rack-scale system | A rack sold as one computer: dozens of GPUs, CPUs, switches, power and liquid cooling wired at the factory. |
| Scale-up network | The very fast links between GPUs inside a rack (for example NVLink). |
| Scale-out (backend) network | The fabric that joins racks into one cluster (Ethernet or InfiniBand at 800 Gbit/s and up). |
| Frontend network | The ordinary network for storage, management and users. |
| Fat tree | A switch topology with as much capacity going up as coming down, so any GPU can talk to any other at full speed. |
| Co-packaged optics (CPO) | Putting the lasers and optics inside the switch package, which cuts power and failure points. |
| DPU / SmartNIC | A network card with its own processor that handles isolation, storage and security offload. |
| MW / GW | Megawatt and gigawatt: units of power. 1 GW = 1,000 MW, roughly a large nuclear reactor. |
| MWh / TWh | Units of energy. 1 TWh = 1,000,000 MWh. |
| IT load | Power drawn by the computers themselves, excluding cooling and electrical losses. |
| PUE | Power usage effectiveness: total facility power divided by IT power. 1.0 is perfect. |
| WUE | Water usage effectiveness: liters of water consumed per kWh of IT energy. |
| Direct-to-chip liquid cooling | Coolant pumped through cold plates bolted to the chips. |
| CDU | Coolant distribution unit: the pump and heat exchanger between the rack loop and the building loop. |
| Dry cooler | A big radiator with fans that rejects heat to outside air without evaporating water. |
| UPS / BESS | Uninterruptible power supply and battery energy storage system. |
| 800 VDC | Distributing power to racks as 800-volt direct current instead of low-voltage alternating current, to cut copper and conversion losses at megawatt-per-rack densities. |
| PPA | Power purchase agreement: a long-term contract to buy electricity from a specific plant. |
| Behind-the-meter | Generation built on the site and wired directly to it, not through the public grid. |

## Data terms

| Term | Meaning |
|---|---|
| Crawl | Systematically fetching web pages. |
| robots.txt | The file where a website states which crawlers may fetch what (RFC 9309). |
| WARC | The standard archive file format for crawled web content. |
| Deduplication | Removing exact and near-identical copies. |
| PII | Personally identifiable information. |
| TDM | Text and data mining. The EU copyright exception that covers it lets rights holders opt out. |
| Fair use | The US doctrine under which some unlicensed uses of copyrighted work are lawful. |
| Synthetic data | Training data generated by models or programs rather than collected from people. |
| Provenance | The recorded origin and license of every item of data. |

## Safety and security terms

| Term | Meaning |
|---|---|
| Guardrail | Any mechanism that keeps a model's behavior inside policy: training, classifiers, permissions, monitoring. |
| Refusal | The model declining a request, ideally narrowly and with a useful alternative. |
| Over-refusal | Declining a request that was actually fine. Measured and minimized alongside harmful compliance. |
| Jailbreak | A prompt designed to make a model ignore its rules. |
| Prompt injection | Instructions hidden in content the model reads (a web page, a file, a tool result) that try to hijack it. |
| Classifier | A separate, smaller model that labels inputs or outputs (for example "weapons uplift: yes or no"). |
| Red teaming | Deliberately attacking the system to find failures before others do. |
| Dangerous-capability evaluation | A test of whether the model could give serious help with catastrophic harm (biological, chemical, cyber, autonomy). |
| Capability threshold | A pre-agreed level of dangerous capability that triggers stronger safeguards or a pause. |
| System card | The public document describing a model's capabilities, evaluations and safeguards. |
| Model weights | The trained parameters. The single most valuable and most stealable asset. |
| Security level (SL1 to SL5) | RAND's scale for how capable an attacker a lab can keep away from its weights, from hobbyists (SL1) to top state programs (SL5). |
| Instruction hierarchy | The rule for whose instructions win: the developer's policy, then the operator's system prompt, then the user, with tool and web content treated as data. |
| Harness | The software around the model that gives it tools, memory, permissions and a loop to work in. |
