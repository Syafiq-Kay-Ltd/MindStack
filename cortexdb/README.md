# CortexDB

## Background

- CortexDB is a note taking app that is inspired from the Zettelkasten method
- addresses two main problems with the notetaking process in general:
  - information overload
  - stagnant thinking
  - unconscious bias? stale knowledge?

## Implementation Strategy

- four types of notes:
  1. fleeting notes
  2. literature notes
  3. permanent notes
  4. structure notes

## Note Taking Guidelines

- own words
- sufficient context
- citation
- concise yet complete ie standalone

## Physical Implementation

- core components
  - cards
  - writing instrument
  - box to store the cards
  - dividers or tabs for navigation and accessibility

- note creation
  - atomicity
  - unique identifier
  - header - short descriptive title and unique id
  - content - explanation, reference, paraphrase, direct quotation
  - links

- organisation and navigation
  - non-hierarchical
  - relationships defined by links and unique id
  - index or register - as entry points ie main topics or structure notes
  - manual connection

- note processing
  - regular review

- workflow
  - capture fleeting thoughts
  - process card periodically
  - with each new note, consider and record connections to one or more related notes
  - regularly review and update notes as your understanding evolves

## CortexDB Implementation

### Objects

- cards
- tables to store cards
- links
- tags

### SQL Implementation

#### Core Table

1. Notes: note_id, title, content, created_at, updated_at
2. Links: link_id, from_note_id, to_note_id, link_type, description
3. Tags: tag_id, name
4. Note-Tags: note_id, tag_id

## Project Plan

### Epic

1. User Workflow
2. Maintenance Routine

#### User Workflow

1. Capture and create notes
2. Edit and connect
3. Search and retrieve
4. Update, merge or split notes
5. Export and use notes

#### Capture and Create Notes

- this is the current task I will be focusing on

- [ ] write tests

### Maintenance Routine

1. Routine backups
2. Index optimisation
3. Cleaning and pruning
4. Documentation updates
5. Schema maintenance
6. Regular health checks
7. Security
