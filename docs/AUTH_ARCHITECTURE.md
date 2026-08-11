# Authentication Architecture

## Overview
- Mobile app authenticates with managed provider (Firebase Auth).
- Provider issues a JWT token.
- Backend API validates token on requests.
- DriveGuard maps the token subject to a local `User` record.

## Guest Flow
1. User launches app, opts to skip login.
2. Firebase creates anonymous user, issues token.
3. App uses app normally with local persistence + cloud sync keyed to anonymous ID.
4. On explicit sign-up, Firebase links credentials to the existing UID.

## Account Deletion
- User requests deletion in-app.
- Backend deletes PII, anonymizes historical telemetry/reports.
- Backend triggers Firebase Auth deletion via Admin SDK.

## Token Refresh
- Handled natively by Firebase Auth SDK on the client.
- Client passes `Authorization: Bearer <token>`.
