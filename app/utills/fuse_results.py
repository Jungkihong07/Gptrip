from collections import defaultdict
from typing import List, Tuple
from app.place.domain.place import Place


def fuse_results(
    results: List[Tuple[str, List[Place]]], top_k: int, alpha: float
) -> List[Place]:
    score_map = defaultdict(lambda: {"place": None, "text": 0.0, "image": 0.0})

    for source, places in results:
        for place in places:
            title = place.title
            score_map[title]["place"] = place
            score_map[title][source] = 1.0

    def compute_score(entry):
        t = entry["text"]
        i = entry["image"]
        return alpha * t + (1 - alpha) * i

    ranked = sorted(score_map.values(), key=compute_score, reverse=True)
    return [entry["place"] for entry in ranked[:top_k]]
