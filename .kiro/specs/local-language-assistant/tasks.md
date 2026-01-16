# Implementation Plan: Local Language Assistant

## Overview

This implementation plan follows an MVP-focused approach, building the assistant incrementally from basic infrastructure through full multi-language support. Each phase builds on the previous, ensuring working functionality at each checkpoint.

## Tasks

- [ ] 1. Project Setup and Basic Infrastructure
  - [-] 1.1 Initialize Python project with FastAPI backend
    - Create project structure with `src/`, `tests/`, `data/` directories
    - Set up `pyproject.toml` with dependencies (FastAPI, uvicorn, pydantic, hypothesis)
    - Create basic configuration module
    - _Requirements: 5.1, 5.2_
  
  - [ ] 1.2 Create core data models and interfaces
    - Implement `ProcessedQuery`, `QueryStatus` dataclasses
    - Implement `Scheme`, `SchemeMatch` dataclasses
    - Implement `AssistantResponse`, `ActionStep` dataclasses
    - Implement `SessionContext`, `SessionRecord` dataclasses
    - _Requirements: 3.3, 6.1_
  
  - [ ] 1.3 Set up basic API endpoint structure
    - Create `/query` POST endpoint accepting `QueryPayload`
    - Implement request validation with Pydantic
    - Return placeholder `ResponsePayload`
    - _Requirements: 1.1_
  
  - [ ] 1.4 Create minimal text-based frontend
    - Create simple HTML/JS chat interface
    - Implement query submission to backend API
    - Display responses in chat format
    - _Requirements: 1.1_

- [ ] 2. Checkpoint - Verify frontend-backend communication
  - Ensure API accepts queries and returns responses
  - Verify chat UI displays responses correctly
  - Ask the user if questions arise

- [ ] 3. Dataset Preparation and Scheme Storage
  - [ ] 3.1 Create scheme data structure and storage
    - Define JSON schema for scheme records
    - Create `SchemeDatabase` class for loading and querying schemes
    - Implement `get_by_id()` and `get_all()` methods
    - _Requirements: 3.1, 3.5_
  
  - [ ] 3.2 Populate initial scheme dataset
    - Create `data/schemes.json` with 10-15 real government schemes
    - Include schemes from education, healthcare, financial aid categories
    - Add localized content for Hindi (primary) and English
    - _Requirements: 3.1, 3.3_
  
  - [ ] 3.3 Write property test for scheme data integrity
    - **Property 7: Scheme Response Completeness**
    - Verify all schemes have required fields (name, description, eligibility)
    - **Validates: Requirements 3.3**

- [ ] 4. Query Processing and Validation
  - [ ] 4.1 Implement QueryProcessor class
    - Implement `process()` method for query normalization
    - Implement `is_valid()` method for whitespace detection
    - Handle truncation for queries > 500 characters
    - _Requirements: 1.1, 1.4, 1.5_
  
  - [ ] 4.2 Write property tests for query validation
    - **Property 1: Query Validation Rejects Invalid Input**
    - **Property 2: Query Truncation Preserves Prefix**
    - **Validates: Requirements 1.4, 1.5**
  
  - [ ] 4.3 Implement basic intent detection
    - Create `IntentExtractor` with keyword-based detection
    - Map keywords to `IntentType` enum values
    - Extract basic entities (category, demographic)
    - _Requirements: 1.2, 3.1_

- [ ] 5. Scheme Matching and Retrieval
  - [ ] 5.1 Implement SchemeRetriever class
    - Implement `search()` method with keyword matching
    - Implement relevance scoring based on keyword overlap
    - Limit results to top 3 matches
    - _Requirements: 3.1, 3.2, 3.6_
  
  - [ ] 5.2 Write property test for search results
    - **Property 6: Search Results Bounded and Ranked**
    - Verify results ≤ 3 and ordered by relevance
    - **Validates: Requirements 3.2, 3.6**
  
  - [ ] 5.3 Implement empty results handling
    - Return related categories when no matches found
    - Generate clarifying questions for ambiguous queries
    - _Requirements: 3.4_
  
  - [ ] 5.4 Write property test for empty results
    - **Property 8: Empty Results Provide Alternatives**
    - **Validates: Requirements 3.4**

- [ ] 6. Checkpoint - Verify scheme retrieval works
  - Test queries return relevant schemes
  - Verify ranking and result limiting
  - Ask the user if questions arise

- [ ] 7. Response Generation
  - [ ] 7.1 Implement ResponseGenerator class
    - Implement `generate()` method for creating responses
    - Implement `simplify_text()` for plain language output
    - Implement `format_action_steps()` for numbered steps
    - _Requirements: 4.1, 4.2, 4.5_
  
  - [ ] 7.2 Write property test for action step formatting
    - **Property 9: Action Steps Formatting Invariants**
    - Verify steps numbered 1-5, locations specified, documents listed
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4**
  
  - [ ] 7.3 Implement response size constraints
    - Enforce 200 word limit
    - Enforce 10KB byte limit
    - Implement pagination for long processes (has_more flag)
    - _Requirements: 4.5, 4.6, 5.1_
  
  - [ ] 7.4 Write property test for response size
    - **Property 11: Response Size Constraints**
    - Verify word count ≤ 200, bytes < 10KB, text-only
    - **Validates: Requirements 4.5, 5.1, 5.4**
  
  - [ ] 7.5 Write property test for pagination
    - **Property 10: Long Process Pagination**
    - Verify has_more=true when steps > 5
    - **Validates: Requirements 4.6**

