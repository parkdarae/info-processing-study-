#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""201-300번째 단어 목록 확인"""

import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/cissp_problem_vocabulary.json', 'r', encoding='utf-8') as f:
    vocab = json.load(f)

missing = [(w, data) for w, data in vocab.items() 
           if not data.get('meaning') or data.get('meaning', '').strip() == '']
missing.sort(key=lambda x: x[1].get('frequency', 0), reverse=True)

print("201-300번째 단어:")
print("=" * 80)
for i, (word, data) in enumerate(missing[200:300], 201):
    freq = data.get('frequency', 0)
    print(f"{i:3d}. {word:20s} (빈도: {freq:4d})")

