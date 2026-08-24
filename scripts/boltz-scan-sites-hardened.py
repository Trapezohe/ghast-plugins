#!/usr/bin/env python3
"""Discover binder contact-site clusters without mixing in target-only chains."""

import argparse
import json
import os
import sys
from collections import Counter

import gemmi
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import atom_coords, indexed_residues  # noqa: E402


def load_records(run_dir):
    index_path = os.path.join(run_dir, "results", "index.jsonl")
    if not os.path.exists(index_path):
        alternate = os.path.join(run_dir, "index.jsonl")
        index_path = alternate if os.path.exists(alternate) else index_path
    if not os.path.exists(index_path):
        sys.exit(f"error: no results/index.jsonl under {run_dir}")
    records = []
    with open(index_path) as source:
        for line in source:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _binder_chain_names(model, target_chain, binder_chains=None):
    """Select binder chains, inferring only an unambiguous single chain."""
    available = {chain.name for chain in model}
    if binder_chains:
        selected = set(binder_chains)
        if target_chain in selected:
            raise ValueError(
                f"target chain '{target_chain}' cannot also be a binder chain"
            )
        missing = selected - available
        if missing:
            raise ValueError(
                f"binder chain(s) {', '.join(sorted(missing))} not found "
                f"(available chains: {', '.join(sorted(available))})"
            )
        return selected

    candidates = available - {target_chain}
    if len(candidates) != 1:
        raise ValueError(
            "binder chains are ambiguous; pass --binder-chain once for each "
            "generated binder chain"
        )
    return candidates


def footprint(cif_path, target_chain, cutoff, binder_chains=None):
    """Return target indices contacted by the selected binder chains."""
    structure = gemmi.read_structure(cif_path)
    structure.setup_entities()
    model = structure[0]
    target = next((chain for chain in model if chain.name == target_chain), None)
    if target is None:
        return None
    selected = _binder_chain_names(model, target_chain, binder_chains)
    pairs, _ = indexed_residues(target.get_polymer())
    binder = np.array(
        [
            [atom.pos.x, atom.pos.y, atom.pos.z]
            for chain in model
            if chain.name in selected
            for residue in chain
            for atom in residue
        ],
        dtype=float,
    )
    if len(binder) == 0:
        return set()
    site = set()
    for index, residue in pairs:
        coordinates = atom_coords(residue)
        squared = (
            (coordinates[:, None, :] - binder[None, :, :]) ** 2
        ).sum(-1)
        if np.sqrt(squared.min()) < cutoff:
            site.add(index)
    return site


def jaccard(left, right):
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def cluster_sites(sites, threshold):
    """Return deterministic single-linkage connected components."""
    remaining = set(range(len(sites)))
    clusters = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        cluster = []
        pending = [seed]
        while pending:
            current = pending.pop()
            cluster.append(current)
            neighbors = {
                other
                for other in remaining
                if jaccard(sites[current], sites[other]) > threshold
            }
            remaining.difference_update(neighbors)
            pending.extend(sorted(neighbors, reverse=True))
        clusters.append(sorted(cluster))
    return sorted(clusters, key=lambda cluster: (-len(cluster), cluster))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("run_dir")
    parser.add_argument("--target-chain", default="A")
    parser.add_argument(
        "--binder-chain",
        action="append",
        help=(
            "generated binder chain ID; repeat for a multi-chain binder "
            "(required when more than one non-target chain is present)"
        ),
    )
    parser.add_argument(
        "--top", type=int, default=20, help="top designs by bc (default 20)"
    )
    parser.add_argument(
        "--cutoff",
        type=float,
        default=6.0,
        help="all-atom contact cutoff in angstrom (default 6)",
    )
    parser.add_argument(
        "--jaccard",
        type=float,
        default=0.25,
        help="Jaccard threshold for single-linkage clustering (default 0.25)",
    )
    args = parser.parse_args()

    records = load_records(args.run_dir)
    records.sort(
        key=lambda record: record.get("metrics", {}).get(
            "binding_confidence", -1
        ),
        reverse=True,
    )
    sites = []
    for record in records[: args.top]:
        relative_path = record.get("paths", {}).get("structure")
        if not relative_path:
            continue
        cif_path = os.path.join(args.run_dir, relative_path)
        if not os.path.exists(cif_path):
            print(f"warning: missing {cif_path}", file=sys.stderr)
            continue
        try:
            site = footprint(
                cif_path,
                args.target_chain,
                args.cutoff,
                args.binder_chain,
            )
        except ValueError as error:
            sys.exit(f"error: {error}")
        if site:
            sites.append(site)
    if not sites:
        sys.exit(
            "error: no footprints computed (check --target-chain and that "
            "per-design CIFs are downloaded)"
        )

    clusters = cluster_sites(sites, args.jaccard)
    print(f"# {len(sites)} footprints -> {len(clusters)} site cluster(s)")
    for index, cluster in enumerate(clusters):
        counts = Counter()
        for member in cluster:
            counts.update(sites[member])
        minimum_hits = 2 if len(cluster) >= 2 else 1
        consensus = sorted(
            residue
            for residue, count in counts.items()
            if count >= minimum_hits
        )
        print(
            f"# cluster {index}: {len(cluster)} design(s), "
            f"consensus {len(consensus)} residues"
        )
        print(json.dumps(consensus))


if __name__ == "__main__":
    main()
