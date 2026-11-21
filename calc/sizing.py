#!/usr/bin/env python3
"""
sizing.py - the arithmetic behind the theoretical frontier-LLM build plan.

Every headline number in the docs comes out of this file. Change an assumption
in the ASSUMPTIONS block, re-run, and the whole plan re-sizes itself.

    python3 calc/sizing.py            # print the report
    python3 calc/sizing.py --json     # machine-readable dump

It is arithmetic only: no network access, no GPUs, no data. Python 3.9+,
standard library only.
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field

# =============================================================================
# 1. ASSUMPTIONS
#    Each value is discussed, with its source and confidence, in
#    docs/01-scope-and-assumptions.md. Units are in the names.
# =============================================================================


@dataclass
class Campus:
    it_power_mw: float = 1000.0          # critical IT load of the campus
    gpu_rack_power_share: float = 0.90   # share of IT power feeding GPU rack positions
    halls: int = 8
    pue: float = 1.15                    # annual-average power usage effectiveness
    peak_facility_ratio: float = 1.30    # electrical nameplate over IT load
    load_factor: float = 0.85            # average IT draw over the year
    grid_price_usd_per_mwh: float = 68.0
    gas_ccgt_t_co2_per_mwh: float = 0.34
    gas_aero_t_co2_per_mwh: float = 0.48
    us_home_mwh_per_year: float = 10.8
    coolant_delta_t_k: float = 10.0      # supply/return temperature difference
    coolant_density_kg_m3: float = 1020  # 25% propylene glycol
    coolant_cp_j_kg_k: float = 3900
    liquid_capture_fraction: float = 0.95  # share of IT heat taken by liquid
    cdu_capacity_mw: float = 2.3
    dry_cooler_capacity_mw: float = 1.8


@dataclass
class Rack:
    name: str = "NVIDIA Vera Rubin NVL72"
    position_power_kw: float = 250.0      # rack plus its share of fabric (vendor: ~2 MW per 8 racks)
    rack_tdp_kw: float = 227.0            # the compute rack alone at full power (analyst estimate)
    gpus: int = 72
    hbm_gb_per_gpu: float = 288.0
    peak_fp4_pf: float = 35.0             # published dense 4-bit figure per GPU
    peak_fp8_pf: float = 17.5             # published dense 8-bit figure
    peak_bf16_pf: float = 4.0             # published dense 16-bit figure
    peak_infer_sparse_fp4_pf: float = 50.0  # published headline inference figure (sparse)
    hbm_bandwidth_tb_s_per_rack: float = 1400.0
    price_usd_m: float = 8.5              # analyst range 6 to 9.1
    scale_out_ports_per_gpu: int = 2      # two 800G ports per GPU, independent planes
    scale_out_gbps_per_port: int = 800


@dataclass
class TrainingEfficiency:
    # Planning rate, anchored on measured results instead of vendor peaks.
    # See docs/05-compute-cluster.md for the derivation.
    sustained_pf_per_gpu: float = 2.5     # while the job is stepping
    uptime: float = 0.85                  # share of wall-clock the job is stepping
    cases: tuple = (("Conservative", 1.2, 0.80), ("Planning", 2.5, 0.85), ("Aggressive", 4.0, 0.90))


@dataclass
class ScalingLaw:
    flops_per_param_token: float = 6.0    # C = 6 N D (forward + backward)
    tokens_per_param: float = 21.62       # Chinchilla table: 216.2T tokens / 10T params
    infer_flops_per_param_token: float = 2.0


@dataclass
class Model:
    """Illustrative flagship: sparse mixture-of-experts decoder-only transformer."""
    d_model: int = 24576
    n_layers: int = 168
    n_heads: int = 192
    head_dim: int = 128
    n_kv_heads: int = 8           # grouped-query attention; small on purpose (cache size)
    n_routed_experts: int = 64
    n_shared_experts: int = 1
    top_k: int = 8
    d_expert: int = 12288         # hidden width of one expert (SwiGLU)
    vocab: int = 262144
    train_tokens: float = 216e12  # pretraining token budget


@dataclass
class DataSource:
    name: str
    tokens_t: float       # trillions of tokens entering the pretraining mix
    kind: str             # text | code | multimodal | synthetic


DATA_MIX = [
    DataSource("Open web text (own crawl + Common Crawl), filtered, deduplicated", 60, "text"),
    DataSource("Code (permissive public repositories, licensed)", 6, "code"),
    DataSource("Books, papers, patents, law, government records", 6, "text"),
    DataSource("Licensed forums, social and news", 3, "text"),
    DataSource("Transcribed speech (licensed audio and video)", 2, "text"),
    DataSource("Two further passes over the best 17T of text and code", 34, "text"),
    DataSource("Synthetic and self-generated (verified reasoning, code, math)", 30, "synthetic"),
    DataSource("Image-text pairs", 5, "multimodal"),
    DataSource("Video frames (licensed)", 60, "multimodal"),
    DataSource("Native audio", 10, "multimodal"),
]


@dataclass
class RunPlan:
    racks_per_replica: int = 4               # one full copy of the model per pod
    cluster_share: float = 0.6               # six of eight halls at 80%
    sequences_per_step: int = 32768
    tokens_per_sequence: int = 8192
    gradient_bytes_per_param: float = 2.0    # 16-bit gradients on the wire
    allreduce_traffic_factor: float = 2.0    # each replica sends and receives about one copy
    rented_gpus: int = 20000                 # interim cloud fleet for research
    rented_pf_sustained_per_gpu: float = 1.0
    component_failures_per_day_campus: float = 140.0


@dataclass
class PostTraining:
    midtrain_tokens: float = 5e12            # curated, long-context continuation
    midtrain_attention_overhead: float = 1.3
    sft_conversations: float = 20e6
    sft_tokens_per_conversation: float = 3000
    reasoning_episodes: float = 2e9
    reasoning_tokens_per_episode: float = 10_000
    agent_episodes: float = 100e6
    agent_context_tokens: float = 150_000    # tool results and files read
    agent_sampled_tokens: float = 30_000
    agent_sandbox_hours: float = 0.75
    agent_campaign_days: float = 60
    vcpus_per_sandbox: float = 2
    teacher_tokens: float = 5e12             # generated for distillation
    mid_tier_active: float = 200e9
    small_tier_active: float = 30e9
    student_tokens: float = 50e12
    eval_tokens: float = 2e12
    variants_multiplier: float = 4.0         # ablations, restarts, parallel candidates


# First-year allocation of the campus, as shares of one campus-year
COMPUTE_BUDGET = [
    ("Research experiments, ablations, scaling sweeps", 0.25),
    ("Pilot and dress-rehearsal runs", 0.03),
    ("Flagship pretraining", None),          # computed
    ("Post-training, all variants", None),   # computed
    ("Evaluations, red teaming, classifier training, synthetic data", 0.04),
    ("Reserve for restarts and reruns", 0.05),
]


@dataclass
class Storage:
    crawl_pages_b: float = 1200.0            # billions of pages fetched (largest disclosed crawl: ~1.2 trillion)
    crawl_kb_per_page_compressed: float = 35.0
    images_b: float = 10.0
    image_kb: float = 200.0
    video_hours_m: float = 100.0
    video_gb_per_hour: float = 1.0
    audio_hours_m: float = 50.0
    audio_mb_per_hour: float = 30.0
    bytes_per_token_stored: float = 4.0
    derived_multiplier: float = 2.0          # cleaned text, shards, latents, indexes
    replication_overhead: float = 1.4        # erasure coding + second site for irreplaceable sets
    optimizer_bytes_per_param: float = 8.0   # two moments, 4 bytes each
    weight_bytes_per_param_train: float = 2.0
    full_checkpoints_kept: int = 40
    weight_checkpoints_kept: int = 400
    checkpoint_write_seconds: float = 300.0
    flash_tier_pb: float = 60.0
    flash_write_tb_s: float = 2.5


@dataclass
class Crawl:
    months: float = 9.0
    kb_per_page_transfer: float = 60.0
    rendered_fraction: float = 0.2
    rendered_mb_per_page: float = 2.0


@dataclass
class Network:
    planes: int = 8                          # each 800G port broken out to 4 x 200G
    plane_gbps: int = 200
    switch_ports: int = 2048                 # 200G ports per fabric switch chassis


@dataclass
class Inference:
    kv_cache_bits: int = 8
    typical_context_tokens: int = 20_000
    max_context_tokens: int = 1_000_000
    stream_cap_tok_s: float = 400.0         # per-token overheads cap small models
    flagship_serving_racks: int = 500
    weight_bits: int = 4
    compute_utilization: float = 0.15       # planning share of the dense 4-bit peak achieved
    memory_step_derate: float = 0.33        # planning share of the bandwidth-bound step rate
    fleet_utilization: float = 0.5          # average load on a serving rack
    rack_life_years: float = 4.0
    facility_capex_usd_m_per_mw: float = 17.5
    facility_life_years: float = 15.0
    ops_usd_m_per_rack_year: float = 0.2


@dataclass
class Cost:
    network_capex_share_of_compute: float = 0.15
    storage_capex_usd_b: float = 1.0
    cpu_fleet_capex_usd_b: float = 1.0
    facility_capex_usd_m_per_mw: float = 17.5
    onsite_generation_mw: float = 1300.0
    generation_usd_per_kw: float = 2200.0
    bess_mwh: float = 800.0
    bess_usd_per_kwh: float = 300.0
    substation_interconnect_usd_b: float = 0.4
    land_site_usd_b: float = 0.15
    hardware_maintenance_rate: float = 0.03
    data_licensing_usd_b_per_year: float = 1.5
    human_data_usd_b_per_year: float = 1.0
    interim_cloud_compute_usd_b: float = 1.5
    # Spend before launch, as "full-rate years" of each steady-state line
    program_months: float = 32.0
    people_full_rate_years: float = 1.36     # headcount ramps from 0 to 2,960
    electricity_full_rate_years: float = 0.75
    maintenance_full_rate_years: float = 0.60
    licensing_full_rate_years: float = 2.50
    human_data_full_rate_years: float = 2.00


@dataclass
class Team:
    # (function, headcount, loaded cost per head in $M/year)
    rows: list = field(default_factory=lambda: [
        ("Research (pretraining, architecture, multimodal, RL, evals)", 350, 2.2),
        ("ML systems and research engineering", 300, 1.2),
        ("Data (crawl, pipeline, licensing, annotation ops, synthetic)", 250, 0.7),
        ("Compute infrastructure (cluster SRE, network, storage, hardware)", 250, 0.8),
        ("Data center engineering and site operations", 600, 0.3),
        ("Energy (procurement, grid, plant oversight)", 60, 0.5),
        ("Safety (safeguards, alignment, red team, frontier evals, policy)", 300, 1.2),
        ("Security (information, physical, insider risk)", 180, 0.7),
        ("Product, inference and harness engineering", 350, 0.9),
        ("Legal, policy, compliance, communications", 120, 0.7),
        ("General and administrative", 200, 0.4),
    ])


# =============================================================================
# 2. DERIVATIONS
# =============================================================================

def cluster(c: Campus, r: Rack, e: TrainingEfficiency) -> dict:
    gpu_power_mw = c.it_power_mw * c.gpu_rack_power_share
    racks = int(gpu_power_mw * 1000 // r.position_power_kw)
    gpus = racks * r.gpus
    running = gpus * e.sustained_pf_per_gpu * 1e15
    wallclock = running * e.uptime
    return {
        "gpu_racks": racks,
        "racks_per_hall": racks // c.halls,
        "gpus": gpus,
        "gpus_per_hall": gpus // c.halls,
        "gpu_power_mw": gpu_power_mw,
        "other_it_power_mw": c.it_power_mw - gpu_power_mw,
        "hbm_total_pb": gpus * r.hbm_gb_per_gpu / 1e6,
        "hbm_per_rack_tb": r.gpus * r.hbm_gb_per_gpu / 1000,
        "headline_fp4_flops": gpus * r.peak_fp4_pf * 1e15,
        "headline_fp4_tflops": gpus * r.peak_fp4_pf * 1e3,
        "headline_fp8_flops": gpus * r.peak_fp8_pf * 1e15,
        "headline_bf16_flops": gpus * r.peak_bf16_pf * 1e15,
        "headline_infer_flops": gpus * r.peak_infer_sparse_fp4_pf * 1e15,
        "running_flops": running,
        "running_tflops": running / 1e12,
        "wallclock_flops": wallclock,
        "sustained_share_of_fp4": e.sustained_pf_per_gpu / r.peak_fp4_pf,
        "sustained_share_of_fp8": e.sustained_pf_per_gpu / r.peak_fp8_pf,
        "sustained_share_of_bf16": e.sustained_pf_per_gpu / r.peak_bf16_pf,
        "flops_per_day": wallclock * 86400,
        "flops_per_100_days": wallclock * 86400 * 100,
        "flops_per_year": wallclock * 86400 * 365,
        "kw_per_gpu_all_in": r.position_power_kw / r.gpus,
    }


def sensitivity(e: TrainingEfficiency, s: ScalingLaw, cl: dict, flagship_flops: float) -> list:
    rows = []
    for name, pf, up in e.cases:
        rate = cl["gpus"] * pf * 1e15 * up
        flops = rate * 86400 * 100
        n = math.sqrt(flops / (s.flops_per_param_token * s.tokens_per_param))
        rows.append((name, pf, up, rate, flops, n, n * s.tokens_per_param, flagship_flops / (rate * 86400)))
    return rows


def model_params(m: Model) -> dict:
    attn = 2 * m.d_model * (m.n_heads * m.head_dim) + 2 * m.d_model * (m.n_kv_heads * m.head_dim)
    expert = 3 * m.d_model * m.d_expert
    router = m.d_model * m.n_routed_experts
    norms = 2 * m.d_model
    emb = m.vocab * m.d_model  # tied input/output embedding

    def active(k):
        return m.n_layers * (attn + (k + m.n_shared_experts) * expert + router + norms) + emb
    layer_total = attn + (m.n_routed_experts + m.n_shared_experts) * expert + router + norms
    return {
        "attention_params_per_layer": attn,
        "params_per_expert": expert,
        "params_per_layer_total": layer_total,
        "params_per_layer_active": (active(m.top_k) - emb) / m.n_layers,
        "embedding_params": emb,
        "total_params": m.n_layers * layer_total + emb,
        "active_params": active(m.top_k),
        "active_params_top2": active(2),
        "active_params_top16": active(16),
        "attention_total": m.n_layers * attn,
        "shared_total": m.n_layers * m.n_shared_experts * expert,
        "routed_total": m.n_layers * m.n_routed_experts * expert,
    }


def chinchilla(flops: float, s: ScalingLaw) -> dict:
    n = math.sqrt(flops / (s.flops_per_param_token * s.tokens_per_param))
    return {"params": n, "tokens": n * s.tokens_per_param}


def training(cl: dict, mp: dict, m: Model, s: ScalingLaw) -> dict:
    def run(active, tokens, share):
        flops = s.flops_per_param_token * active * tokens
        return {
            "active": active, "tokens": tokens,
            "flops": flops,
            "days_full_cluster": flops / cl["flops_per_day"],
            "days_at_share": flops / (cl["flops_per_day"] * share),
            "share": share,
            "tokens_per_second_running": cl["running_flops"] * share / (s.flops_per_param_token * active),
        }
    opt = chinchilla(cl["flops_per_100_days"], s)
    return {
        "flagship_moe": run(mp["active_params"], m.train_tokens, 0.6),
        "sparser_top2": run(mp["active_params_top2"], m.train_tokens, 0.6),
        "denser_top16": run(mp["active_params_top16"], m.train_tokens, 0.6),
        "dense_100_day": run(opt["params"], opt["tokens"], 1.0),
        "dense_10t": run(10e12, 10e12 * s.tokens_per_param, 1.0),
        "pilot_1t_dense": run(1e12, 1e12 * s.tokens_per_param, 0.25),
        "chinchilla_for_100_days": opt,
        "tokens_per_total_param": m.train_tokens / mp["total_params"],
        "tokens_per_active_param": m.train_tokens / mp["active_params"],
    }


def run_plan(rp: RunPlan, r: Rack, cl: dict, mp: dict, m: Model, s: ScalingLaw) -> dict:
    gpus = cl["gpus"] * rp.cluster_share
    gpus_per_replica = rp.racks_per_replica * r.gpus
    replicas = gpus / gpus_per_replica
    running = cl["running_flops"] * rp.cluster_share
    tok_s = running / (s.flops_per_param_token * mp["active_params"])
    batch = rp.sequences_per_step * rp.tokens_per_sequence
    grad_tb = mp["total_params"] * rp.gradient_bytes_per_param / 1e12
    replica_tb_s = gpus_per_replica * r.scale_out_ports_per_gpu * r.scale_out_gbps_per_port / 8 / 1000
    rented = rp.rented_gpus * rp.rented_pf_sustained_per_gpu * 1e15
    ladder = []
    for name, n, tokens, where, rate in (
        ("Rung 1", 1e9, 1e9 * s.tokens_per_param, "rented", rented),
        ("Rung 2", 10e9, 10e9 * s.tokens_per_param, "rented", rented),
        ("Rung 3: first working model", 100e9, 100e9 * s.tokens_per_param, "rented", rented),
        ("Rung 4: pilot", 1e12, 1e12 * s.tokens_per_param, "halls 1-2", cl["wallclock_flops"] * 0.25),
        ("Rung 5: dress rehearsal", mp["active_params"], 20e12, "halls 1-4 at 50%", cl["wallclock_flops"] * 0.25),
        ("Rung 6: flagship", mp["active_params"], m.train_tokens, "halls 1-6 at 80%", cl["wallclock_flops"] * rp.cluster_share),
    ):
        flops = s.flops_per_param_token * n * tokens
        ladder.append((name, n, tokens, flops, where, flops / rate / 86400))
    return {
        "gpus_in_run": gpus,
        "gpus_per_replica": gpus_per_replica,
        "replicas": replicas,
        "hbm_per_replica_tb": gpus_per_replica * r.hbm_gb_per_gpu / 1000,
        "tokens_per_second": tok_s,
        "tokens_per_step": batch,
        "seconds_per_step": batch / tok_s,
        "steps": m.train_tokens / batch,
        "sequences_per_replica_per_step": rp.sequences_per_step / replicas,
        "gradient_tb": grad_tb,
        "replica_bandwidth_tb_s": replica_tb_s,
        "gradient_sync_seconds": grad_tb * rp.allreduce_traffic_factor / replica_tb_s,
        "rejoin_seconds": grad_tb / replica_tb_s,
        "minutes_between_component_failures": 24 * 60 / (rp.component_failures_per_day_campus * rp.cluster_share),
        "token_bytes_per_second_mb": tok_s * 4 / 1e6,
        "ladder": ladder,
    }


def post_training(pt: PostTraining, mp: dict, s: ScalingLaw, cl: dict) -> dict:
    n = mp["active_params"]
    train, infer = s.flops_per_param_token, s.infer_flops_per_param_token
    reasoning_tokens = pt.reasoning_episodes * pt.reasoning_tokens_per_episode
    agent_tokens = pt.agent_episodes * (pt.agent_context_tokens + pt.agent_sampled_tokens)
    stages = {
        "Mid-training (curated, long context)": train * n * pt.midtrain_tokens * pt.midtrain_attention_overhead,
        "Supervised fine-tuning": train * n * pt.sft_conversations * pt.sft_tokens_per_conversation,
        "Reasoning RL (sample + train)": (train + infer) * n * reasoning_tokens,
        "Agentic RL (sample + train)": (train + infer) * n * agent_tokens,
        "Distillation (teacher output + two students)": (
            infer * n * pt.teacher_tokens
            + train * pt.mid_tier_active * pt.student_tokens
            + train * pt.small_tier_active * pt.student_tokens),
        "Evaluation passes": infer * n * pt.eval_tokens,
    }
    one_pass = sum(stages.values())
    sandbox_hours = pt.agent_episodes * pt.agent_sandbox_hours
    concurrent = sandbox_hours / (pt.agent_campaign_days * 24)
    return {
        "stages": stages,
        "one_pass_flops": one_pass,
        "with_variants_flops": one_pass * pt.variants_multiplier,
        "one_pass_days_full_cluster": one_pass / cl["flops_per_day"],
        "with_variants_days_full_cluster": one_pass * pt.variants_multiplier / cl["flops_per_day"],
        "reasoning_tokens": reasoning_tokens,
        "agent_tokens": agent_tokens,
        "sandbox_hours": sandbox_hours,
        "concurrent_sandboxes": concurrent,
        "sandbox_vcpus": concurrent * pt.vcpus_per_sandbox,
    }


def compute_budget(cl: dict, tr: dict, po: dict) -> dict:
    year = cl["flops_per_year"]
    rows = []
    for name, share in COMPUTE_BUDGET:
        if name == "Flagship pretraining":
            flops = tr["flagship_moe"]["flops"]
        elif name.startswith("Post-training"):
            flops = po["with_variants_flops"]
        else:
            flops = share * year
        rows.append((name, flops, flops / year))
    used = sum(f for _, f, _ in rows)
    rows.append(("Inference: internal use, previews, launch", year - used, (year - used) / year))
    return {"rows": rows, "year_flops": year}


def data_mix() -> dict:
    total = sum(d.tokens_t for d in DATA_MIX)
    by_kind: dict = {}
    for d in DATA_MIX:
        by_kind[d.kind] = by_kind.get(d.kind, 0) + d.tokens_t
    return {"total_t": total, "by_kind": by_kind,
            "rows": [(d.name, d.tokens_t, d.tokens_t / total) for d in DATA_MIX]}


def storage(st: Storage, mp: dict, m: Model) -> dict:
    crawl_pb = st.crawl_pages_b * 1e9 * st.crawl_kb_per_page_compressed * 1e3 / 1e15
    images_pb = st.images_b * 1e9 * st.image_kb * 1e3 / 1e15
    video_pb = st.video_hours_m * 1e6 * st.video_gb_per_hour * 1e9 / 1e15
    audio_pb = st.audio_hours_m * 1e6 * st.audio_mb_per_hour * 1e6 / 1e15
    tokens_pb = m.train_tokens * st.bytes_per_token_stored / 1e15
    raw_pb = crawl_pb + images_pb + video_pb + audio_pb
    lake_pb = (raw_pb * st.derived_multiplier + tokens_pb) * st.replication_overhead
    weights_tb = mp["total_params"] * st.weight_bytes_per_param_train / 1e12
    full_tb = mp["total_params"] * (st.weight_bytes_per_param_train + st.optimizer_bytes_per_param) / 1e12
    ckpt_pb = (st.full_checkpoints_kept * full_tb + st.weight_checkpoints_kept * weights_tb) / 1000
    return {
        "crawl_pb": crawl_pb, "images_pb": images_pb, "video_pb": video_pb,
        "audio_pb": audio_pb, "tokenized_pb": tokens_pb, "raw_pb": raw_pb,
        "data_lake_provisioned_pb": lake_pb,
        "weights_checkpoint_tb": weights_tb, "full_checkpoint_tb": full_tb,
        "checkpoint_store_pb": ckpt_pb,
        "checkpoint_write_gb_s": full_tb * 1000 / st.checkpoint_write_seconds,
        "flash_tier_pb": st.flash_tier_pb,
        "full_checkpoint_seconds_on_flash": full_tb / st.flash_write_tb_s,
        "speech_tokens_t": (st.video_hours_m + st.audio_hours_m) * 1e6 * 12000 / 1e12,
        "video_tokens_per_frame": 60e12 / (st.video_hours_m * 1e6 * 3600),
    }


def crawl(cr: Crawl, st: Storage) -> dict:
    seconds = cr.months * 30.44 * 86400
    pages_s = st.crawl_pages_b * 1e9 / seconds
    plain_gbps = pages_s * (1 - cr.rendered_fraction) * cr.kb_per_page_transfer * 1e3 * 8 / 1e9
    rendered_gbps = pages_s * cr.rendered_fraction * cr.rendered_mb_per_page * 1e6 * 8 / 1e9
    media_bytes = (st.video_hours_m * 1e6 * st.video_gb_per_hour * 1e9
                   + st.audio_hours_m * 1e6 * st.audio_mb_per_hour * 1e6
                   + st.images_b * 1e9 * st.image_kb * 1e3)
    return {
        "pages_per_second": pages_s,
        "pages_per_day_b": pages_s * 86400 / 1e9,
        "crawl_gbps": plain_gbps + rendered_gbps,
        "media_ingest_gbps": media_bytes * 8 / seconds / 1e9,
    }


def power_cooling(c: Campus, cl: dict) -> dict:
    facility_mw = c.it_power_mw * c.pue
    twh = facility_mw * 8760 / 1e6
    liquid_w = c.it_power_mw * 1e6 * c.liquid_capture_fraction
    flow_m3_s = liquid_w / (c.coolant_density_kg_m3 * c.coolant_cp_j_kg_k * c.coolant_delta_t_k)
    return {
        "facility_mw": facility_mw,
        "facility_nameplate_mw": c.it_power_mw * c.peak_facility_ratio,
        "overhead_mw": facility_mw - c.it_power_mw,
        "energy_twh_per_year": twh,
        "energy_twh_per_year_at_load_factor": twh * c.load_factor,
        "energy_cost_usd_m_per_year": twh * c.grid_price_usd_per_mwh,
        "energy_cost_usd_m_per_year_at_load_factor": twh * c.load_factor * c.grid_price_usd_per_mwh,
        "co2_mt_per_year_if_gas": twh * c.gas_ccgt_t_co2_per_mwh,
        "co2_mt_per_year_if_aero": twh * c.gas_aero_t_co2_per_mwh,
        "equivalent_us_homes": twh * 1e6 / c.us_home_mwh_per_year,
        "liquid_heat_mw": liquid_w / 1e6,
        "coolant_flow_m3_s": flow_m3_s,
        "coolant_flow_l_min": flow_m3_s * 1000 * 60,
        "coolant_flow_l_min_per_gpu_rack": flow_m3_s * 1000 * 60 * c.gpu_rack_power_share / cl["gpu_racks"],
        "cdus": math.ceil(liquid_w / 1e6 / c.cdu_capacity_mw * 1.1),
        "dry_coolers": math.ceil(facility_mw / c.dry_cooler_capacity_mw * 1.1),
        "heat_rejected_mw": facility_mw,
    }


def network(n: Network, r: Rack, cl: dict) -> dict:
    gpus = cl["gpus"]
    half = n.switch_ports // 2
    leaf = math.ceil(gpus / half)
    spine = math.ceil(leaf * half / n.switch_ports)
    ports_800g = gpus * r.scale_out_ports_per_gpu
    return {
        "host_ports_800g": ports_800g,
        "planes": n.planes,
        "max_gpus_two_tier": n.switch_ports ** 2 // 2,
        "leaf_per_plane": leaf, "spine_per_plane": spine,
        "fabric_switches": (leaf + spine) * n.planes,
        "host_lanes_200g": gpus * n.planes,
        "leaf_spine_lanes_200g": leaf * half * n.planes,
        "links_800g_equivalent": 2 * ports_800g,
        "host_transceivers_800g": ports_800g,
        "pluggables_if_no_cpo": 4 * ports_800g,
        "edge_capacity_pbps": ports_800g * r.scale_out_gbps_per_port / 1e6,
        "bisection_pbps": ports_800g * r.scale_out_gbps_per_port / 2e6,
        "tbps_per_gpu": r.scale_out_ports_per_gpu * r.scale_out_gbps_per_port / 1000,
    }


def kv_cache(i: Inference, m: Model, r: Rack, weights_tb: float) -> dict:
    values_per_token = 2 * m.n_kv_heads * m.head_dim * m.n_layers
    bytes_per_token = values_per_token * i.kv_cache_bits / 8
    free_tb = r.gpus * r.hbm_gb_per_gpu / 1000 - weights_tb
    typical_gb = bytes_per_token * i.typical_context_tokens / 1e9
    max_gb = bytes_per_token * i.max_context_tokens / 1e9
    return {
        "bytes_per_token": bytes_per_token,
        "typical_context_gb": typical_gb,
        "max_context_gb": max_gb,
        "free_memory_tb": free_tb,
        "streams_at_typical_context": free_tb * 1000 / typical_gb,
        "streams_at_max_context": free_tb * 1000 / max_gb,
    }


def rack_cost_per_year(i: Inference, r: Rack, c: Campus) -> dict:
    parts = {
        "Rack, depreciated": r.price_usd_m / i.rack_life_years,
        "Facility share, depreciated": i.facility_capex_usd_m_per_mw * r.position_power_kw / 1000 / i.facility_life_years,
        "Electricity": r.position_power_kw / 1000 * c.pue * 8760 * c.grid_price_usd_per_mwh / 1e6,
        "Operations and maintenance": i.ops_usd_m_per_rack_year,
    }
    return {"parts": parts, "total": sum(parts.values())}


def inference(i: Inference, r: Rack, c: Campus, s: ScalingLaw, params_active: float,
              params_total: float) -> dict:
    flops_tok = s.infer_flops_per_param_token * params_active
    rack_peak = r.gpus * r.peak_fp4_pf * 1e15          # dense 4-bit
    weight_tb = params_total * i.weight_bits / 8 / 1e12
    compute_bound = rack_peak / flops_tok
    planning_rack = compute_bound * i.compute_utilization
    steps_bound = r.hbm_bandwidth_tb_s_per_rack / weight_tb
    stream = min(steps_bound * i.memory_step_derate, i.stream_cap_tok_s)
    cost_year = rack_cost_per_year(i, r, c)["total"]

    def cost_at(util):
        return cost_year * 1e6 / (planning_rack * util * 86400 * 365 / 1e6)
    return {
        "flops_per_token": flops_tok,
        "weights_tb": weight_tb,
        "hbm_per_rack_tb": r.gpus * r.hbm_gb_per_gpu / 1000,
        "rack_compute_bound_tok_s": compute_bound,
        "rack_planning_tok_s": planning_rack,
        "stream_bound_tok_s": steps_bound,
        "stream_planning_tok_s": stream,
        "concurrent_streams_per_rack": planning_rack / stream,
        "rack_cost_usd_m_per_year": cost_year,
        "cost_usd_per_m_output_tokens": cost_at(i.fleet_utilization),
        "cost_at_25": cost_at(0.25), "cost_at_75": cost_at(0.75),
        "tokens_per_day_per_rack_b": planning_rack * i.fleet_utilization * 86400 / 1e9,
    }


def team(t: Team) -> dict:
    heads = sum(h for _, h, _ in t.rows)
    cost_b = sum(h * c for _, h, c in t.rows) / 1000
    return {"rows": t.rows, "headcount": heads, "cost_usd_b_per_year": cost_b}


def cost(k: Cost, c: Campus, r: Rack, cl: dict, pw: dict, team_cost_b: float) -> dict:
    compute = cl["gpu_racks"] * r.price_usd_m / 1000
    capex = {
        "GPU racks": compute,
        "Scale-out network, optics, cabling": compute * k.network_capex_share_of_compute,
        "Storage": k.storage_capex_usd_b,
        "CPU fleet (data processing, RL environments)": k.cpu_fleet_capex_usd_b,
        "Buildings, electrical, cooling": k.facility_capex_usd_m_per_mw * c.it_power_mw / 1000,
        "On-site generation": k.onsite_generation_mw * 1000 * k.generation_usd_per_kw / 1e9,
        "Battery storage": k.bess_mwh * 1000 * k.bess_usd_per_kwh / 1e9,
        "Substations and grid interconnect": k.substation_interconnect_usd_b,
        "Land and site works": k.land_site_usd_b,
    }
    hardware = compute * (1 + k.network_capex_share_of_compute) + k.storage_capex_usd_b + k.cpu_fleet_capex_usd_b
    opex = {
        "People": team_cost_b,
        "Electricity (full load)": pw["energy_cost_usd_m_per_year"] / 1000,
        "Hardware maintenance and spares": hardware * k.hardware_maintenance_rate,
        "Data licensing": k.data_licensing_usd_b_per_year,
        "Human data (annotation, expert tasks, red-team vendors)": k.human_data_usd_b_per_year,
    }
    to_launch = {
        "People": opex["People"] * k.people_full_rate_years,
        "Electricity": opex["Electricity (full load)"] * k.electricity_full_rate_years,
        "Hardware maintenance and spares": opex["Hardware maintenance and spares"] * k.maintenance_full_rate_years,
        "Data licensing": opex["Data licensing"] * k.licensing_full_rate_years,
        "Human data": opex["Human data (annotation, expert tasks, red-team vendors)"] * k.human_data_full_rate_years,
        "Rented compute before the campus is live": k.interim_cloud_compute_usd_b,
    }
    capex_total = sum(capex.values())
    launch_total = sum(to_launch.values())
    return {
        "capex": capex, "capex_total_usd_b": capex_total,
        "it_hardware_usd_b": hardware,
        "facility_power_usd_b": capex_total - hardware,
        "opex_per_year": opex, "opex_total_usd_b_per_year": sum(opex.values()),
        "operating_to_launch": to_launch, "operating_to_launch_usd_b": launch_total,
        "program_total_usd_b": capex_total + launch_total,
        "capex_usd_b_per_gw": capex_total / (c.it_power_mw / 1000),
    }


def build() -> dict:
    c, r, e, s, m = Campus(), Rack(), TrainingEfficiency(), ScalingLaw(), Model()
    st, cr, n, i, k, t, pt = Storage(), Crawl(), Network(), Inference(), Cost(), Team(), PostTraining()
    cl = cluster(c, r, e)
    mp = model_params(m)
    tm = team(t)
    pw = power_cooling(c, cl)
    tr = training(cl, mp, m, s)
    po = post_training(pt, mp, s, cl)
    rn = run_plan(RunPlan(), r, cl, mp, m, s)
    inf = inference(i, r, c, s, mp["active_params"], mp["total_params"])
    opt_n = tr["chinchilla_for_100_days"]["params"]
    return {
        "cluster": cl,
        "sensitivity": sensitivity(e, s, cl, tr["flagship_moe"]["flops"]),
        "model": mp,
        "training": tr,
        "run_plan": rn,
        "post_training": po,
        "compute_budget": compute_budget(cl, tr, po),
        "data_mix": data_mix(),
        "storage": storage(st, mp, m),
        "crawl": crawl(cr, st),
        "power_cooling": pw,
        "network": network(n, r, cl),
        "rack_cost": rack_cost_per_year(i, r, c),
        "inference_flagship": inf,
        "inference_top2": inference(i, r, c, s, mp["active_params_top2"], mp["total_params"]),
        "inference_top16": inference(i, r, c, s, mp["active_params_top16"], mp["total_params"]),
        "inference_dense_opt": inference(i, r, c, s, opt_n, opt_n),
        "inference_dense_10t": inference(i, r, c, s, 10e12, 10e12),
        "inference_mid": inference(i, r, c, s, pt.mid_tier_active, 1e12),
        "inference_small": inference(i, r, c, s, pt.small_tier_active, 100e9),
        "kv_cache": kv_cache(i, m, r, mp["total_params"] * i.weight_bits / 8 / 1e12),
        "serving_fleet": {
            "racks": i.flagship_serving_racks,
            "power_mw": i.flagship_serving_racks * r.position_power_kw / 1000,
            "share_of_campus": i.flagship_serving_racks / cl["gpu_racks"],
            "tok_s": inf["rack_planning_tok_s"] * i.fleet_utilization * i.flagship_serving_racks,
            "tokens_per_day_t": inf["tokens_per_day_per_rack_b"] * i.flagship_serving_racks / 1000,
            "streams": inf["concurrent_streams_per_rack"] * i.flagship_serving_racks,
        },
        "team": tm,
        "cost": cost(k, c, r, cl, pw, tm["cost_usd_b_per_year"]),
    }


# =============================================================================
# 3. REPORT
# =============================================================================

def si(x: float, unit: str = "") -> str:
    for div, suf in ((1e24, "Y"), (1e21, "Z"), (1e18, "E"), (1e15, "P"), (1e12, "T"),
                     (1e9, "B"), (1e6, "M"), (1e3, "k")):
        if abs(x) >= div:
            return f"{x / div:,.2f} {suf}{unit}".strip()
    return f"{x:,.2f} {unit}".strip()


def sci(x: float) -> str:
    return f"{x:.2e}"


def report(d: dict) -> str:
    cl, mp, tr = d["cluster"], d["model"], d["training"]
    st, cr, pw, nw = d["storage"], d["crawl"], d["power_cooling"], d["network"]
    tm, co = d["team"], d["cost"]
    L: list = []
    add = L.append

    def head(t):
        add("")
        add(t)
        add("-" * len(t))

    def row(label, value):
        add(f"  {label:<60} {value}")

    head("CLUSTER")
    row("GPU racks / per hall", f"{cl['gpu_racks']:,} / {cl['racks_per_hall']}")
    row("GPUs / per hall", f"{cl['gpus']:,} / {cl['gpus_per_hall']:,}")
    row("GPU rack positions / other IT (MW)", f"{cl['gpu_power_mw']:,.0f} / {cl['other_it_power_mw']:,.0f}")
    row("All-in kW per GPU", f"{cl['kw_per_gpu_all_in']:.2f}")
    row("GPU memory, total (PB) / per rack (TB)", f"{cl['hbm_total_pb']:,.1f} / {cl['hbm_per_rack_tb']:,.1f}")
    row("Headline 4-bit (FLOP/s) = TFLOPS", f"{sci(cl['headline_fp4_flops'])} = {cl['headline_fp4_tflops']:,.0f}")
    row("Headline 8-bit / 16-bit (FLOP/s)", f"{sci(cl['headline_fp8_flops'])} / {sci(cl['headline_bf16_flops'])}")
    row("Headline sparse 4-bit inference (FLOP/s)", sci(cl['headline_infer_flops']))
    row("Sustained while running (FLOP/s) = TFLOPS", f"{sci(cl['running_flops'])} = {cl['running_tflops']:,.0f}")
    row("Sustained as share of 4-bit / 8-bit / 16-bit peak", f"{cl['sustained_share_of_fp4']:.1%} / {cl['sustained_share_of_fp8']:.1%} / {cl['sustained_share_of_bf16']:.1%}")
    row("Sustained, wall-clock (FLOP/s)", sci(cl['wallclock_flops']))
    row("FLOPs per day / per 100 days / per year", f"{sci(cl['flops_per_day'])} / {sci(cl['flops_per_100_days'])} / {sci(cl['flops_per_year'])}")

    head("SENSITIVITY (100 full-campus days, dense compute-optimal; flagship days on full campus)")
    for name, pf, up, rate, flops, n, tok, fdays in d["sensitivity"]:
        row(f"{name}: {pf} PF/GPU at {up:.0%} uptime", f"{sci(rate)} FLOP/s, {sci(flops)} FLOPs, {n / 1e12:.1f}T params, {tok / 1e12:.0f}T tokens; flagship {fdays:.0f} days")

    head("MODEL (illustrative flagship configuration)")
    row("Attention parameters per layer", si(mp['attention_params_per_layer']))
    row("Parameters per expert", si(mp['params_per_expert']))
    row("Per layer: total / active", f"{si(mp['params_per_layer_total'])} / {si(mp['params_per_layer_active'])}")
    row("Attention / shared / routed totals", f"{si(mp['attention_total'])} / {si(mp['shared_total'])} / {si(mp['routed_total'])}")
    row("Embedding", si(mp['embedding_params']))
    row("Total parameters", si(mp['total_params']))
    row("Active per token: top-2 / top-8 / top-16", f"{si(mp['active_params_top2'])} / {si(mp['active_params'])} / {si(mp['active_params_top16'])}")
    row("Active share (top-8)", f"{mp['active_params'] / mp['total_params']:.1%}")
    row("Training tokens per total / active parameter", f"{tr['tokens_per_total_param']:.1f} / {tr['tokens_per_active_param']:.0f}")

    head("TRAINING RUNS")
    ch = tr["chinchilla_for_100_days"]
    row("Compute-optimal dense model for 100 full-campus days", f"{si(ch['params'])} params on {si(ch['tokens'])} tokens")
    for key, label in (("flagship_moe", "Flagship (sparse, top-8)"),
                       ("sparser_top2", "Sparser variant (top-2)"),
                       ("denser_top16", "Denser variant (top-16)"),
                       ("dense_100_day", "Dense, 100-day optimum"),
                       ("dense_10t", "Dense 10T"),
                       ("pilot_1t_dense", "Pilot: dense 1T")):
        r = tr[key]
        row(f"{label}: FLOPs", sci(r['flops']))
        row(f"{label}: days full campus / at {r['share']:.0%}", f"{r['days_full_cluster']:.1f} / {r['days_at_share']:.1f}")
        row(f"{label}: tokens per second at that share", si(r['tokens_per_second_running']))

    rn = d["run_plan"]
    head("FLAGSHIP RUN PLAN")
    row("GPUs in the run / per model replica / replicas", f"{rn['gpus_in_run']:,.0f} / {rn['gpus_per_replica']} / {rn['replicas']:,.0f}")
    row("GPU memory per replica (TB)", f"{rn['hbm_per_replica_tb']:.1f}")
    row("Tokens per second while running", si(rn['tokens_per_second']))
    row("Tokens per step / seconds per step / steps", f"{si(rn['tokens_per_step'])} / {rn['seconds_per_step']:.2f} / {rn['steps']:,.0f}")
    row("Sequences per replica per step", f"{rn['sequences_per_replica_per_step']:.0f}")
    row("Gradient size (TB) / replica bandwidth (TB/s)", f"{rn['gradient_tb']:.1f} / {rn['replica_bandwidth_tb_s']:.1f}")
    row("Gradient exchange per step (s) / weight copy to rejoin (s)", f"{rn['gradient_sync_seconds']:.2f} / {rn['rejoin_seconds']:.2f}")
    row("Minutes between component failures in the run", f"{rn['minutes_between_component_failures']:.0f}")
    row("Token stream to the cluster (MB/s)", f"{rn['token_bytes_per_second_mb']:.0f}")
    head("SCALING LADDER")
    for name, n, tokens, flops, where, days in rn["ladder"]:
        row(f"{name} ({where})"[:60], f"{si(n)} params, {si(tokens)} tokens, {sci(flops)} FLOPs, {days:.2f} days")

    po, cb = d["post_training"], d["compute_budget"]
    head("POST-TRAINING (one pass through every stage)")
    for name, f in po["stages"].items():
        row(name, f"{sci(f)}   {f / po['one_pass_flops']:.0%}")
    row("One pass: FLOPs / full-campus days", f"{sci(po['one_pass_flops'])} / {po['one_pass_days_full_cluster']:.1f}")
    row("With variants and reruns: FLOPs / full-campus days", f"{sci(po['with_variants_flops'])} / {po['with_variants_days_full_cluster']:.1f}")
    row("Reasoning RL tokens / agentic RL tokens", f"{si(po['reasoning_tokens'])} / {si(po['agent_tokens'])}")
    row("Sandbox-hours / concurrent sandboxes / vCPUs", f"{si(po['sandbox_hours'])} / {po['concurrent_sandboxes']:,.0f} / {po['sandbox_vcpus']:,.0f}")

    head("FIRST-YEAR COMPUTE BUDGET (share of one campus-year)")
    for name, f, share in cb["rows"]:
        row(name[:60], f"{sci(f)}   {share:.1%}")

    head("DATA MIX (trillions of tokens)")
    for name, t, share in d["data_mix"]["rows"]:
        row(name[:60], f"{t:>6.0f}   {share:.0%}")
    row("TOTAL", f"{d['data_mix']['total_t']:>6.0f}")
    row("By kind", ", ".join(f"{k} {v:.0f}" for k, v in d["data_mix"]["by_kind"].items()))
    row("Check: speech tokens from licensed hours (T)", f"{st['speech_tokens_t']:.1f}")
    row("Check: video tokens per sampled frame", f"{st['video_tokens_per_frame']:.0f}")

    head("STORAGE")
    row("Raw crawl / images / video / audio (PB)", f"{st['crawl_pb']:.1f} / {st['images_pb']:.1f} / {st['video_pb']:.1f} / {st['audio_pb']:.1f}")
    row("Raw total (PB) / tokenized training set (PB)", f"{st['raw_pb']:.1f} / {st['tokenized_pb']:.2f}")
    row("Data lake to provision (PB)", f"{st['data_lake_provisioned_pb']:.0f}")
    row("Checkpoint: weights only / full state (TB)", f"{st['weights_checkpoint_tb']:.1f} / {st['full_checkpoint_tb']:.1f}")
    row("Checkpoint store (PB)", f"{st['checkpoint_store_pb']:.1f}")
    row("Write rate to land a full checkpoint in 5 min (GB/s)", f"{st['checkpoint_write_gb_s']:.0f}")
    row("Flash tier (PB) / full checkpoint time on it (s)", f"{st['flash_tier_pb']:.0f} / {st['full_checkpoint_seconds_on_flash']:.0f}")

    head("CRAWL AND INGEST")
    row("Pages per second / billions per day", f"{cr['pages_per_second']:,.0f} / {cr['pages_per_day_b']:.2f}")
    row("Crawl bandwidth (Gbit/s)", f"{cr['crawl_gbps']:.0f}")
    row("Media ingest bandwidth (Gbit/s)", f"{cr['media_ingest_gbps']:.0f}")

    head("POWER AND COOLING")
    row("Facility power: annual average / nameplate (MW)", f"{pw['facility_mw']:,.0f} / {pw['facility_nameplate_mw']:,.0f}")
    row("Energy per year: full load / at load factor (TWh)", f"{pw['energy_twh_per_year']:.2f} / {pw['energy_twh_per_year_at_load_factor']:.2f}")
    row("Electricity per year: full load / load factor ($M)", f"{pw['energy_cost_usd_m_per_year']:,.0f} / {pw['energy_cost_usd_m_per_year_at_load_factor']:,.0f}")
    row("CO2 per year, full load: combined cycle / aero (Mt)", f"{pw['co2_mt_per_year_if_gas']:.2f} / {pw['co2_mt_per_year_if_aero']:.2f}")
    row("Equivalent US homes", f"{pw['equivalent_us_homes']:,.0f}")
    row("Heat to liquid (MW)", f"{pw['liquid_heat_mw']:,.0f}")
    row("Coolant flow (m3/s) / (L/min)", f"{pw['coolant_flow_m3_s']:.1f} / {pw['coolant_flow_l_min']:,.0f}")
    row("Coolant flow per GPU rack (L/min)", f"{pw['coolant_flow_l_min_per_gpu_rack']:.0f}")
    row("Coolant distribution units / heat-rejection units", f"{pw['cdus']:,} / {pw['dry_coolers']:,}")

    head("BACKEND NETWORK (8 planes, two tiers each)")
    row("800G host ports / Tbit/s per GPU", f"{nw['host_ports_800g']:,} / {nw['tbps_per_gpu']:.1f}")
    row("Largest two-tier plane these switches allow (GPUs)", f"{nw['max_gpus_two_tier']:,}")
    row("Leaf / spine per plane; switch chassis in total", f"{nw['leaf_per_plane']} / {nw['spine_per_plane']}; {nw['fabric_switches']:,}")
    row("200G lanes: host side / leaf-spine", f"{nw['host_lanes_200g']:,} / {nw['leaf_spine_lanes_200g']:,}")
    row("800G-equivalent optical links", f"{nw['links_800g_equivalent']:,}")
    row("Host-side 800G transceivers / pluggables without CPO", f"{nw['host_transceivers_800g']:,} / {nw['pluggables_if_no_cpo']:,}")
    row("Edge capacity / bisection (Pbit/s)", f"{nw['edge_capacity_pbps']:.0f} / {nw['bisection_pbps']:.0f}")

    kv, fleet, rc = d["kv_cache"], d["serving_fleet"], d["rack_cost"]
    head("INFERENCE: rack economics and context cache")
    for name, v in rc["parts"].items():
        row(f"Rack-year: {name} ($M)", f"{v:.2f}")
    row("Rack-year total ($M)", f"{rc['total']:.2f}")
    row("Cache per token (MB)", f"{kv['bytes_per_token'] / 1e6:.3f}")
    row("Cache at typical / maximum context (GB)", f"{kv['typical_context_gb']:.1f} / {kv['max_context_gb']:.0f}")
    row("Rack memory left after weights (TB)", f"{kv['free_memory_tb']:.1f}")
    row("Streams that fit: typical / maximum context", f"{kv['streams_at_typical_context']:,.0f} / {kv['streams_at_max_context']:.0f}")
    row("Flagship fleet: racks / MW / share of campus", f"{fleet['racks']} / {fleet['power_mw']:.0f} / {fleet['share_of_campus']:.0%}")
    row("Flagship fleet: tok/s average / trillions per day / streams", f"{fleet['tok_s']:,.0f} / {fleet['tokens_per_day_t']:.2f} / {fleet['streams']:,.0f}")

    for label, key in (("flagship (sparse, top-8)", "inference_flagship"), ("sparser variant (top-2)", "inference_top2"),
                       ("denser variant (top-16)", "inference_top16"),
                       ("dense 100-day optimum", "inference_dense_opt"), ("dense 10T", "inference_dense_10t"),
                       ("mid tier", "inference_mid"), ("small tier", "inference_small")):
        x = d[key]
        head(f"INFERENCE on one rack: {label}")
        row("FLOPs per generated token / weights at 4-bit (TB)", f"{sci(x['flops_per_token'])} / {x['weights_tb']:.2f}")
        row("Rack throughput: compute bound / planning (tok/s)", f"{x['rack_compute_bound_tok_s']:,.0f} / {x['rack_planning_tok_s']:,.0f}")
        row("Per stream: bandwidth bound / planning (tok/s)", f"{x['stream_bound_tok_s']:,.0f} / {x['stream_planning_tok_s']:,.0f}")
        row("Concurrent streams per rack", f"{x['concurrent_streams_per_rack']:,.0f}")
        row("Cost per million output tokens at 25 / 50 / 75% load ($)", f"{x['cost_at_25']:.2f} / {x['cost_usd_per_m_output_tokens']:.2f} / {x['cost_at_75']:.2f}")
        row("Tokens per day per rack (billions)", f"{x['tokens_per_day_per_rack_b']:.1f}")

    head("TEAM")
    for name, h, c in tm["rows"]:
        row(name[:60], f"{h:>5}   ${h * c / 1000:.2f}B")
    row("TOTAL", f"{tm['headcount']:>5}   ${tm['cost_usd_b_per_year']:.2f}B per year")

    head("COST ($B)")
    for name, v in co["capex"].items():
        row(f"capex: {name}", f"{v:6.2f}")
    row("IT hardware / facility and power", f"{co['it_hardware_usd_b']:.1f} / {co['facility_power_usd_b']:.1f}")
    row("CAPEX TOTAL", f"{co['capex_total_usd_b']:6.1f}   (${co['capex_usd_b_per_gw']:.0f}B per GW)")
    for name, v in co["opex_per_year"].items():
        row(f"steady-state per year: {name}", f"{v:6.2f}")
    row("STEADY-STATE OPERATING COST per year", f"{co['opex_total_usd_b_per_year']:6.1f}")
    for name, v in co["operating_to_launch"].items():
        row(f"before launch: {name}", f"{v:6.2f}")
    row("OPERATING COST BEFORE LAUNCH", f"{co['operating_to_launch_usd_b']:6.1f}")
    row("PROGRAM TOTAL TO LAUNCH", f"{co['program_total_usd_b']:6.1f}")
    add("")
    return "\n".join(L)


if __name__ == "__main__":
    data = build()
    if "--json" in sys.argv:
        print(json.dumps(data, indent=2, default=str))
    else:
        print(report(data))
