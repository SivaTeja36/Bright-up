# Frontend Adoption Prompt: Batch "Mentor" → "mentor_id" + Mentor Dropdown from Users API

## Context

The backend (FastAPI) batch endpoints have been changed:

1. The batch `mentor` field was renamed to `mentor_id`. It stores the **user id** of the mentor (from the `users` table).
2. The batch response now includes BOTH `mentor_id` (the user id) and `mentor` (the mentor's display name).
3. The mentor dropdown in the create/edit batch form must no longer be hardcoded. It must be populated by calling the **Users API** and listing users (no role filter).

## Backend API reference

### 1. Batches API (existing endpoints)

- `POST /batches` — create batch
  Request body (relevant fields):
  ```json
  {
    "syllabus_ids": [1, 2],
    "start_date": "2026-08-10",
    "end_date": "2026-12-20",
    "mentor_id": 5,
    "is_active": true
  }
  ```
  **NOTE:** `mentor` in the request body no longer works. Use `mentor_id` (integer = user id).

- `PUT /batches/{batch_id}` — update batch (same body shape, uses `mentor_id`)

- `GET /batches` — list batches
- `GET /batches/{batch_id}` — single batch

  Response item shape (relevant fields):
  ```json
  {
    "id": 1,
    "mentor_id": 5,
    "mentor": "Siva Teja",
    "syllabus": [...],
    "start_date": "...",
    "end_date": "...",
    ...
  }
  ```
  Use `mentor_id` as the option value and `mentor` as the display label when rendering existing batches.

### 2. Users API (used to populate the mentor dropdown)

- `GET /users`

  Supports query params: `search`, `filter_by`, `filter_values`, `sort_by`, `order_by`, `page`, `page_size`.

  Response shape:
  ```json
  {
    "status_message": "SUCCESS",
    "page": 1,
    "page_size": 1000,
    "total_items": 42,
    "data": [
      {
        "id": 5,
        "name": "Siva Teja",
        "email": "...",
        "gender": "MALE",
        "phone_number": "...",
        "role": "MENTOR",
        "created_at": "...",
        "updated_at": "...",
        "is_active": true
      }
    ]
  }
  ```
  - **Parsing (important):** the user array is nested under `data`. 
    - With axios: `const users = response.data.data;`
    - The response body is `{ status_message, page, page_size, total_items, data: [...] }` — `data` is the array, NOT the whole response.
  - Note: the dropdown will only contain the users that exist in the database (currently only 1 user is seeded). Create more users in the app if more entries are expected.

  **Role values returned by the API:** `ADMIN`, `MENTOR`, `STUDENT`, `GUEST`.

## Required frontend changes

1. **Create/Edit Batch forms**
   - Rename the `mentor` form field to `mentor_id`.
   - Send `mentor_id` (integer, the selected mentor's user id) in the create/update request body.
   - Remove any hardcoded mentor list.

2. **Populate the mentor dropdown from the Users API**
   - When the user clicks **Create Batch** (i.e., when the create batch form/dialog opens), call the Users API to load user names:
     ```
     GET /users?page=1&page_size=1000&sort_by=name&order_by=asc
     ```
   - Show all users in the dropdown (no role filtering).
   - Build dropdown options:
     ```js
     options = users.map(u => ({ value: u.id, label: u.name }));
     ```
   - Store the selected option's `value` (user id) in `mentor_id`.
   - The request must happen on each "Create Batch" click; do not load the user list at batch module mount.

3. **Displaying batches in tables/detail views**
   - Show `mentor` (the name string from the batch response) for display.
   - Keep `mentor_id` for edit pre-selection (match the selected dropdown option against `mentor_id`).

4. **Auth**
   - The Users API is a protected endpoint. Ensure the request includes the same `Authorization: Bearer <token>` header already used for other protected calls.

5. **Loading / error handling**
   - Show a loading state while the users request is in flight.
   - On failure, keep the dropdown empty and show an appropriate error/empty message (do not block the rest of the form).

## Acceptance criteria

- [ ] Create batch sends `mentor_id` (integer), not `mentor`.
- [ ] Update batch sends `mentor_id` (integer).
- [ ] Clicking **Create Batch** calls `GET /users` and shows user names in the mentor dropdown (all users, no role filter).
- [ ] Batch list/detail shows the mentor's name.
- [ ] Editing a batch pre-selects the correct mentor in the dropdown using `mentor_id`.
- [ ] No hardcoded mentor lists remain.