- [ ] 8. Session Context Management
  - [ ] 8.1 Implement SessionManager class
    - Implement `get_or_create()` for session handling
    - Implement `update()` for storing conversation context
    - Implement `is_expired()` for 30-minute timeout check
    - _Requirements: 6.1, 6.3_
  
  - [ ] 8.2 Implement reference resolution
    - Implement `resolve_reference()` for pronoun handling
    - Track mentioned scheme IDs in session
    - Resolve "it", "this scheme" to last mentioned scheme
    - _Requirements: 6.2_
  
  - [ ] 8.3 Write property tests for session management
    - **Property 12: Session Context Preservation**
    - **Property 13: Session Expiration**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
  
  - [ ] 8.4 Write property test for session privacy
    - **Property 14: Session Privacy**
    - Verify no PII stored in session records
    - **Validates: Requirements 6.5**

- [ ] 9. Checkpoint - Verify session context works
  - Test multi-turn conversations maintain context
  - Verify reference resolution works
  - Test session expiration
  - Ask the user if questions arise

- [ ] 10. Multi-Language Support
  - [ ] 10.1 Implement LanguageDetector class
    - Implement `detect()` method using character/word patterns
    - Support Hindi, Tamil, Telugu, Bengali, Marathi detection
    - Return confidence score with detection result
    - _Requirements: 2.1, 2.2_
  
  - [ ] 10.2 Write property test for language detection
    - **Property 3: Language Detection Consistency**
    - Verify detected language matches response language
    - **Validates: Requirements 2.2, 2.3**
  
  - [ ] 10.3 Implement language switching
    - Detect language change requests in queries
    - Update session language preference
    - Persist language choice across session
    - _Requirements: 2.4_
  
  - [ ] 10.4 Write property test for language switching
    - **Property 4: Language Switch Persistence**
    - **Validates: Requirements 2.4**
  
  - [ ] 10.5 Implement low-confidence fallback
    - Default to Hindi when confidence < 0.7
    - Prompt user to confirm language preference
    - _Requirements: 2.5_
  
  - [ ] 10.6 Write property test for language fallback
    - **Property 5: Low Confidence Language Fallback**
    - **Validates: Requirements 2.5, 7.2**
  
  - [ ] 10.7 Add localized scheme content
    - Extend scheme dataset with Tamil, Telugu, Bengali, Marathi translations
    - Add localized action step templates
    - _Requirements: 2.1, 2.3_

- [ ] 11. Error Handling
  - [ ] 11.1 Implement error response generation
    - Create localized error messages for all supported languages
    - Implement `handle_error()` in APIHandler
    - Ensure no technical details exposed to users
    - _Requirements: 7.1, 7.3_
  
  - [ ] 11.2 Write property test for error messages
    - **Property 15: Error Message Localization**
    - Verify errors in user's language, no technical terms
    - **Validates: Requirements 7.3, 7.5**
  
  - [ ] 11.3 Implement escalation to helpline
    - Track consecutive UNKNOWN intents in session
    - Provide helpline number after 2 failed clarifications
    - _Requirements: 7.4_
  
  - [ ] 11.4 Write property test for escalation
    - **Property 16: Escalation After Failed Clarifications**
    - **Validates: Requirements 7.4**
  
  - [ ] 11.5 Implement graceful degradation
    - Handle database unavailability with cached data
    - Handle language service failure with Hindi default
    - _Requirements: 7.1, 7.2_

- [ ] 12. Low-Bandwidth Optimization
  - [ ] 12.1 Implement response payload optimization
    - Use short field names in JSON responses (q, s, m, a, n, e)
    - Remove null/empty fields from responses
    - Compress response where beneficial
    - _Requirements: 5.1, 5.4_
  
  - [ ] 12.2 Implement client-side caching
    - Cache scheme categories and common responses
    - Implement offline fallback with cached data
    - _Requirements: 5.3_
  
  - [ ] 12.3 Implement request retry logic
    - Auto-retry failed requests up to 2 times
    - Show "Retrying..." message to user
    - _Requirements: 5.6_

- [ ] 13. Integration and Wiring
  - [ ] 13.1 Wire all components in APIHandler
    - Connect QueryProcessor → LanguageDetector → IntentExtractor
    - Connect IntentExtractor → SchemeRetriever → ResponseGenerator
    - Integrate SessionManager throughout flow
    - _Requirements: 1.1, 3.1, 4.1_
  
  - [ ] 13.2 Implement complete query flow
    - Process query → detect language → extract intent → search schemes → generate response
    - Handle all error cases in flow
    - Return properly formatted APIResponse
    - _Requirements: 1.1, 1.3_
  
  - [ ] 13.3 Write integration tests
    - Test end-to-end query flow
    - Test multi-turn conversations
    - Test language switching mid-conversation
    - Test error recovery scenarios
    - _Requirements: 1.1, 6.1, 2.4, 7.1_

- [ ] 14. Final Checkpoint - Complete system verification
  - Run all property tests (minimum 100 iterations each)
  - Run all unit and integration tests
  - Verify response times acceptable
  - Test with sample queries in multiple languages
  - Ask the user if questions arise

## Notes

- All tasks are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests use Hypothesis library with minimum 100 iterations
- Unit tests complement property tests for edge cases and specific examples
