# ADR 04: User profile avatar storage (local filesystem vs object storage)

## Status

Accepted (strategy); **implementation choice is environment-dependent** (see Consequences).

## Context

Phase 3.1 introduces a `profiles` Django app with a `UserProfile` model that may include an **avatar** (`ImageField` or equivalent). Uploaded files must be stored somewhere served to browsers (`MEDIA_URL` / `MEDIA_ROOT` in Django).

Constraints differ by environment:

- **Local development:** A directory on disk under `MEDIA_ROOT` is simple and sufficient.
- **Cloud deployment (Phase 4):** Many PaaS filesystems are **ephemeral**. New releases or restarts can **delete** files written only to local disk, breaking avatar URLs. Production therefore often needs **durable object storage** (e.g. S3, Cloudflare R2, GCS) or a **persistent volume** attached to the app.

## Decision

1. **Development:** Store avatars on the **local filesystem** via Django’s default `FileSystemStorage` and `MEDIA_ROOT` / `MEDIA_URL`.
2. **Production:** Prefer **object storage** (S3-compatible API) using `django-storages` (or equivalent) **or** a platform-managed persistent disk, configured via environment variables. The exact provider (AWS S3, R2, etc.) is an implementation detail; the architectural rule is **durability and backup independent of the app container**.

## Rationale

- Keeps developer setup minimal while avoiding silent data loss in containerized production.
- Avoids rewriting product docs on every hosting change: the **decision** is “local vs durable remote storage by environment,” not a single vendor name.

## Consequences

- **Positive:** Clear migration path from local dev to cloud without changing the `UserProfile` model’s field type in most cases (only `DEFAULT_FILE_STORAGE` / `STORAGES` settings change).
- **Positive:** Aligns with Phase 4 checklist (secrets, `ALLOWED_HOSTS`, static/media strategy).
- **Negative:** Production requires extra configuration (bucket, credentials, CORS if assets are served from a CDN domain).
- **Neutral:** Optional image processing (resize, thumbnails) can be added later; out of scope for this ADR.

---

*Date: 23 March, 2026* | *Author: Aníbal Rojo*
