# AI Service – AI vs Non-AI Questions

## Purpose

Identify which virtual assistant requests need AI and which can be handled using deterministic logic, database queries, or predefined rules.

## A. Questions That Need AI

| No. | User Question | Reason |
|---|---|---|
| 1 | Can you summarize these lecture notes? | Requires understanding and summarizing natural language. |
| 2 | Can you explain recursion in a simpler way? | Requires generating a contextual explanation. |
| 3 | What does the user mean by "I'm overwhelmed with work"? | Requires interpreting informal language and context. |
| 4 | Can you turn these messy notes into a study plan? | Requires understanding unstructured information. |
| 5 | Can you rewrite this email more professionally? | Requires natural language generation and tone adaptation. |
| 6 | What are the main differences between these two articles? | Requires semantic comparison of documents. |
| 7 | Can you explain why my Python code might be incorrect? | Requires interpreting code and reasoning about possible errors. |
| 8 | Can you suggest improvements to my project proposal? | Requires evaluating open-ended content and generating suggestions. |
| 9 | Can you extract action items from this meeting transcript? | Requires interpreting conversational context. |
| 10 | Can you answer a question using the meaning of this uploaded document? | Requires semantic understanding and contextual question answering. |

## B. Questions That Do Not Need AI

| No. | User Question | Reason |
|---|---|---|
| 1 | What is the current date? | A system clock provides the date. |
| 2 | What is 25 + 37? | A deterministic arithmetic operation is sufficient. |
| 3 | Show my saved tasks. | A database query can return stored tasks. |
| 4 | How many tasks remain incomplete? | Counting records with a completed-status filter is sufficient. |
| 5 | Mark task #5 as completed. | A standard database update handles the request. |
| 6 | Show my schedule for Monday. | Calendar records can be filtered by date. |
| 7 | Set a reminder for 7:00 PM. | A scheduler can register a reminder using structured input. |
| 8 | Sort my assignments by deadline. | A standard sorting algorithm is sufficient. |
| 9 | What is the total duration of my classes today? | Time intervals can be summed programmatically. |
| 10 | Is my password at least 12 characters long? | A simple length check is sufficient. |

## Decision Rule

Use AI when a request requires semantic interpretation, open-ended reasoning, or natural language generation.

Use deterministic services for structured input, arithmetic, scheduling, filtering, and basic data operations.

**Important:** Natural-language input may require AI for interpretation even when the underlying action does not need AI. For example, setting a reminder is deterministic once its time and content are extracted.

## Conclusion

A virtual assistant should not use an LLM for every request. Separating AI tasks from conventional software operations improves predictability, efficiency, privacy, and maintainability.