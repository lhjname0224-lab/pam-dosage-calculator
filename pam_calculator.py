#!/usr/bin/env python3
"""PAM Dosage Calculator — Open-source CLI tool for estimating polyacrylamide flocculant consumption.

Reference & interactive web calculator:
  https://chinapolyacrylamide.com/tools/pam-dosage-consumption-calculator
  https://chinapolyacrylamide.com/blog/polyacrylamide-dosage-calculation
"""

import argparse
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ApplicationPreset:
    key: str
    name: str
    pam_type: str
    unit: str
    dosage_range: Tuple[float, float]
    default_dosage: float
    mode: str  # "flow_mgl" | "sludge_ds" | "ore_g_per_ton" | "paper_kg_per_ton"


PRESETS: Dict[int, ApplicationPreset] = {
    1: ApplicationPreset(
        key="municipal-wastewater",
        name="Municipal wastewater clarification",
        pam_type="Anionic (APAM)",
        unit="mg/L",
        dosage_range=(0.5, 2.0),
        default_dosage=1.0,
        mode="flow_mgl",
    ),
    2: ApplicationPreset(
        key="industrial-effluent",
        name="Industrial effluent treatment",
        pam_type="Anionic (APAM) or Cationic (CPAM) by water charge",
        unit="mg/L",
        dosage_range=(2.0, 10.0),
        default_dosage=5.0,
        mode="flow_mgl",
    ),
    3: ApplicationPreset(
        key="sludge-belt-press",
        name="Sludge dewatering (belt press)",
        pam_type="Cationic (CPAM)",
        unit="kg/ton DS",
        dosage_range=(2.0, 6.0),
        default_dosage=3.0,
        mode="sludge_ds",
    ),
    4: ApplicationPreset(
        key="sludge-centrifuge",
        name="Sludge dewatering (decanter centrifuge)",
        pam_type="Cationic (CPAM)",
        unit="kg/ton DS",
        dosage_range=(3.0, 8.0),
        default_dosage=4.5,
        mode="sludge_ds",
    ),
    5: ApplicationPreset(
        key="mining-tailings",
        name="Mining tailings thickening",
        pam_type="Anionic (APAM) or Nonionic (NPAM) for acidic slurries",
        unit="g/ton ore",
        dosage_range=(20.0, 100.0),
        default_dosage=40.0,
        mode="ore_g_per_ton",
    ),
    6: ApplicationPreset(
        key="paper-retention",
        name="Paper making retention & drainage",
        pam_type="Cationic (CPAM)",
        unit="kg/ton paper",
        dosage_range=(0.3, 1.5),
        default_dosage=0.6,
        mode="paper_kg_per_ton",
    ),
}


def compute_daily_kg(preset: ApplicationPreset, quantity: float, dosage: float, solids_pct: float = 0.0) -> Tuple[float, float]:
    """Return (daily_pam_kg, dry_solids_tons_per_day_or_0)."""
    if preset.mode == "flow_mgl":
        return quantity * dosage / 1000.0, 0.0
    if preset.mode == "sludge_ds":
        ds_tons = quantity * solids_pct / 100.0
        return ds_tons * dosage, ds_tons
    if preset.mode == "ore_g_per_ton":
        return quantity * dosage / 1000.0, 0.0
    if preset.mode == "paper_kg_per_ton":
        return quantity * dosage, 0.0
    raise ValueError(f"Unsupported calculation mode: {preset.mode}")


def print_summary(preset: ApplicationPreset, daily_kg: float, ds_tons: float, dosage: float) -> None:
    print(f"\n--- {preset.name} ---")
    print(f"Recommended PAM Type : {preset.pam_type}")
    print(f"Typical Dosage Range : {preset.dosage_range[0]}-{preset.dosage_range[1]} {preset.unit}")
    print(f"Selected Dosage      : {dosage} {preset.unit}")
    print("\n--- Consumption Estimate ---")
    if ds_tons > 0:
        print(f"Dry solids per day   : {ds_tons:.2f} tons/day")
    print(f"Daily PAM consumption: {daily_kg:.2f} kg/day")
    print(f"Monthly (30 days)    : {daily_kg * 30:.1f} kg/month")
    print(f"Annual (365 days)    : {daily_kg * 365 / 1000:.2f} tons/year")
    print("\n--- Standard Make-Down Reference ---")
    print("Stock concentration  : 0.1%-0.2% (1-2 g/L)")
    print("Dissolution water    : 500-1,000 L clean water per 1 kg dry powder")
    print("Agitation time       : 45-60 minutes at low shear; use within 24 hours")
    print("Note                 : Confirm final grade and dosage with site jar tests.")
    print("\nWeb calculator & jar-test reference:")
    print("  https://chinapolyacrylamide.com/tools/pam-dosage-consumption-calculator")
    print("  https://chinapolyacrylamide.com/blog/polyacrylamide-jar-test-procedure")


def run_interactive() -> None:
    print("\n=== PAM Dosage Calculator ===")
    print("Reference: https://chinapolyacrylamide.com/tools/pam-dosage-consumption-calculator\n")
    for idx, p in PRESETS.items():
        print(f"  {idx}. {p.name} ({p.dosage_range[0]}-{p.dosage_range[1]} {p.unit})")
    choice = int(input("\nSelect application (1-6): ").strip())
    if choice not in PRESETS:
        raise SystemExit("Invalid application number. Choose 1-6.")
    preset = PRESETS[choice]
    solids_pct = 0.0
    if preset.mode == "flow_mgl":
        quantity = float(input("Enter daily flow rate (m3/day): ").strip())
    elif preset.mode == "sludge_ds":
        quantity = float(input("Enter daily wet sludge volume (m3/day): ").strip())
        solids_pct = float(input("Enter sludge dry solids content (%): ").strip())
    elif preset.mode == "ore_g_per_ton":
        quantity = float(input("Enter daily dry ore/solids tonnage (tons/day): ").strip())
    else:
        quantity = float(input("Enter daily paper production (tons/day): ").strip())
    raw_dosage = input(f"Enter dosage ({preset.unit}, default {preset.default_dosage}): ").strip()
    dosage = float(raw_dosage) if raw_dosage else preset.default_dosage
    daily_kg, ds_tons = compute_daily_kg(preset, quantity, dosage, solids_pct)
    print_summary(preset, daily_kg, ds_tons, dosage)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate polyacrylamide (PAM) flocculant daily and monthly consumption."
    )
    parser.add_argument("--app", type=int, choices=sorted(PRESETS.keys()), help="Application preset ID (1-6)")
    parser.add_argument("--quantity", type=float, help="Daily flow (m3/day), sludge volume (m3/day), or tonnage (tons/day)")
    parser.add_argument("--solids", type=float, default=3.0, help="Sludge dry solids %% (for apps 3 and 4)")
    parser.add_argument("--dosage", type=float, help="Custom dosage in preset units")
    args = parser.parse_args()

    if args.app is None:
        run_interactive()
        return

    if args.quantity is None or args.quantity <= 0:
        parser.error("--quantity must be a positive number when --app is specified.")
    preset = PRESETS[args.app]
    dosage = args.dosage if args.dosage is not None else preset.default_dosage
    daily_kg, ds_tons = compute_daily_kg(preset, args.quantity, dosage, args.solids)
    print_summary(preset, daily_kg, ds_tons, dosage)


if __name__ == "__main__":
    main()
