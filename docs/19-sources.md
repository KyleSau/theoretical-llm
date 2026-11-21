# 19. Sources

[Back to the overview](../README.md) · Previous: [18. Glossary](18-glossary.md)

Published figures in this plan were gathered on 21 November 2026. This chapter lists where they came from, grouped by the chapter that uses them.

How to read the list:

- **Primary** means the organization's own page, filing, paper or court document.
- **Press** or **analyst** means a secondary report; these carry more risk of error and are used mainly for prices and estimates that companies do not publish.
- **Estimate** means a third party's model, most often Epoch AI's.
- Pages change. A figure quoted here was on the page on the research date.
- Anything in the chapters not traceable to this list is the plan's own design or arithmetic, reproducible from [`calc/sizing.py`](../calc/sizing.py).

## Chapters 5 and 6: compute, network, storage

| What | Source | Kind |
|---|---|---|
| Vera Rubin NVL72 specifications: 72 GPUs, 288 GB each, 35 / 17.5 / 4 PF dense at 4 / 8 / 16-bit, memory bandwidth, CPUs, networking | [NVIDIA product page](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/) | Primary |
| Shipping status and first-quarter revenue | [NVIDIA third-quarter fiscal 2027 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx) | Primary |
| About 2 MW per 8 racks; two 800G ports per GPU; reference switch counts; storage guidance | [SuperPOD reference architecture, InfiniBand](https://docs.nvidia.com/dgx-superpod-reference-architecture-with-dgx-vera-rubin-nvl72.pdf), [Spectrum-X version](https://docs.nvidia.com/dgx-superpod-spectrum-x-reference-architecture-with-dgx-vera-rubin-nvl72.pdf) | Primary |
| Power shelves, AC feed, 54 V busbar | [DGX Vera Rubin user guide](https://docs.nvidia.com/dgx/dgxvr-user-guide/hardware.html) | Primary |
| Rack weight, energy storage per GPU, liquid cooling, 45 °C inlet | [NVIDIA developer blog, March 2026](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer) | Primary |
| Rack dimensions | [Supermicro product page](https://www.supermicro.com/en/products/rack/srs-vr-nvl72) | Primary |
| Rack power of 180 to 227 kW by power profile | [SemiAnalysis, February 2026](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) | Analyst |
| Rack price estimates, $6M to $9.1M | [Morgan Stanley via PC Gamer](https://pcgamer.com/hardware/a-single-nvidia-vera-rubin-rack-is-estimated-to-cost-usd7-803-148-with-over-usd2-million-of-that-figure-spent-on-memory-alone), [Bernstein via Wccftech](https://wccftech.com/bernstein-warns-nvidias-vera-rubin-racks-will-hit-9-1-million-as-hbm4-prices-triple-to-53-per-gigabyte/) | Analyst, press |
| Measured training gain over the previous generation: 1.4 to 2.0 times per GPU | [NVIDIA on MLPerf Training v6.1, November 2026](https://developer.nvidia.com/blog/?p=125323) | Primary |
| Previous generation (GB300 NVL72) | [NVIDIA product page](https://www.nvidia.com/en-us/data-center/gb300-nvl72.md), [Lenovo Press](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) | Primary |
| AMD Helios | [Supermicro datasheet](https://www.supermicro.com/datasheet/datasheet_AMD_Helios.pdf), [AMD third-quarter 2026 results](https://ir.amd.com/news-events/press-releases/detail/1303/amd-reports-third-quarter-2026-financial-results) | Primary |
| Google TPU 8 | [Google Cloud technical post](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive) | Primary |
| AWS Trainium3 and Project Rainier chip count | [Amazon announcement](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost) | Primary |
| Rubin Ultra and Kyber roadmap; reported delay | [GTC 2026 keynote transcript](https://www.nvidia.com/gtc/keynote/transcript.md), [The Next Web](https://thenextweb.com/news/nvidia-kyber-rack-delay-2028) | Primary, press |
| Ethernet switches, co-packaged optics, 5 W against 25 W per port | [NVIDIA Spectrum-X](https://www.nvidia.com/en-us/networking/spectrumx/), [silicon photonics](https://www.nvidia.com/en-us/networking/products/silicon-photonics/) | Primary |
| Two-tier multi-plane networks reaching about 131,000 GPUs | [OpenAI on supercomputer networking](https://openai.com/index/mrc-supercomputer-networking/) | Primary |
| Fairwater network, rack power, no backup for the GPU fleet | [Microsoft, November 2025](https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/) | Primary |
| Sizes of the largest sites | [Epoch AI data centers dataset](https://epoch.ai/data/ai-data-centers) | Estimate |
| Utilization of 38 to 43%, interruptions, storage for a 16,000-GPU run | [Llama 3 paper](https://arxiv.org/abs/2407.21783) | Primary |
| 55% utilization on 12,288 GPUs | [MegaScale paper](https://arxiv.org/abs/2402.15627) | Primary |
| 8-bit training; GPU-hours and token count for DeepSeek-V3 | [DeepSeek-V3 paper](https://arxiv.org/abs/2412.19437) | Primary |
| 4-bit training study | [NVFP4 paper](https://arxiv.org/abs/2509.25149) | Primary |
| Specialized inference hardware speeds | [Cerebras](https://www.cerebras.ai/blog/how-cerebras-serves-gpt-5-6-sol-at-up-to-750-tokens-per-second) | Primary (vendor claim) |

## Chapter 7: data center, power, cooling

| What | Source | Kind |
|---|---|---|
| NVIDIA content of about $40B per GW for this generation; about $60B total | [NVIDIA earnings call, August 2026](https://s201.q4cdn.com/141608511/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf) | Primary |
| $50B to $60B per GW | [NVIDIA earnings call, August 2025](https://s201.q4cdn.com/141608511/files/doc_financials/2026/q2/NVDA-Q2-2026-Earnings-Call-27-August-2025-5_00-PM-ET.pdf) | Primary |
| Up to $47B per GW and 3,557 racks | [Foxconn via Wccftech](https://wccftech.com/foxconn-pegs-nvidia-vera-rubin-ai-datacenter-at-47-billion-per-gigawatt/) | Press |
| $49B per GW; facility $16M to $19M per MW | [Morgan Stanley via 24/7 Wall St.](https://247wallst.com/investing/2026/07/15/morgan-stanley-drops-a-50-billion-bombshell-can-big-tech-still-afford-to-build-the-ai-factories-of-the-future/) | Analyst |
| $17.6M per MW average facility cost | [Cushman & Wakefield 2026 guide](https://finviz.com/news/388803/cushman-wakefield-releases-2026-data-center-development-cost-guide-citing-21-rise-in-per-mw-construction-costs) | Primary (press release) |
| Grid connection waits of more than four years | [JLL data center outlook](https://www.jll.com/en-us/insights/market-outlook/data-center-outlook) | Primary |
| Cost model, PUE 1.14, build speeds | [Epoch AI cost breakdown](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown), [build-out speeds](https://epoch.ai/data-insights/data-centers-buildout-speeds) | Estimate |
| Abilene: 1.2 GW, buildings, power, cooling | [Crusoe](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts), [Epoch AI entry](https://epoch.ai/data/ai-data-centers/directory/openai-stargate-abilene) | Primary, estimate |
| Colossus 2 power and batteries | [Epoch AI entry](https://epoch.ai/data/ai-data-centers/directory/colossus-2), [Canary Media](https://www.canarymedia.com/articles/batteries/xai-massive-battery-memphis-data-center) | Estimate, press |
| Hyperion gas plants and cost | [Meta](https://datacenters.atmeta.com/richland-parish-data-center/), [WWNO](https://www.wwno.org/investigations/2026-11-19/entergys-meta-gas-plant-costs-soar-as-utility-seeks-approval-for-seven-more) | Primary, press |
| Fairwater Wisconsin: size, materials, cooling, jobs | [Microsoft, September 2025](https://blogs.microsoft.com/blog/2025/09/18/inside-the-worlds-most-powerful-ai-datacenter/) | Primary |
| Texas large-load queue | [ERCOT presentation, July 2026](https://www.ercot.com/files/docs/2026/07/29/ERCOT-Senate-July-29-Panel-1-Assessing-The-Grid.pdf) | Primary |
| Gas turbine backlog and prices | [Utility Dive](https://www.utilitydive.com/news/ge-vernova-gas-turbine-backlog-climbs-to-116-gw/826039/) | Press |
| Transformer lead times | [POWER magazine](https://powermag.com/transformers-in-2026-shortage-scramble-or-self-inflicted-crisis/) | Press |
| Fuel cells at gigawatt scale | [Bloom Energy and Oracle](https://www.bloomenergy.com/news/bloom-energy-and-oracle-expand-strategic-partnership-to-deploy-up-to-2-8-gw-to-accelerate-ai-infrastructure-build-out/) | Primary |
| Industrial electricity prices by state | [US Energy Information Administration](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_b) | Primary |
| Emission factors and heat rates | [EIA carbon coefficients](https://www.eia.gov/environment/emissions/co2_vol_mass.php), [EIA heat rates](https://www.eia.gov/electricity/annual/html/epa_08_02.html) | Primary |
| 800 V DC architecture and timeline | [NVIDIA developer blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/), [NVIDIA at OCP](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin) | Primary |
| In-rack energy storage and power smoothing | [NVIDIA developer blog](https://developer.nvidia.com/blog/how-new-gb300-nvl72-features-provide-steady-power-for-ai) | Primary |
| Training-load power swings and mitigations | [Paper, August 2025](https://arxiv.org/abs/2508.14318) | Primary |
| 1,500 MW load-loss event | [NERC incident review](https://www.nerc.com/pa/rrm/ea/Documents/Incident_Review_Large_Load_Loss.pdf) | Primary |
| Coolant distribution unit capacity and flow | [CoolIT CHx2000](https://www.coolitsystems.com/product/chx2000/) | Primary |
| Fleet PUE and water figures | [Google](https://datacenters.google/efficiency/), [Microsoft](https://datacenters.microsoft.com/sustainability/efficiency/), [AWS](https://sustainability.aboutamazon.com/products-services/aws-cloud) | Primary |
| District-heating reuse | [Fortum](https://www.fortum.com/data-centres-helsinki-region) | Primary |
| Failure rates in large GPU clusters | [Meta reliability paper](https://arxiv.org/abs/2410.21680) | Primary |
| Nuclear supply contracts | [Constellation](http://www.constellationenergy.com/news/2024/Constellation-to-Launch-Crane-Clean-Energy-Center-Restoring-Jobs-and-Carbon-Free-Power-to-The-Grid.html), [AP via Spectrum News](https://spectrumnews1.com/oh/columbus/news/2026/01/09/meta-lines-up-massive-supply-of-nuclear-power-to-energize-ai-data-centers) | Primary, press |

## Chapters 2 and 3: data

| What | Source | Kind |
|---|---|---|
| Common Crawl crawl sizes | [October 2026 crawl](https://commoncrawl.org/blog/october-2026-crawl-archive-now-available), [crawl statistics](https://commoncrawl.github.io/cc-crawl-statistics/plots/crawlsize/monthly.csv) | Primary |
| Tokens on the web, in Common Crawl, in video | [Epoch AI paper](https://arxiv.org/abs/2211.04325), [Epoch AI blog](https://epoch.ai/blog/can-ai-scaling-continue-through-2030) | Estimate |
| A 1.2-trillion-page crawl and its filtering funnel; 7.4T-token code corpus; sourcing rules | [Microsoft AI report, June 2026](https://microsoft.ai/pdf/mai-thinking-1.pdf) | Primary |
| Wikipedia sizes | [Size of Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia), [List of Wikipedias](https://meta.wikimedia.org/wiki/List_of_Wikipedias) | Primary |
| Reddit corpus size and licensing revenue | [Reddit annual report](https://www.sec.gov/Archives/edgar/data/1713445/000171344526000022/rddt-20251231.htm), [quarterly report](https://www.sec.gov/Archives/edgar/data/1713445/000171344526000116/rddt-20260930.htm) | Primary |
| Stack Exchange dump | [Internet Archive mirror](https://archive.org/details/stackexchange_20251231) | Primary |
| GitHub size | [Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) | Primary |
| Software Heritage size | [Software Heritage, May 2026](https://www.softwareheritage.org/2026/05/18/oin-linux-system-table-software-heritage-archive/) | Primary |
| The Stack v2 | [Dataset card](https://huggingface.co/datasets/bigcode/the-stack-v2) | Primary |
| arXiv, PubMed Central, Semantic Scholar | [arXiv statistics](https://arxiv.org/stats/monthly_submissions), [PMC count](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=open+access%5Bfilter%5D&rettype=count), [Semantic Scholar datasets](https://api.semanticscholar.org/datasets/v1/release/latest) | Primary |
| Internet Archive holdings | [Storage meeting slides, 2026](https://www.digitalpreservation.gov/meetings/DSA2026/0117_jonah_edwards_ia_dsa_2026.pdf) | Primary |
| Harvard Institutional Books | [Paper](https://arxiv.org/abs/2506.08300) | Primary |
| Google Books | [Google, 2019](https://www.blog.google/products/search/15-years-google-books/) | Primary |
| Patents | [USPTO annual report](https://www.uspto.gov/sites/default/files/documents/USPTOFY2026AFR.pdf), [Google Patents](https://support.google.com/faqs/answer/7049585) | Primary |
| Case law | [CourtListener](https://free.law/projects/courtlistener/), [Caselaw Access Project](https://huggingface.co/datasets/free-law/Caselaw_Access_Project) | Primary |
| Company filings | [SEC EDGAR](https://www.sec.gov/submit-filings/about-edgar) | Primary |
| YouTube size | [YouTube press page](https://blog.youtube/press/), [sampling estimate](https://ethanzuckerman.com/2023/12/22/how-big-is-youtube/), [YouTube-Commons](https://huggingface.co/datasets/PleIAs/YouTube-Commons) | Primary, estimate |
| Podcasts | [Listen Notes statistics](https://www.listennotes.com/podcast-stats/) | Primary |
| Image-text sets | [Re-LAION-5B](https://laion.ai/blog/relaion-5b/), [DataComp](https://arxiv.org/abs/2304.14108) | Primary |
| Curated web corpora | [FineWeb](https://huggingface.co/datasets/HuggingFaceFW/fineweb) and [paper](https://arxiv.org/abs/2406.17557), [FineWeb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2), [FinePDFs](https://huggingface.co/datasets/HuggingFaceFW/finepdfs), [Essential-Web](https://huggingface.co/datasets/EssentialAI/essential-web-v1.0), [Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus), [RedPajama-V2](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-V2) | Primary |
| Licensing deals | [Press Gazette tracker](https://pressgazette.co.uk/platforms/news-publisher-ai-deals-lawsuits-openai-google/), [Authors Guild on HarperCollins](https://authorsguild.org/news/harpercollins-ai-licensing-deal/), [Wiley results](https://www.sec.gov/Archives/edgar/data/107140/000162828026060252/ex991earningsrelease.htm), [Shutterstock quarterly report](https://www.sec.gov/Archives/edgar/data/1549346/000154934626000034/sstk-20260930.htm) | Press, primary |
| Paid crawling and licensing standards | [Cloudflare pay per crawl](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/), [Internet Licensing Collective](https://internetcollective.org/press/ilc-launch-2026), [Really Simple Licensing](https://rslstandard.org/rsl), [TollBit](https://tollbit.com/blog/how-much-web-traffic-is-ai-bots) | Primary, vendor data |
| Crawler norms and traffic | [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html), [Cloudflare, September 2026](https://blog.cloudflare.com/agentic-web/), [Cloudflare crawler shares](https://blog.cloudflare.com/crawlers-click-ai-bots-training/), [Wikimedia on bot load](https://diff.wikimedia.org/2025/04/01/how-crawlers-impact-the-operations-of-the-wikimedia-projects/), [OpenAI crawlers](https://developers.openai.com/api/docs/bots), [Common Crawl FAQ](https://commoncrawl.org/faq) | Primary |
| US cases | [Settlement site for Bartz v. Anthropic](https://www.anthropiccopyrightsettlement.com/), [Authors Guild summary](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/), [Kadrey v. Meta ruling](https://storage.courtlistener.com/recap/gov.uscourts.cand.415175/gov.uscourts.cand.415175.598.0.pdf), [Thomson Reuters v. Ross, Third Circuit](https://www2.ca3.uscourts.gov/opinarch/252153p.pdf), [Reddit v. Anthropic remand order](https://www.courthousenews.com/wp-content/uploads/2026/03/reddit-v-anthropic-remand-order.pdf), [US Copyright Office on AI](https://www.copyright.gov/ai/) | Primary |
| EU rules and cases | [AI Act Article 53](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53), [Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai), [training-content summary template](https://digital-strategy.ec.europa.eu/en/library/explanatory-notice-and-template-public-summary-training-content-general-purpose-ai-models), [Advocate General's opinion, Like Company v Google](https://curia.europa.eu/site/jcms/p1_1000088855) | Primary |
| UK, Japan, Singapore | [Getty v Stability judgment](https://caselaw.nationalarchives.gov.uk/ewhc/ch/2025/2863), [UK government report, March 2026](https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence), [Japan guidance](https://www.bunka.go.jp/english/policy/copyright/pdf/94055801_01.pdf), [Singapore factsheet](https://www.ipos.gov.sg/docs/default-source/resources-library/copyright/copyright-act-factsheet.pdf) | Primary |
| Privacy | [EDPB Opinion 28/2024](https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf), [EDPB draft scraping guidelines](https://www.edpb.europa.eu/public-consultations/guidelines-032026-on-web-scraping-in-the-context-of-generative-ai_en) | Primary |
| Abuse material in datasets; reporting duty | [Stanford Internet Observatory report](https://stacks.stanford.edu/file/druid:kh752sm9123/ml_training_data_csam_report-2023-12-23.pdf), [18 U.S.C. 2258A](https://www.law.cornell.edu/uscode/text/18/2258A), [NCMEC](https://www.missingkids.org/theissues/generative-ai), [industry principles](https://www.thorn.org/blog/generative-ai-principles/) | Primary |

## Chapter 4: model scale and scaling laws

| What | Source | Kind |
|---|---|---|
| Projection table: 10T parameters, 216.2T tokens, 1.30e28 FLOPs | [Hoffmann et al., "Chinchilla"](https://arxiv.org/pdf/2203.15556) | Primary |
| Re-analysis supporting about 20 tokens per parameter | [Besiroglu et al.](https://arxiv.org/html/2404.10102) | Primary |
| Repeating data up to about four times | [Muennighoff et al.](https://arxiv.org/abs/2305.16264) | Primary |
| Sparse-model scaling studies | [Ludziejewski et al.](https://arxiv.org/abs/2502.05172) | Primary |
| Training compute estimates, including the largest run to date, and the fivefold-a-year trend | [Epoch AI model database](https://epoch.ai/data/all_ai_models.csv), [Epoch AI trends](https://epoch.ai/trends) | Estimate |
| Final training runs as a share of research compute | [Epoch AI on OpenAI's compute spend](https://epoch.ai/data-insights/openai-compute-spend) | Estimate |
| Largest disclosed parameter counts | [Kimi K3.1 Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro), [Microsoft AI pre-training report](https://microsoft.ai/pdf/Frontier-Pre-training-at-Microsoft-AI.pdf?v=2), [Qwen 3.8](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B), [DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [Mistral Large 4](https://mistral.ai/news/mistral-large-4/) | Primary |
| Earlier models | [Kimi K2](https://arxiv.org/abs/2507.20534), [Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/), [Llama 3](https://arxiv.org/abs/2407.21783), [DeepSeek-V3](https://arxiv.org/abs/2412.19437) | Primary |

## Chapter 9: post-training

| What | Source | Kind |
|---|---|---|
| Reinforcement learning for reasoning, with scale | [DeepSeek-R1 paper](https://arxiv.org/html/2501.12948) | Primary |
| Market for reinforcement-learning environments | [Epoch AI survey](https://epoch.ai/gradient-updates/state-of-rl-envs) | Estimate |
| A lab pausing reinforcement-learning training | [OpenAI, August 2026](https://openai.com/index/pacing-model-development-cyber-capabilities/) | Primary |
| Written specifications used in training | [Anthropic's constitution](https://www.anthropic.com/constitution), [OpenAI Model Spec](https://model-spec.openai.com/2026-10-29.html) | Primary |

## Chapters 10, 11 and 13: safety, evaluation, security

| What | Source | Kind |
|---|---|---|
| Frontier safety frameworks | [Anthropic Responsible Scaling Policy](https://www.anthropic.com/rsp), [OpenAI Preparedness Framework](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf), [Google DeepMind Frontier Safety Framework](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf), [Meta](https://research.meta.ai/static/meta-superintelligence-scaling-framework) | Primary |
| System cards cited for 2026 practice | [OpenAI GPT-6.2](https://deploymentsafety.openai.com/gpt-6-2-astra-sol), [Anthropic Fable 5.2 and Mythos 5.2](https://www.anthropic.com/claude-fable-5-2-mythos-5-2-system-card), [Anthropic risk report, August 2026](https://anthropic.com/aug-2026-risk-report), [OpenAI on managing frontier risk](https://openai.com/index/managing-frontier-ai-risk/) | Primary |
| Classifier results: 86% to 4.4%; about 1% overhead in the second generation | [Constitutional classifiers](https://www.anthropic.com/research/constitutional-classifiers), [second-generation paper](https://arxiv.org/html/2601.04603v1) | Primary |
| Open guard models tested independently | [Study, 2026](https://arxiv.org/abs/2605.28830) | Primary |
| Prompt-injection defenses and their limits | [CaMeL](https://arxiv.org/html/2503.18813v2), [adaptive attacks paper](https://arxiv.org/html/2510.09023v1), [browser agent results](https://claude.com/blog/claude-in-chrome-generally-available), [Gray Swan arena](https://www.grayswan.ai/blog/your-ai-agent-can-be-compromised-youd-never-know) | Primary |
| Universal jailbreaks found in every system tested | [UK AI Security Institute trends report](https://www.aisi.gov.uk/frontier-ai-trends-report) | Primary |
| Time horizons and cheating on long tasks | [METR time horizons](https://metr.org/time-horizons/), [fourth-quarter 2026 update](https://metr.org/blog/2026-11-20-q4-2026-capability-update/), [frontier risk report](https://metr.org/blog/2026-05-19-frontier-risk-report/) | Primary |
| Evaluation awareness | [Apollo Research](https://www.apolloresearch.ai/research) | Primary |
| Security levels | [RAND, Securing AI Model Weights](https://www.rand.org/pubs/research_reports/RRA2849-1.html), [RAND, Achieving SL3](https://www.rand.org/pubs/research_reports/RRA4704-1.html) | Primary |
| EU AI Act thresholds and timing | [Article 51](https://artificialintelligenceact.eu/article/51/), [Commission guidelines](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers) | Primary |
| US state and federal rules | [California SB 53](https://www.gov.ca.gov/2025/09/29/governor-newsom-signs-sb-53-advancing-californias-world-leading-artificial-intelligence-industry/), [New York RAISE Act](https://www.nysenate.gov/legislation/bills/2025/S6953/amendment/B), [Executive order, June 2026](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/) | Primary |
| A model under export control | [Anthropic, July 2026](https://www.anthropic.com/news/redeploying-fable-5) | Primary |
| Abuse-material reporting volumes | [NCMEC CyberTipline data](https://ncmec.org/gethelpnow/cybertipline/cybertiplinedata) | Primary |
| Text watermarking | [SynthID-Text in Nature](https://www.nature.com/articles/s41586-024-08025-4) | Primary |

## Chapters 12, 14 and 15: serving, people, money

| What | Source | Kind |
|---|---|---|
| Measured output speeds | [Artificial Analysis](https://artificialanalysis.ai/) | Independent measurement |
| List prices | [Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI](https://developers.openai.com/api/docs/pricing) | Primary |
| Token volumes | [Alphabet third-quarter 2026 message](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/) | Primary |
| Headcount, personnel and compute expense | [Anthropic registration statement](https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm), [Anthropic prospectus materials](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072952/anthropicpbc-fwpukmaterials.htm), [Fortune on OpenAI](https://fortune.com/2026/03/21/openai-double-headcount-this-year-sam-altman-anthropic-google/) | Primary, press |
| Compensation | [Levels.fyi](https://www.levels.fyi/companies/anthropic/salaries/software-engineer) | Self-reported data |
| Expert human-data market | [Sacra on Mercor](https://sacra.com/c/mercor/) | Analyst |

## What could not be verified

The research passes ran out of search budget before finishing. These items were looked for and not found, or were seen only in secondary reports:

- A vendor-published rack power figure, coolant flow rate, or list price for the chosen rack.
- Any published utilization figure for a training run on this hardware generation.
- Published optics, fiber or switch counts for clusters above 100,000 GPUs.
- Published PUE or water figures for any of the named gigawatt campuses.
- Total hours of video on YouTube, total podcast hours, and a per-hour licensing price for audio.
- Bulk prices for licensed video (only a per-minute range from 2025 press reports).
- Any lab's own disclosure of how much compute goes to post-training.
- Any lab attesting that it has reached a named security level.

Where the plan depends on one of these, the chapter says it is an assumption.
