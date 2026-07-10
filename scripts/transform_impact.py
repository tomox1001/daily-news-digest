#!/usr/bin/env python3
"""
Transform news-digest HTML files:
1. Extract impact-grid blocks from individual articles
2. Remove those blocks from articles
3. Add a consolidated commentary section before </main>
"""

import re
import glob
import os

files = sorted(glob.glob('/Users/tomonori-kawano/Project/daily_news_digest/docs/news-digest-2026-*.html'))

for filepath in files:
    basename = os.path.basename(filepath)

    if 'news-digest-2026-03-22' in filepath:
        print(f"SKIP (already done): {basename}")
        continue

    with open(filepath, 'r') as f:
        content = f.read()

    # Check if impact-grid exists in the file
    if 'impact-grid' not in content:
        print(f"SKIP (no impact-grid): {basename}")
        continue

    # Check if already transformed (has commentary-section)
    if 'commentary-section' in content:
        print(f"SKIP (already transformed): {basename}")
        continue

    # Extract all impact texts before removing them
    # Handle both <p>/<div> for impact-text, and <div>/<span> for impact-label
    lm_texts = re.findall(
        r'<div class="impact-box lm-impact">\s*<(?:div|span) class="impact-label">[^<]*</(?:div|span)>\s*<(?:p|div) class="impact-text">\s*(.*?)\s*</(?:p|div)>\s*</div>',
        content, re.DOTALL
    )
    hr_texts = re.findall(
        r'<div class="impact-box hr-impact">\s*<(?:div|span) class="impact-label">[^<]*</(?:div|span)>\s*<(?:p|div) class="impact-text">\s*(.*?)\s*</(?:p|div)>\s*</div>',
        content, re.DOTALL
    )

    if not lm_texts and not hr_texts:
        print(f"SKIP (no impact texts extracted): {basename}")
        continue

    # Remove impact-grid blocks from articles
    # The structure is: <div class="impact-grid"> ... </div>\n  </div>\n  </div>
    # We need to match the outer impact-grid div and its two child impact-box divs
    content_new = re.sub(
        r'\s*<div class="impact-grid">\s*<div class="impact-box lm-impact">.*?</div>\s*<div class="impact-box hr-impact">.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # Verify removal worked
    # Count remaining impact-grid in non-CSS parts (CSS definitions should remain)
    body_part = content_new.split('</style>')[-1] if '</style>' in content_new else content_new
    remaining = body_part.count('<div class="impact-grid">')
    if remaining > 0:
        print(f"WARNING: {basename} still has {remaining} impact-grid blocks in body after removal!")

    # Build commentary section
    lm_combined = '\n'.join([f'        <p class="impact-text">{t.strip()}</p>' for t in lm_texts])
    hr_combined = '\n'.join([f'        <p class="impact-text">{t.strip()}</p>' for t in hr_texts])

    commentary = f"""
  <!-- ===== 総評：LMビジネスへの影響 & HR／組織への示唆 ===== -->
  <section class="commentary-section">
    <h2 class="commentary-title">📊 総評：本日のニュースが示すLMビジネスと組織への影響</h2>
    <div class="impact-grid" style="margin-bottom: 32px;">
      <div class="impact-box lm-impact">
        <div class="impact-label">📊 LMビジネスへの影響</div>
{lm_combined}
      </div>
      <div class="impact-box hr-impact">
        <div class="impact-label">👥 HR／組織への示唆</div>
{hr_combined}
      </div>
    </div>
  </section>
"""

    # Insert before </main>
    content_new = content_new.replace('</main>', commentary + '\n</main>')

    # Add CSS if not already present
    if '.commentary-section' not in content_new:
        css_addition = """
.commentary-section {
  margin-top: 48px;
  padding-top: 48px;
  border-top: 3px solid var(--border);
}
.commentary-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 24px;
  padding-left: 4px;
}
.commentary-section .impact-box {
  padding: 28px;
}
.commentary-section .impact-text + .impact-text {
  margin-top: 12px;
}
"""
        content_new = content_new.replace('</style>', css_addition + '</style>')

    with open(filepath, 'w') as f:
        f.write(content_new)

    print(f"DONE: {basename} (LM: {len(lm_texts)}, HR: {len(hr_texts)})")
