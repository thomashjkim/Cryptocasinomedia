with open('explore.html', 'r', encoding='utf-8') as f:
    exp = f.read()

exp = exp.replace("'1mi · Brooklyn, NY'", "'Brooklyn, NY'")
exp = exp.replace("1mi · ", "")
exp = exp.replace("1mi ", "")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp)

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx = idx.replace("'1mi · Brooklyn, NY'", "'Brooklyn, NY'")
idx = idx.replace("1mi · ", "")
idx = idx.replace("1mi ", "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print("✅ Removed all 1mi occurrences from explore.html and index.html")
