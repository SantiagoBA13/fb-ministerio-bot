# src/verse_history.py
import os
import json
import random
import hashlib
from typing import Dict, Any, List

DEFAULT_HISTORY_PATH = "state/verse_history.json"

def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

def load_history(path: str = DEFAULT_HISTORY_PATH) -> Dict[str, Any]:
    _ensure_parent_dir(path)
    if not os.path.exists(path):
        data = {"version": 1, "seed": None, "slots": {}}
        save_history(data, path)
        return data
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(data: Dict[str, Any], path: str = DEFAULT_HISTORY_PATH) -> None:
    _ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _slot_seed(base_seed: int, slot: str, cycle: int) -> int:
    h = hashlib.sha256(slot.encode("utf-8")).hexdigest()
    slot_int = int(h[:8], 16)
    return base_seed ^ slot_int ^ (cycle * 1000003)

def _build_order(n: int, seed: int) -> List[int]:
    order = list(range(n))
    rng = random.Random(seed)
    rng.shuffle(order)
    return order

def next_index(slot: str, n_items: int, path: str = DEFAULT_HISTORY_PATH) -> int:
    hist = load_history(path)

    if hist.get("seed") is None:
        # seed estable: si no existe, crea uno y ya queda persistente
        hist["seed"] = random.SystemRandom().randint(1, 2_000_000_000)

    base_seed = int(hist["seed"])
    slots = hist.setdefault("slots", {})

    st = slots.get(slot)
    if not st or st.get("n_items") != n_items:
        # Si es primera vez o cambió el tamaño de la lista, reiniciamos estado del slot
        st = {"n_items": n_items, "cycle": 0, "cursor": 0, "order": []}

    # Si no hay order o no coincide, generamos
    if not st.get("order") or len(st["order"]) != n_items:
        st["order"] = _build_order(n_items, _slot_seed(base_seed, slot, int(st["cycle"])))

    cursor = int(st.get("cursor", 0))
    cycle = int(st.get("cycle", 0))

    # Si ya se consumió toda la lista, iniciamos siguiente ciclo (aquí volverá a repetirse,
    # pero solo después de haber usado todos los items)
    if cursor >= n_items:
        cycle += 1
        cursor = 0
        st["cycle"] = cycle
        st["order"] = _build_order(n_items, _slot_seed(base_seed, slot, cycle))

    idx = int(st["order"][cursor])
    st["cursor"] = cursor + 1
    st["n_items"] = n_items

    slots[slot] = st
    hist["slots"] = slots
    save_history(hist, path)

    return idx
