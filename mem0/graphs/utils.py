# utils.py  (mem0/graphs/utils.py)

UPDATE_GRAPH_PROMPT = """
You are an AI expert specializing in graph memory management and optimization. Your task is to analyze existing graph memories alongside new information, and update the relationships in the memory list to ensure the most accurate, current, and coherent representation of knowledge.

Input:
1. Existing Graph Memories: A list of current graph memories, each containing source, target, and relationship information.
2. New Graph Memory: Fresh information to be integrated into the existing graph structure.

Guidelines:
1. Identification: Use the source and target as primary identifiers when matching existing memories with new information.
2. Conflict Resolution:
   - If new information contradicts an existing memory:
     a) When source and target match but content differs, update the relationship of the existing memory.
     b) If the new memory is more recent or accurate, update the existing memory accordingly.
3. Comprehensive Review: Examine each existing graph memory against the new information; multiple updates may be required.
4. Consistency & Style: Keep a uniform, concise, and clear style across all memories.
5. Semantic Coherence: Updates must improve or preserve the overall semantic structure of the graph.
6. Temporal Awareness: Prefer the most recent information if timestamps are available.
7. Relationship Refinement: Prefer precise, general, timeless relationships.
8. Redundancy Elimination: Merge redundant or highly similar relationships.
9. Relationship Equivalence: Consolidate semantically identical relationships into a single normalized type.
   For example:
      plans_to_visit, plans_to_travel, will_travel_in  ->  PLANS_TO_TRAVEL
10. Use ALL_CAPS with underscores for relationship names (e.g., LIVES_IN, STUDIES_AT).

Memory Format:
source -- RELATIONSHIP -- destination

Task Details:
======= Existing Graph Memories:=======
{existing_memories}

======= New Graph Memory:=======
{new_memories}

Output:
Provide a list of update instructions, each specifying the source, target, and the new (normalized) relationship to be set. Only include memories that require updates.
"""

EXTRACT_RELATIONS_PROMPT = """
You are an advanced algorithm designed to extract structured information from text to construct knowledge graphs. Your goal is to capture comprehensive and accurate information from SPANISH user input, then NORMALIZE to ENGLISH before returning the entities and relationships.

Follow these key principles:

GENERAL RULES
1) Normalize ALL entity and relationship names to ENGLISH before returning them.
2) Use ALL_CAPS with underscores for relationships (e.g., LIVES_IN, STUDIES_AT, LIKES, PLANS_TO_TRAVEL, HAS_NAME, HAS_AGE, RELATED_TO).
3) Extract ONLY information explicitly stated in the text (no hallucinations).
4) Establish relationships ONLY among entities explicitly mentioned in the message.
5) For any self-reference (I, me, my, etc.), use the user node name: "USER_ID" (the literal user node identifier).
6) Avoid self-loops (e.g., paciente -- HAS_NAME --> paciente).
7) Avoid duplicates and near-duplicates; consolidate semantically equivalent relationships:
      plans_to_visit / plans_to_travel / will_travel_in -> PLANS_TO_TRAVEL
8) Prefer general, timeless relationship types (e.g., professor instead of became_professor) when applicable.
9) OUTPUT MUST be normalized:
   - lowercase entity names
   - remove accents/diacritics (áéíóúü -> aeio uu), replace ñ with n
   - spaces -> underscores
   - keep only ASCII letters, numbers, and underscores in entity names
   - relationships: strictly ALL_CAPS with underscores

ENTITY CONSISTENCY
- Keep entity naming consistent across extractions (use the same normalized form).
- Do NOT invent new variants if a normalized concept exists (e.g., matematicas -> mathematics; ingenieria_informatica -> computer_science).
- Ages should normalize as 21_years, 22_years, etc. (use _years suffix).
- Dates/months should normalize like may_2023, april_2026, etc.

STRUCTURE
- Return ONLY relationships among existing or explicitly mentioned entities in the user message.
- Do NOT create any relationship without both source and destination entities.
- Do NOT include any properties (timestamps or others) in the extraction; just (source, relationship, destination).

CUSTOM_PROMPT
"""

DELETE_RELATIONS_SYSTEM_PROMPT = """
You are a graph memory manager specializing in identifying, managing, and optimizing relationships within graph-based memories. Your primary task is to analyze a list of existing relationships and determine which ones should be deleted based on the new information provided.

Input:
1. Existing Graph Memories: A list of current graph memories, each containing source, relationship, and destination information.
2. New Text: The new information to be integrated into the existing graph structure.
3. Use "USER_ID" as node for any self-references (e.g., "I," "me," "my," etc.) in user messages.

Guidelines:
1. Identification: Use the new information to evaluate existing relationships in the memory graph.
2. Deletion Criteria: Delete a relationship only if it meets at least one of these conditions:
   - Outdated or Inaccurate: The new information is more recent or accurate.
   - Contradictory: The new information conflicts with or negates the existing information.
3. DO NOT DELETE if there is a possibility of the same relationship type but with different destination nodes.
4. Comprehensive Analysis:
   - Thoroughly examine each existing relationship against the new information and delete as necessary.
   - Multiple deletions may be required based on the new information.
5. Semantic Integrity:
   - Ensure that deletions maintain or improve the overall semantic structure of the graph.
   - Avoid deleting relationships that are NOT contradictory/outdated.
6. Temporal Awareness: Prefer recency when timestamps are available.
7. Necessity Principle: Delete ONLY when necessary to maintain an accurate and coherent memory graph.

Example where NOT to delete:
Existing: alice -- LOVES_TO_EAT -- pizza
New:     alice also loves to eat burger
Do NOT delete the first relationship; both can coexist.

Memory Format:
source -- relationship -- destination

Provide a list of deletion instructions, each specifying the relationship to be deleted.
"""


def get_delete_messages(existing_memories_string: str, data: str, user_id: str):
    """
    Returns (system_prompt, user_prompt) for the deletion pass.
    The placeholder USER_ID is replaced with the plain user node name (e.g., 'paciente').
    """
    return (
        DELETE_RELATIONS_SYSTEM_PROMPT.replace("USER_ID", user_id),
        f"Here are the existing memories:\n{existing_memories_string}\n\nNew Information:\n{data}",
    )
