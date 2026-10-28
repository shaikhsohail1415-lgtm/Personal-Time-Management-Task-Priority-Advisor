from fuzzy.inference import MamdaniFuzzySystem

fis = MamdaniFuzzySystem()
r = fis.infer(85, 90, 80, 70)
assert 0 <= r["score"] <= 100
assert r["level"] in {"Very Low","Low","Medium","High","Very High"}
assert r["memberships"]
assert isinstance(r["rules"], list)
print("Fuzzy engine smoke test passed.")
print("Score:", round(r["score"], 2), "Level:", r["level"])
