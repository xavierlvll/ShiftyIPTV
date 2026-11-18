# SHiFTyIPTV Project TODO

## Phase 1: Exploration & Research
- [x] Inspect the repository (Done)
- [ ] Research HLS and IPTV streaming architecture
- [ ] Investigate Pluto TV's HSL behavior (Ads, transitions, etc.)

## Phase 2: Design & Architecture
- [ ] Define application architecture (Backend, Streaming Engine, Dashboard, Database)
- [ ] Design Database schema (Providers, Channels, EPG, Settings, Logs)
- [ ] Design API specification (REST/WebSockets)
- [ ] Design Streaming Engine logic (HLS management, Segment monitoring, Recovery)
- [ ] Design Dashboard UI/UX (Dark theme, Dashboard, Providers, Channels, Monitoring, EPG, Settings)

## Phase 3: Backend Implementation
- [ ] Setup project structure and base environment
- [ ] Implement Database layer
- [ ] Implement Provider management (M3U import, testing, etc.)
- [ ] Implement Channel management (Metadata, groups, etc.)
- [ ] Implement EPG management (XMLTV import, matching, etc.)
- [ ] Implement API endpoints

## Phase 4: HLS Streaming Engine (Core)
- [ ] Implement HLS playlist parsing (Master, Media, Live)
- [ ] Implement Segment monitoring and management
- [ ] Implement Stream recovery logic (Retry, backoch, reconnection)
- [ ] Implement Stream handoff mechanism (Handling playlist/segment changes)
- [ ] Implement Stream delivery (HTTP/HLS/MPEG-TS passthrough)
- [ ] Implement optional FFmpeg remuxing/transcoding capability

## Phase 5: Web Dashboard Implementation
- [ ] Setup Web Dashboard (React/Vue/Svelte/etc.)
- [ ] Implement Dashboard Overview (Stats)
- [ ] Implement Provider Management UI
- [ ] Implement Channel Management UI
- [ ] Implement Stream Monitoring UI (Active connections, logs, etc.)
- [ ] Implement EPG Management UI
- [ ] Implement Settings UI

## Phase 6: Monitoring, Logging, & Testing
- [ ] Implement detailed logging system (Per-stream diagnostic history)
- [ ] Implement monitoring and alerting
- [ ] Implement automated test suite (M3U, EPG, HLS parsing, Recovery, API, etc.)
- [ ] Implement Mock HLS providers for testing

## Phase 7: Deployment & Finalization
- [ ] Implement Dockerfile and Docker Compose
- [ ] Implement Authentication and Security
- [ ] Complete Documentation (README, Technical Docs)
- [ ] Final Testing and Debugging
- [ ] Prepare GitHub Release
