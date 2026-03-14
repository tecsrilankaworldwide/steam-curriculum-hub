# STEAM Curriculum Hub — Updated Plan (POC → V1 → Features → Testing)

## 1) Objectives
- Prove the **core learning flow** works end-to-end: **browse → open lesson → switch language (EN/Si/Ta) → bilingual display → premium checkout → return**.
- Complete multilingual content pipeline in a controlled way:
  - Round 1: **Sinhala + Tamil (GPT-5.2)** for all AI lessons (running).
  - Round 2: **Mandarin + Cantonese (GPT-4o-mini)** with smaller, cost-controlled scope.
- Ship a stable V1 experience including:
  - **AI-STEAM curriculum** browsing by age group
  - **Word Glossary** (EN ↔ native)
  - **Payments** (Stripe + Sri Lanka bank option)
  - **Branding** aligned to Education Reforms Bureau + TEC Sri Lanka Worldwide Pvt Ltd
- Maintain reliability: translation jobs resumable, no schema breaks, solid QA.

---

## 2) Implementation Steps (Phased)

### Phase 1 — Core Workflow POC (isolation + fix until works)
**Why:** Translation + payments are external dependencies; validate core flows before expanding.

**User stories (POC)**
1. As a learner, I can load the lesson catalog from MongoDB and open a lesson detail page.
2. As a learner, I can toggle language between **English and Sinhala/Tamil** and see translated text if available.
3. As an admin, I can run a translation job and see translated fields appear in MongoDB.
4. As a product owner, I can measure translation progress and resume safely after interruption.
5. As a tester, I can confirm the API returns consistent lesson schema across languages.

**POC tasks — Status**
- ✅ Fixed data scripts (generator/loader/translator) to remove hardcoded paths and use env-driven MongoDB.
- ✅ Generated **1000 AI lessons** across 5 age groups.
- ✅ Loaded **1000 AI lessons** into MongoDB Atlas.
- 🔄 Translation Round 1 (GPT-5.2): **Sinhala + Tamil** running in background (**174/1000 complete**).
- ✅ Sync translated lessons to local MongoDB for preview/testing.

**Exit criteria (POC)**
- ✅ Lessons reliably served with schema: `title/description/content` as language maps.
- ✅ Language switching works with correct fallback.
- ✅ Translation progress measurable and resumable.

---

### Phase 2 — V1 App Development (MVP around proven core)
**Focus:** Learner browsing + lesson viewing + language UX polish.

**User stories (V1)**
1. As a parent/teacher, I can filter lessons by **curriculum, subject, grade, age group**.
2. As a student, I can open a lesson and read in English.
3. As a student, I can switch to Sinhala/Tamil; the UI remembers my choice.
4. As a student, I see clear fallback to English when a translation is missing.
5. As a user, I can share a lesson link.

**Build steps — Status**
- ✅ Frontend language switcher updated to use **DB translations** (no MyMemory dependency) with bilingual display.
- ✅ Lesson detail page includes **Show English / Hide English** toggle when translations exist.
- ✅ AI-STEAM curriculum filter added to lesson catalog.
- ✅ Age-group URL routing implemented: `/lessons?age=5-7` and page banner.
- ✅ Beautiful kid-friendly **section covers** on Home page:
  - 5–7 mint/green, 8–9 soft blue, 10–12 lavender
  - plus 13–15 amber, 16–18 pink
- ✅ Themed age-group lesson cards + subtle watermark.
- ✅ Branding updated in footer:
  - “Made by Education Reforms Bureau”
  - “© TEC Sri Lanka Worldwide Pvt Ltd”

**End of Phase 2 testing**
- ✅ Testing agent: **Backend 98%**, **Frontend 95%**, **0 critical bugs**.

---

### Phase 3 — Add Monetization (Stripe) + Access Control
**Core dependency:** Stripe checkout + status polling + webhook.

**User stories (Payments)**
1. As a user, I can start a subscription checkout and return to the app on success.
2. As a user, I can confirm payment success from the return page.
3. As an admin, I can validate webhook events update transaction status reliably.
4. As a non-subscriber, I see a paywall (future).
5. As a subscriber, I can access premium actions (future gating).

**Build — Status**
- ✅ Stripe checkout integrated:
  - Standard: **$5/mo**
  - Premium: **$10/mo**
- ✅ `PaymentSuccess` page with status polling.
- ✅ Webhook endpoint implemented.
- ✅ Transactions persisted in MongoDB (`payment_transactions`).
- ✅ Sri Lanka bank-transfer option displayed:
  - Standard: **LKR 1500**
  - Premium: **LKR 3000**

**Remaining work (Payments / Access control)**
- ⏳ Implement subscription/user association and enforce gating for premium actions (PDF/full language packs, etc.).
- ⏳ Add idempotency rules and admin view for transactions.

---

### Phase 4 — TTS (Proof + V1)
**Decision update:** TTS will **not** be implemented now because users will rely on **Google Voice app** for voice in target countries.

**Status**
- ✅ No work required for V1.

---

### Phase 5 — Round 2 Translation (Mandarin + Cantonese)
**User stories (Round 2 translation)**
1. As an admin, I can translate a selected language set only (cost control).
2. As an admin, I can translate only missing lessons (resume).
3. As a learner, I can select Mandarin and see translated content.
4. As a learner, I can select Cantonese and see translated content.

**Steps (Planned)**
- Decide language codes:
  - Mandarin: `zh` (Simplified)
  - Cantonese: `yue` (recommended) or `zh-HK` (confirm preferred script: typically Traditional for HK)
- Create a separate translator config for **GPT-4o-mini**.
- Run in controlled batches (e.g., 50 lessons), verify quality, then complete.

---

### Phase 6 — Comprehensive QA + Hardening
**User stories (QA)**
1. As a user, I never see broken lesson pages even if some fields are missing.
2. As a user, navigation stays fast with pagination/search.
3. As an admin, background jobs can be restarted safely.
4. As a subscriber (future), access persists across sessions/devices.
5. As a maintainer, logs/metrics help diagnose failures quickly.

**Tasks (Remaining / Ongoing)**
- Regression test across languages + age groups as translation coverage increases.
- Performance checks (indexes, pagination, search).
- Backup/export plan for lessons + translations.
- Production readiness checks:
  - environment variables
  - webhook config
  - HTTPS + domain

---

## 3) Next Actions (immediate)
1. **Monitor Round 1 translation** until completion; verify counts for `title.si` and `title.ta`.
2. Keep syncing translated lessons from Atlas to the local preview DB (for demos/testing).
3. Add **subscription access control** (gating) on premium features (PDF download, full language packs).
4. Expand the **Word Glossary** beyond 20 terms (optional, staged).
5. Prepare **DigitalOcean production deployment steps**:
   - `git pull` on server
   - ensure `.env` contains Stripe keys and Atlas connection
   - restart services
   - verify webhook URL in Stripe dashboard

---

## 4) Success Criteria
- **Content:** 1000 AI lessons in Atlas; Sinhala + Tamil fields present for ~100% of lessons (or clearly tracked missing).
- **Core UX:** Catalog + lesson detail pages load reliably; language switching instant with correct fallback; bilingual display works.
- **Payments:** Stripe checkout works in test mode; webhook records transactions; PaymentSuccess verification works.
- **Glossary:** Glossary page available with EN ↔ Sinhala/Tamil terms and search/filter.
- **Branding:** Footer shows Education Reforms Bureau + TEC Sri Lanka Worldwide Pvt Ltd; kid-friendly academic palette for 5–12 sections.
- **Reliability:** Translation jobs resumable; no schema breaks; automated tests show no critical issues.
