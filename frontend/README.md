# Survey Application Platform – Frontend

This repository contains the **React frontend** for the **Survey Application Platform (WE-POC)**.  
It provides a bilingual (English / Telugu) public survey form and a secure admin dashboard with rich analytics charts — powered by the Django REST API backend.

---

## Objectives

- Present a fully **dynamic, multi-step survey** driven from the backend schema
- Support **English and Telugu** languages with a live language toggle
- Verify respondents by **mobile number** before allowing submission
- Provide admins with **aggregated analytics dashboards** (ECharts)
- Be **mobile-first, responsive**, and deployment-ready (Docker / Nginx)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | React 19, TypeScript 5.9 |
| Build tool | Vite 7 |
| Styling | Bootstrap 5.3, React Bootstrap 2, Bootstrap Icons |
| Charts | Apache ECharts 6 |
| Routing | React Router DOM 7 |
| Icons | React Icons 5 |
| State | React Context API (FormContext, LanguageContext) |
| Auth | JWT Bearer (stored in memory, refreshed via API) |

---

## Prerequisites

- **Node.js** ≥ 18.x  (LTS recommended — 20.x or 22.x)
- **npm** ≥ 9.x (ships with Node.js)

Verify your versions:

```bash
node --version   # e.g. v20.18.0
npm --version    # e.g. 10.8.2
```

---

## Project Structure

```text
frontend/
├── public/                  # Static public assets
├── src/
│   ├── assets/              # Images, icons
│   ├── components/
│   │   └── ProtectedRoute.tsx   # Auth guard for admin routes
│   ├── constants/
│   │   └── translations.ts      # en / te translation map
│   ├── context/
│   │   ├── FormContext.tsx       # Survey form state
│   │   └── LanguageContext.tsx   # Active language (en / te)
│   ├── Data/                    # Static JSON fallbacks
│   ├── hooks/
│   │   └── useProgressiveForm.ts  # Multi-step form state & logic
│   ├── services/                  # API service layer
│   │   ├── analyticsService.ts
│   │   ├── authService.ts
│   │   ├── formService.ts
│   │   └── locationService.ts
│   ├── shared/
│   │   ├── charts/              # ECharts wrapper components
│   │   │   ├── BarChart.tsx
│   │   │   ├── DonutChart.tsx
│   │   │   ├── HorizontalBarChart.tsx
│   │   │   ├── LineChart.tsx
│   │   │   ├── PieChart.tsx
│   │   │   └── ...
│   │   └── components/          # Reusable UI components
│   │       ├── DisclaimerModal.tsx
│   │       ├── LoadingSpinner.tsx
│   │       ├── Navbar.tsx
│   │       └── FormFields/
│   ├── UI/
│   │   ├── Auth/                # Protected admin pages (require JWT)
│   │   │   ├── Admin.tsx        # Main dashboard
│   │   │   ├── CreatePassword.tsx
│   │   │   └── Invite.tsx
│   │   └── PreAuth/             # Public pages (no auth required)
│   │       ├── Login.tsx
│   │       ├── MobileVerificationScreen.tsx
│   │       ├── SurveyForm.tsx
│   │       ├── ReviewPage.tsx
│   │       └── AlreadySubmittedScreen.tsx
│   ├── App.tsx                  # Root component + router
│   ├── App.css
│   ├── index.css
│   └── main.tsx
├── .env                         # Environment variables (see below)
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Base URL of the Django REST API | `http://localhost:8000` |

> All Vite env variables must be prefixed with `VITE_` to be accessible in the browser bundle.

---

## Installation

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

---

## Running the Development Server

```bash
npm run dev
```

The app will be available at **http://localhost:5173**

> The backend API must be running at the URL specified in `VITE_API_BASE_URL` for API calls to succeed.

---

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite dev server with hot-reload |
| `npm run build` | Type-check and produce optimised production build in `dist/` |
| `npm run preview` | Locally preview the production build |
| `npm run lint` | Run ESLint across the source tree |

---

## Application Pages

### Public (no login required)

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | `MobileVerificationScreen` | Enter mobile number to begin survey |
| `/survey` | `SurveyForm` | Multi-step dynamic survey form |
| `/review` | `ReviewPage` | Review answers before submission |
| `/already-submitted` | `AlreadySubmittedScreen` | Shown when mobile already has a submission |
| `/login` | `Login` | Admin login |
| `/activate` | `CreatePassword` | Admin account activation via invite link |

### Protected (JWT required)

| Route | Component | Purpose |
|-------|-----------|---------|
| `/dashboard` | `Admin` | Analytics dashboard with all charts |
| `/invite` | `Invite` | Invite a new admin via email |

---

## Key Features

### Dynamic Survey Form
- Steps and questions are fetched from `/api/survey/schema/`
- Supports `dropdown`, `radio`, `checkbox`, `chips`, and `cards` input types
- Conditional visibility via `visible_when` field rules
- Cascading location dropdowns: District → Division → Mandal → Village

### Mobile Verification
- 10-digit number, must start with 6–9
- No all-repeating digit patterns allowed
- Checked for uniqueness against the backend before form entry

### Bilingual Support
- Language toggle (English / Telugu) visible on the survey page
- All UI strings resolved via `t(key, language)` in `translations.ts`
- Language propagated through `LanguageContext` and serializer `?lang=` param

### Admin Dashboard
- JWT login with RSA-encrypted password transmission
- Token auto-refresh on expiry
- Charts: DonutChart, BarChart, PieChart, HorizontalBarChart, LineChart, StackedAreaChart, WaterfallChart, and more
- All ECharts instances properly disposed on component unmount

---

## Docker / Production Build

A `dockerfile` and `nginx.conf` are provided for containerised deployments.

```bash
# Build production assets
npm run build

# Or build & serve via Docker (from project root)
docker compose up --build frontend
```

The Nginx config serves the SPA from the `dist/` folder and proxies `/api/` to the Django backend.

---

## Notes

- The frontend is **loosely coupled** to the backend — the survey schema evolves without UI code changes.
- No Redux — state is managed via React Context API only.
- TypeScript strict mode is enabled; all new code must be fully typed.
- New UI strings must be added to `src/constants/translations.ts` for both `en` and `te`.

---

**Built for impact. Designed for privacy.**
