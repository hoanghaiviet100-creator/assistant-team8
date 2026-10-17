# UI Specification: Citation & Source Presentation

## 1. Overview & Purpose

This document specifies the visual presentation, interactive behavior, and data structure for displaying **citations and source references** under assistant answers in the Smart Virtual Assistant.

- **Component:** `ui`
- **Issue:** UI: show sources under each answer (#7)
- **Status:** Approved Design Specification
- **Target Frameworks:** Streamlit (initial phase) & React/Next.js (future production phase)

### Core Objectives
1. **Trust & Verifiability:** Provide transparent grounding for all answers so students and staff can immediately verify accuracy.
2. **Clean Information Hierarchy:** Keep the answer as the primary focus, with citation metadata neatly organized beneath.
3. **Multi-Source Support:** Gracefully handle structured tabular records (e.g., campus office directory) and unstructured documents (e.g., PDF handbooks, policy manuals).
4. **Progressive Disclosure:** Use compact badge/pill representations that can expand into full context excerpts on demand.

---

## 2. Citation Data Schema

To support both the current rule-based system and the future AI/RAG service (defined in [`docs/ai-interface.md`](ai-interface.md)), the citation payload follows a standardized schema:

```typescript
interface Citation {
  id: string;                      // Unique citation identifier (e.g., "cite-001")
  source_type: "csv" | "document"; // Type of grounding source
  title: string;                   // Display title or filename (e.g., "offices.csv", "student_handbook_2024.pdf")
  location: string;                // Location reference (e.g., "Row: Training Office", "Page 18, Section 4.3")
  excerpt: string;                 // Grounding text snippet or structured field values
  confidence?: number;             // Retrieval relevance score (0.0 - 1.0, optional)
  url?: string;                    // Link to file or external source (optional)
}
```

---

## 3. Visual Layout & Component Anatomy

Each assistant message bubble is divided into three distinct vertical zones:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [🤖 Assistant]                                           10:42 AM      │  <- Header
├────────────────────────────────────────────────────────────────────────┤
│ Training Office is located at room I.101 and is open                   │
│ Monday to Friday from 07:30 to 16:30.                                  │  <- Answer Body
├────────────────────────────────────────────────────────────────────────┤
│ 📎 Sources (1)                                                         │  <- Citation Zone
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ 📊 offices.csv · Row: Training Office                              │ │
│ │ "name: Training Office | room: I.101 | hours: Mon-Fri 07:30-16:30" │ │
│ └────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Component Details
- **Source Count Badge:** Indicates the number of sources used to generate the answer (e.g., `📎 Sources (1)`).
- **Source Pill / Card Header:** Shows source icon (`📊` for dataset/CSV, `📄` for PDF/document), filename, and specific section/page location.
- **Source Body (Excerpt):** Shows the exact quote or structured record attributes used.
- **Interactive Trigger:** Collapsible/expandable container (`st.expander` in Streamlit, accordion/popover in React) to keep chat clean when multiple sources exist.

---

## 4. UI Mockups with Examples

### Example 1: Structured CSV Source (`data/offices.csv`)

This example demonstrates how citations appear for campus office inquiries grounded in the local dataset [`data/offices.csv`](../data/offices.csv).

#### Scenario
- **User Question:** *"Where is the Training Office and what are its opening hours?"*
- **Backend Response:** Generated via rule lookup in `data/offices.csv`.

#### ASCII UI Mockup (Desktop / Streamlit Layout)

```text
+----------------------------------------------------------------------------------------------------+
| 🎓 HCMUS Smart Virtual Assistant                                                                   |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [👤 User]                                                                               10:30 AM  |
|  Where is the Training Office and what are its opening hours?                                      |
|                                                                                                    |
|  ------------------------------------------------------------------------------------------------  |
|                                                                                                    |
|  [🤖 Assistant]                                                                          10:30 AM  |
|  The Training Office is in room I.101. It is open Monday through Friday, 07:30 - 16:30.            |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  | v 📎 Sources (1)                                                              [CSV Dataset]  |  |
|  +----------------------------------------------------------------------------------------------+  |
|  | +------------------------------------------------------------------------------------------+ |  |
|  | | 📊 data/offices.csv  •  Record #2                                                        | |  |
|  | |                                                                                          | |  |
|  | | Matched Entry: Training Office                                                           | |  |
|  | | • Room  : I.101                                                                          | |  |
|  | | • Hours : Mon-Fri 07:30-16:30                                                            | |  |
|  | |                                                                                          | |  |
|  | | [📂 View Source File: data/offices.csv]                                                  | |  |
|  | +------------------------------------------------------------------------------------------+ |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
| [ Ask anything about campus offices, procedures, or regulations...                       ] [ Send ] |
+----------------------------------------------------------------------------------------------------+
```

#### Underlying JSON Payload
```json
{
  "answer": "The Training Office is in room I.101. It is open Monday through Friday, 07:30 - 16:30.",
  "citations": [
    {
      "id": "cite-csv-001",
      "source_type": "csv",
      "title": "data/offices.csv",
      "location": "Row: Training Office",
      "excerpt": "name: Training Office, room: I.101, hours: Mon-Fri 07:30-16:30",
      "url": "file:///data/offices.csv"
    }
  ]
}
```

---

### Example 2: Unstructured Document / PDF Source (`student_handbook_2024.pdf`)

This example illustrates the presentation of citations from academic documents, handbooks, and PDFs processed by the future RAG / Document AI pipeline (as prototyped in `smartassistantprototype_version0.1`).

#### Scenario
- **User Question:** *"What is the deadline for dropping a course without academic penalty?"*
- **Backend Response:** Synthesized by LLM retrieval over campus policy documentation.

#### ASCII UI Mockup (Desktop / Streamlit Layout)

```text
+----------------------------------------------------------------------------------------------------+
| 🎓 HCMUS Smart Virtual Assistant                                                                   |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [👤 User]                                                                               10:35 AM  |
|  What is the deadline for dropping a course without academic penalty?                             |
|                                                                                                    |
|  ------------------------------------------------------------------------------------------------  |
|                                                                                                    |
|  [🤖 Assistant]                                                                          10:35 AM  |
|  You can drop a course without academic penalty up until 17:00 on Friday of Week 3 of the         |
|  semester. Courses dropped before this deadline will not appear on your official transcript.       |
|  Drops requested between Week 4 and Week 8 will receive a 'W' (Withdrawal) notation.              |
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  | v 📎 Sources (2)                                                              [Verified RAG] |  |
|  +----------------------------------------------------------------------------------------------+  |
|  | [1] 📄 student_handbook_2024.pdf  •  Page 18, Section 4.3                                   |  |
|  | +------------------------------------------------------------------------------------------+ |  |
|  | | "...Students may drop enrolled courses without academic penalty or notation on           | |  |
|  | | official academic transcripts until 17:00 on Friday of Week 3 of each standard          | |  |
|  | | semester. Requests must be submitted via the Student Portal..."                          | |  |
|  | +------------------------------------------------------------------------------------------+ |  |
|  |                                                                                              |  |
|  | [2] 📄 academic_regulations_v2.pdf  •  Page 7, Article 12                                  |  |
|  | +------------------------------------------------------------------------------------------+ |  |
|  | | "...Late course drops after Week 3 and before Week 8 require academic advisor approval     | |  |
|  | | and will be recorded as 'W' (Withdrawn) on transcript records..."                       | |  |
|  | +------------------------------------------------------------------------------------------+ |  |
|  |                                                                                              |  |
|  | [📥 Open student_handbook_2024.pdf (p. 18)]   [📥 Open academic_regulations_v2.pdf (p. 7)]   |  |
|  +----------------------------------------------------------------------------------------------+  |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
| [ Ask anything about campus offices, procedures, or regulations...                       ] [ Send ] |
+----------------------------------------------------------------------------------------------------+
```

#### Underlying JSON Payload
```json
{
  "answer": "You can drop a course without academic penalty up until 17:00 on Friday of Week 3 of the semester. Courses dropped before this deadline will not appear on your official transcript. Drops requested between Week 4 and Week 8 will receive a 'W' (Withdrawal) notation.",
  "citations": [
    {
      "id": "cite-pdf-001",
      "source_type": "document",
      "title": "student_handbook_2024.pdf",
      "location": "Page 18, Section 4.3",
      "excerpt": "Students may drop enrolled courses without academic penalty or notation on official academic transcripts until 17:00 on Friday of Week 3 of each standard semester. Requests must be submitted via the Student Portal...",
      "confidence": 0.94,
      "url": "docs/student_handbook_2024.pdf#page=18"
    },
    {
      "id": "cite-pdf-002",
      "source_type": "document",
      "title": "academic_regulations_v2.pdf",
      "location": "Page 7, Article 12",
      "excerpt": "Late course drops after Week 3 and before Week 8 require academic advisor approval and will be recorded as 'W' (Withdrawn) on transcript records...",
      "confidence": 0.88,
      "url": "docs/academic_regulations_v2.pdf#page=7"
    }
  ]
}
```

---

## 5. Interaction States & Edge Cases

| State | User Experience / Display Behavior |
|---|---|
| **Default / Collapsed** | Summary badge shown (e.g. `📎 Sources (2)`). Clicking toggles accordion expansion. |
| **Expanded** | Detailed source cards showing filename, page/location, and quoted excerpt block. |
| **No Citations Needed** | For greetings (`"hi"`, `"xin chào"`) or help text (`"help"`), the citation zone is omitted completely. |
| **No Match Found** | When the assistant cannot answer (`"I don't know that yet..."`), no citation is shown, prompting user to refine query. |
| **Source Truncation** | Quotes longer than 200 characters display with `... [Show more]` to prevent vertical clutter. |
| **Click to View Source** | Clicking the source filename opens or scrolls to the corresponding document viewer or row viewer. |

---

## 6. Implementation Guidance

### Streamlit Integration (Phase 2 & 3)

In the planned Streamlit application (`ui/app.py`), citations are rendered using native `st.expander` and markdown components:

```python
import streamlit as st

def render_message_with_citations(role: str, text: str, citations: list[dict] | None = None):
    with st.chat_message(role):
        st.markdown(text)
        if citations:
            count = len(citations)
            with st.expander(f"📎 Sources ({count})", expanded=False):
                for idx, src in enumerate(citations, 1):
                    icon = "📊" if src.get("source_type") == "csv" else "📄"
                    st.markdown(f"**[{idx}] {icon} `{src['title']}` • {src['location']}**")
                    st.info(f"“{src['excerpt']}”")
                    if "url" in src:
                        st.caption(f"[Open source reference]({src['url']})")
```

### Next.js / React Integration (Future Production Phase)

In the production React interface (referencing `smartassistantprototype_version0.1/components/sources/CitationCard.tsx`):

```tsx
export function CitationCard({ citation }: { citation: Citation }) {
  return (
    <div className="citation-card rounded-lg border p-3 bg-muted/40 text-sm">
      <div className="flex items-center gap-2 font-medium text-primary">
        <FileText size={16} />
        <span>{citation.title}</span>
        <span className="text-muted-foreground text-xs">• {citation.location}</span>
      </div>
      <blockquote className="mt-2 border-l-2 pl-2 italic text-muted-foreground">
        "{citation.excerpt}"
      </blockquote>
    </div>
  );
}
```

---

## 7. Acceptance Checklist & Verification

| Requirement | Specification in this Document | Status |
|---|---|:---:|
| Design how citations appear under each answer | Defined in Section 3 & 4 with visual hierarchy | ✅ Pass |
| Mockup in `docs/ui-sources.md` | Provided in Section 4 with comprehensive ASCII diagrams | ✅ Pass |
| Exactly 2 detailed examples | Example 1 (CSV dataset) & Example 2 (PDF document) | ✅ Pass |
| Integration with current backend | Section 4 (Example 1) links with `data/offices.csv` | ✅ Pass |
| Integration with future AI service | Section 4 (Example 2) links with `docs/ai-interface.md` | ✅ Pass |
| Streamlit & Next.js implementation plan | Section 6 provides code templates for both frameworks | ✅ Pass |
