# Research Steps — Social Media and Mental Health Analytics

Reconstructed from the project poster and the two analysis figures
(`rq1_screen_time_vs_anxiety.png`, `rq2_sleep_vs_late_night.png`).

## 1. Problem Definition
- **Context:** Social media usage is constantly rising and is affecting young adults' mental health.
- **Core concern:** Heavy / late-night social media use may be linked to anxiety and poor sleep.
- **Research questions:**
  - **RQ1:** Does more **screen time** affect **anxiety** levels?
  - **RQ2:** Does social media usage **at night** affect **sleep** time?

## 2. State of the Art / Current Issues
- Anxiety (especially in young adults / Gen Z) is rising in parallel with screen time.
- Standard clinical instrument: **GAD-7** for anxiety — used as the outcome variable here.
- Open issues in the field:
  - Most evidence is **cross-sectional** -> correlation, not causation.
  - **Directionality** unclear (does screen time cause anxiety, or vice versa?).
  - Inconsistent measures of "nighttime use" across studies.

## 3. Existing Research (literature grounding)
References in `ref.txt` position this work in prior literature:
- **Screen time <-> anxiety:** Vannucci et al. (2017); Keles et al. (2020); Tang et al. (2021).
- **Nighttime use <-> sleep:** Levenson et al. (2016); Alonzo et al. (2021).
- Gap addressed: a **quantitative, statistics-first** demonstration of both effects on one
  dataset with clear visual reporting.

## 4. Proposed Approach (data analysis + improved analytics presentation)
- **Dataset:** ~8,000 social-media users, 15 columns; computer-generated but grounded in
  psychological research.
- **Data preparation:** handle **outliers** and **missing data** (did not affect the results).
- **Statistical methods:**
  - **RQ1 — One-way ANOVA:** compares mean **GAD-7** across the **4 screen-time quartiles**
    (Q1 Low -> Q4 High). *(Figure: `rq1_screen_time_vs_anxiety.png` — boxplots + scatter, r = 0.63.)*
  - **RQ2 — Independent-samples t-test:** compares mean **sleep duration** between
    **late-night vs. no late-night** users. *(Figure: `rq2_sleep_vs_late_night.png` — boxplots + distributions.)*
- **Improved analytics/visualization:** boxplots, scatter with trend line, and distribution
  histograms to make group differences visually obvious.

## 5. Results & Lessons Learned
- **RQ1:** GAD-7 rises across screen-time quartiles; scatter shows a **moderate positive
  correlation (r = 0.63)** -> more screen time => higher anxiety.
- **RQ2:** Late-night users sleep **less** (median ~5.1h vs ~6.3h); distributions shift left
  -> late-night use => shorter sleep.
- **Significance:** **p < 0.0001** for both -> reject the null; results unlikely due to chance.
- **Conclusion:** Social media usage **increases anxiety** and **reduces sleep**.
- **Recommendation:** Reduce social media use overall, **especially at night before bed**.
- **Lesson:** Correlational/observational design — significant association, but **not proof of
  causation**; synthetic data limits generalizability.

## 6. Further Research
- Use **real-world (non-synthetic)** data and **longitudinal** designs to test causality.
- Add **controls/covariates** (age, gender, baseline mental health, socioeconomic status).
- Distinguish **passive vs. active** use and **specific platforms** (effects differ by platform).
- Move beyond ANOVA/t-test to **regression / mediation models** (e.g., does sleep mediate the
  screen-time -> anxiety link?).
- Consider **predictive ML models** for individual anxiety/sleep risk.
