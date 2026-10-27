#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 85 HTML demo pages, one per UI style. Each page uses a distinct
layout archetype + signature components so styles differ structurally, not just in skin."""
import csv, re, os, html

SRC = r"C:\Users\yasin\AppData\Local\hermes\skills\ui-ux-pro-max\data\styles.csv"
OUT = r"C:\Users\yasin\SetupAgent\ui-style-gallery"
STYLES_DIR = os.path.join(OUT, "styles")

DEFAULT = dict(
    bg="#FFFFFF", ink="#111827", muted="#6B7280",
    accent="#3B82F6", a2="#6366F1",
    card="#FFFFFF", card_ink="#111827",
    radius="12px", border="1px solid #E5E7EB",
    shadow="0 1px 3px rgba(0,0,0,.08)",
    fh="Inter", fb="Inter", fx="",
)

R = {}
R[1]  = dict(bg="#FFFFFF", ink="#000000", muted="#525252", accent="#000000", card="#FFFFFF", radius="0px", border="1px solid #E5E5E5", shadow="none", fh="Inter", fb="Inter")
R[2]  = dict(bg="#E0E5EC", ink="#3D4852", muted="#6B7280", accent="#6C63FF", card="#E0E5EC", card_ink="#3D4852", radius="16px", border="none", shadow="9px 9px 18px rgba(163,177,198,.7), -9px -9px 18px rgba(255,255,255,.9)", fh="Plus Jakarta Sans", fb="Inter", fx=".ext{background:#E0E5EC;box-shadow:9px 9px 18px rgba(163,177,198,.7),-9px -9px 18px rgba(255,255,255,.9)}.ins{background:#E0E5EC;box-shadow:inset 6px 6px 12px rgba(163,177,198,.7),inset -6px -6px 12px rgba(255,255,255,.9)}")
R[3]  = dict(bg="linear-gradient(135deg,#667EEA 0%,#764BA2 45%,#F093FB 100%)", ink="#FFFFFF", muted="rgba(255,255,255,.8)", accent="#FFFFFF", a2="#00E5FF", card="rgba(255,255,255,.14)", card_ink="#FFFFFF", radius="18px", border="1px solid rgba(255,255,255,.25)", shadow="0 8px 32px rgba(0,0,0,.35)", fh="Inter", fb="Inter", fx=".glass{background:rgba(255,255,255,.14);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.25)}")
R[4]  = dict(bg="#FFFFFF", ink="#000000", muted="#333333", accent="#FF0000", card="#FFFFFF", radius="0px", border="3px solid #000000", shadow="6px 6px 0 #000000", fh="Arial", fb="Arial", fx="body{transition:none}.card,.btn,.chip{transition:none}")
R[5]  = dict(bg="radial-gradient(ellipse at 30% 20%,#0A2E4D 0%,#001F3F 55%,#000A14 100%)", ink="#E8EFF5", muted="#9DB4C8", accent="#FFD700", card="rgba(255,255,255,.05)", card_ink="#E8EFF5", radius="10px", border="1px solid rgba(255,215,0,.25)", shadow="0 20px 50px rgba(0,0,0,.6)", fh="Space Grotesk", fb="Inter", fx=".scene{perspective:1000px}.cube3{width:110px;height:110px;background:linear-gradient(135deg,#FFD700,#B8860B);border-radius:16px;transform:rotateX(14deg) rotateY(-18deg) rotateZ(6deg);box-shadow:0 30px 60px rgba(0,0,0,.6), inset -8px -8px 24px rgba(0,0,0,.4), inset 8px 8px 24px rgba(255,255,255,.25);animation:spin3 12s linear infinite}@keyframes spin3{from{transform:rotateX(14deg) rotateY(-18deg) rotateZ(0)}to{transform:rotateX(14deg) rotateY(342deg) rotateZ(0)}}")
R[6]  = dict(bg="#111111", ink="#FFFFFF", muted="#D4D4D4", accent="#FF1493", a2="#00FFFF", card="#1C1C1E", card_ink="#FFFFFF", radius="0px", border="3px solid #FF1493", shadow="8px 8px 0 #00FFFF", fh="Space Grotesk", fb="Inter", fx=".chip{background:#39FF14;color:#000;font-weight:800}")
R[7]  = dict(bg="#000000", ink="#FFFFFF", muted="#A3A3A3", accent="#39FF14", card="#121212", card_ink="#E5E5E5", radius="12px", border="1px solid #1F1F1F", shadow="none", fh="Inter", fb="Inter", fx=".glow{text-shadow:0 0 12px rgba(57,255,20,.8)}.btn{box-shadow:0 0 18px rgba(57,255,20,.45)}")
R[8]  = dict(bg="#FFFFFF", ink="#111111", muted="#444444", accent="#0A5CFF", card="#FFFFFF", radius="6px", border="2px solid #111111", shadow="none", fh="Arial", fb="Arial", fx="body{font-size:17px}.btn:focus-visible,.field:focus-visible{outline:4px solid #0A5CFF;outline-offset:2px}")
R[9]  = dict(bg="#FDE8E4", ink="#3B2E2A", muted="#7A6A64", accent="#FF8FAB", card="#FFF7F5", card_ink="#3B2E2A", radius="22px", border="4px solid #E8C4BC", shadow="6px 6px 0 #DDB8AE, inset -3px -3px 8px rgba(0,0,0,.06)", fh="Nunito", fb="Nunito", fx=".btn{transition:transform .2s cubic-bezier(.34,1.56,.64,1)}.btn:hover{transform:scale(1.05)}")
R[10] = dict(bg="linear-gradient(120deg,#0080FF,#8B00FF,#FF1493,#00BFA5,#0080FF)", ink="#FFFFFF", muted="rgba(255,255,255,.85)", accent="#FFFFFF", card="rgba(255,255,255,.12)", card_ink="#FFFFFF", radius="20px", border="1px solid rgba(255,255,255,.3)", shadow="0 12px 40px rgba(0,0,0,.3)", fh="Space Grotesk", fb="Inter", fx="body{background-size:300% 300%;animation:aurora 12s ease infinite}@keyframes aurora{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}")
R[11] = dict(bg="#1A1A2E", ink="#E0E0E0", muted="#8A8AA3", accent="#FF006E", a2="#00FFFF", card="rgba(255,255,255,.04)", card_ink="#E0E0E0", radius="4px", border="1px solid #FF006E", shadow="0 0 18px rgba(255,0,110,.35)", fh="Chakra Petch", fb="JetBrains Mono", fx=".neon{text-shadow:0 0 8px #FF006E,0 0 20px #FF006E}body::after{content:'';position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 2px,rgba(0,255,255,.04) 2px 4px);z-index:999}")
R[12] = dict(bg="#FFFFFF", ink="#222222", muted="#666666", accent="#FF5722", a2="#2196F3", card="#FFFFFF", radius="4px", border="2px solid #EEEEEE", shadow="none", fh="Inter", fb="Inter")
R[13] = dict(bg="linear-gradient(160deg,#6B4A2B 0%,#8B5A2B 50%,#5C3A21 100%)", ink="#F5E6C8", muted="#D8C49A", accent="#FFD700", card="linear-gradient(160deg,#7A5230,#6B4A2B)", card_ink="#F5E6C8", radius="8px", border="2px solid #A0703B", shadow="0 12px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.12)", fh="Georgia", fb="Georgia")
R[14] = dict(bg="linear-gradient(135deg,#00FFFF,#FF00FF,#0066FF,#00FF66,#00FFFF)", ink="#FFFFFF", muted="rgba(255,255,255,.85)", accent="#FFFFFF", card="rgba(255,255,255,.18)", card_ink="#FFFFFF", radius="24px", border="1px solid rgba(255,255,255,.4)", shadow="0 20px 60px rgba(0,0,0,.4)", fh="Inter", fb="Inter", fx="body{background-size:400% 400%;animation:liq 14s ease infinite}@keyframes liq{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}.hero h1{text-shadow:2px 0 0 rgba(255,0,0,.35),-2px 0 0 rgba(0,255,255,.35)}")
R[15] = dict(bg="#FFFFFF", ink="#111111", muted="#6B7280", accent="#6366F1", card="#FFFFFF", radius="16px", border="1px solid #E5E7EB", shadow="0 8px 30px rgba(0,0,0,.08)", fh="Space Grotesk", fb="Inter", fx=".card{transition:transform .35s cubic-bezier(.22,1,.36,1)}.card:hover{transform:translateY(-6px)}.reveal{animation:rise .6s cubic-bezier(.22,1,.36,1) both}@keyframes rise{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}")
R[16] = dict(bg="#F8FAFC", ink="#111827", muted="#6B7280", accent="#22C55E", card="#FFFFFF", radius="10px", border="1px solid #E5E7EB", shadow="0 1px 2px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".btn{transition:transform .08s ease}.btn:active{transform:scale(.96)}.card{transition:box-shadow .15s ease}.card:hover{box-shadow:0 4px 12px rgba(0,0,0,.08)}")
R[17] = dict(bg="#FFFFFF", ink="#000000", muted="#3F3F46", accent="#7C2D12", card="#FFFFFF", radius="4px", border="2px solid #000000", shadow="none", fh="Arial", fb="Arial", fx="body{font-size:17px}.chip{border:2px dashed #000;background:#FFF}a:focus-visible,.btn:focus-visible{outline:4px solid #FFB300;outline-offset:2px}")
R[18] = dict(bg="#FAFAFA", ink="#111111", muted="#737373", accent="#10B981", card="#FFFFFF", radius="14px", border="1px solid #F0F0F0", shadow="0 2px 8px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".field{background:#F5F5F5;border:none}")
R[19] = dict(bg="#E8EDF2", ink="#2D3748", muted="#718096", accent="#4C6FFF", card="#EDF2F7", card_ink="#2D3748", radius="10px", border="none", shadow="0 2px 6px rgba(45,55,72,.08), 0 12px 24px rgba(45,55,72,.06)", fh="Inter", fb="Inter", fx=".btn{box-shadow:0 2px 6px rgba(76,111,255,.35)}")
R[20] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#4F46E5", card="#FFFFFF", radius="14px", border="1px solid #E5E7EB", shadow="0 10px 30px rgba(0,0,0,.07)", fh="Space Grotesk", fb="Inter", fx=".hero{background:radial-gradient(ellipse at 70% 10%,rgba(79,70,229,.14),transparent 55%),linear-gradient(180deg,#F9FAFB,#FFFFFF)}")
R[21] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#16A34A", card="#FFFFFF", radius="8px", border="1px solid #E5E7EB", shadow="0 1px 2px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".field:focus{border-color:#16A34A;box-shadow:0 0 0 3px rgba(22,163,74,.15)}")
R[22] = dict(bg="#F9FAFB", ink="#111827", muted="#6B7280", accent="#2563EB", card="#FFFFFF", radius="12px", border="1px solid #E5E7EB", shadow="0 1px 3px rgba(0,0,0,.06)", fh="Inter", fb="Inter", fx=".card{transition:transform .2s ease,box-shadow .2s ease}.card:hover{transform:translateY(-4px);box-shadow:0 12px 24px rgba(0,0,0,.08)}")
R[23] = dict(bg="#FFFFFF", ink="#1A1A1A", muted="#6B7280", accent="#111111", card="#FFFFFF", radius="0px", border="none", shadow="none", fh="Inter", fb="Inter")
R[24] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#2563EB", card="#F9FAFB", card_ink="#111827", radius="12px", border="1px solid #E5E7EB", shadow="0 4px 12px rgba(0,0,0,.06)", fh="Inter", fb="Inter", fx=".stars{color:#FBBF24;letter-spacing:2px}")
R[25] = dict(bg="#0F172A", ink="#E2E8F0", muted="#94A3B8", accent="#38BDF8", card="rgba(255,255,255,.06)", card_ink="#E2E8F0", radius="10px", border="1px solid rgba(148,163,184,.25)", shadow="0 20px 60px rgba(0,0,0,.5)", fh="Space Grotesk", fb="Inter", fx=".mock{background:#0B1220;border:1px solid #1E293B;border-radius:8px}")
R[26] = dict(bg="#F8FAFC", ink="#111827", muted="#64748B", accent="#1E40AF", card="#FFFFFF", radius="10px", border="1px solid #E2E8F0", shadow="0 2px 8px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".ok{background:#ECFDF5;color:#059669;border:1px solid #A7F3D0}")
R[27] = dict(bg="#FFFFFF", ink="#1C1917", muted="#78716C", accent="#B45309", card="#FFFBEB", card_ink="#1C1917", radius="8px", border="1px solid #FDE68A", shadow="none", fh="DM Serif Display", fb="Inter", fx=".hero{background:linear-gradient(180deg,#FFF7ED,#FFFFFF)}")
R[28] = dict(bg="#F5F5F5", ink="#333333", muted="#777777", accent="#2563EB", card="#FFFFFF", card_ink="#333333", radius="6px", border="1px solid #E0E0E0", shadow="none", fh="Inter", fb="Inter", fx="body{font-size:14px}")
R[29] = dict(bg="#FFFFFF", ink="#1F2937", muted="#6B7280", accent="#EF4444", card="#FFFFFF", radius="4px", border="1px solid #E5E7EB", shadow="none", fh="Inter", fb="Inter")
R[30] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#0F766E", card="#FFFFFF", radius="12px", border="1px solid #E5E7EB", shadow="0 1px 3px rgba(0,0,0,.07)", fh="Inter", fb="Inter", fx=".kpi-num{font-size:40px;font-weight:800;letter-spacing:-.03em}")
R[31] = dict(bg="#0B1220", ink="#E2E8F0", muted="#94A3B8", accent="#22C55E", card="rgba(255,255,255,.05)", card_ink="#E2E8F0", radius="10px", border="1px solid rgba(148,163,184,.2)", shadow="none", fh="Inter", fb="Inter", fx=".dot{width:10px;height:10px;border-radius:50%;background:#22C55E;animation:pulse 1.6s ease infinite}@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(34,197,94,.5)}50%{opacity:.6;box-shadow:0 0 0 6px rgba(34,197,94,0)}}")
R[32] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#7C3AED", card="#FFFFFF", radius="10px", border="1px solid #E5E7EB", shadow="0 1px 2px rgba(0,0,0,.05)", fh="Inter", fb="Inter")
R[33] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#2563EB", card="#FFFFFF", radius="10px", border="1px solid #E5E7EB", shadow="0 1px 2px rgba(0,0,0,.05)", fh="Inter", fb="Inter")
R[34] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#8B5CF6", card="#FFFFFF", radius="10px", border="1px solid #E5E7EB", shadow="0 1px 2px rgba(0,0,0,.05)", fh="Inter", fb="Inter")
R[35] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#3B82F6", card="#FFFFFF", radius="8px", border="1px solid #E5E7EB", shadow="none", fh="Inter", fb="Inter")
R[36] = dict(bg="#FFFFFF", ink="#111827", muted="#64748B", accent="#003366", card="#FFFFFF", radius="8px", border="1px solid #E2E8F0", shadow="none", fh="Inter", fb="Inter")
R[37] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#2563EB", card="#FFFFFF", radius="8px", border="1px solid #E5E7EB", shadow="0 1px 2px rgba(0,0,0,.05)", fh="Inter", fb="Inter")
R[38] = dict(bg="#FFFDF5", ink="#000000", muted="#404040", accent="#FF5252", a2="#FFEB3B", card="#FFFFFF", card_ink="#000000", radius="0px", border="3px solid #000000", shadow="5px 5px 0 #000000", fh="Archivo", fb="Inter", fx=".chip{background:#FFEB3B;border:2px solid #000;box-shadow:3px 3px 0 #000}.btn:active{transform:translate(3px,3px);box-shadow:none}")
R[39] = dict(bg="#F5F5F7", ink="#1D1D1F", muted="#6E6E73", accent="#0071E3", card="#FFFFFF", card_ink="#1D1D1F", radius="24px", border="none", shadow="0 2px 8px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".card{transition:transform .2s ease}.card:hover{transform:scale(1.02)}")
R[40] = dict(bg="linear-gradient(135deg,#FF69B4 0%,#9400D3 40%,#00FFFF 100%)", ink="#FFFFFF", muted="rgba(255,255,255,.85)", accent="#00FFFF", card="linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,.12))", card_ink="#FFFFFF", radius="999px", border="2px solid rgba(255,255,255,.6)", shadow="0 10px 30px rgba(0,0,0,.35)", fh="Syne", fb="Inter", fx=".chrome{background:linear-gradient(180deg,#fff 0%,#C0C0C0 35%,#8A8A8A 50%,#E8E8E8 65%,#fff 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 4px rgba(0,0,0,.4))}")
R[41] = dict(bg="#0D0D0D", ink="#00FF00", muted="#00AA00", accent="#FF00FF", a2="#00FFFF", card="rgba(0,255,0,.05)", card_ink="#00FF00", radius="0px", border="1px solid #00FF00", shadow="0 0 12px rgba(0,255,0,.25)", fh="Chakra Petch", fb="JetBrains Mono", fx="body::after{content:'';position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 3px,rgba(0,255,0,.05) 3px 4px);z-index:999}.glow{text-shadow:0 0 10px #00FF00}")
R[42] = dict(bg="#F5F5DC", ink="#2D2D1E", muted="#6B6B4E", accent="#228B22", card="#FBFAEC", card_ink="#2D2D1E", radius="24px", border="none", shadow="0 8px 24px rgba(0,0,0,.08)", fh="Nunito", fb="Nunito", fx=".hero{background:radial-gradient(circle at 85% 20%,rgba(135,206,235,.35),transparent 50%),#F5F5DC}")
R[43] = dict(bg="#F5F5F5", ink="#111111", muted="#6B7280", accent="#6366F1", card="#FFFFFF", card_ink="#111111", radius="14px", border="1px solid #E5E5E5", shadow="0 2px 8px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".bubble-u{background:#E0E7FF;border-radius:16px 16px 4px 16px}.bubble-a{background:#FFFFFF;border-radius:16px 16px 16px 4px;border:1px solid #E5E5E5}.typing span{width:7px;height:7px;border-radius:50%;background:#6366F1;display:inline-block;animation:blink 1.2s infinite}.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}@keyframes blink{0%,80%,100%{opacity:.25}40%{opacity:1}}")
R[44] = dict(bg="#FFFFFF", ink="#222222", muted="#666666", accent="#FF71CE", a2="#FFCE5C", card="#FFFFFF", radius="0px", border="2px solid #222222", shadow="4px 4px 0 #222222", fh="Archivo", fb="Inter")
R[45] = dict(bg="linear-gradient(180deg,#2E1B4E 0%,#5B2A86 45%,#FF71CE 100%)", ink="#FFFFFF", muted="rgba(255,255,255,.85)", accent="#01CDFE", a2="#05FFA1", card="rgba(255,255,255,.1)", card_ink="#FFFFFF", radius="8px", border="1px solid rgba(1,205,254,.4)", shadow="0 0 24px rgba(1,205,254,.25)", fh="Chakra Petch", fb="JetBrains Mono", fx=".neon{text-shadow:0 0 12px #01CDFE,0 0 32px #FF71CE}")
R[46] = dict(bg="#F5F5F5", ink="#1F2937", muted="#6B7280", accent="#6366F1", card="#FFFFFF", card_ink="#1F2937", radius="12px", border="none", shadow="0 10px 20px rgba(0,0,0,.1)", fh="Inter", fb="Inter")
R[47] = dict(bg="#FFFFFF", ink="#000000", muted="#525252", accent="#FF3D00", card="#FFFFFF", radius="0px", border="none", shadow="none", fh="Archivo", fb="Inter", fx=".hero h1{font-size:clamp(3rem,9vw,7rem);font-weight:900;letter-spacing:-.05em;line-height:.95}")
R[48] = dict(bg="#0A0A0A", ink="#FFFFFF", muted="#A3A3A3", accent="#00E5FF", card="rgba(255,255,255,.05)", card_ink="#FFFFFF", radius="12px", border="1px solid rgba(255,255,255,.12)", shadow="none", fh="Space Grotesk", fb="Inter", fx=".kinetic{background:linear-gradient(90deg,#00E5FF,#FF3D00,#00E5FF);background-size:200% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:kin 4s linear infinite}@keyframes kin{to{background-position:200% center}}.typed::after{content:'|';animation:caret 1s steps(1) infinite}@keyframes caret{50%{opacity:0}}")
R[49] = dict(bg="#FFFFFF", ink="#111111", muted="#6B7280", accent="#D97706", card="#FFFFFF", radius="0px", border="1px solid #E5E5E5", shadow="none", fh="DM Serif Display", fb="Inter")
R[50] = dict(bg="#FFFFFF", ink="#000000", muted="#525252", accent="#FF3D00", card="#FFFFFF", radius="0px", border="1px solid #E5E5E5", shadow="none", fh="Inter", fb="Helvetica", fx=".hero{border-bottom:4px solid #000}")
R[51] = dict(bg="#000812", ink="#00FFFF", muted="#7FB8C9", accent="#00FFFF", a2="#FF0000", card="rgba(0,255,255,.04)", card_ink="#00FFFF", radius="0px", border="1px solid rgba(0,255,255,.4)", shadow="0 0 14px rgba(0,255,255,.2)", fh="JetBrains Mono", fb="JetBrains Mono", fx="body::after{content:'';position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 3px,rgba(0,255,255,.03) 3px 4px);z-index:999}")
R[52] = dict(bg="#1A1C2C", ink="#FFFFFF", muted="#B0B5CC", accent="#FFD300", card="#242742", card_ink="#FFFFFF", radius="0px", border="4px solid #0D0E17", shadow="4px 4px 0 #0D0E17", fh="Press Start 2P", fb="VT323", fx=".btn{box-shadow:4px 4px 0 #0D0E17;text-transform:uppercase;image-rendering:pixelated}")
R[53] = dict(bg="#F5F5F7", ink="#1D1D1F", muted="#86868B", accent="#1D1D1F", card="#FFFFFF", card_ink="#1D1D1F", radius="20px", border="none", shadow="0 2px 10px rgba(0,0,0,.04)", fh="Inter", fb="Inter")
R[54] = dict(bg="#0B3A6F", ink="#EAF2FF", muted="#9CC0E4", accent="#7FD4FF", a2="#FFD98A", card="rgba(10,42,80,.55)", card_ink="#EAF2FF", radius="0px", border="1px solid rgba(127,212,255,.35)", shadow="none", fh="JetBrains Mono", fb="Inter", fx=""".bp-sheet{border:1px solid rgba(127,212,255,.55);background:#0A2A50;box-shadow:0 0 0 1px rgba(127,212,255,.15) inset}
.bp-head,.bp-stamp{display:flex;justify-content:space-between;gap:12px;padding:9px 14px;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:#9CC0E4;border-bottom:1px solid rgba(127,212,255,.35)}
.bp-stamp{border-bottom:none;border-top:1px solid rgba(127,212,255,.35)}
.bp-body{padding:26px;display:grid;grid-template-columns:1.5fr .5fr;gap:22px}
.bp-frame{position:relative;border:1px dashed rgba(127,212,255,.45);min-height:260px;display:flex;align-items:center;justify-content:center;padding:34px;background-image:linear-gradient(rgba(127,212,255,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(127,212,255,.13) 1px,transparent 1px);background-size:22px 22px}
.bp-center{text-align:center;border:1px solid rgba(127,212,255,.5);padding:22px 30px;background:rgba(10,42,80,.72)}
.bp-center b{display:block;font-size:12.5px;letter-spacing:.22em}
.bp-center span{font-size:11px;color:#9CC0E4;letter-spacing:.06em}
.bp-dim{position:absolute;display:flex;align-items:center;gap:6px;font-size:10.5px;color:#9CC0E4;letter-spacing:.12em}
.bp-dim i{flex:1;height:1px;background:rgba(127,212,255,.6);position:relative}
.bp-dim-h{left:14px;right:14px;top:8px}.bp-dim-v{flex-direction:column;top:14px;bottom:14px;right:8px;width:auto}
.bp-dim-v i{width:1px;height:auto;flex:1}
.bp-callout{position:absolute;display:flex;align-items:center;gap:7px;font-size:10.5px;color:#9CC0E4}
.bp-callout b{width:19px;height:19px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(127,212,255,.7);font-size:10.5px;color:#EAF2FF}
.bp-c1{top:46px;left:18px}.bp-c2{bottom:52px;left:18px}.bp-c3{bottom:120px;right:32px}
.bp-legend{display:flex;flex-direction:column;gap:10px;font-size:11px;color:#9CC0E4}
.bp-lg{display:flex;align-items:center;gap:9px}
.bp-lg i{width:26px;height:1px;flex-shrink:0}
.bp-lg .l1{background:#7FD4FF}.bp-lg .l2{background:repeating-linear-gradient(90deg,#7FD4FF 0 5px,transparent 5px 9px)}
.bp-lg .l3{height:11px;background:repeating-linear-gradient(45deg,rgba(127,212,255,.7) 0 1px,transparent 1px 4px);border:1px solid rgba(127,212,255,.5)}""")
R[55] = dict(bg="linear-gradient(160deg,#0A0A1E 0%,#1B1040 60%,#3A2E6E 100%)", ink="#FFFFFF", muted="rgba(255,255,255,.75)", accent="#A78BFA", card="rgba(255,255,255,.16)", card_ink="#FFFFFF", radius="28px", border="1px solid rgba(255,255,255,.3)", shadow="0 24px 60px rgba(0,0,0,.45)", fh="Inter", fb="Inter", fx=".glass{backdrop-filter:blur(40px) saturate(180%);-webkit-backdrop-filter:blur(40px) saturate(180%)}")
R[56] = dict(bg="#FDFBF7", ink="#1A1A1A", muted="#4A4A4A", accent="#1A1A1A", card="#FFFFFF", card_ink="#1A1A1A", radius="0px", border="1px solid #E0E0E0", shadow="none", fh="Source Serif 4", fb="Georgia", fx="body{transition:none}.card,.btn,.chip{transition:none}")
R[57] = dict(bg="#FFFFFF", ink="#111111", muted="#555555", accent="#FF00FF", a2="#00FF00", card="#FFF9C4", card_ink="#111111", radius="0px", border="3px dashed #111111", shadow="5px 5px 0 #111111", fh="Archivo", fb="Inter", fx=".marquee{overflow:hidden;white-space:nowrap;background:#00FF00;color:#000;border:2px solid #000}.marquee span{display:inline-block;animation:marq 8s linear infinite}@keyframes marq{from{transform:translateX(100%)}to{transform:translateX(-100%)}}")
R[58] = dict(bg="radial-gradient(ellipse at 20% 80%,#0A3D2E 0%,#001E3C 60%,#000810 100%)", ink="#E8FFF2", muted="#9FD8C0", accent="#00FF41", card="rgba(255,255,255,.05)", card_ink="#E8FFF2", radius="24px", border="1px solid rgba(0,255,65,.2)", shadow="0 0 30px rgba(0,255,65,.12)", fh="Nunito", fb="Inter", fx=".blob{position:absolute;border-radius:50%;filter:blur(60px);opacity:.25;animation:breathe 5s ease-in-out infinite}@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}")
R[59] = dict(bg="#FAFAF8", ink="#1A1A1A", muted="#4A4A4A", accent="#C4A77D", card="#FFFFFF", card_ink="#1A1A1A", radius="255px 15px 225px 15px/15px 225px 15px 255px", border="2px solid #1A1A1A", shadow="3px 3px 0 #1A1A1A", fh="Caveat", fb="Patrick Hand", fx=".card{transform:rotate(-.6deg)}.card:nth-child(3){transform:rotate(.8deg)}body{background-image:radial-gradient(rgba(0,0,0,.03) 1px,transparent 1px);background-size:22px 22px}")
R[60] = dict(bg="#FDF2F8", ink="#332F3A", muted="#8B7F92", accent="#FF9ECD", card="linear-gradient(180deg,#FFFFFF,#FDE4F0)", card_ink="#332F3A", radius="24px", border="none", shadow="0 14px 30px rgba(255,158,205,.4), inset 0 -4px 0 rgba(0,0,0,.06)", fh="Nunito", fb="Inter", fx=".btn{border-radius:999px;transition:transform .2s cubic-bezier(.34,1.56,.64,1)}.btn:hover{transform:scale(1.06)}.btn:active{transform:scale(.94)}")
R[61] = dict(bg="#F5F0E1", ink="#3B3226", muted="#8A7B66", accent="#C67B5C", card="#FAF6EA", card_ink="#3B3226", radius="16px", border="1px solid #E3D9C3", shadow="0 8px 20px rgba(59,50,38,.08)", fh="Fraunces", fb="Inter", fx=".hero{background:radial-gradient(circle at 80% 20%,rgba(198,123,92,.18),transparent 50%)}")
R[62] = dict(bg="#FFFFFF", ink="#111111", muted="#6B7280", accent="#FF3D00", card="#FFFFFF", radius="12px", border="1px solid #E5E5E5", shadow="0 4px 12px rgba(0,0,0,.06)", fh="Inter", fb="Inter", fx="body{cursor:none}")
R[63] = dict(bg="#FAFAFA", ink="#111111", muted="#737373", accent="#6B8FAF", card="#FFFFFF", radius="16px", border="1px solid #F0F0F0", shadow="0 2px 8px rgba(0,0,0,.05)", fh="Inter", fb="Inter", fx=".wave{display:flex;align-items:center;gap:3px;height:48px}.wave i{width:4px;border-radius:2px;background:#6B8FAF;animation:wave 1s ease-in-out infinite}.wave i:nth-child(2n){animation-delay:.15s}.wave i:nth-child(3n){animation-delay:.3s}@keyframes wave{0%,100%{height:8px}50%{height:44px}}")
R[64] = dict(bg="#E8E8E8", ink="#111111", muted="#666666", accent="#3B82F6", card="#FFFFFF", radius="12px", border="1px solid #DDDDDD", shadow="0 4px 16px rgba(0,0,0,.1)", fh="Inter", fb="Inter", fx=".stage{background:radial-gradient(circle at 50% 40%,#3B82F6,#1E3A8A);border-radius:16px;perspective:900px}.cube{width:90px;height:90px;background:linear-gradient(135deg,#93C5FD,#1D4ED8);border-radius:14px;animation:spin 9s linear infinite}@keyframes spin{from{transform:rotateY(0) rotateX(8deg)}to{transform:rotateY(360deg) rotateX(8deg)}}")
R[65] = dict(bg="linear-gradient(135deg,#00FFFF,#FF00FF,#FFFF00,#0066FF,#00FF66,#00FFFF)", ink="#FFFFFF", muted="rgba(255,255,255,.85)", accent="#FFFFFF", card="rgba(255,255,255,.16)", card_ink="#FFFFFF", radius="20px", border="1px solid rgba(255,255,255,.35)", shadow="0 16px 48px rgba(0,0,0,.35)", fh="Inter", fb="Inter", fx="body{background-size:400% 400%;animation:mesh 12s ease infinite}@keyframes mesh{0%{background-position:0% 0%}25%{background-position:100% 0%}50%{background-position:100% 100%}75%{background-position:0% 100%}100%{background-position:0% 0%}}")
R[66] = dict(bg="#FFFFFF", ink="#111111", muted="#6B7280", accent="#B91C1C", card="#FFFFFF", radius="0px", border="1px solid #E5E5E5", shadow="none", fh="DM Serif Display", fb="Source Serif 4", fx=".dropcap::first-letter{font-size:3.2em;float:left;line-height:.9;padding-right:8px;font-family:'DM Serif Display';color:#B91C1C}")
R[67] = dict(bg="#0A0A0A", ink="#FFFFFF", muted="#888888", accent="#00FF00", card="rgba(255,255,255,.06)", card_ink="#FFFFFF", radius="0px", border="1px solid rgba(255,255,255,.15)", shadow="none", fh="Space Grotesk", fb="Inter", fx=".rgb{text-shadow:2px 0 0 rgba(255,0,0,.6),-2px 0 0 rgba(0,255,255,.6);animation:jitter 3.2s steps(2) infinite}@keyframes jitter{0%,92%,100%{transform:none}94%{transform:translateX(-1px)}96%{transform:translateX(1px)}98%{transform:translateX(-.5px)}}")
R[68] = dict(bg="#F5E6C8", ink="#3D2B1F", muted="#8A7260", accent="#D4A574", card="#FBF1DD", card_ink="#3D2B1F", radius="0px", border="1px solid #E0CDA8", shadow="0 8px 20px rgba(61,43,31,.12)", fh="Special Elite", fb="Georgia", fx="body::before{content:'';position:fixed;inset:0;pointer-events:none;background:url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"140\" height=\"140\"><filter id=\"n\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"0.8\" numOctaves=\"2\"/><feColorMatrix type=\"saturate\" values=\"0\"/></filter><rect width=\"140\" height=\"140\" filter=\"url(%23n)\" opacity=\"0.06\"/></svg>');z-index:999}")
R[69] = dict(bg="#F0F0F0", ink="#121212", muted="#555555", accent="#D02020", a2="#1040C0", card="#FFFFFF", card_ink="#121212", radius="0px", border="2px solid #121212", shadow="4px 4px 0 #121212", fh="Outfit", fb="Inter", fx=".hero h1{font-weight:900;text-transform:uppercase;letter-spacing:-.02em}.btn{border-radius:999px;font-weight:800;text-transform:uppercase;letter-spacing:.04em}.btn:active{transform:translate(2px,2px);box-shadow:none}.circle{width:110px;height:110px;border-radius:50%;background:#F0C020;border:2px solid #121212;box-shadow:4px 4px 0 #121212}")
R[70] = dict(bg="#FFFFFF", ink="#000000", muted="#525252", accent="#000000", card="#FFFFFF", card_ink="#000000", radius="0px", border="2px solid #000000", shadow="none", fh="Playfair Display", fb="Source Serif 4", fx=".tag{font-family:'JetBrains Mono';font-size:11px;letter-spacing:.18em;text-transform:uppercase}.divider{height:4px;background:#000}")
R[71] = dict(bg="linear-gradient(180deg,#0A0A0F 0%,#020203 100%)", ink="#EDEDEF", muted="#8A8F98", accent="#5E6AD2", card="rgba(255,255,255,.05)", card_ink="#EDEDEF", radius="16px", border="1px solid rgba(255,255,255,.08)", shadow="0 12px 40px rgba(0,0,0,.5)", fh="Inter", fb="Inter", fx=".blob{position:absolute;border-radius:50%;filter:blur(50px);opacity:.12;animation:drift 14s ease-in-out infinite}@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-30px)}}.btn{box-shadow:0 0 24px rgba(94,106,210,.35)}")
R[72] = dict(bg="#FAFAFA", ink="#0F172A", muted="#64748B", accent="#0052FF", a2="#4D7CFF", card="#FFFFFF", card_ink="#0F172A", radius="16px", border="1px solid #E2E8F0", shadow="0 4px 10px rgba(0,0,0,.06)", fh="Calistoga", fb="Inter", fx=".btn{background:linear-gradient(90deg,#0052FF,#4D7CFF)}.pl{background:rgba(0,82,255,.05);border:1px solid rgba(0,82,255,.2);color:#0052FF;font-family:'JetBrains Mono';font-size:11px;letter-spacing:.08em;text-transform:uppercase;border-radius:999px}")
R[73] = dict(bg="#050505", ink="#33FF00", muted="#1A3D1A", accent="#33FF00", a2="#FFB000", card="rgba(51,255,0,.04)", card_ink="#33FF00", radius="0px", border="1px solid #33FF00", shadow="none", fh="JetBrains Mono", fb="Space Mono", fx="body::after{content:'';position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 3px,rgba(51,255,0,.04) 3px 4px);z-index:999}.cursor{display:inline-block;width:10px;height:1.1em;background:#33FF00;vertical-align:text-bottom;animation:blinkc .6s steps(1) infinite}@keyframes blinkc{50%{opacity:0}}")
R[74] = dict(bg="#09090B", ink="#FAFAFA", muted="#A1A1AA", accent="#DFE104", card="#111113", card_ink="#FAFAFA", radius="0px", border="2px solid #3F3F46", shadow="none", fh="Space Grotesk", fb="Inter", fx=".marquee{overflow:hidden;white-space:nowrap;background:#DFE104;color:#000;border:2px solid #3F3F46}.marquee span{display:inline-block;animation:marq 6s linear infinite;font-weight:800;text-transform:uppercase}@keyframes marq{from{transform:translateX(0)}to{transform:translateX(-50%)}}")
R[75] = dict(bg="#FFFFFF", ink="#111827", muted="#6B7280", accent="#3B82F6", a2="#10B981", card="#FFFFFF", card_ink="#111827", radius="8px", border="1px solid #E5E7EB", shadow="none", fh="Inter", fb="Inter", fx=".btn:active{transform:scale(.97)}")
R[76] = dict(bg="#FFFBFE", ink="#1C1B1F", muted="#625B71", accent="#6750A4", card="#F3EDF7", card_ink="#1C1B1F", radius="16px", border="none", shadow="0 1px 3px rgba(0,0,0,.08)", fh="Inter", fb="Inter", fx=".btn{border-radius:999px}.chip{border-radius:999px;background:#E8DEF8;color:#1D192B}.field{border-radius:999px;background:#E7E0EC;border:none}")
R[77] = dict(bg="#FFFDF5", ink="#000000", muted="#555555", accent="#FF6B6B", a2="#FFD93D", card="#FFFFFF", card_ink="#000000", radius="0px", border="4px solid #000000", shadow="6px 6px 0 #000000", fh="Space Grotesk", fb="Inter", fx=".card{transform:rotate(-1deg)}.card:nth-child(2){transform:rotate(1.5deg)}.card:nth-child(3){transform:rotate(-.8deg)}.chip{background:#FFD93D;border:3px solid #000;border-radius:999px;box-shadow:3px 3px 0 #000}.btn:active{transform:translate(4px,4px);box-shadow:none}")
R[78] = dict(bg="#0A0A0A", ink="#FAFAFA", muted="#737373", accent="#FF3D00", card="#111111", card_ink="#FAFAFA", radius="0px", border="1px solid #262626", shadow="none", fh="Inter", fb="JetBrains Mono", fx=".cta-line{border-bottom:3px solid #FF3D00}.tag{font-family:'JetBrains Mono';font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#FF3D00}")
R[79] = dict(bg="#1C1714", ink="#E8DFD4", muted="#9C8B7A", accent="#C9A962", a2="#8B2635", card="#251E19", card_ink="#E8DFD4", radius="4px", border="1px solid #4A3F35", shadow="0 10px 24px rgba(0,0,0,.5)", fh="Cormorant Garamond", fb="Crimson Pro", fx=".overline{font-family:'Cinzel';letter-spacing:.22em;text-transform:uppercase;font-size:11px;color:#C9A962}.arch{border-radius:120px 120px 0 0}.dbrass{height:1px;background:linear-gradient(90deg,transparent,#C9A962,transparent)}")
R[80] = dict(bg="#0A0A0F", ink="#E0E0E0", muted="#6E6E85", accent="#00FF88", a2="#FF00FF", card="#12121A", card_ink="#E0E0E0", radius="0px", border="1px solid #2A2A3A", shadow="0 0 18px rgba(0,255,136,.2)", fh="Orbitron", fb="JetBrains Mono", fx=".chamfer{clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px)}body::after{content:'';position:fixed;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 3px,rgba(0,255,136,.04) 3px 4px);z-index:999}.corner{position:relative}.corner::before,.corner::after{content:'';position:absolute;width:14px;height:14px;border:2px solid #00FF88}.corner::before{top:-6px;left:-6px;border-right:none;border-bottom:none}.corner::after{bottom:-6px;right:-6px;border-left:none;border-top:none}")
R[81] = dict(bg="#030304", ink="#FFFFFF", muted="#94A3B8", accent="#F7931A", a2="#FFD600", card="#0F1115", card_ink="#FFFFFF", radius="24px", border="1px solid rgba(30,41,59,.4)", shadow="0 8px 30px rgba(0,0,0,.5)", fh="Space Grotesk", fb="Inter", fx=".btn{background:linear-gradient(90deg,#EA580C,#F7931A);box-shadow:0 0 22px rgba(247,147,26,.35)}.mono{font-family:'JetBrains Mono'}.gridbg{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:50px 50px}")
R[82] = dict(bg="#F4F1FA", ink="#332F3A", muted="#635F69", accent="#7C3AED", a2="#DB2777", card="rgba(255,255,255,.75)", card_ink="#332F3A", radius="32px", border="1px solid rgba(255,255,255,.9)", shadow="12px 12px 24px rgba(160,150,180,.25), -8px -8px 20px rgba(255,255,255,.9)", fh="Nunito", fb="DM Sans", fx=".btn{background:linear-gradient(90deg,#A78BFA,#7C3AED);border-radius:20px}.btn:active{transform:scale(.92)}.blob{position:absolute;border-radius:50%;filter:blur(50px);opacity:.25;animation:drift 9s ease-in-out infinite}@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(20px,20px)}}")
R[83] = dict(bg="#F8FAFC", ink="#0F172A", muted="#64748B", accent="#4F46E5", a2="#7C3AED", card="#FFFFFF", card_ink="#0F172A", radius="16px", border="1px solid #E2E8F0", shadow="0 4px 12px rgba(79,70,229,.08)", fh="Plus Jakarta Sans", fb="Plus Jakarta Sans", fx=".btn{background:linear-gradient(90deg,#4F46E5,#7C3AED);border-radius:12px}.skel{background:linear-gradient(90deg,#E2E8F0 25%,#F1F5F9 50%,#E2E8F0 75%);background-size:200% 100%;animation:skel 1.4s infinite}@keyframes skel{from{background-position:200% 0}to{background-position:-200% 0}}")
R[84] = dict(bg="#FDFBF7", ink="#2D2D2D", muted="#6B6B6B", accent="#FF4D4D", a2="#2D5DA1", card="#FFFFFF", card_ink="#2D2D2D", radius="15px 25px 20px 10px", border="3px solid #2D2D2D", shadow="4px 4px 0 #2D2D2D", fh="Kalam", fb="Patrick Hand", fx=".card{transform:rotate(-1deg)}.card:nth-child(2){transform:rotate(1deg)}.card:nth-child(3){transform:rotate(-.5deg)}.btn{background:#FFF9C4;border-radius:12px 18px 14px 20px}.btn:active{transform:translate(4px,4px);box-shadow:none}body{background-image:url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"200\" height=\"200\"><filter id=\"p\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"0.7\" numOctaves=\"2\"/><feColorMatrix type=\"saturate\" values=\"0\"/></filter><rect width=\"200\" height=\"200\" filter=\"url(%23p)\" opacity=\"0.05\"/></svg>')}")

# ---------------- layout archetypes (structural) ----------------
ARCH = {}
for i in range(1, 86):
    ARCH[i] = "centered"
arch_assign = {
    1:"minimal", 2:"centered", 3:"glass", 4:"brutal", 5:"poster", 6:"brutal", 7:"centered",
    8:"minimal", 9:"centered", 10:"glass", 11:"hud", 12:"centered", 13:"centered", 14:"glass",
    15:"centered", 16:"centered", 17:"minimal", 18:"minimal", 19:"centered", 20:"landing",
    21:"landing", 22:"landing", 23:"minimal", 24:"landing", 25:"landing", 26:"landing",
    27:"editorial", 28:"dashboard", 29:"dashboard", 30:"dashboard", 31:"dashboard",
    32:"dashboard", 33:"dashboard", 34:"dashboard", 35:"dashboard", 36:"dashboard",
    37:"dashboard", 38:"brutal", 39:"bento", 40:"centered", 41:"hud", 42:"centered",
    43:"chat", 44:"centered", 45:"poster", 46:"centered", 47:"poster", 48:"poster",
    49:"editorial", 50:"minimal", 51:"hud", 52:"brutal", 53:"bento", 54:"blueprint", 55:"glass",
    56:"editorial", 57:"brutal", 58:"centered", 59:"editorial", 60:"centered",
    61:"centered", 62:"centered", 63:"chat", 64:"centered", 65:"glass", 66:"editorial",
    67:"poster", 68:"editorial", 69:"poster", 70:"editorial", 71:"mobile", 72:"mobile",
    73:"terminal", 74:"poster", 75:"mobile", 76:"mobile", 77:"mobile", 78:"poster",
    79:"editorial", 80:"hud", 81:"mobile", 82:"mobile", 83:"mobile", 84:"mobile",
}
for k, v in arch_assign.items():
    ARCH[k] = v

# ---- layout variants: same archetype, different internal structure ----
# so adjacent styles are structurally distinct, not just re-skinned
V = {}
def vv(arch_map):
    for k, v in arch_map.items():
        V[k] = v

vv({1:"v1",2:"v2",3:"v1",4:"v1",5:"v2",6:"v2",7:"v1",8:"v2",9:"v2",10:"v2",11:"v1",
    12:"v2",13:"v3",14:"v2",15:"v1",16:"v2",17:"v2",18:"v3",19:"v4",20:"v1",21:"v3",
    22:"v2",23:"v1",24:"v2",25:"v1",26:"v3",27:"v3",28:"v1",29:"v2",30:"v1",31:"v3",
    32:"v1",33:"v3",34:"v2",35:"v3",36:"v1",37:"v3",38:"v1",39:"v1",40:"v2",41:"v1",
    42:"v4",43:"v1",44:"v3",45:"v3",46:"v1",47:"v1",48:"v2",49:"v2",50:"v1",51:"v2",
    52:"v2",53:"v1",54:"v1",55:"v1",56:"v1",57:"v2",58:"v4",59:"v2",60:"v2",61:"v3",62:"v1",
    63:"v2",64:"v3",65:"v2",66:"v1",67:"v3",68:"v2",69:"v1",70:"v1",71:"v1",72:"v3",
    73:"v1",74:"v2",75:"v2",76:"v3",77:"v2",78:"v1",79:"v3",80:"v2",81:"v1",82:"v2",
    83:"v3",84:"v2",85:"v2"})

# ---------------- signature components per style ----------------
COMPS = {}
default_comps = dict(
    minimal=["nav","quote","table","steps"],
    editorial=["dropcap","quote","timeline","table"],
    bento=["avatar","badges","stat","toggle"],
    brutal=["table","alerts","steps","nav"],
    dashboard=["kpi","bars","table","heatmap","alerts","breadcrumb"],
    glass=["nav","badges","avatar","pricing","toggle"],
    terminal=["term","steps","alerts","table"],
    hud=["gauge","stat","table","alerts","ticker"],
    centered=["nav","toggle","slider","avatar","badges","quote"],
    landing=["nav","pricing","stats","quote","logos","timeline"],
    chat=["chat","steps","search"],
    poster=["stat","quote","table","steps"],
    mobile=["toggle","slider","avatar","badges","steps","search"],
    blueprint=["table","steps","alerts"],
)
comp_overrides = {
    2:["toggle","slider","badges"], 9:["toggle","slider","avatar"], 16:["toggle","slider","badges"],
    21:["alerts","steps","quote"], 24:["logos","quote","stats"], 29:["heatmap","kpi"],
    30:["kpi","gauge","stat"], 31:["alerts","ticker","kpi"], 32:["breadcrumb","table","steps"],
    33:["table","kpi","bars"], 34:["table","gauge","alerts"], 35:["funnel","table","steps"],
    36:["table","kpi","bars"], 37:["gauge","table","kpi"], 43:["chat","search","steps"],
    52:["table","alerts","steps"], 54:["table","steps","alerts"], 57:["marquee","badges","quote"], 63:["chat","search"],
    73:["term","table","alerts"], 79:["dropcap","quote","timeline"], 80:["gauge","ticker","stat"],
    81:["gauge","table","badges"],
}
for k, v in comp_overrides.items():
    COMPS[k] = v

FONTS = {
    "Inter": "wght@400;600;700;800;900", "Space Grotesk": "wght@400;500;700",
    "Playfair Display": "wght@400;600;800", "DM Serif Display": "",
    "Source Serif 4": "wght@400;600", "JetBrains Mono": "wght@400;700",
    "Space Mono": "wght@400;700", "Press Start 2P": "", "VT323": "",
    "Outfit": "wght@400;700;900", "Archivo": "wght@400;700;900", "Kalam": "wght@400;700",
    "Patrick Hand": "", "Nunito": "wght@400;700;900", "Plus Jakarta Sans": "wght@400;600;800",
    "Calistoga": "", "Orbitron": "wght@400;700;900", "Cinzel": "wght@400;700",
    "Cormorant Garamond": "wght@400;600;700", "Crimson Pro": "wght@400;600",
    "Syne": "wght@400;700;800", "Chakra Petch": "wght@400;700", "Caveat": "wght@400;700",
    "Special Elite": "", "Fraunces": "wght@400;600;900", "DM Sans": "wght@400;500",
}

def parse_csv():
    rows = []
    with open(SRC, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("No") and r["No"].strip():
                rows.append(r)
    return rows

def hexpairs(s):
    out = []
    for m in re.finditer(r'#[0-9A-Fa-f]{6}', s or ""):
        pre = (s or "")[: m.start()]
        name = pre.split(",")[-1].strip().strip(":-–— ").strip()
        hexv = m.group(0).upper()
        if name and hexv not in [h for _, h in out]:
            out.append((name, hexv))
    return out

def esc(s):
    return html.escape(s or "")

def recipe_for(i):
    r = dict(DEFAULT)
    r.update(R.get(i, {}))
    return r

def font_link(r):
    fams = []
    for f in (r["fh"], r["fb"]):
        if f and f not in fams and FONTS.get(f) is not None:
            fams.append(f)
    if not fams:
        return ""
    parts = []
    for f in fams:
        w = FONTS.get(f, "")
        parts.append("family=" + f.replace(" ", "+") + (":" + w if w else ""))
    return '<link href="https://fonts.googleapis.com/css2?' + "&".join(parts) + "&display=swap" + '" rel="stylesheet">'

def css_from(r):
    return f""":root{{
--bg:{r['bg']};--ink:{r['ink']};--muted:{r['muted']};
--accent:{r['accent']};--a2:{r['a2']};
--card:{r['card']};--card-ink:{r['card_ink']};
--radius:{r['radius']};--border:{r['border']};--shadow:{r['shadow']};
--fh:'{r['fh']}';--fb:'{r['fb']}';
}}
body{{background:var(--bg);color:var(--ink);font-family:var(--fb)}}
h1,h2,h3,.fh{{font-family:var(--fh)}}
.card{{background:var(--card);color:var(--card-ink);border-radius:var(--radius);border:var(--border);box-shadow:var(--shadow)}}
.btn{{background:var(--accent);color:#fff;border-radius:max(calc(var(--radius) * .7), 6px);border:none;font-weight:700}}
.btn2{{background:transparent;color:var(--accent);border:2px solid var(--accent);border-radius:max(calc(var(--radius) * .7), 6px);font-weight:700}}
.chip{{background:var(--accent);color:#fff;border-radius:999px;font-weight:600}}
.field{{background:var(--bg);color:var(--ink);border:2px solid var(--muted);border-radius:var(--radius)}}
a{{color:var(--accent)}}
"""

# ================= component builders =================
def c_nav(r):
    return f"""<div class="navi"><b class="logo">LOGO</b><span class="nlink on">Product</span><span class="nlink">Features</span><span class="nlink">Pricing</span><span class="nlink">Docs</span><button class="btn sm">Sign up</button></div>"""

def c_toggle(r):
    return f"""<div class="ctrl-row"><span class="c-label">Notifications</span><div class="switch"><i></i></div></div>
<div class="ctrl-row"><span class="c-label">Dark mode</span><div class="switch off"><i></i></div></div>
<div class="ctrl-row"><span class="c-label">Weekly digest</span><div class="switch"><i></i></div></div>"""

def c_slider(r):
    return f"""<div class="ctrl-row col"><span class="c-label">Volume &mdash; 70%</span><input type="range" min="0" max="100" value="70" class="range"></div>
<div class="ctrl-row col"><span class="c-label">Brightness &mdash; 45%</span><input type="range" min="0" max="100" value="45" class="range"></div>"""

def c_avatar(r):
    return f"""<div class="avs"><span>AL</span><span>RK</span><span>MJ</span><span>+12</span></div>
<p class="cmut">48 team members online now</p>"""

def c_badges(r):
    return f"""<div class="kw"><span class="chip">Pro</span><span class="chip2">New</span><span class="chip2">Beta</span><span class="chip2">Popular</span><span class="chip2">AI</span></div>"""

def c_pricing(r):
    return f"""<div class="price-row">
<div class="card p-card"><h3>Starter</h3><div class="p-price">$9<span>/mo</span></div><ul class="p-list"><li>&#10003; 3 projects</li><li>&#10003; 1 GB storage</li><li>&#10003; Community support</li></ul><button class="btn2 wide">Choose</button></div>
<div class="card p-card hot"><h3>Pro</h3><div class="p-price">$29<span>/mo</span></div><ul class="p-list"><li>&#10003; Unlimited projects</li><li>&#10003; 50 GB storage</li><li>&#10003; Priority support</li></ul><button class="btn wide">Choose</button></div>
<div class="card p-card"><h3>Team</h3><div class="p-price">$99<span>/mo</span></div><ul class="p-list"><li>&#10003; Everything in Pro</li><li>&#10003; SSO &amp; audit logs</li><li>&#10003; Dedicated manager</li></ul><button class="btn2 wide">Choose</button></div>
</div>"""

def c_table(r):
    rows = [("Acme Corp","Enterprise","$12,400","Active"),("Northwind","Startup","$2,150","Trial"),
            ("Vertex Lab","Mid-market","$6,800","Active"),("Luma Inc","Enterprise","$24,900","Active"),
            ("Halcyon","Startup","$980","Churned")]
    trs = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td><span class="okchip">{d}</span></td></tr>' for a,b,c,d in rows)
    return f"""<div class="table-wrap"><table class="tbl"><thead><tr><th>Company</th><th>Segment</th><th>MRR</th><th>Status</th></tr></thead><tbody>{trs}</tbody></table></div>"""

def c_timeline(r):
    items = [("Q1","Research & discovery"),("Q2","MVP build"),("Q3","Private beta"),("Q4","Public launch")]
    lis = "".join(f'<div class="tl-item"><span class="tl-dot"></span><div><b>{a}</b><p>{b}</p></div></div>' for a,b in items)
    return f"""<div class="tl">{lis}</div>"""

def c_stat(r):
    return f"""<div class="stat-band">
<div><b>4,800+</b><span>teams</span></div><div><b>99.99%</b><span>uptime</span></div><div><b>212%</b><span>growth</span></div><div><b>4.9/5</b><span>rating</span></div>
</div>"""

def c_quote(r):
    return f"""<blockquote class="bigq">&#8220;The best part is how invisible it gets &mdash; the design does its job without ever showing off.&#8221;</blockquote><p class="cmut">— Jamie R., Head of Product</p>"""

def c_chat(r):
    return f"""<div class="chatbox">
<div class="chat-h">AI Assistant <span class="dot small"></span></div>
<div class="chat-body">
<div class="bubble-a">Halo! Ada yang bisa saya bantu hari ini?</div>
<div class="bubble-u">Ringkasin insight minggu ini dong</div>
<div class="bubble-a">Tentu. Tiga hal utama: <b>konversi naik 12%</b>, churn turun ke 1.08%, dan fitur baru dipakai 64% pengguna aktif.</div>
<div class="typing"><span></span><span></span><span></span></div>
</div>
<div class="chat-in"><input class="field" placeholder="Tulis pesan..."><button class="btn sm">Kirim</button></div>
</div>"""

def c_term(r):
    return f"""<div class="term">
<div class="term-bar"><span class="t-dot r"></span><span class="t-dot y"></span><span class="t-dot g"></span> bash &mdash; 80x24</div>
<div class="term-body"><span class="pr">user@dev</span>:~$ npm run build<br>
<span class="dim">&gt; app@1.0.0 build<br>&gt; vite build</span><br>
<span class="dim">vite v5.0.0 building for production...</span><br>
&#10003; 42 modules transformed.<br>
<span class="dim">dist/index.html&nbsp;&nbsp;&nbsp;&nbsp;2.13 kB<br>dist/assets/app.js&nbsp;148.6 kB</span><br>
<span class="pr">user@dev</span>:~$ <span class="cursor"></span></div>
</div>"""

def c_alerts(r):
    return f"""<div class="al info"><b>&#8505; Info</b><span>Deploy finished in 42s.</span></div>
<div class="al warn"><b>&#9888; Warning</b><span>API rate limit at 85%.</span></div>
<div class="al err"><b>&#10007; Error</b><span>Webhook failed &mdash; retrying in 30s.</span></div>
<div class="al ok"><b>&#10003; Success</b><span>Backup completed.</span></div>"""

def c_breadcrumb(r):
    return f"""<div class="crumb">Dashboard <span>&#47;</span> Analytics <span>&#47;</span> <b>Revenue</b></div>"""

def c_steps(r):
    steps = [("01","Define","Scope the problem and goals"),("02","Design","Explore directions fast"),("03","Build","Ship incrementally"),("04","Learn","Measure and iterate")]
    s = "".join(f'<div class="step"><span class="s-num">{a}</span><b>{b}</b><p>{c}</p></div>' for a,b,c in steps)
    return f"""<div class="steps">{s}</div>"""

def c_search(r):
    return f"""<div class="searchbar"><span>&#128269;</span><input class="field" placeholder="Search projects, people, docs..."><kbd>Ctrl K</kbd></div>"""

def c_heatmap(r):
    import random
    random.seed(7)
    cells = []
    for row in range(6):
        for col in range(14):
            v = random.random()
            if v < .35: c = "rgba(239,68,68,.18)"
            elif v < .6: c = "rgba(239,68,68,.45)"
            elif v < .85: c = "rgba(239,68,68,.75)"
            else: c = "#EF4444"
            cells.append(f'<i style="background:{c}"></i>')
    return f"""<div class="heat">{"".join(cells)}</div>"""

def c_funnel(r):
    stages = [("Visitors", 100), ("Signups", 62), ("Activated", 41), ("Paid", 18)]
    bars = "".join(f'<div class="fn-row"><span>{a}</span><div class="fn-track"><i style="width:{b}%"></i></div><b>{b}%</b></div>' for a, b in stages)
    return f"""<div class="funnel">{bars}</div>"""

def c_gauge(r):
    return f"""<div style="display:flex;gap:26px;justify-content:center;flex-wrap:wrap">
<div class="gauge-wrap"><div class="gauge" style="background:conic-gradient(var(--accent) 0 72%, var(--card) 72% 100%)"><i>72%</i></div><span class="cmut">Quota</span></div>
<div class="gauge-wrap"><div class="gauge" style="background:conic-gradient(var(--a2) 0 48%, var(--card) 48% 100%)"><i>48%</i></div><span class="cmut">Forecast</span></div>
<div class="gauge-wrap"><div class="gauge" style="background:conic-gradient(#EF4444 0 91%, var(--card) 91% 100%)"><i>91%</i></div><span class="cmut">Utilization</span></div>
</div>"""

def c_ticker(r):
    return f"""<div class="tick"><span>SYSTEM ONLINE &#8226; LATENCY 42ms &#8226; UPTIME 99.98% &#8226; NODES 128/128 &#8226; THREAT LEVEL NOMINAL &#8226; QUEUE 0.02s &#8226; </span></div>"""

def c_marquee(r):
    return f"""<div class="marquee"><span>NEW DROP &#9733; 50% OFF &#9733; LIMITED EDITION &#9733; FREE SHIPPING &#9733; </span></div>"""

def c_dropcap(r):
    return f"""<div class="article-body"><p class="dropcap">Typography is the voice of the interface. It whispers hierarchy, shouts emphasis, and quietly sets the mood before a single word is read. In great editorial design, every paragraph earns its measure and every headline earns its weight.</p>
<p>Structure arrives through contrast: tight headlines against airy body text, rule lines that divide without shouting, and margins that let content breathe. The grid is the scaffolding; the type is the building.</p></div>"""

def c_logos(r):
    return f"""<div class="logo-strip"><span>ACME</span><span>NORTHWIND</span><span>VERTEX</span><span>LUMA</span><span>HALCYON</span><span>ORBITAL</span></div>"""

COMPONENTS = {
    "nav": c_nav, "toggle": c_toggle, "slider": c_slider, "avatar": c_avatar,
    "badges": c_badges, "pricing": c_pricing, "table": c_table, "timeline": c_timeline,
    "stat": c_stat, "quote": c_quote, "chat": c_chat, "term": c_term,
    "alerts": c_alerts, "breadcrumb": c_breadcrumb, "steps": c_steps, "search": c_search,
    "heatmap": c_heatmap, "funnel": c_funnel, "gauge": c_gauge, "ticker": c_ticker,
    "marquee": c_marquee, "dropcap": c_dropcap, "logos": c_logos,
}
COMP_LABEL = {
    "nav":"Navigation", "toggle":"Toggles & Controls", "slider":"Sliders", "avatar":"Avatars",
    "badges":"Badges & Chips", "pricing":"Pricing", "table":"Data Table", "timeline":"Timeline",
    "stat":"Stat Band", "quote":"Testimonial Quote", "chat":"Conversation", "term":"Terminal",
    "alerts":"Alerts & States", "breadcrumb":"Breadcrumbs", "steps":"Process Steps",
    "search":"Search", "heatmap":"Heatmap", "funnel":"Funnel", "gauge":"Gauges",
    "ticker":"Status Ticker", "marquee":"Marquee", "dropcap":"Editorial Body", "logos":"Logo Strip",
}

# ================= archetype builders =================
ARCH_NOTE = {
    "minimal": ("sparse single-column", {"v1":"single column", "v2":"split panel", "v3":"two-column cards"}),
    "editorial": ("magazine grid", {"v1":"masthead + article", "v2":"feature spread", "v3":"narrative timeline"}),
    "bento": ("modular asymmetric grid", {}),
    "brutal": ("raw structural layout", {"v1":"statement + stat blocks", "v2":"raw table + marquee"}),
    "dashboard": ("sidebar + dense data", {"v1":"sidebar + KPI + bars", "v2":"top bar + table + spark", "v3":"widget grid + gauges"}),
    "glass": ("floating frosted panels", {"v1":"pill nav + hero + cards", "v2":"full panel + feature list"}),
    "terminal": ("command-line surface", {}),
    "hud": ("heads-up display", {"v1":"4-panel matrix", "v2":"3-panel + ticker"}),
    "centered": ("balanced centered composition", {"v1":"3-card grid", "v2":"split hero + controls", "v3":"stacked sections", "v4":"alternating zigzag"}),
    "landing": ("conversion-focused page", {"v1":"hero + mockup + features", "v2":"center hero + pricing", "v3":"lead form + trust"}),
    "chat": ("conversational surface", {"v1":"assistant chat", "v2":"voice-first chat"}),
    "poster": ("typographic statement", {"v1":"giant stack type", "v2":"number + meta poster", "v3":"split type blocks"}),
    "mobile": ("touch-first phone layout", {"v1":"wallet home", "v2":"list / conversation", "v3":"stats & settings"}),
    "blueprint": ("drafting sheet grid", {"v1":"sheet + dimension callouts"}),
}
def hero_base(sid, row, r, arch, variant):
    name = row["Style Category"].strip()
    stype = row["Type"].strip()
    kws = [k.strip() for k in (row.get("Keywords", "") or "").split(",") if k.strip()]
    tagline = ", ".join(kws[:8]) or "—"
    base_note, vnotes = ARCH_NOTE[arch]
    note = vnotes.get(variant, base_note) if variant else base_note
    return f"""<section class="hero">
<span class="tag">{esc(stype)} &middot; {esc((row.get('Era/Origin','') or '').strip())} &middot; Complexity: {esc((row.get('Complexity','') or '').strip())} &middot; <b>layout: {note}</b></span>
<h1>Style {sid:02d}: {esc(name)}</h1>
<p>{esc(tagline)}</p>
<div class="badges">
<span class="badge">Light: {esc((row.get('Light Mode','') or '').strip()[:12] or '—')}</span>
<span class="badge">Dark: {esc((row.get('Dark Mode','') or '').strip()[:12] or '—')}</span>
<span class="badge">Perf: {esc((row.get('Performance','') or '').strip()[:14] or '—')}</span>
<span class="badge">A11y: {esc((row.get('Accessibility','') or '').strip()[:18] or '—')}</span>
<span class="badge">Conversion: {esc((row.get('Conversion-Focused','') or '').strip()[:14] or '—')}</span>
</div>
</section>"""

def arch_minimal_v1(row, r):
    return hero_base(int(row["No"]), row, r, "minimal", "v1") + """
<section class="single-col">
<p class="lead">One column. One message. Every element earns its place — the whitespace is a feature, not an absence.</p>
<div class="rule"></div>
<div class="two-col-text">
<div><h3>Clarity first</h3><p>Hierarchy from type weight and spacing alone. No decoration, no noise — just signal.</p></div>
<div><h3>Speed by design</h3><p>A page this light loads instantly, reads in seconds, and leaves nothing to decode.</p></div>
</div>
<div class="cta-row"><button class="btn">Get started</button><a href="#">Learn more &#8594;</a></div>
</section>"""

def arch_minimal_v2(row, r):
    return hero_base(int(row["No"]), row, r, "minimal", "v2") + """
<section class="split-panel">
<div class="sp-left">
<p class="lead">Less chrome.<br>More signal.</p>
<p class="sp-sub">A split composition: the message on one side, the essentials on the other. Nothing competes.</p>
<div class="cta-row"><button class="btn">Primary</button><a href="#">Docs &#8594;</a></div>
</div>
<div class="sp-right">
<div class="sp-card"><b>Uptime</b><span class="big">99.99%</span></div>
<div class="sp-card"><b>Latency</b><span class="big">42ms</span></div>
<div class="sp-card"><b>Teams</b><span class="big">4,800+</span></div>
</div>
</section>"""

def arch_minimal_v3(row, r):
    return hero_base(int(row["No"]), row, r, "minimal", "v3") + """
<section class="m3-wrap">
<div class="m3-card"><span class="m3-no">01</span><h3>Define</h3><p>One problem, clearly stated, before any pixels move.</p></div>
<div class="m3-card"><span class="m3-no">02</span><h3>Refine</h3><p>Reduce until removing more would break it.</p></div>
<div class="m3-card"><span class="m3-no">03</span><h3>Deliver</h3><p>Ship something so obvious it feels inevitable.</p></div>
</section>"""

def arch_editorial_v1(row, r):
    return hero_base(int(row["No"]), row, r, "editorial", "v1") + """
<div class="masthead"><span>THE DAILY LAYOUT</span><span>Vol. 85 &mdash; Design Review</span></div>
<div class="article-head">
<h2 class="art-h">Why style systems fail &mdash; and the ones that don't</h2>
<div class="byline">By A. Designer &middot; 8 min read &middot; Filed under Interface</div>
</div>
<div class="art-cols">
<div class="art-main">
<p class="dropcap">Every system starts with good intentions: tokens, components, a shared language. And yet most die quietly under the weight of exceptions nobody documented.</p>
<p>The survivors share one trait — they treat the grid as a contract. Columns are not suggestions; spacing is not a feeling. What looks like restraint is actually the discipline of saying no.</p>
</div>
<aside class="art-side">
<div class="pullq">&#8220;Restraint is the discipline of saying no.&#8221;</div>
<div class="side-card"><b>Related</b><p>The return of the drop cap<br>Grids that breathe</p></div>
</aside>
</div>"""

def arch_editorial_v2(row, r):
    return hero_base(int(row["No"]), row, r, "editorial", "v2") + """
<div class="spread">
<div class="spread-visual"><div class="spread-art"><span>VOL.84</span><h2 class="spread-h">The<br>Feature<br>Spread</h2></div></div>
<div class="spread-body">
<span class="spread-kicker">COVER STORY</span>
<h3 class="spread-sub">One image, one headline, one story — the rest of the page serves it.</h3>
<p class="spread-p">Editorial layout gives the hero full runway. The copy below is set in a measure built for reading: 60-70 characters, generous leading, and a quiet grid underneath.</p>
<div class="spread-meta"><span>PHOTOGRAPHY</span><span>ESSAY</span><span>6 MIN</span></div>
</div>
</div>"""

def arch_editorial_v3(row, r):
    return hero_base(int(row["No"]), row, r, "editorial", "v3") + """
<div class="chapter-block">
<div class="chapter">
<div class="ch-num">I.</div>
<div class="ch-body"><h3>The origin</h3><p>Every system starts with good intentions: tokens, components, a shared language.</p></div>
</div>
<div class="chapter">
<div class="ch-num">II.</div>
<div class="ch-body"><h3>The drift</h3><p>Exceptions accumulate, docs go stale, and the grid quietly stops being a contract.</p></div>
</div>
<div class="chapter">
<div class="ch-num">III.</div>
<div class="ch-body"><h3>The return</h3><p>What looks like restraint is the discipline of saying no — over and over again.</p></div>
</div>
</div>"""

def arch_bento(row, r):
    return hero_base(int(row["No"]), row, r, "bento", "") + """
<section class="bento">
<div class="b-card b-lg"><div class="b-ico">&#128200;</div><h3>Revenue up 212%</h3><p>Quarterly momentum across all segments, driven by activation improvements.</p><div class="spark">▂▄▆█▅▃▇▆█</div></div>
<div class="b-card"><div class="b-ico">&#128101;</div><h3>4,800+ teams</h3><p>and counting.</p></div>
<div class="b-card b-tall"><div class="b-ico">&#128274;</div><h3>Private by default</h3><p>Zero tracking. Full export.</p></div>
<div class="b-card"><div class="b-ico">&#9889;</div><h3>Fast</h3><p>42ms median response.</p></div>
<div class="b-card b-wide"><div class="b-ico">&#127793;</div><h3>Sustainable</h3><p>Carbon-aware scheduling cuts our footprint 38%.</p></div>
</section>"""

def arch_brutal_v1(row, r):
    return hero_base(int(row["No"]), row, r, "brutal", "v1") + """
<section class="brutal-block">
<div class="brutal-left">
<h2 class="brut-h">NO<br>FRILLS.<br>JUST<br>WORKS.</h2>
<p>Raw borders, hard shadows, zero gradient. This is the web without makeup.</p>
<button class="btn brutal-btn">DO THE THING</button>
</div>
<div class="brutal-right">
<div class="brutal-card"><b>MEMBERS</b><span class="big">48,201</span></div>
<div class="brutal-card"><b>SPEED</b><span class="big">0.4s</span></div>
<div class="brutal-card"><b>UPTIME</b><span class="big">99.9%</span></div>
<div class="brutal-list"><div class="brow"><span>01</span> Hard borders</div><div class="brow"><span>02</span> Offset shadows</div><div class="brow"><span>03</span> No gradients</div><div class="brow"><span>04</span> Instant states</div></div>
</div>
</section>"""

def arch_brutal_v2(row, r):
    return hero_base(int(row["No"]), row, r, "brutal", "v2") + """
<section class="raw-marquee"><div class="marquee"><span>FREE THE GRID &#9733; NO BORDERS WERE HARMED &#9733; RAW IS LAW &#9733; </span></div></section>
<section class="raw-grid">
<div class="raw-list">
<div class="raw-row"><span class="rw-idx">01</span><b>PRICING</b><span>$0 — $99</span></div>
<div class="raw-row"><span class="rw-idx">02</span><b>SUPPORT</b><span>24/7 CHAT</span></div>
<div class="raw-row"><span class="rw-idx">03</span><b>SHIPPING</b><span>FREE WORLDWIDE</span></div>
<div class="raw-row"><span class="rw-idx">04</span><b>RETURNS</b><span>60 DAYS</span></div>
<div class="raw-row"><span class="rw-idx">05</span><b>LICENSE</b><span>MIT</span></div>
</div>
<div class="raw-card">
<div class="raw-stat"><b class="big2">48K</b><span>USERS</span></div>
<div class="raw-stat"><b class="big2">0.4s</b><span>LOAD</span></div>
<div class="raw-stat"><b class="big2">99.9%</b><span>UPTIME</span></div>
<button class="btn brutal-btn wide2">GET IT NOW</button>
</div>
</section>"""

def arch_dashboard_v1(row, r):
    bars = [42, 68, 55, 83, 61, 90, 47, 74]
    b = "".join(f'<i style="height:{h}%"></i>' for h in bars)
    return hero_base(int(row["No"]), row, r, "dashboard", "v1") + """
<section class="dash">
<aside class="dash-side">
<div class="dash-logo">ACME&#174;</div>
<div class="dash-item on">&#9632; Overview</div>
<div class="dash-item">&#9632; Analytics</div>
<div class="dash-item">&#9632; Reports</div>
<div class="dash-item">&#9632; Team</div>
<div class="dash-item">&#9632; Settings</div>
<div class="dash-user">JS <span>Jordan S.</span></div>
</aside>
<div class="dash-main">
<div class="crumb">Overview <span>&#47;</span> This week</div>
<div class="kpi-row">
<div class="kpi"><div class="l">Revenue</div><div class="v">$128.4K</div><div class="d up">&#9650; +12.4%</div></div>
<div class="kpi"><div class="l">Users</div><div class="v">48,201</div><div class="d up">&#9650; +8.1%</div></div>
<div class="kpi"><div class="l">Conv. Rate</div><div class="v">3.42%</div><div class="d down">&#9660; -0.6%</div></div>
<div class="kpi"><div class="l">Churn</div><div class="v">1.08%</div><div class="d up">&#9650; -0.2%</div></div>
</div>
<div class="bars">{b}</div>
</div>
</section>"""

def arch_dashboard_v2(row, r):
    return hero_base(int(row["No"]), row, r, "dashboard", "v2") + """
<section class="d2">
<div class="d2-top">
<div class="d2-title"><b>Analytics</b><span class="d2-range">Last 30 days &#9662;</span></div>
<div class="d2-actions"><button class="btn sm">Export</button><button class="btn2 sm">Filter</button></div>
</div>
<div class="d2-kpis">
<div class="kpi"><div class="l">Sessions</div><div class="v">284K</div><div class="sparkline">▁▂▃▅▆▇▆▅▆▇</div></div>
<div class="kpi"><div class="l">Bounce</div><div class="v">31.2%</div><div class="sparkline">▇▆▅▄▅▄▃▃▂▃</div></div>
<div class="kpi"><div class="l">Page/sess</div><div class="v">4.6</div><div class="sparkline">▂▃▅▄▆▅▇▆▇▆</div></div>
</div>
<div class="d2-table">
<div class="table-wrap"><table class="tbl">
<thead><tr><th>Page</th><th>Views</th><th>Avg time</th><th>Trend</th></tr></thead>
<tbody>
<tr><td>/pricing</td><td>48,201</td><td>3:42</td><td class="up">&#9650; +12%</td></tr>
<tr><td>/features</td><td>36,908</td><td>4:11</td><td class="up">&#9650; +8%</td></tr>
<tr><td>/docs</td><td>21,344</td><td>6:02</td><td class="down">&#9660; -3%</td></tr>
<tr><td>/blog</td><td>17,820</td><td>2:58</td><td class="up">&#9650; +21%</td></tr>
</tbody></table></div>
</div>
</section>"""

def arch_dashboard_v3(row, r):
    return hero_base(int(row["No"]), row, r, "dashboard", "v3") + """
<section class="d3">
<div class="d3-grid">
<div class="d3-widget"><span class="d3-tag">REVENUE</span><div class="d3-num">$128.4K</div><div class="d3-delta up">&#9650; +12.4%</div><div class="bars mini"><i style="height:40%"></i><i style="height:65%"></i><i style="height:50%"></i><i style="height:80%"></i><i style="height:95%"></i></div></div>
<div class="d3-widget"><span class="d3-tag">FORECAST</span><div class="gauge-wrap"><div class="gauge" style="background:conic-gradient(var(--accent) 0 72%, var(--bg) 72% 100%)"><i>72%</i></div></div></div>
<div class="d3-widget"><span class="d3-tag">ALERTS</span>
<div class="al info"><b>&#8505; Info</b><span>Deploy finished.</span></div>
<div class="al warn"><b>&#9888; Warn</b><span>Rate limit 85%.</span></div>
<div class="al err"><b>&#10007; Error</b><span>Webhook retrying.</span></div>
</div>
<div class="d3-widget"><span class="d3-tag">TOP SEGMENT</span><div class="d3-seg"><b>Enterprise</b><span>38% of MRR</span></div><div class="progress"><i style="width:38%"></i></div></div>
</div>
</section>"""

def arch_glass_v1(row, r):
    return hero_base(int(row["No"]), row, r, "glass", "v1") + """
<section class="glass-wrap">
<nav class="glass-nav glass"><b>LUMA</b><span>Product</span><span>Pricing</span><span>About</span><button class="btn sm">Launch</button></nav>
<div class="glass-hero glass"><span class="tag">Floating &middot; Blurred &middot; Layered</span>
<h2>Light as air,<br>solid as steel.</h2>
<p>Frosted panels float above a vivid backdrop. Depth comes from blur, not borders.</p>
<div class="cta-row"><button class="btn">Explore</button><button class="btn2">Watch demo</button></div></div>
<div class="glass-cards">
<div class="glass card"><h3>&#128274; Secure</h3><p>Encrypted end-to-end, always.</p></div>
<div class="glass card"><h3>&#9889; Instant</h3><p>Interactions feel weightless.</p></div>
<div class="glass card"><h3>&#128200; Clear</h3><p>Data without the clutter.</p></div>
</div>
</section>"""

def arch_glass_v2(row, r):
    return hero_base(int(row["No"]), row, r, "glass", "v2") + """
<section class="glass-wrap">
<div class="glass-full glass">
<div class="gf-left"><span class="tag">TRANSPARENT BY DESIGN</span>
<h2>One panel.<br>Everything inside.</h2>
<p>A single frosted surface carries the whole composition — nav, content, and action in one continuous plane.</p></div>
<div class="gf-right">
<div class="gf-row"><span>&#10003;</span><div><b>Blur layers</b><p>backdrop-filter does the heavy lifting</p></div></div>
<div class="gf-row"><span>&#10003;</span><div><b>Hairline borders</b><p>1px of light defines every edge</p></div></div>
<div class="gf-row"><span>&#10003;</span><div><b>Vibrant backdrops</b><p>color shows through the frost</p></div></div>
</div>
</div>
<div class="glass-chips"><span class="chip">Glass</span><span class="chip2 glass">Translucent</span><span class="chip2 glass">Blur 18px</span><span class="chip2 glass">Layered</span></div>
</section>"""

def arch_terminal(row, r):
    return hero_base(int(row["No"]), row, r, "terminal", "") + """
<section class="term-section">
<div class="term big">
<div class="term-bar"><span class="t-dot r"></span><span class="t-dot y"></span><span class="t-dot g"></span> zsh &mdash; 100x30</div>
<div class="term-body">
<span class="dim">[ OK ] Loading kernel modules.................... done</span><br>
<span class="dim">[ OK ] Mounting /dev/design........................ done</span><br>
<span class="dim">[ OK ] Starting UI daemon........................... done</span><br>
<span class="pr">user@machine</span>:~$ ls ./components<br>
<span class="dim">toggles&nbsp;&nbsp;sliders&nbsp;&nbsp;tables&nbsp;&nbsp;alerts&nbsp;&nbsp;gauges&nbsp;&nbsp;funnels</span><br>
<span class="pr">user@machine</span>:~$ ./deploy --env=prod<br>
<span class="dim">&gt; building bundle ................... [#####---] 68%</span><br>
<span class="dim">&gt; upload ............................ [#######-] 87%</span><br>
&#10003; deploy complete in 42.3s — <span class="dim">https://app.example.com</span><br>
<span class="pr">user@machine</span>:~$ <span class="cursor"></span>
</div>
</div>
</section>"""

def arch_hud_v1(row, r):
    return hero_base(int(row["No"]), row, r, "hud", "v1") + """
<section class="hud-wrap">
<div class="hud-status"><span>SYS.ONLINE</span><span>LAT 42ms</span><span>NODES 128</span><span class="pulse">&#9679; SECURE</span></div>
<div class="hud-grid">
<div class="hud-panel corner chamfer"><span class="hud-tag">// POWER CORE</span><div class="gauge" style="background:conic-gradient(var(--accent) 0 72%, rgba(255,255,255,.06) 72% 100%)"><i>72%</i></div></div>
<div class="hud-panel corner chamfer"><span class="hud-tag">// THROUGHPUT</span><div class="hud-bars"><i style="height:45%"></i><i style="height:70%"></i><i style="height:55%"></i><i style="height:90%"></i><i style="height:62%"></i><i style="height:80%"></i></div></div>
<div class="hud-panel corner chamfer"><span class="hud-tag">// EVENT LOG</span><div class="hud-log"><span class="dim">&gt; 14:02:11 auth ok node-07</span><br><span class="dim">&gt; 14:02:13 sync done 42KB</span><br><span class="dim">&gt; 14:02:16 alert low mem</span><br><span class="dim">&gt; 14:02:19 realloc ok</span></div></div>
<div class="hud-panel corner chamfer"><span class="hud-tag">// STATUS</span><div class="hud-stat"><b>99.98%</b><span>uptime</span></div><div class="hud-stat"><b>128</b><span>nodes</span></div><div class="hud-stat"><b>0</b><span>incidents</span></div></div>
</div>
<div class="tick"><span>SCAN COMPLETE &#8226; 6,204 ASSETS &#8226; 0 VULNERABILITIES &#8226; NEXT SWEEP IN 60s &#8226; </span></div>
</section>"""

def arch_hud_v2(row, r):
    return hero_base(int(row["No"]), row, r, "hud", "v2") + """
<section class="hud-wrap">
<div class="hud-status"><span>MAIN.BUS</span><span>PWR 92%</span><span class="pulse">&#9679; LINK UP</span></div>
<div class="hud-row3">
<div class="hud-panel corner chamfer b"><span class="hud-tag">// TELEMETRY</span><div class="hud-bars tall"><i style="height:30%"></i><i style="height:55%"></i><i style="height:45%"></i><i style="height:75%"></i><i style="height:60%"></i><i style="height:88%"></i><i style="height:52%"></i><i style="height:96%"></i></div></div>
<div class="hud-panel corner chamfer b"><span class="hud-tag">// SYSTEMS</span>
<div class="hud-sys"><span class="hud-dot on"></span> Navigation <b>OK</b></div>
<div class="hud-sys"><span class="hud-dot warn"></span> Comms <b>88%</b></div>
<div class="hud-sys"><span class="hud-dot on"></span> Life support <b>OK</b></div>
<div class="hud-sys"><span class="hud-dot err"></span> Shield <b>RECHARGE</b></div>
</div>
<div class="hud-panel corner chamfer b"><span class="hud-tag">// CARGO</span><div class="hud-stat"><b>12.4T</b><span>of 20T</span></div><div class="progress"><i style="width:62%"></i></div></div>
</div>
<div class="tick"><span>ORBITAL INSERTION IN 04:12 &#8226; DRIFT 0.02&#176; &#8226; FUEL 62% &#8226; ALL HANDS TO STATIONS &#8226; </span></div>
</section>"""

def arch_centered_v1(row, r):
    return hero_base(int(row["No"]), row, r, "centered", "v1") + """
<section class="feature-grid">
<div class="card"><div class="ico">&#9881;</div><h3>Configurable</h3><p>Every knob exposed, defaults sane, opinions optional.</p></div>
<div class="card"><div class="ico">&#9889;</div><h3>Instant</h3><p>Renders fast, feels faster. No jank, no placeholder soup.</p></div>
<div class="card"><div class="ico">&#128274;</div><h3>Private</h3><p>Data stays yours. Zero tracking, full export.</p></div>
</section>"""

def arch_centered_v2(row, r):
    return hero_base(int(row["No"]), row, r, "centered", "v2") + """
<section class="c2">
<div class="c2-left">
<span class="tag">HANDS-ON</span>
<h2 class="c2-h">Tune it<br>your way.</h2>
<p class="c2-p">A split composition with the pitch on the left and the controls on the right — form follows function.</p>
<div class="cta-row"><button class="btn">Try it</button><button class="btn2">How it works</button></div>
</div>
<div class="c2-right">
<div class="c2-controls card">
<div class="ctrl-row"><span class="c-label">Notifications</span><div class="switch"><i></i></div></div>
<div class="ctrl-row"><span class="c-label">Dark mode</span><div class="switch off"><i></i></div></div>
<div class="ctrl-row col"><span class="c-label">Volume — 70%</span><input type="range" min="0" max="100" value="70" class="range"></div>
</div>
</div>
</section>"""

def arch_centered_v3(row, r):
    return hero_base(int(row["No"]), row, r, "centered", "v3") + """
<section class="c3">
<div class="c3-hero"><span class="tag">ONE THING AT A TIME</span><h2 class="c3-h">Stacked. Focused.</h2><p class="c3-p">Sections build downward like paragraphs — each one earning the next.</p></div>
<div class="c3-block card"><div class="ico">&#128200;</div><div><h3>Measure everything</h3><p>Real numbers, real decisions. No vanity metrics, no noise.</p></div></div>
<div class="c3-block card"><div class="ico">&#127919;</div><div><h3>Ship the boring parts</h3><p>Reliability is a feature. Downtime is a bug.</p></div></div>
<div class="c3-block card"><div class="ico">&#128161;</div><div><h3>Keep the spark</h3><p>Small wins compound. Celebrate the 1% days.</p></div></div>
</section>"""

def arch_centered_v4(row, r):
    return hero_base(int(row["No"]), row, r, "centered", "v4") + """
<section class="c4">
<div class="c4-row">
<div class="c4-visual"><div class="c4-art">&#127807;</div></div>
<div class="c4-text"><h3>Grow organically</h3><p>Natural curves, living colors — motion that follows the seasons, not the fads.</p></div>
</div>
<div class="c4-row flip">
<div class="c4-visual"><div class="c4-art">&#127793;</div></div>
<div class="c4-text"><h3>Stay grounded</h3><p>Earthy materials and calm surfaces keep the product feeling human.</p></div>
</div>
<div class="c4-row">
<div class="c4-visual"><div class="c4-art">&#128154;</div></div>
<div class="c4-text"><h3>Breathe</h3><p>Whitespace is the rhythm section — it makes the notes matter.</p></div>
</div>
</section>"""

def arch_landing_v1(row, r):
    return hero_base(int(row["No"]), row, r, "landing", "v1") + """
<section class="l-hero">
<div class="l-left">
<span class="tag">&#127775; New: AI copilot is live</span>
<h2 class="l-h">Ship calmer.<br>Grow faster.</h2>
<p class="l-p">The workspace that gets out of your way — plan, build, and launch without the busywork.</p>
<div class="cta-row"><button class="btn">Start free trial</button><button class="btn2">&#9654; Watch demo</button></div>
<div class="mini-proof">&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 from 2,300+ reviews</div>
</div>
<div class="l-right">
<div class="mock"><div class="mock-bar"><span></span><span></span><span></span></div>
<div class="mock-body"><div class="mock-line w70"></div><div class="mock-line w90"></div><div class="mock-line w55"></div><div class="mock-line w80"></div><div class="mock-block"></div></div></div>
</div>
</section>
<section class="feature-grid">
<div class="card"><div class="ico">&#128101;</div><h3>Trusted by teams</h3><p>From two-person startups to public companies.</p></div>
<div class="card"><div class="ico">&#127942;</div><h3>Proven results</h3><p>+212% activation in 90 days across 4,800+ teams.</p></div>
<div class="card"><div class="ico">&#128274;</div><h3>Enterprise grade</h3><p>SOC 2 Type II, SSO, region pinning, 99.99% SLA.</p></div>
</section>"""

def arch_landing_v2(row, r):
    return hero_base(int(row["No"]), row, r, "landing", "v2") + """
<section class="l2-hero">
<span class="tag">SIMPLE PRICING</span>
<h2 class="l2-h">One workspace.<br>Every size of team.</h2>
<p class="l2-p">No per-seat tricks. Pick a plan, invite everyone, upgrade when you're ready.</p>
<div class="cta-row center"><button class="btn">Start for free</button><button class="btn2">Talk to sales</button></div>
</section>
<section class="price-row">
<div class="card p-card"><h3>Starter</h3><div class="p-price">$9<span>/mo</span></div><ul class="p-list"><li>&#10003; 3 projects</li><li>&#10003; 1 GB storage</li><li>&#10003; Community support</li></ul><button class="btn2 wide">Choose</button></div>
<div class="card p-card hot"><h3>Pro</h3><div class="p-price">$29<span>/mo</span></div><ul class="p-list"><li>&#10003; Unlimited projects</li><li>&#10003; 50 GB storage</li><li>&#10003; Priority support</li></ul><button class="btn wide">Choose</button></div>
<div class="card p-card"><h3>Team</h3><div class="p-price">$99<span>/mo</span></div><ul class="p-list"><li>&#10003; Everything in Pro</li><li>&#10003; SSO &amp; audit logs</li><li>&#10003; Dedicated manager</li></ul><button class="btn2 wide">Choose</button></div>
</section>"""

def arch_landing_v3(row, r):
    return hero_base(int(row["No"]), row, r, "landing", "v3") + """
<section class="l3">
<div class="l3-form card">
<span class="tag">GET STARTED IN 2 MINUTES</span>
<h3 class="l3-h">Claim your workspace</h3>
<div class="form-stack">
<input class="field" placeholder="Work email">
<input class="field" placeholder="Company name">
<button class="btn wide">Create free account</button>
<div class="l3-note">&#128274; No credit card. Cancel anytime.</div>
</div>
</div>
<div class="l3-side">
<div class="l3-trust"><b>&#128274; SOC 2 Type II</b><span>Audited annually</span></div>
<div class="l3-trust"><b>&#127993; GDPR ready</b><span>EU data residency</span></div>
<div class="l3-trust"><b>&#9889; 99.99% SLA</b><span>Multi-region failover</span></div>
<div class="l3-trust"><b>&#128101; 4,800+ teams</b><span>2,300+ reviews</span></div>
</div>
</section>"""

def arch_chat_v1(row, r):
    return hero_base(int(row["No"]), row, r, "chat", "v1") + """
<section class="chat-shell">
<div class="chatbox big">
<div class="chat-h"><span class="ai-dot"></span> AI Assistant <span class="cmut">online</span></div>
<div class="chat-body">
<div class="bubble-a">Halo! Saya asisten AI kamu. Tanya apa saja soal project, jadwal, atau ide.</div>
<div class="bubble-u">Buatkan draft email untuk klien soal penundaan rilis</div>
<div class="bubble-a">Tentu, ini draftnya:<br><br><i>"Halo [Nama],<br>Terima kasih atas kesabaranmu. Kami memundurkan rilis ke Jumat pekan depan karena QA menemukan beberapa isu yang ingin kami selesaikan dengan benar. Kami akan kirim update Jumat pagi."</i><br><br>Mau saya sesuaikan nadanya?</div>
<div class="bubble-u">Ya, bikin lebih hangat</div>
<div class="typing"><span></span><span></span><span></span></div>
</div>
<div class="chat-in"><input class="field" placeholder="Tulis pesan..."><button class="btn sm">Kirim</button></div>
</div>
</section>"""

def arch_chat_v2(row, r):
    return hero_base(int(row["No"]), row, r, "chat", "v2") + """
<section class="voice-shell">
<div class="voice-card card">
<div class="v-orb"><div class="v-ring r1"></div><div class="v-ring r2"></div><div class="v-core">&#127908;</div></div>
<div class="v-status"><span class="listening-dot"></span> Listening&hellip;</div>
<div class="wave"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
<div class="v-transcript card">"Buatkan jadwal meeting dengan tim desain besok jam 10"</div>
<div class="v-hints"><span class="chip2">&#127909; Hands-free</span><span class="chip2">&#127911; Audio cues</span><span class="chip2">&#128172; Conversational</span></div>
</div>
</section>"""

def arch_poster_v1(row, r):
    return hero_base(int(row["No"]), row, r, "poster", "v1") + """
<section class="poster">
<div class="p-num">%s</div>
<h2 class="p-h">MAKE<br>IT<br>LOUD.</h2>
<p class="p-sub">Type is the interface. Everything else is decoration.</p>
<div class="p-cta">START NOW <span class="p-arr">&#8594;</span></div>
<div class="p-meta"><span>EST. 2026</span><span>85 STYLES</span><span>NO. %s</span></div>
</section>""" % (int(row["No"]), int(row["No"]))

def arch_poster_v2(row, r):
    return hero_base(int(row["No"]), row, r, "poster", "v2") + """
<section class="poster">
<div class="p-big-num">85</div>
<div class="p-title-row"><span class="p-kicker">STYLE INDEX</span><span class="p-kicker">2026 EDITION</span></div>
<div class="p-stat-row">
<div><b>13</b><span>layouts</span></div>
<div><b>23</b><span>components</span></div>
<div><b>161</b><span>palettes</span></div>
</div>
<div class="p-meta"><span>NO. %s</span><span>THINK BIG</span><span>TYPE FIRST</span></div>
</section>""" % (int(row["No"]))

def arch_poster_v3(row, r):
    return hero_base(int(row["No"]), row, r, "poster", "v3") + """
<section class="p3">
<div class="p3-block p3-a"><span class="p3-label">FORM</span><h2 class="p3-h">STYLE<br>IS<br>FORM</h2></div>
<div class="p3-block p3-b"><span class="p3-label">FUNCTION</span><h2 class="p3-h">FORM<br>IS<br>FUNCTION</h2></div>
<div class="p3-foot"><span>NO. %s</span><span>EVERY PIXEL EARNED</span></div>
</section>""" % (int(row["No"]))

def arch_mobile_v1(row, r):
    return hero_base(int(row["No"]), row, r, "mobile", "v1") + """
<section class="phone-wrap">
<div class="phone">
<div class="p-notch"><span></span></div>
<div class="p-status"><span>9:41</span><span>&#128268; &#128246; &#128267;</span></div>
<div class="p-body">
<div class="p-hi"><span class="tag">TODAY</span><h3>Good morning,<br>Jordan</h3></div>
<div class="p-balance card"><div class="p-b-label">Total balance</div><div class="p-b-num">$2,480.00</div><div class="p-b-delta up">&#9650; +18.2% this week</div></div>
<div class="p-grid">
<div class="card p-mini"><div class="ico sm">&#128200;</div><b>Stats</b><span class="up">+12.4%</span></div>
<div class="card p-mini"><div class="ico sm">&#128176;</div><b>Income</b><span>$4,120</span></div>
</div>
<div class="card p-goal"><div style="display:flex;justify-content:space-between;margin-bottom:10px"><b>Monthly goal</b><span>72%</span></div><div class="progress"><i style="width:72%"></i></div></div>
<div class="p-actions"><button class="btn" style="flex:1">Send</button><button class="btn2" style="flex:1">Request</button></div>
</div>
<div class="p-tabbar"><span class="on">&#127968;</span><span>&#128200;</span><span>&#128269;</span><span>&#9881;</span></div>
</div>
</section>"""

def arch_mobile_v2(row, r):
    return hero_base(int(row["No"]), row, r, "mobile", "v2") + """
<section class="phone-wrap">
<div class="phone">
<div class="p-notch"><span></span></div>
<div class="p-status"><span>9:41</span><span>&#128268; &#128246; &#128267;</span></div>
<div class="p-body">
<div class="p-hi"><span class="tag">INBOX</span><h3>Messages</h3></div>
<div class="p-list">
<div class="p-msg card"><div class="p-ava">AL</div><div><b>Alya L.</b><p>Design review udah aku update, cek ya!</p><span class="p-time">10:24</span></div></div>
<div class="p-msg card"><div class="p-ava">RK</div><div><b>Raka K.</b><p>Oke, meeting geser ke jam 2</p><span class="p-time">09:12</span></div></div>
<div class="p-msg card"><div class="p-ava">MJ</div><div><b>Maya J.</b><p>Data Q2 udah masuk dashboard &#128200;</p><span class="p-time">08:47</span></div></div>
</div>
<div class="p-actions"><button class="btn" style="flex:1">&#128221; New message</button></div>
</div>
<div class="p-tabbar"><span>&#127968;</span><span class="on">&#128172;</span><span>&#128269;</span><span>&#9881;</span></div>
</div>
</section>"""

def arch_mobile_v3(row, r):
    return hero_base(int(row["No"]), row, r, "mobile", "v3") + """
<section class="phone-wrap">
<div class="phone">
<div class="p-notch"><span></span></div>
<div class="p-status"><span>9:41</span><span>&#128268; &#128246; &#128267;</span></div>
<div class="p-body">
<div class="p-hi"><span class="tag">SETTINGS</span><h3>Preferences</h3></div>
<div class="p-grid">
<div class="card p-mini"><div class="ico sm">&#128200;</div><b>Usage</b><span class="up">6.2 GB</span></div>
<div class="card p-mini"><div class="ico sm">&#9889;</div><b>Battery</b><span>82%</span></div>
</div>
<div class="p-settings card">
<div class="ctrl-row"><span class="c-label">Notifications</span><div class="switch"><i></i></div></div>
<div class="ctrl-row"><span class="c-label">Dark mode</span><div class="switch off"><i></i></div></div>
<div class="ctrl-row"><span class="c-label">Auto-sync</span><div class="switch"><i></i></div></div>
<div class="ctrl-row"><span class="c-label">Face ID</span><div class="switch"><i></i></div></div>
</div>
<div class="p-actions"><button class="btn" style="flex:1">Save changes</button></div>
</div>
<div class="p-tabbar"><span>&#127968;</span><span>&#128200;</span><span>&#128269;</span><span class="on">&#9881;</span></div>
</div>
</section>"""

def arch_blueprint_v1(row, r):
    return hero_base(int(row["No"]), row, r, "blueprint", "v1") + """
<section>
<div class="sec-h"><h2>Drafting Sheet</h2><small>DWG-054 &middot; scale 1:1 &middot; rev C</small></div>
<div class="bp-sheet">
<div class="bp-head"><span>UI / LAYOUT SHEET</span><span>GRID 12 COL &middot; GUTTER 24</span></div>
<div class="bp-body">
<div class="bp-frame">
<div class="bp-dim bp-dim-h"><i></i><span>1024</span></div>
<div class="bp-dim bp-dim-v"><i></i><span>640</span></div>
<div class="bp-center"><b>PRIMARY WORK AREA</b><span>content column &middot; 1024 &times; 640</span></div>
<div class="bp-callout bp-c1"><b>A</b><span>title block</span></div>
<div class="bp-callout bp-c2"><b>B</b><span>dimension line</span></div>
<div class="bp-callout bp-c3"><b>C</b><span>hatch fill</span></div>
</div>
<div class="bp-legend">
<div class="bp-lg"><i class="l1"></i><span>A &mdash; solid stroke, 1px</span></div>
<div class="bp-lg"><i class="l2"></i><span>B &mdash; dashed guide, 1px</span></div>
<div class="bp-lg"><i class="l3"></i><span>C &mdash; 45&deg; hatch, 4px pitch</span></div>
<div class="bp-lg"><i class="l1"></i><span>All strokes hairline, no blur</span></div>
</div>
</div>
<div class="bp-stamp"><span>DRAWN: gallery</span><span>CHECKED: &mdash;</span><span>REV C</span></div>
</div>
</section>
<section>
<div class="sec-h"><h2>Part Schedule</h2><small>annotation keys resolved from the sheet above</small></div>
<div class="table-wrap"><table class="tbl">
<thead><tr><th>Key</th><th>Part</th><th>Spec</th><th>Qty</th></tr></thead>
<tbody>
<tr><td><b>A</b></td><td>Title block</td><td>Mono 10.5px, tracking .2em, uppercase</td><td>1</td></tr>
<tr><td><b>B</b></td><td>Dimension line</td><td>1px, terminal ticks, label centred</td><td>4</td></tr>
<tr><td><b>C</b></td><td>Hatch fill</td><td>45&deg; repeating-linear-gradient, 1px on 4px</td><td>3</td></tr>
<tr><td><b>D</b></td><td>Grid overlay</td><td>22px cell, 13% cyan on navy</td><td>1</td></tr>
</tbody></table></div>
</section>
<section>
<div class="sec-h"><h2>Annotation Rules</h2><small>how the sheet is read</small></div>
<div class="al info"><b>A</b><span>Label every region with a lettered key, then resolve it in the part schedule. No label floats unreferenced.</span></div>
<div class="al warn"><b>!</b><span>Hairlines only: 1px solid or 1px dashed. Drop shadows belong to the paper, not the parts.</span></div>
<div class="al ok"><b>&#10003;</b><span>Cyan on blueprint navy holds AA at 11px and up &mdash; keep labels at that floor, never smaller.</span></div>
</section>"""

ARCH_BUILDERS = {
    ("minimal","v1"): arch_minimal_v1, ("minimal","v2"): arch_minimal_v2, ("minimal","v3"): arch_minimal_v3,    ("editorial","v1"): arch_editorial_v1, ("editorial","v2"): arch_editorial_v2, ("editorial","v3"): arch_editorial_v3,
    ("bento",""): arch_bento,
    ("brutal","v1"): arch_brutal_v1, ("brutal","v2"): arch_brutal_v2,
    ("dashboard","v1"): arch_dashboard_v1, ("dashboard","v2"): arch_dashboard_v2, ("dashboard","v3"): arch_dashboard_v3,
    ("glass","v1"): arch_glass_v1, ("glass","v2"): arch_glass_v2,
    ("terminal",""): arch_terminal,
    ("hud","v1"): arch_hud_v1, ("hud","v2"): arch_hud_v2,
    ("centered","v1"): arch_centered_v1, ("centered","v2"): arch_centered_v2,
    ("centered","v3"): arch_centered_v3, ("centered","v4"): arch_centered_v4,
    ("landing","v1"): arch_landing_v1, ("landing","v2"): arch_landing_v2, ("landing","v3"): arch_landing_v3,
    ("chat","v1"): arch_chat_v1, ("chat","v2"): arch_chat_v2,
    ("poster","v1"): arch_poster_v1, ("poster","v2"): arch_poster_v2, ("poster","v3"): arch_poster_v3,
    ("mobile","v1"): arch_mobile_v1, ("mobile","v2"): arch_mobile_v2, ("mobile","v3"): arch_mobile_v3,
    ("blueprint","v1"): arch_blueprint_v1,
}

# ================= page template =================
HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITLE%%</title>
%%FONTS%%
<style>
%%CSS%%
%%FX%%
/* ---------- shared layout ---------- */
*{margin:0;padding:0;box-sizing:border-box}
.wrap{max-width:1100px;margin:0 auto;padding:0 26px}
.topnav{display:flex;align-items:center;gap:12px;padding:14px 26px;font-size:13px;border-bottom:var(--border);background:var(--bg);position:sticky;top:0;z-index:60}
.topnav a{text-decoration:none;font-weight:600;opacity:.9}
.topnav .sp{flex:1}
.hero{padding:66px 0 46px}
.hero .tag{display:inline-block;font-size:12px;letter-spacing:.12em;text-transform:uppercase;opacity:.75;font-weight:700;margin-bottom:14px}
.hero h1{font-size:clamp(2.1rem,5vw,3.4rem);line-height:1.04;letter-spacing:-.02em;margin-bottom:16px}
.hero p{font-size:16px;max-width:680px;line-height:1.6;opacity:.85}
.badges{display:flex;gap:10px;margin-top:24px;flex-wrap:wrap}
.badge{font-size:12px;font-weight:700;padding:7px 14px;border-radius:999px;border:var(--border);background:var(--card);color:var(--card-ink)}
section{margin-bottom:64px}
.sec-h{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:20px;gap:16px;flex-wrap:wrap}
.sec-h h2{font-size:21px;letter-spacing:-.01em}
.sec-h small{opacity:.6}
.swatches{display:flex;gap:14px;flex-wrap:wrap}
.swatch{width:150px;border-radius:14px;overflow:hidden;border:1px solid rgba(128,128,128,.25);cursor:pointer;transition:transform .15s ease;background:var(--card)}
.swatch:hover{transform:translateY(-3px)}
.swatch .color{height:72px}
.swatch .meta{padding:9px 11px;font-size:11px;line-height:1.5;color:var(--card-ink)}
.swatch .meta b{display:block;font-size:11px;font-weight:700}
.swatch .meta span{opacity:.75;font-family:'JetBrains Mono',monospace}
.copied{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#111;color:#fff;padding:9px 18px;border-radius:999px;font-size:13px;font-weight:600;opacity:0;transition:opacity .25s;pointer-events:none;z-index:9999}
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.card{padding:24px;transition:transform .18s ease, box-shadow .18s ease}
.card .ico{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:14px;background:var(--accent);color:#fff}
.card h3{font-size:16px;margin-bottom:8px}
.card p{font-size:13.5px;line-height:1.55;opacity:.8}
.btn{padding:13px 26px;font-size:14.5px;cursor:pointer;font-family:var(--fb)}
.btn.sm{padding:9px 16px;font-size:13px}
.btn2{padding:12px 24px;font-size:14.5px;cursor:pointer;font-family:var(--fb);background:transparent}
.cta-row{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap;align-items:center}
.field{padding:13px 16px;font-size:14px;font-family:var(--fb)}
.field:focus{outline:none;border-color:var(--accent)}
.progress{height:8px;background:var(--card);border:var(--border);border-radius:999px;overflow:hidden}
.progress i{display:block;height:100%;background:var(--accent);border-radius:999px}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.info-box{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px}
.info-box h4{font-size:12px;text-transform:uppercase;letter-spacing:.12em;margin-bottom:12px;opacity:.7}
.info-box ul{list-style:none}
.info-box li{font-size:13.5px;line-height:1.65;padding-left:18px;position:relative;margin-bottom:7px;opacity:.92}
.info-box li::before{content:"\\2022";position:absolute;left:2px;color:var(--accent);font-weight:900}
.kw{display:flex;flex-wrap:wrap;gap:8px}
.kw span{font-size:12px;padding:6px 12px;border-radius:999px;border:var(--border);background:var(--card);color:var(--card-ink)}
.tokens{font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.7;background:var(--bg);border:var(--border);border-radius:10px;padding:16px;white-space:pre-wrap;cursor:pointer;color:var(--ink)}
.tokens:hover{border-color:var(--accent)}
.foot{padding:40px 0;border-top:var(--border);margin-top:80px;font-size:13px;opacity:.7;text-align:center}
.up{color:#22C55E}.down{color:#EF4444}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.kpi{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px}
.kpi .l{font-size:11.5px;text-transform:uppercase;letter-spacing:.1em;opacity:.65;margin-bottom:6px}
.kpi .v{font-size:26px;font-weight:800;letter-spacing:-.02em}
.kpi .d{font-size:12px;margin-top:4px}
.bars{display:flex;align-items:flex-end;gap:10px;height:150px;padding:18px;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}
.bars i{flex:1;background:var(--accent);border-radius:6px 6px 0 0;opacity:.85;min-height:8px}
.bars i:nth-child(2n){background:var(--a2);opacity:.8}
/* components */
.navi{display:flex;align-items:center;gap:20px;padding:14px 22px;border-radius:var(--radius);background:var(--card);border:var(--border);box-shadow:var(--shadow);flex-wrap:wrap}
.navi .logo{font-family:var(--fh);font-size:17px;letter-spacing:-.01em}
.nlink{font-size:13.5px;opacity:.7;cursor:pointer}
.nlink.on{opacity:1;font-weight:700;color:var(--accent)}
.ctrl-row{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 18px;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);margin-bottom:10px}
.ctrl-row.col{flex-direction:column;align-items:stretch}
.c-label{font-size:14px;font-weight:600}
.switch{width:52px;height:30px;border-radius:999px;background:var(--accent);position:relative;transition:.2s;flex-shrink:0}
.switch i{position:absolute;top:3px;right:3px;width:24px;height:24px;border-radius:50%;background:#fff}
.switch.off{background:var(--muted);opacity:.5}
.switch.off i{right:auto;left:3px}
.range{width:100%;accent-color:var(--accent);height:6px}
.avs{display:flex}
.avs span{width:38px;height:38px;border-radius:50%;border:2px solid var(--card);margin-left:-10px;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.avs span:first-child{margin-left:0}
.cmut{font-size:12.5px;opacity:.65;margin-top:10px}
.chip2{border:var(--border);background:var(--card);color:var(--card-ink);padding:7px 14px;border-radius:999px;font-size:12.5px;font-weight:700}
.price-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.p-card{padding:26px 22px}
.p-card h3{font-size:15px;opacity:.75}
.p-price{font-size:34px;font-weight:800;letter-spacing:-.03em;margin:10px 0 16px;font-family:var(--fh)}
.p-price span{font-size:13px;opacity:.6;font-weight:400}
.p-list{list-style:none;margin-bottom:20px}
.p-list li{font-size:13.5px;padding:5px 0;opacity:.85}
.wide{width:100%}
.table-wrap{overflow-x:auto;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl th{text-align:left;text-transform:uppercase;font-size:11px;letter-spacing:.1em;opacity:.6;padding:12px 16px;border-bottom:var(--border)}
.tbl td{padding:12px 16px;border-bottom:var(--border);opacity:.9}
.okchip{background:rgba(34,197,94,.12);color:#16A34A;padding:3px 10px;border-radius:999px;font-size:11.5px;font-weight:700}
.tl{border-left:2px solid var(--accent);margin-left:8px;padding-left:24px}
.tl-item{position:relative;padding-bottom:22px}
.tl-dot{position:absolute;left:-31px;top:4px;width:12px;height:12px;border-radius:50%;background:var(--accent);border:2px solid var(--bg)}
.tl-item b{font-size:14px}
.tl-item p{font-size:13px;opacity:.7;margin-top:3px}
.stat-band{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stat-band div{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px;text-align:center}
.stat-band b{display:block;font-size:30px;font-weight:800;letter-spacing:-.03em;font-family:var(--fh)}
.stat-band span{font-size:12px;text-transform:uppercase;letter-spacing:.1em;opacity:.6}
.bigq{font-size:clamp(1.3rem,2.6vw,1.8rem);font-family:var(--fh);line-height:1.35;border-left:4px solid var(--accent);padding-left:22px;margin:6px 0 12px;max-width:760px}
.al{display:flex;gap:10px;align-items:flex-start;padding:13px 16px;border-radius:var(--radius);background:var(--card);border:var(--border);box-shadow:var(--shadow);margin-bottom:10px;font-size:13.5px}
.al b{flex-shrink:0}
.al.info{border-left:4px solid var(--accent)}
.al.warn{border-left:4px solid #F59E0B}
.al.err{border-left:4px solid #EF4444}
.al.ok{border-left:4px solid #22C55E}
.crumb{font-size:13px;opacity:.75;margin-bottom:14px}
.crumb b{opacity:1;color:var(--accent)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.step{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px}
.s-num{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;color:var(--accent);display:block;margin-bottom:10px}
.step b{font-size:14.5px;display:block;margin-bottom:6px}
.step p{font-size:12.5px;opacity:.7;line-height:1.5}
.searchbar{display:flex;align-items:center;gap:12px;padding:10px 10px 10px 18px;background:var(--card);border:var(--border);border-radius:999px;box-shadow:var(--shadow)}
.searchbar .field{flex:1;border:none;background:transparent;padding:8px 0}
.searchbar kbd{border:var(--border);border-radius:6px;padding:4px 9px;font-size:11px;opacity:.7;font-family:'JetBrains Mono',monospace}
.heat{display:grid;grid-template-columns:repeat(14,1fr);gap:4px;background:var(--card);border:var(--border);border-radius:var(--radius);padding:14px}
.heat i{aspect-ratio:1;border-radius:3px}
.funnel{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px}
.fn-row{display:flex;align-items:center;gap:14px;margin-bottom:14px}
.fn-row span{width:80px;font-size:13px;font-weight:600}
.fn-track{flex:1;height:26px;background:var(--bg);border-radius:6px;overflow:hidden}
.fn-track i{display:block;height:100%;background:var(--accent);border-radius:6px;opacity:.85}
.fn-row b{width:44px;text-align:right;font-size:13px;font-family:'JetBrains Mono',monospace}
.gauge-wrap{text-align:center}
.gauge{width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 8px}
.gauge i{width:76px;height:76px;border-radius:50%;background:var(--card);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px}
.tick{overflow:hidden;white-space:nowrap;background:var(--card);border:var(--border);border-radius:8px;padding:9px 0;font-size:12px;font-family:'JetBrains Mono',monospace;opacity:.9}
.tick span{display:inline-block;animation:marq 14s linear infinite}
@keyframes marq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.marquee{overflow:hidden;white-space:nowrap;background:var(--accent);color:#fff;border:var(--border);padding:10px 0;font-weight:800}
.marquee span{display:inline-block;animation:marq 8s linear infinite}
.article-body p{font-size:16.5px;line-height:1.75;margin-bottom:18px;opacity:.92;max-width:72ch}
.dropcap::first-letter{font-size:3.2em;float:left;line-height:.9;padding-right:8px;font-family:var(--fh);color:var(--accent)}
.logo-strip{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:center;padding:22px 26px;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);opacity:.5;filter:grayscale(1);font-weight:800;font-size:15px;letter-spacing:.04em}
.typography-scale{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:28px 30px}
.ts-h{font-family:var(--fh);font-size:clamp(2rem,5vw,3.2rem);line-height:1.05;letter-spacing:-.02em;margin-bottom:6px}
.ts-sub{font-family:var(--fh);font-size:1.35rem;margin-bottom:6px;opacity:.92}
.ts-body{font-size:1rem;line-height:1.7;max-width:56ch;opacity:.85}
.ts-cap{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;opacity:.6;margin-top:14px}
.pattern-strip{display:flex;gap:16px;flex-wrap:wrap}
.pattern-box{flex:1;min-width:150px;background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;text-align:center;font-size:12.5px;opacity:.92}
.pattern-box b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.12em;margin-bottom:14px;opacity:.65}
.px{height:96px;border-radius:var(--radius);border:var(--border);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;background:var(--card);color:var(--card-ink)}
/* archetype css */
.single-col{max-width:720px;margin:0 auto;padding:30px 0}
.lead{font-size:clamp(1.2rem,2.4vw,1.6rem);line-height:1.5;font-family:var(--fh);margin-bottom:34px}
.rule{height:2px;background:var(--ink);opacity:.15;margin-bottom:34px}
.two-col-text{display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-bottom:8px}
.two-col-text h3{font-size:15px;margin-bottom:10px}
.two-col-text p{font-size:14px;line-height:1.65;opacity:.8}
.masthead{display:flex;justify-content:space-between;font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.6;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:10px 0;margin-bottom:30px;font-family:var(--fh)}
.art-h{font-size:clamp(1.8rem,4vw,2.9rem);line-height:1.06;letter-spacing:-.02em;max-width:18ch;margin-bottom:14px}
.byline{font-size:12.5px;opacity:.6;margin-bottom:26px;letter-spacing:.04em}
.art-cols{display:grid;grid-template-columns:2fr 1fr;gap:44px}
.art-main p{font-size:16.5px;line-height:1.75;margin-bottom:18px;opacity:.92}
.pullq{font-family:var(--fh);font-size:1.35rem;line-height:1.4;border-left:3px solid var(--accent);padding-left:16px;margin-bottom:26px}
.side-card{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px}
.side-card p{font-size:13px;line-height:1.7;opacity:.75;margin-top:8px}
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:150px;gap:16px}
.b-card{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px;display:flex;flex-direction:column;justify-content:flex-end;transition:transform .2s ease}
.b-card:hover{transform:scale(1.02)}
.b-card h3{font-size:16px;margin-bottom:6px}
.b-card p{font-size:12.5px;opacity:.75;line-height:1.5}
.b-ico{width:38px;height:38px;border-radius:11px;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:17px;margin-bottom:12px}
.b-lg{grid-column:span 2;grid-row:span 2}
.b-tall{grid-row:span 2}
.b-wide{grid-column:span 2}
.spark{font-size:20px;letter-spacing:2px;opacity:.8;margin-top:12px}
.brutal-block{display:grid;grid-template-columns:1.1fr 1fr;gap:34px;align-items:start}
.brut-h{font-size:clamp(2.4rem,6vw,4.4rem);font-weight:900;line-height:.92;letter-spacing:-.02em;text-transform:uppercase;margin-bottom:18px}
.brutal-left p{font-size:15px;line-height:1.6;opacity:.85;margin-bottom:22px;max-width:38ch}
.brutal-btn{border-radius:0;padding:16px 30px;font-size:15px;text-transform:uppercase;letter-spacing:.05em}
.brutal-card{background:var(--card);border:var(--border);box-shadow:var(--shadow);padding:18px 20px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center}
.brutal-card b{font-size:12px;letter-spacing:.14em}
.brutal-card .big{font-size:26px;font-weight:900;font-family:var(--fh)}
.brutal-list{border:var(--border);box-shadow:var(--shadow);background:var(--card)}
.brow{display:flex;gap:14px;padding:12px 18px;border-bottom:var(--border);font-size:14px;font-weight:600}
.brow:last-child{border-bottom:none}
.brow span{font-family:'JetBrains Mono',monospace;opacity:.5;font-size:12px}
.dash{display:grid;grid-template-columns:220px 1fr;gap:20px;align-items:start}
.dash-side{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px;position:sticky;top:70px}
.dash-logo{font-weight:900;font-family:var(--fh);margin-bottom:20px;font-size:16px}
.dash-item{padding:10px 12px;border-radius:8px;font-size:13.5px;opacity:.7;margin-bottom:4px;cursor:pointer}
.dash-item.on{background:var(--accent);color:#fff;opacity:1;font-weight:700}
.dash-user{margin-top:22px;border-top:var(--border);padding-top:14px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px}
.dash-user span{opacity:.6;font-weight:400}
.dash-main{min-width:0}
.dash-main .bars{margin-bottom:16px}
.glass-wrap{display:flex;flex-direction:column;gap:18px}
.glass-nav{display:flex;align-items:center;gap:22px;padding:14px 22px;border-radius:999px}
.glass-nav b{font-family:var(--fh);font-size:16px}
.glass-nav span{font-size:13.5px;opacity:.85;cursor:pointer}
.glass-nav .sp{flex:1}
.glass-hero{padding:52px 44px;border-radius:28px}
.glass-hero h2{font-size:clamp(2rem,4.5vw,3.2rem);line-height:1.05;letter-spacing:-.02em;margin:12px 0}
.glass-hero p{opacity:.9;max-width:46ch;font-size:15.5px;line-height:1.6}
.glass-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.term-section{display:flex;justify-content:center}
.term{width:100%;max-width:760px;background:var(--bg);border:var(--border);border-radius:10px;overflow:hidden;box-shadow:var(--shadow)}
.term.big .term-body{padding:22px;font-size:14px;line-height:1.85}
.term-bar{display:flex;align-items:center;gap:8px;padding:11px 16px;border-bottom:var(--border);font-size:12px;opacity:.8;font-family:'JetBrains Mono',monospace}
.t-dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.t-dot.r{background:#FF5F57}.t-dot.y{background:#FEBC2E}.t-dot.g{background:#28C840}
.term-body{padding:16px;font-size:13px;line-height:1.75;font-family:'JetBrains Mono',monospace}
.term-body .dim{opacity:.6}
.term-body .pr{color:var(--accent)}
.hud-wrap{display:flex;flex-direction:column;gap:14px}
.hud-status{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.12em;padding:10px 16px;border:1px solid var(--border);background:var(--card);color:var(--card-ink)}
.pulse{animation:pulse 1.6s ease infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.45}}
.hud-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.hud-panel{background:var(--card);border:1px solid var(--border);padding:20px}
.hud-tag{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.16em;opacity:.7;display:block;margin-bottom:16px}
.hud-bars{display:flex;align-items:flex-end;gap:6px;height:90px}
.hud-bars i{flex:1;background:var(--accent);min-height:8px}
.hud-log{font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.8}
.hud-stat{margin-bottom:10px}
.hud-stat b{font-size:26px;font-weight:800;font-family:var(--fh);display:block}
.hud-stat span{font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.6}
.chat-shell{display:flex;justify-content:center}
.chatbox{width:100%;max-width:660px;background:var(--card);border:var(--border);border-radius:20px;box-shadow:var(--shadow);overflow:hidden}
.chat-h{display:flex;align-items:center;gap:10px;padding:15px 20px;border-bottom:var(--border);font-weight:700;font-size:14.5px}
.ai-dot{width:10px;height:10px;border-radius:50%;background:#22C55E;display:inline-block}
.chat-body{padding:20px;display:flex;flex-direction:column;gap:12px;min-height:280px}
.bubble-a,.bubble-u{max-width:78%;padding:12px 16px;font-size:14px;line-height:1.6}
.bubble-a{align-self:flex-start}
.bubble-u{align-self:flex-end;background:var(--accent);color:#fff;border-radius:16px 16px 4px 16px}
.typing span{width:7px;height:7px;border-radius:50%;background:var(--accent);display:inline-block;animation:blink 1.2s infinite}
.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,80%,100%{opacity:.25}40%{opacity:1}}
.chat-in{display:flex;gap:10px;padding:14px 20px;border-top:var(--border)}
.chat-in .field{flex:1}
.poster{text-align:center;padding:30px 0}
.p-num{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.3em;opacity:.5;margin-bottom:26px}
.p-h{font-size:clamp(3rem,11vw,8.5rem);font-weight:900;line-height:.9;letter-spacing:-.04em;text-transform:uppercase}
.p-sub{font-size:16px;opacity:.75;margin-top:26px;letter-spacing:.04em}
.p-cta{display:inline-block;margin-top:38px;font-weight:800;letter-spacing:.08em;font-size:15px;border-bottom:3px solid var(--accent);padding-bottom:8px;cursor:pointer}
.p-arr{color:var(--accent)}
.p-meta{display:flex;justify-content:space-between;margin-top:64px;padding-top:18px;border-top:1px solid var(--border);font-size:11px;letter-spacing:.2em;opacity:.55;font-family:'JetBrains Mono',monospace}
.phone-wrap{display:flex;justify-content:center}
.phone{width:350px;border-radius:46px;border:var(--border);box-shadow:var(--shadow);overflow:hidden;background:var(--bg)}
.p-notch{height:32px;display:flex;align-items:center;justify-content:center}
.p-notch span{width:110px;height:6px;border-radius:99px;background:var(--muted);opacity:.4}
.p-status{display:flex;justify-content:space-between;padding:0 24px;font-size:12px;font-weight:700;opacity:.9}
.p-body{padding:16px 20px}
.p-hi h3{font-size:22px;font-weight:800;margin-top:4px;line-height:1.15}
.p-balance{border-radius:22px;padding:20px;margin:18px 0 14px}
.p-b-label{font-size:12px;opacity:.65;text-transform:uppercase;letter-spacing:.08em}
.p-b-num{font-size:30px;font-weight:800;letter-spacing:-.02em;margin:6px 0}
.p-b-delta{font-size:12.5px;font-weight:700}
.p-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
.p-mini{border-radius:20px;padding:16px}
.p-mini b{font-size:13.5px;display:block;margin-top:8px}
.p-mini span{font-size:12px;font-weight:700}
.ico.sm{width:34px;height:34px;font-size:15px;margin-bottom:0}
.p-goal{border-radius:20px;padding:16px;margin-bottom:14px;font-size:13px}
.p-actions{display:flex;gap:10px;margin-bottom:8px}
.p-tabbar{height:56px;border-top:var(--border);display:flex;align-items:center;justify-content:space-around;font-size:17px;opacity:.75;background:var(--card)}
.p-tabbar .on{color:var(--accent);opacity:1}
/* ---- variant css ---- */
.split-panel{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:center;padding:30px 0}
.sp-sub{font-size:15px;line-height:1.65;opacity:.75;margin:18px 0 0;max-width:44ch}
.sp-right{display:flex;flex-direction:column;gap:12px}
.sp-card{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 24px;display:flex;justify-content:space-between;align-items:center}
.sp-card b{font-size:12px;text-transform:uppercase;letter-spacing:.12em;opacity:.65}
.sp-card .big{font-size:26px;font-weight:800;font-family:var(--fh)}
.m3-wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;padding:40px 0}
.m3-card{border-top:3px solid var(--ink);padding-top:18px;opacity:.9}
.m3-no{font-family:'JetBrains Mono',monospace;font-size:12px;opacity:.5;display:block;margin-bottom:12px}
.m3-card h3{font-size:17px;margin-bottom:8px}
.m3-card p{font-size:13.5px;line-height:1.6;opacity:.75}
.spread{display:grid;grid-template-columns:1.15fr 1fr;gap:0;border:var(--border);box-shadow:var(--shadow);background:var(--card)}
.spread-visual{background:var(--accent);color:#fff;min-height:380px;display:flex;align-items:flex-end;padding:30px;position:relative}
.spread-art span{font-size:11px;letter-spacing:.3em;opacity:.8;position:absolute;top:24px;left:30px}
.spread-h{font-size:clamp(2rem,4.5vw,3.4rem);font-weight:900;line-height:.95;letter-spacing:-.02em;text-transform:uppercase}
.spread-body{padding:38px;display:flex;flex-direction:column;justify-content:center}
.spread-kicker{font-size:11px;letter-spacing:.24em;opacity:.6;margin-bottom:14px}
.spread-sub{font-size:clamp(1.1rem,2vw,1.5rem);line-height:1.35;margin-bottom:16px}
.spread-p{font-size:14px;line-height:1.7;opacity:.8}
.spread-meta{display:flex;gap:18px;margin-top:22px;font-size:11px;letter-spacing:.18em;opacity:.6}
.chapter-block{max-width:720px;margin:0 auto}
.chapter{display:grid;grid-template-columns:90px 1fr;gap:18px;padding:26px 0;border-bottom:1px solid var(--border)}
.chapter:last-child{border-bottom:none}
.ch-num{font-family:var(--fh);font-size:26px;opacity:.4}
.ch-body h3{font-size:18px;margin-bottom:8px}
.ch-body p{font-size:14px;line-height:1.65;opacity:.8}
.raw-marquee{margin-bottom:20px}
.raw-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:18px}
.raw-list{border:var(--border);box-shadow:var(--shadow);background:var(--card)}
.raw-row{display:grid;grid-template-columns:44px 1fr auto;align-items:center;gap:12px;padding:15px 18px;border-bottom:var(--border);font-size:13.5px}
.raw-row:last-child{border-bottom:none}
.rw-idx{font-family:'JetBrains Mono',monospace;font-size:11px;opacity:.5}
.raw-row b{font-size:12px;letter-spacing:.12em}
.raw-card{border:var(--border);box-shadow:var(--shadow);background:var(--card);padding:22px;display:flex;flex-direction:column;gap:14px}
.raw-stat{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:12px;border-bottom:var(--border)}
.big2{font-size:30px;font-weight:900;font-family:var(--fh)}
.raw-stat span{font-size:11px;letter-spacing:.16em}
.wide2{width:100%;padding:16px}
.d2-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:10px}
.d2-title b{font-size:19px;font-family:var(--fh)}
.d2-range{font-size:12.5px;opacity:.65;margin-left:12px}
.d2-actions{display:flex;gap:8px}
.d2-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:16px}
.sparkline{font-size:16px;letter-spacing:1px;margin-top:8px;opacity:.8}
.d3-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.d3-widget{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px}
.d3-tag{font-size:10.5px;letter-spacing:.16em;opacity:.6;display:block;margin-bottom:12px}
.d3-num{font-size:30px;font-weight:800;font-family:var(--fh);letter-spacing:-.02em}
.d3-delta{font-size:12.5px;font-weight:700;margin:4px 0 12px}
.bars.mini{height:60px;padding:10px;box-shadow:none;border:none;background:var(--bg)}
.d3-seg{margin-bottom:10px}
.d3-seg b{display:block;font-size:15px;margin-bottom:4px}
.d3-seg span{font-size:12px;opacity:.65}
.glass-full{display:grid;grid-template-columns:1.1fr 1fr;gap:36px;padding:52px 46px;border-radius:30px;align-items:center}
.gf-left h2{font-size:clamp(1.8rem,4vw,2.9rem);line-height:1.05;letter-spacing:-.02em;margin:14px 0}
.gf-left p{font-size:15px;line-height:1.65;opacity:.9;max-width:44ch}
.gf-row{display:flex;gap:14px;align-items:flex-start;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.gf-row:last-child{border-bottom:none}
.gf-row > span{width:26px;height:26px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.gf-row b{font-size:14.5px;display:block;margin-bottom:3px}
.gf-row p{font-size:12.5px;opacity:.75}
.glass-chips{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.hud-row3{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:14px}
.hud-panel.b{padding:22px}
.hud-bars.tall{height:130px}
.hud-sys{display:flex;align-items:center;gap:10px;font-size:12.5px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.07);font-family:'JetBrains Mono',monospace}
.hud-sys:last-child{border-bottom:none}
.hud-sys b{margin-left:auto}
.hud-dot{width:8px;height:8px;border-radius:50%;background:var(--muted);flex-shrink:0}
.hud-dot.on{background:#22C55E;box-shadow:0 0 8px #22C55E}
.hud-dot.warn{background:#F59E0B}
.hud-dot.err{background:#EF4444;animation:pulse 1s infinite}
.c2{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.c2-h{font-size:clamp(2rem,4.5vw,3.2rem);line-height:1.02;letter-spacing:-.03em;margin:12px 0 16px}
.c2-p{font-size:15px;line-height:1.65;opacity:.8;max-width:42ch}
.c2-controls{padding:22px}
.c3{max-width:760px;margin:0 auto}
.c3-hero{text-align:center;margin-bottom:34px}
.c3-h{font-size:clamp(1.8rem,4vw,2.8rem);letter-spacing:-.02em;margin:10px 0}
.c3-p{font-size:14.5px;opacity:.75}
.c3-block{display:flex;gap:18px;align-items:flex-start;padding:22px 26px;margin-bottom:14px}
.c3-block .ico{margin-bottom:0;flex-shrink:0}
.c3-block h3{font-size:15.5px;margin-bottom:5px}
.c3-block p{font-size:13.5px;opacity:.78;line-height:1.6}
.c4{max-width:860px;margin:0 auto}
.c4-row{display:grid;grid-template-columns:200px 1fr;gap:34px;align-items:center;padding:26px 0;border-bottom:1px solid var(--border)}
.c4-row.flip{grid-template-columns:1fr 200px}
.c4-row.flip .c4-visual{order:2}
.c4-art{height:130px;border-radius:var(--radius);background:var(--card);border:var(--border);box-shadow:var(--shadow);display:flex;align-items:center;justify-content:center;font-size:40px}
.c4-text h3{font-size:19px;margin-bottom:8px}
.c4-text p{font-size:14px;line-height:1.65;opacity:.8;max-width:52ch}
.l2-hero{text-align:center;padding:44px 0 10px}
.l2-h{font-size:clamp(2rem,5vw,3.4rem);letter-spacing:-.03em;line-height:1.04;margin:12px 0 14px}
.l2-p{font-size:15.5px;opacity:.8;max-width:52ch;margin:0 auto}
.cta-row.center{justify-content:center}
.l3{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
.l3-form{padding:30px}
.l3-h{font-size:22px;margin:10px 0 20px}
.form-stack{display:flex;flex-direction:column;gap:12px}
.form-stack .btn{padding:15px}
.l3-note{font-size:12.5px;text-align:center;opacity:.65}
.l3-side{display:flex;flex-direction:column;gap:12px}
.l3-trust{background:var(--card);border:var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px 20px;display:flex;justify-content:space-between;align-items:center}
.l3-trust b{font-size:13.5px}
.l3-trust span{font-size:12px;opacity:.6}
.voice-shell{display:flex;justify-content:center}
.voice-card{max-width:560px;padding:44px;text-align:center}
.v-orb{position:relative;width:150px;height:150px;margin:0 auto 22px;display:flex;align-items:center;justify-content:center}
.v-core{width:74px;height:74px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;position:relative;z-index:2}
.v-ring{position:absolute;border-radius:50%;border:2px solid var(--accent);opacity:.5;animation:ring 2.4s ease-out infinite}
.v-ring.r1{inset:6px}.v-ring.r2{inset:6px;animation-delay:1.2s}
@keyframes ring{0%{transform:scale(.92);opacity:.55}100%{transform:scale(1.18);opacity:0}}
.v-status{font-size:14px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;justify-content:center;gap:8px}
.listening-dot{width:10px;height:10px;border-radius:50%;background:#22C55E;animation:pulse 1.5s infinite}
.wave{display:flex;align-items:center;justify-content:center;gap:3px;height:52px;margin-bottom:20px}
.wave i{width:5px;border-radius:3px;background:var(--accent);animation:wave 1s ease-in-out infinite}
.wave i:nth-child(2n){animation-delay:.12s}.wave i:nth-child(3n){animation-delay:.24s}.wave i:nth-child(4n){animation-delay:.36s}
@keyframes wave{0%,100%{height:10px}50%{height:48px}}
.v-transcript{font-size:14.5px;line-height:1.6;padding:18px;margin-bottom:18px;font-style:italic}
.v-hints{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.p-big-num{font-size:clamp(8rem,30vw,22rem);font-weight:900;line-height:.8;letter-spacing:-.06em;opacity:.14;font-family:var(--fh)}
.p-title-row{display:flex;justify-content:space-between;margin:26px 0;font-size:11px;letter-spacing:.28em;opacity:.6;font-family:'JetBrains Mono',monospace}
.p-stat-row{display:flex;justify-content:center;gap:56px;margin:30px 0}
.p-stat-row b{font-size:42px;font-weight:900;font-family:var(--fh);display:block;letter-spacing:-.03em}
.p-stat-row span{font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.6}
.p3{display:grid;grid-template-columns:1fr 1fr;min-height:420px;border:var(--border);box-shadow:var(--shadow)}
.p3-block{padding:40px;display:flex;flex-direction:column;justify-content:flex-end;gap:14px}
.p3-a{background:var(--accent);color:#fff}
.p3-b{background:var(--card);color:var(--card-ink)}
.p3-label{font-size:11px;letter-spacing:.3em;text-transform:uppercase;opacity:.7}
.p3-h{font-size:clamp(2rem,5vw,3.8rem);font-weight:900;line-height:.95;letter-spacing:-.02em;text-transform:uppercase}
.p3-foot{grid-column:1/-1;display:flex;justify-content:space-between;padding:14px 22px;border-top:var(--border);font-size:11px;letter-spacing:.2em;opacity:.6;font-family:'JetBrains Mono',monospace}
.p-list{display:flex;flex-direction:column;gap:10px}
.p-msg{display:flex;gap:12px;align-items:flex-start;padding:14px;margin-bottom:10px}
.p-ava{width:38px;height:38px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0}
.p-msg b{font-size:13.5px;display:block}
.p-msg p{font-size:12.5px;opacity:.75;margin:3px 0;line-height:1.45}
.p-time{font-size:10.5px;opacity:.5}
.p-settings{padding:8px 16px;margin-bottom:14px}
.p-settings .ctrl-row{border:none;box-shadow:none;background:transparent;padding:10px 0;margin-bottom:0;border-bottom:1px solid rgba(128,128,128,.15)}
.p-settings .ctrl-row:last-child{border-bottom:none}
@media (max-width:900px){
.feature-grid,.glass-cards,.price-row{grid-template-columns:1fr}
.kpi-row{grid-template-columns:repeat(2,1fr)}
.art-cols{grid-template-columns:1fr}
.brutal-block{grid-template-columns:1fr}
.dash{grid-template-columns:1fr}
.dash-side{position:static}
.hud-grid{grid-template-columns:repeat(2,1fr)}
.bento{grid-template-columns:repeat(2,1fr)}
.steps,.stat-band{grid-template-columns:repeat(2,1fr)}
.info-grid{grid-template-columns:1fr}
.bp-body{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="topnav">
<a href="../index.html">&#9776; All 85 Styles</a>
<span class="sp"></span>
<a href="%%PREV%%">&#8592; Prev</a>
<span style="opacity:.55">%%ID%%/85</span>
<a href="%%NEXT%%">Next &#8594;</a>
</div>
<div class="wrap">
%%ARCH%%%%COMPS_SECTION%%
<section>
<div class="sec-h"><h2>Typography Scale</h2><small>%%FHNAME%% + %%FBNAME%%</small></div>
<div class="typography-scale">
<div class="ts-cap">Display / Heading</div>
<div class="ts-h">The quick brown fox</div>
<div class="ts-sub">Subheading — jumps over the lazy dog</div>
<div class="ts-body">Body copy sits at a comfortable reading size with relaxed leading. Buttons, chips, and inputs inherit the same voice, so the whole interface feels like one system — not a collage of parts.</div>
</div>
</section>
<section>
<div class="sec-h"><h2>Color Palette</h2><small>click to copy hex</small></div>
<div class="swatches">%%SWATCHES%%</div>
</section>
<section>
<div class="sec-h"><h2>Signature Pattern</h2><small>surface / accent / secondary</small></div>
<div class="pattern-strip">
<div class="pattern-box"><b>Surface</b><div class="px">var(--card)</div></div>
<div class="pattern-box"><b>Primary Accent</b><div class="px" style="background:var(--accent);color:#fff">var(--accent)</div></div>
<div class="pattern-box"><b>Secondary</b><div class="px" style="background:var(--a2);color:#fff">var(--a2)</div></div>
</div>
</section>
<section>
<div class="sec-h"><h2>Usage Guide</h2></div>
<div class="info-grid">
<div class="info-box"><h4>&#10003; Best For</h4><ul>%%BEST%%</ul></div>
<div class="info-box"><h4>&#10007; Avoid For</h4><ul>%%AVOID%%</ul></div>
<div class="info-box"><h4>Key Elements</h4><div class="kw">%%KW%%</div></div>
<div class="info-box"><h4>Design Tokens &#8212; click to copy</h4><div class="tokens" onclick="copyTok(this)">%%TOKENS%%</div></div>
</div>
</section>
</div>
<div class="foot">%%NAME%% &middot; generated from ui-ux-pro-max styles.csv &middot; <a href="../index.html">back to gallery</a></div>
<div class="copied" id="copied">Copied!</div>
<script>
var sw=document.querySelectorAll('.swatch');
sw.forEach(function(s){s.addEventListener('click',function(){var h=s.dataset.hex;navigator.clipboard.writeText(h).then(function(){flash('Copied '+h)})})});
function flash(t){var c=document.getElementById('copied');c.textContent=t;c.style.opacity=1;setTimeout(function(){c.style.opacity=0},1200)}
function copyTok(el){navigator.clipboard.writeText(el.textContent.trim()).then(function(){flash('Tokens copied')})}
</script>
</body>
</html>
"""

def swatch_html(pairs):
    out = []
    for name, hexv in pairs:
        out.append(f'<div class="swatch" data-hex="{hexv}" title="Click to copy {hexv}"><div class="color" style="background:{hexv}"></div><div class="meta"><b>{esc(name)}</b><span>{hexv}</span></div></div>')
    return "".join(out)

def ul_html(items, limit=8):
    lis = []
    for it in items:
        if not it.strip():
            continue
        lis.append(f"<li>{esc(it.strip())}</li>")
        if len(lis) >= limit:
            break
    return "".join(lis)

def main():
    rows = parse_csv()
    os.makedirs(STYLES_DIR, exist_ok=True)
    sids = [int(r["No"]) for r in rows]
    print(f"parsed {len(rows)} styles")

    entries = []
    for row in rows:
        sid = int(row["No"])
        name = row["Style Category"].strip()
        stype = row["Type"].strip()
        r = recipe_for(sid)
        arch = ARCH.get(sid, "centered")
        variant = V.get(sid, "v1")

        primary = hexpairs(row.get("Primary Colors", ""))
        secondary = hexpairs(row.get("Secondary Colors", ""))
        pairs = primary + [p for p in secondary if p[1] not in [q[1] for q in primary]]

        kws = [k.strip() for k in (row.get("Keywords", "") or "").split(",") if k.strip()]
        best = (row.get("Best For", "") or "").split(",")
        avoid = (row.get("Do Not Use For", "") or "").split(",")
        tokens = (row.get("Design System Variables", "") or "").strip()

        swatches = swatch_html(pairs)
        if not pairs:
            fb = [("Accent", r["accent"]), ("Secondary", r["a2"]), ("Card", r["card"]),
                  ("Ink", r["ink"]), ("Muted", r["muted"]), ("Background", r["bg"])]
            seen = set(); fall = []
            for n, v in fb:
                if re.fullmatch(r"#[0-9A-Fa-f]{6}", v) and v not in seen:
                    seen.add(v); fall.append((n, v.upper()))
            swatches = swatch_html(fall) or '<span style="opacity:.6">no colors defined</span>'

        # components section
        comps = COMPS.get(sid, default_comps[arch])
        comp_html = []
        for c in comps:
            fn = COMPONENTS.get(c)
            if not fn:
                continue
            comp_html.append(f'<section><div class="sec-h"><h2>{COMP_LABEL[c]}</h2><small>{esc(stype)}</small></div>{fn(r)}</section>')
        comps_section = "".join(comp_html) if comp_html else ""

        prev_link = f"style-{sid-1:02d}.html" if sid > 1 else "style-01.html"
        nxt = sids[sids.index(sid) + 1] if sids.index(sid) + 1 < len(sids) else sid
        next_link = f"style-{nxt:02d}.html"

        page = HEADER
        page = page.replace("%%TITLE%%", f"Style {sid} — {esc(name)} · UI Style Gallery")
        page = page.replace("%%FONTS%%", font_link(r))
        page = page.replace("%%CSS%%", css_from(r))
        page = page.replace("%%FX%%", r["fx"])
        page = page.replace("%%PREV%%", prev_link)
        page = page.replace("%%NEXT%%", next_link)
        page = page.replace("%%ID%%", f"{sid:02d}")
        page = page.replace("%%NAME%%", esc(name))
        key = (arch, variant)
        if key not in ARCH_BUILDERS:
            key = (arch, "")
        page = page.replace("%%ARCH%%", ARCH_BUILDERS[key](row, r))
        page = page.replace("%%COMPS_SECTION%%", comps_section)
        page = page.replace("%%FHNAME%%", esc(r["fh"]))
        page = page.replace("%%FBNAME%%", esc(r["fb"]))
        page = page.replace("%%SWATCHES%%", swatches)
        page = page.replace("%%BEST%%", ul_html(best))
        page = page.replace("%%AVOID%%", ul_html(avoid))
        page = page.replace("%%KW%%", "".join(f"<span>{esc(k)}</span>" for k in kws[:14]))
        page = page.replace("%%TOKENS%%", esc(tokens or "no tokens defined"))

        fn_out = os.path.join(STYLES_DIR, f"style-{sid:02d}.html")
        with open(fn_out, "w", encoding="utf-8") as f:
            f.write(page)
        entries.append((sid, name, stype, pairs))
        print(f"  {fn_out} [{arch}]")

    # index
    cards = []
    for sid, name, stype, pairs in entries:
        dots = "".join(f'<span style="background:{h}" title="{esc(n)} {h}"></span>' for n, h in pairs[:6])
        cards.append(f"""
<div class="card" data-name="{esc(name.lower())}" data-type="{esc(stype.lower())}">
<a href="styles/style-{sid:02d}.html" class="c-link">
<div class="c-top"><span class="c-no">{sid:02d}</span><span class="c-type">{esc(stype)}</span></div>
<h3>{esc(name)}</h3>
<div class="dots">{dots}</div>
</a>
</div>""")

    index_css = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0E1512;color:#E7F0EA;font-family:Inter,system-ui,sans-serif;min-height:100vh}
.wrap{max-width:1180px;margin:0 auto;padding:40px 28px 80px}
h1{font-size:clamp(1.8rem,4vw,2.8rem);letter-spacing:-.02em;margin-bottom:8px}
.sub{color:#8FA99A;margin-bottom:28px;font-size:15px}
.sub b{color:#34D399}
.search{width:100%;max-width:520px;padding:14px 20px;font-size:15px;border-radius:14px;border:1px solid #1F3A2C;background:#0F1A14;color:#E7F0EA;outline:none;margin-bottom:34px}
.search:focus{border-color:#10B981;box-shadow:0 0 0 3px rgba(16,185,129,.15)}
.search::placeholder{color:#5C7A68}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.card{background:#111B15;border:1px solid #1F3A2C;border-radius:16px;padding:18px;transition:transform .18s ease,border-color .18s ease;display:none}
.card.show{display:block}
.card:hover{transform:translateY(-4px);border-color:#10B981}
.c-link{text-decoration:none;color:inherit;display:block}
.c-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.c-no{font-size:11px;font-weight:800;color:#34D399;font-family:'JetBrains Mono',monospace;border:1px solid #1F3A2C;padding:3px 8px;border-radius:8px}
.c-type{font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;color:#8FA99A}
.card h3{font-size:15.5px;line-height:1.3;margin-bottom:14px}
.dots{display:flex;gap:5px}
.dots span{width:22px;height:22px;border-radius:7px;border:1px solid rgba(255,255,255,.15)}
.count{font-size:13px;color:#8FA99A;margin-bottom:20px}
footer{margin-top:60px;font-size:13px;color:#5C7A68;text-align:center}
"""
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UI Style Gallery — 85 Styles</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>__INDEX_CSS__</style>
</head>
<body>
<div class="wrap">
<h1>UI Style Gallery</h1>
<p class="sub"><b>85 halaman demo</b> — tiap style punya layout &amp; komponen khas berbeda</p>
<input class="search" id="q" placeholder="Cari style... (mis. neumorphism, dark, brutal, bento)">
<p class="count" id="count">Menampilkan 85 style</p>
<div class="grid">__CARDS__</div>
<footer>Generated from styles.csv · klik kartu untuk buka demo halaman style</footer>
</div>
<script>
var cards=[].slice.call(document.querySelectorAll('.card'));
var q=document.getElementById('q');
var count=document.getElementById('count');
function apply(){
 var v=q.value.trim().toLowerCase();
 var n=0;
 cards.forEach(function(c){
  var hit=!v||c.dataset.name.indexOf(v)>-1||c.dataset.type.indexOf(v)>-1;
  c.classList.toggle('show',hit);
  if(hit)n++;
 });
 count.textContent='Menampilkan '+n+' style';
}
cards.forEach(function(c){c.classList.add('show')});
q.addEventListener('input',apply);
apply();
</script>
</body>
</html>"""
    index_html = index_html.replace("__INDEX_CSS__", index_css).replace("__CARDS__", "".join(cards))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"index.html with {len(entries)} cards")

if __name__ == "__main__":
    main()
