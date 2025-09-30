import json
import pathlib
import random
import sys
from datetime import datetime, timezone

# Умовні пули — далі легко замінимо на реальні (Uniswap/Curve/Balancer)
POOLS = [
    {"chain": "Base", "pair": "ETH/USDC"},
    {"chain": "Arbitrum", "pair": "ETH/USDT"},
    {"chain": "OP", "pair": "WBTC/ETH"},
]

def mock_volatility():
    # добова волатильність, %
    return round(random.uniform(0.3, 5.0), 2)

def mock_volume_usd():
    # добовий обіг, USD
    return round(random.uniform(50_000, 2_000_000), 2)

def mock_apr():
    # плейсхолдер APR з фі
    return round(random.uniform(2.0, 18.0), 2)

def build_snapshot():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data = {"ts": now, "pools": []}
    for p in POOLS:
        data["pools"].append({
            "chain": p["chain"],
            "pair": p["pair"],
            "volatility_24h_pct": mock_volatility(),
            "volume_24h_usd": mock_volume_usd(),
            "fee_apr_est_pct": mock_apr()
        })
    return data

def write_snapshot(payload):
    dt = datetime.now(timezone.utc)
    folder = pathlib.Path("data") / dt.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{dt.strftime('%H%M%S')}.json"  # унікально до секунд
    path.write_text(json.dumps(payload, indent=2))
    return path

if __name__ == "__main__":
    out = write_snapshot(build_snapshot())
    print(f"[update.py] wrote file: {out}")
    sys.exit(0)
