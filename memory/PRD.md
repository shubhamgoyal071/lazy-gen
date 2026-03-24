# LazyGen Landing Page PRD

## Original Problem Statement
Build a minimal, ultra-cool black & white landing page for "LazyGen" - an AI job application autopilot startup with a sleepy panda brand mascot.

## User Personas
- **Primary**: GenZ job seekers tired of repetitive job applications
- **Secondary**: Young professionals looking to optimize their job hunt

## Core Requirements
- Strict black & white theme (no bright colors)
- Panda logo as main character with animations
- GenZ-friendly tone (chill, confident, slightly sarcastic)
- Waitlist form to capture leads (name + email)
- Apple-like minimalism + GenZ attitude

## What's Been Implemented (December 2025)
- [x] Hero section with animated panda logo + headline
- [x] Panda breathing/bobbing animation using Framer Motion
- [x] Panda story section with rotating animation
- [x] How it works - 3 step cards with icons
- [x] Pain points - 4 relatable cards with hover effects
- [x] Value section - 4 checkmark items
- [x] Waitlist form with MongoDB storage
- [x] Duplicate email validation
- [x] Toast notifications (sonner)
- [x] Minimal footer (no social links)
- [x] Noise texture overlay
- [x] Smooth scroll to waitlist CTA
- [x] Custom typography (Outfit + JetBrains Mono)

## Tech Stack
- Frontend: React + Framer Motion + Tailwind CSS
- Backend: FastAPI + MongoDB
- UI: Custom B&W design system

## API Endpoints
- `POST /api/waitlist` - Submit name + email
- `GET /api/waitlist/count` - Get total signups

## P0/P1/P2 Features Remaining

### P0 (MVP - DONE)
All core features implemented

### P1 (Next Phase)
- Email confirmation/welcome email integration
- Admin dashboard to view waitlist signups
- Analytics tracking

### P2 (Future)
- Referral system for early access priority
- Landing page A/B testing
- Mobile app waitlist

## Next Tasks
1. Add email integration (SendGrid/Resend) for welcome emails
2. Build admin panel to manage waitlist
3. Add analytics (Mixpanel/Amplitude)
