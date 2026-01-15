# Strategic Web Development Plan: Pedro Alcàcer

Based on the recent UX/UI and Digital Marketing audit, this roadmap outlines the steps to professionalize `pedroalcacer.com` and capture both the "Early Music" and "Sound Design" markets. This plan is designed to be executed over 5 days (or phases).

## Overview
- **Goal:** Transform the site from a "business card" into a "marketing engine".
- **Key Focus:** Duality (Classical vs. Electronic), Promoter Friction (EPK), and Accessibility.

---

## Phase 1: Accessibility, SEO & Foundation (Day 1)
*Audit Steps: 4 & 5*

**Objective:** Immediate quick wins to improve readability, navigation, and search visibility.

1.  **Contrast & Typography Overhaul**
    *   **Action:** Update `style.css` to darken body text from `#888` to `#222`.
    *   **Action:** Increase font size for navigation menu for better clickability.
    *   **Action:** Verify/Add Alt-Text to key instrument images.
2.  **Navigation & Languages**
    *   **Action:** Review Mobile implementation (Hamburger menu) vs Desktop Top Bar.
    *   **Action:** Ensure the Multilingual Toggle (ES | EN | DE | CA | FR | IT) is prominent and easy to use on all devices.
3.  **SEO Fundamentals**
    *   **Action:** Update `config.toml` or page headers to include high-value keywords ("Theorbo player Berlin", "Sound Design").

## Phase 2: The New "Sound Design" Sector (Day 2)
*Audit Step: 3 (Addressing the "Sound Design Ghost")*

**Objective:** Create the destination content for the "Electronic" persona before we link to it.

1.  **Content Creation**
    *   **Action:** Create a new content section `sound-design` (or `electronic`) in all languages.
    *   **Action:** Create a layout that supports "One-click" playback (embedded audio/video players) specifically for this section.
    *   **Action:** Highlight "Modern/Electronic" works distinct from the classical "Programs".

## Phase 3: The Promoter Path (Day 3)
*Audit Step: 3 (The 2-Click Rule)*

**Objective:** Make it effortless for a promoter to book Pedro.

1.  **EPK Implementation (`/epk`)**
    *   **Action:** Create a dedicated "Electronic Press Kit" page (possibly hidden from main nav, or linked via Footer/About).
    *   **Action:** Include:
        *   High-Res Headshot Downloads (Zip or direct links).
        *   Short/Medium/Long Bios (Copy-paste ready).
        *   Direct "Booking Inquiry" form.
    *   **Action:** Clarify the "Calendar" view (Past vs Upcoming) to show momentum.

## Phase 4: The "Split-Screen" Homepage (Day 4)
*Audit Step: 1*

**Objective:** The visual centerpiece of the transformation.

1.  **Homepage Redirect/Design**
    *   **Action:** Redesign `layouts/index.html`.
    *   **Action:** Implement a visual "Split" or "Gate":
        *   **Left:** "Early Music" (Links to existing Main flow).
        *   **Right:** "Sound Design" (Links to the new section from Phase 2).
    *   **Action:** Ensure this works on Mobile (stacked view) vs Desktop (split view).

## Phase 5: Engagement & Polish (Day 5)
*Audit Step: 2*

**Objective:** Keep them listening and finalizing the user journey.

1.  **Global Audio Player**
    *   **Action:** Investigate and implement a persistent (or footer-based) Audio Player. *Note: Truly persistent playback on navigation requires specific technical handling (SPA/Pjax) or a specialized widget.*
2.  **Contact/CTA Optimization**
    *   **Action:** Add "Book Now" or "Inquiry" CTAs to the Header or prominent locations.
    *   **Action:** Final Walkthrough and device testing.

---
**Ready to begin? Phase 1 starts now.**
