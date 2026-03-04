---
title: "EXP-06 Results — Tokenization Domain Ratios"
tags: [results, tokenization, tiktoken, bpe, llm-behavior]
aliases: [exp-06-results, tokenization-results]
---

# EXP-06 Results — Tokenization: Domain-Specific Token Ratios

**Run date:** 2026-03-04
**Tokenizer:** `cl100k_base`
**Vocabulary size:** 100,277 tokens
**API calls:** 0 (local computation only)
**Estimated cost:** $0.00

---

## Domain Ratio Summary

| Domain | Words | Tokens | Ratio | vs English prose |
|--------|------:|-------:|------:|:----------------:|
| common_english | 131 | 164 | 1.25 | baseline |
| technical_english | 122 | 163 | 1.34 | 1.07× |
| medical_legal | 104 | 177 | 1.70 | 1.36× |
| emoji_heavy | 93 | 164 | 1.76 | 1.41× |
| python_code | 129 | 271 | 2.10 | 1.68× |
| json_structured | 52 | 216 | 4.15 | 3.32× |
| arabic | 61 | 291 | 4.77 | 3.81× |
| japanese | 7 | 259 | 37.00 | 29.55× |

---

## Hypothesis Verdict

✅ **Confirmed** — The ratio spread between cheapest (common_english: 1.25) and most
expensive (japanese: 37.00) is **29.55×**,
which exceeds the predicted 2× threshold.

---

## Token Boundary Previews

`|` = token boundary. Each segment between pipes is one token.

**common_english** (131 words → 164 tokens, ratio 1.25)
```
The| sun| rose| slowly| over| the| mountains|,| casting| long| golden| shadows|↵|ac|ross| the|
valley| below|.| A| light| breeze| moved| through|…
```

**technical_english** (122 words → 163 tokens, ratio 1.34)
```
Large| language| models| are| aut|ore|gressive| transformer| architectures|↵|that| model| the|
conditional| probability| distribution| over|…
```

**python_code** (129 words → 271 tokens, ratio 2.10)
```
import| tik|token|↵|from| typing| import| Optional|↵↵|def| count|_tokens|(↵|   | text|:| str|,↵|   |
model|:| str| =| "|g|pt|-|4|o|-mini|",↵|   | overhead|…
```

**json_structured** (52 words → 216 tokens, ratio 4.15)
```
{↵| | "|experiment|":| {↵|   | "|id|":| "|EXP|-|06|",↵|   | "|title|":| "|Token|ization| Domain|
Rat|ios|",↵|   | "|status|":| "|in|_progress|",↵|   | "|model|…
```

**japanese** (7 words → 259 tokens, ratio 37.00)
```
人|工|知|能|と|は|、|コ|ン|ピ|ュ|ー�|�|が|人|間|の|よ|う|な|知|的|な|行|動|を|模|�|�|する|技|�|�|の|こ|と|です|。↵|�|�|�|�|�|�|学|�|�|�|
は|、|大|量|の|デ|ー�|�|から|パ|タ|ー|ン|を|学|�|�|�|さ|せ|る|こ|と|で|、|コ|ン|ピ|ュ|ー�|�|に|↵|新|し|い|能|力|を|持|た|せ|る|手|法|です|。|�|
�|�|�|学|�|�|�|は|、|多|�|�|の|ニ|ュ|ー�|…
```

**arabic** (61 words → 291 tokens, ratio 4.77)
```
ال|ذ|ك|اء| ال|ا|ص|ط|ن|ا|ع|ي| ه|و| م|ج|ال| ع|ل|م|ي| ي|ه|د|ف| إ|لى| م|ح|ا|ك|ا|ة| ال|ق|د|ر|ات|
ال|إ|د|ر|ا|ك|ية| ال|ب|ش|ر|ية|↵|ف|ي| ال|أ|ن|ظ|م|ة| ال|ح|اس|و|ب|ية|.| ت|ع|ل|م| ال|�|�|ل|ة| ه|و| أ|ح|د|
ف|رو|ع|ه| ال|…
```

**medical_legal** (104 words → 177 tokens, ratio 1.70)
```
The| patient| presented| with| bilateral| pneumonia|,| hyp|ox|emia|,| and|↵|t|ach|yc|ard|ia|.|
Chest| radi|ograph| revealed| consolidation| in| the|…
```

**emoji_heavy** (93 words → 164 tokens, ratio 1.76)
```
Just| shipped| the| new| feature| �|�|�|�|�|�| and| honestly| couldn|'t| be| more|↵|exc|ited|
�|�|�|�| The| team| crushed| it| this| sprint| �|�|�|�|�| We| went|…
```


---

## Key Numbers

| Metric | Value |
|--------|-------|
| Cheapest domain | `common_english` — 1.25 tokens/word |
| Most expensive domain | `japanese` — 37.00 tokens/word |
| Spread (max/min) | **29.55×** |
| Baseline (common English) | 1.25 tokens/word |

---

*Generated automatically by `code.py` — do not edit manually.*
*For analysis and interpretation → `analysis.md`*
