# Graph Report - contact_carddav  (2026-06-23)

## Corpus Check
- 4 files · ~666 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 23 nodes · 33 edges · 7 communities (3 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]

## God Nodes (most connected - your core abstractions)
1. `DavCollection` - 16 edges
2. `Extract the vobject Component from a radicale Item or vobject.` - 1 edges
3. `Build a name-indexed dict of vobject children.` - 1 edges
4. `Get all children including duplicates.` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- 1-file cycle: `__init__.py -> __init__.py`
- 1-file cycle: `models/__init__.py -> models/__init__.py`

## Communities (7 total, 4 thin omitted)

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DavCollection` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.550) - this node is a cross-community bridge._
- **What connects `Extract the vobject Component from a radicale Item or vobject.`, `Build a name-indexed dict of vobject children.`, `Get all children including duplicates.` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._