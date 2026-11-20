-- Modelet: users database (Postgres / Supabase)
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  phone text unique not null check (phone ~ '^09[0-9]{9}$'),
  first text not null, last text not null, city text not null,
  gender text, birth_year int,
  created_at timestamptz default now(), last_login timestamptz
);
create table if not exists otp_codes (
  phone text primary key,
  code_hash text not null,
  purpose text not null,            -- login | signup
  profile jsonb,                    -- signup form data, saved only after verify
  expires_at timestamptz not null,
  attempts int not null default 0,
  sent_at timestamptz not null default now()
);
create table if not exists sessions (
  token_hash text primary key,
  user_id uuid references users(id) on delete cascade,
  created_at timestamptz default now(),
  expires_at timestamptz not null
);
alter table users enable row level security;
alter table otp_codes enable row level security;
alter table sessions enable row level security;
-- no policies: only the edge function (service role) can touch these tables
