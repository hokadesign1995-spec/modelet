// Supabase Edge Function "modelet-auth" (Deno). Kavenegar SMS (verify/lookup).
// Secrets: KAVENEGAR_KEY, KAVENEGAR_TEMPLATE, OTP_PEPPER, ALLOW_ORIGIN
import { createClient } from "npm:@supabase/supabase-js@2";
const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const ORIGIN = Deno.env.get("ALLOW_ORIGIN") || "*";
const cors = { "access-control-allow-origin": ORIGIN, "access-control-allow-headers": "content-type, authorization", "access-control-allow-methods": "GET,POST,OPTIONS" };
const J = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...cors, "content-type": "application/json" } });
const enc = new TextEncoder();
async function sha(s: string) { const h = await crypto.subtle.digest("SHA-256", enc.encode(s + (Deno.env.get("OTP_PEPPER") || ""))); return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, "0")).join(""); }
const code4 = () => String(crypto.getRandomValues(new Uint32Array(1))[0] % 10000).padStart(4, "0");
const okPhone = (p: unknown) => typeof p === "string" && /^09\d{9}$/.test(p);
const pub = (u: any) => ({ id: u.id, phone: u.phone, first: u.first, last: u.last, city: u.city, gender: u.gender, year: u.birth_year });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  const path = new URL(req.url).pathname.replace(/^.*modelet-auth/, "");
  try {
    if (path === "/otp/send" && req.method === "POST") {
      const { phone, purpose, profile } = await req.json();
      if (!okPhone(phone)) return J({ error: "bad_phone" }, 400);
      const { data: u } = await db.from("users").select("id").eq("phone", phone).maybeSingle();
      if (purpose === "signup" && u) return J({ error: "exists" }, 409);
      if (purpose !== "signup" && !u) return J({ error: "not_found" }, 404);
      if (purpose === "signup") {
        const p = profile || {};
        if (!p.first || !p.last || !p.city) return J({ error: "bad_profile" }, 400);
      }
      const { data: prev } = await db.from("otp_codes").select("sent_at").eq("phone", phone).maybeSingle();
      if (prev && Date.now() - new Date(prev.sent_at).getTime() < 60_000) return J({ error: "too_soon" }, 429);
      const code = code4();
      await db.from("otp_codes").upsert({ phone, code_hash: await sha(phone + code), purpose, profile: purpose === "signup" ? profile : null, expires_at: new Date(Date.now() + 120_000).toISOString(), attempts: 0, sent_at: new Date().toISOString() });
      const r = await fetch(`https://api.kavenegar.com/v1/${Deno.env.get("KAVENEGAR_KEY")}/verify/lookup.json?receptor=${phone}&token=${code}&template=${Deno.env.get("KAVENEGAR_TEMPLATE")}`);
      if (!r.ok) return J({ error: "sms_failed" }, 502);
      return J({ ok: true });
    }
    if (path === "/otp/verify" && req.method === "POST") {
      const { phone, code } = await req.json();
      if (!okPhone(phone) || !/^\d{4}$/.test(String(code))) return J({ error: "wrong" }, 400);
      const { data: o } = await db.from("otp_codes").select("*").eq("phone", phone).maybeSingle();
      if (!o) return J({ error: "expired" }, 400);
      if (new Date(o.expires_at).getTime() < Date.now()) return J({ error: "expired" }, 400);
      if (o.attempts >= 5) return J({ error: "locked" }, 429);
      if (o.code_hash !== await sha(phone + code)) { await db.from("otp_codes").update({ attempts: o.attempts + 1 }).eq("phone", phone); return J({ error: "wrong" }, 400); }
      await db.from("otp_codes").delete().eq("phone", phone);
      let { data: u } = await db.from("users").select("*").eq("phone", phone).maybeSingle();
      if (!u) {
        if (o.purpose !== "signup" || !o.profile) return J({ error: "not_found" }, 404);
        const p = o.profile;
        const ins = await db.from("users").insert({ phone, first: String(p.first).slice(0, 60), last: String(p.last).slice(0, 60), city: String(p.city).slice(0, 60), gender: p.gender || null, birth_year: p.year ? +p.year : null }).select().single();
        if (ins.error) return J({ error: "server" }, 500);
        u = ins.data;
      }
      await db.from("users").update({ last_login: new Date().toISOString() }).eq("id", u.id);
      const token = crypto.randomUUID() + crypto.randomUUID();
      await db.from("sessions").insert({ token_hash: await sha(token), user_id: u.id, expires_at: new Date(Date.now() + 30 * 864e5).toISOString() });
      return J({ token, user: pub(u) });
    }
    const tok = (req.headers.get("authorization") || "").replace(/^Bearer /, "");
    if (path === "/me" && req.method === "GET") {
      if (!tok) return J({ error: "auth" }, 401);
      const { data: s } = await db.from("sessions").select("user_id,expires_at").eq("token_hash", await sha(tok)).maybeSingle();
      if (!s || new Date(s.expires_at).getTime() < Date.now()) return J({ error: "auth" }, 401);
      const { data: u } = await db.from("users").select("*").eq("id", s.user_id).single();
      return J({ user: pub(u) });
    }
    if (path === "/logout" && req.method === "POST") {
      if (tok) await db.from("sessions").delete().eq("token_hash", await sha(tok));
      return J({ ok: true });
    }
    return J({ error: "not_found" }, 404);
  } catch (_e) { return J({ error: "server" }, 500); }
});
