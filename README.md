# PAM Dosage Calculator

An open-source Python CLI calculator for estimating **polyacrylamide (PAM)** flocculant daily, monthly, and annual consumption across water treatment, sludge dewatering, mining tailings, and paper-making applications.

## Features

- Supports 6 common industrial polymer dosing workflows:
  1. Municipal wastewater clarification (`mg/L`)
  2. Industrial effluent treatment (`mg/L`)
  3. Sludge dewatering — belt filter press (`kg/ton DS`)
  4. Sludge dewatering — decanter centrifuge (`kg/ton DS`)
  5. Mining tailings thickening (`g/ton ore`)
  6. Paper making retention & drainage (`kg/ton paper`)
- Works in both **interactive prompt mode** and **scriptable CLI flag mode**
- Outputs daily, 30-day monthly, and annual polymer estimates plus standard `0.1%–0.2%` solution make-down reminders
- Pure Python standard library (zero third-party dependencies, Python 3.8+)

## Quick Start

### Interactive mode

```bash
python3 pam_calculator.py
```

### Command-line mode

```bash
# Example: 500 m3/day sludge at 3.5% dry solids on a belt press (3.0 kg/ton DS)
python3 pam_calculator.py --app 3 --quantity 500 --solids 3.5 --dosage 3.0
```

Example output:

```text
--- Sludge dewatering (belt press) ---
Recommended PAM Type : Cationic (CPAM)
Typical Dosage Range : 2.0-6.0 kg/ton DS
Selected Dosage      : 3.0 kg/ton DS

--- Consumption Estimate ---
Dry solids per day   : 17.50 tons/day
Daily PAM consumption: 52.50 kg/day
Monthly (30 days)    : 1575.0 kg/month
Annual (365 days)    : 19.16 tons/year

--- Standard Make-Down Reference ---
Stock concentration  : 0.1%-0.2% (1-2 g/L)
Dissolution water    : 500-1,000 L clean water per 1 kg dry powder
Agitation time       : 45-60 minutes at low shear; use within 24 hours
Note                 : Confirm final grade and dosage with site jar tests.
```

## Online Tools & Technical Guides

Prefer a browser-based calculator or full make-down & jar-test reference?

- Interactive PAM Dosage Calculator: https://chinapolyacrylamide.com/tools/pam-dosage-consumption-calculator
- Polymer Solution Preparation Tank Calculator: https://chinapolyacrylamide.com/tools/pam-solution-preparation-tank-calculator
- PAM Grade Selector: https://chinapolyacrylamide.com/tools/pam-selector
- Polyacrylamide Dosage Calculation Guide: https://chinapolyacrylamide.com/blog/polyacrylamide-dosage-calculation
- Jar Test Procedure: https://chinapolyacrylamide.com/blog/polyacrylamide-jar-test-procedure

## About

Maintained by the technical team at [ChinaPAM](https://chinapolyacrylamide.com) (export brand of Henan Jinghua New Material Technology Co., Ltd., Xinxiang, Henan, China).

Need lab samples or grade recommendations for jar testing? Request samples via https://chinapolyacrylamide.com/request-quote.

## License

MIT — see [LICENSE](LICENSE).
