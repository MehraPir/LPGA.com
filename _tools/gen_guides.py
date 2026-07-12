#!/usr/bin/env python3
"""One-shot generator for Cipher Munch guide pages (output committed as static HTML)."""
import html, json, os

OUT = "/Users/mehra/Developer/Websites/LPGA New"
DOMAIN = "https://www.learningplaygroundapps.com"
APP = "https://apps.apple.com/us/app/cipher-munch/id6773527361"

BADGE = '''<a class="badge-appstore" href="{app}" aria-label="Download Cipher Munch on the App Store">
<svg viewBox="0 0 180 54" role="img" aria-hidden="true" focusable="false"><rect x="0.75" y="0.75" width="178.5" height="52.5" rx="10" fill="#000" stroke="#a6a6a6" stroke-width="1.5"/><path fill="#fff" d="M36.4 27.6c0-3.4 2.8-5 2.9-5.1-1.6-2.3-4-2.6-4.9-2.7-2.1-.2-4.1 1.2-5.1 1.2-1 0-2.7-1.2-4.4-1.2-2.3 0-4.4 1.3-5.5 3.3-2.4 4.1-.6 10.1 1.7 13.4 1.1 1.6 2.4 3.4 4.2 3.4 1.7-.1 2.3-1.1 4.4-1.1 2 0 2.6 1.1 4.4 1.1 1.8 0 3-1.6 4.1-3.3 1.3-1.9 1.8-3.7 1.8-3.8-.1 0-3.5-1.4-3.6-5.2zM33 17.6c.9-1.1 1.5-2.7 1.4-4.3-1.3.1-3 .9-3.9 2-.9 1-1.6 2.6-1.4 4.1 1.5.1 3-.7 3.9-1.8z"/><text x="48" y="22" fill="#fff" font-family="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif" font-size="10.5" letter-spacing="0.4">Download on the</text><text x="48" y="41" fill="#fff" font-family="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif" font-size="19" font-weight="600">App Store</text></svg></a>'''.format(app=APP)

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{domain}/assets/img/og-image.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" type="image/png" sizes="64x64" href="/assets/img/favicon-64.png" />
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600..700&family=IBM+Plex+Mono:wght@400;600&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/css/site.css" />
  <script defer src="/assets/js/site.js"></script>
  {jsonld}
</head>
<body>
  <header class="site-header">
    <nav class="nav" aria-label="Primary navigation">
      <a class="brand" href="/">
        <img src="/assets/img/app-icon-256.png" alt="Cipher Munch app icon" width="34" height="34" />
        <span>Cipher Munch</span>
      </a>
      <ul class="nav-links">
        <li><a href="/#how-it-works">How it works</a></li>
        <li><a href="/#codebusters">For Codebusters</a></li>
        <li><a href="/guides/"{guides_current}>Guides</a></li>
        <li><a href="/#faq">FAQ</a></li>
        <li><a class="nav-cta" href="''' + APP + '''">Download</a></li>
      </ul>
    </nav>
  </header>
'''

FOOTER = '''
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <h4>Learning Playground Apps</h4>
          <p>An independent studio making playful, brainy iOS apps. Cipher Munch is our love letter to classical ciphers, and to the coaches and students who race to crack them.</p>
        </div>
        <div>
          <h4>Guides</h4>
          <ul>
            <li><a href="/guides/codebusters-practice-app/">Codebusters practice</a></li>
            <li><a href="/guides/codebusters-team-practice/">For coaches</a></li>
            <li><a href="/guides/cryptograms-for-beginners/">For beginners</a></li>
            <li><a href="/guides/printable-cryptogram-puzzles/">Printable puzzles</a></li>
            <li><a href="/guides/">All guides</a></li>
          </ul>
        </div>
        <div>
          <h4>App</h4>
          <ul>
            <li><a href="''' + APP + '''">Download on the App Store</a></li>
            <li><a href="/privacy-policy.html">Privacy policy</a></li>
            <li><a href="/terms-of-use.html">Terms of use</a></li>
            <li><a href="mailto:LearningPlayGroundApps@gmail.com">Contact</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-base">
        <span>© 2026 Learning Playground Apps. All rights reserved.</span>
        <span>Made for code crackers everywhere. Android coming soon.</span>
      </div>
    </div>
  </footer>
</body>
</html>
'''

CTA = '''<div class="article-cta">
  <h2 style="font-family:var(--font-display);font-weight:620;font-size:1.6rem;margin-bottom:10px;">{cta_head}</h2>
  <p style="margin-bottom:22px;">{cta_sub}</p>
  <div class="hero-ctas" style="justify-content:center;">''' + BADGE + '''<span class="android-note">Android: coming soon</span></div>
</div>'''

GUIDES = {}  # slug -> dict; populated below, order preserved (py3.7+)

def G(slug, **kw):
    GUIDES[slug] = kw

# ---------------------------------------------------------------- guide 1
G("codebusters-practice-app",
  tag="Competition",
  title="The Codebusters Practice App: How Students Train with Cipher Munch",
  page_title="Codebusters Practice App: Train for Science Olympiad | Cipher Munch",
  desc="How Science Olympiad students use Cipher Munch as a Codebusters practice app: Aristocrats, Patristocrats, Xenocrypts, timed stats, and print-ready puzzles.",
  dek="Codebusters rewards one thing above all: reps. Here's how to turn a phone or iPad into a daily training tool for every cipher on the test.",
  cta_head="Start your Codebusters training today",
  cta_sub="Free Starter packs for every Codebusters cipher type. No ads, no account: just practice.",
  related=["codebusters-team-practice", "aristocrat-practice", "improve-cryptogram-solving-speed"],
  body="""
<p>If you compete in Science Olympiad Codebusters, you already know the uncomfortable truth: the students who win aren't the ones who memorized the most theory. They're the ones who have solved hundreds of ciphers, so the patterns jump off the page. Cipher Munch was designed for exactly that kind of volume practice. It's a cryptogram app built by and for people who care about the competition formats.</p>

<h2>Every Codebusters cipher format, in one app</h2>
<p>Cipher Munch covers the classical-cipher events that appear on Division B and C tests:</p>
<ul>
  <li><strong>Aristocrats</strong>: classic monoalphabetic substitution with spaces preserved, including <strong>K1 and K2 keyword</strong> variants</li>
  <li><strong>Patristocrats K1 &amp; K2</strong>: letters regrouped into 5-letter blocks with no word boundaries</li>
  <li><strong>Xenocrypts</strong>: Spanish-language Aristocrats on the 27-letter alphabet, Ñ included</li>
  <li><strong>Caesar</strong>: using the forward-shift convention you'll see in competition materials</li>
  <li><strong>Affine and Atbash</strong>: plus visual ciphers (Pigpen, Dancing Men, Knights Templar) for warming up</li>
</ul>
<p>Every puzzle hides a real quote, the same way competition questions do, so you also build the "this word is probably <em>THE</em> or <em>THAT</em>" instincts that only come from quote-shaped plaintext.</p>

<h2>Train with helpers on, compete with them off</h2>
<p>The core of the app is a set of helper tools you can toggle per cipher, which makes it work at any level:</p>
<div class="callout"><span class="tag">In the app</span>
<p>Open any puzzle → <strong>Options</strong> → Display. Toggle <strong>letter frequencies</strong>, <strong>multiple-letter highlighting</strong>, <strong>error highlighting</strong>, and <strong>translation tables</strong> independently for each cipher type. Your settings stick, per cipher.</p></div>
<p>A training progression that works well:</p>
<ol>
  <li><strong>Learning a cipher:</strong> everything on. Frequencies under each letter, matching cells highlighted, errors flagged when the board is full.</li>
  <li><strong>Getting comfortable:</strong> turn off error highlighting. Now you have to check your own work: exactly what the test demands.</li>
  <li><strong>Competition mode:</strong> frequencies off too. You're now solving under test conditions, and your solve times tell you honestly where you stand.</li>
</ol>

<h2>Make it feel like the real test</h2>
<p>Codebusters is a pencil-and-paper event. When you want practice that matches the medium, print the puzzle:</p>
<div class="callout"><span class="tag">In the app</span>
<p><strong>Print / Share</strong> lets you print any puzzle with the frequency table included or hidden, with or without your current answers, and share it as a PDF: a one-tap way to recreate the paper test setup at home or at practice.</p></div>

<h2>Measure readiness, not vibes</h2>
<p>The Statistics screen tracks solves per cipher type, fastest and average times, and how many puzzles you solved with hints. Before a tournament, look at your average time on hint-free Aristocrats: that number is your realistic pace, and it tells you how many questions your team should assign you on test day. The daily streak on the main menu keeps the habit alive between tournaments.</p>

<h2>What it costs</h2>
<p>Every cipher type has a free Starter pack, so a full training loop costs nothing to try. When you need more volume, you can unlock a single volume of one cipher, subscribe to one cipher type, or get All Access. There are no ads either way: nothing interrupts a timed solve.</p>
""")

# ---------------------------------------------------------------- guide 2
G("codebusters-team-practice",
  tag="Coaches",
  title="Running Codebusters Team Practice with One App",
  page_title="Codebusters Team Practice for Coaches | Cipher Munch",
  desc="A coach's guide to running Science Olympiad Codebusters team practice with Cipher Munch: printable cipher tests, per-student assignments, and progress you can verify.",
  dek="You don't have time to hand-write cipher tests every week. Here's a practice structure where the app does the preparation and you do the coaching.",
  cta_head="Give your team a shared practice tool",
  cta_sub="Free Starter packs on every student's device. Print unlimited paper practice from any of them.",
  related=["codebusters-practice-app", "printable-cryptogram-puzzles", "improve-cryptogram-solving-speed"],
  body="""
<p>Ask any Codebusters coach what eats their prep time and the answer is the same: making practice material. Writing clean ciphers, checking the encryption, formatting the sheet, making an answer key. It's an hour of work for fifteen minutes of practice. Cipher Munch removes that bottleneck: thousands of pre-built, verified puzzles in every competition format, each one printable as a clean sheet.</p>

<h2>The paper session, without the prep</h2>
<p>Codebusters is solved on paper, so paper practice matters. From any puzzle in the app:</p>
<div class="callout"><span class="tag">In the app</span>
<p>Open a puzzle → <strong>Print / Share</strong>. Choose whether the sheet includes <strong>frequency counts under each letter</strong>, a <strong>frequency table</strong>, or neither (harder). Print directly to AirPrint or share a PDF to the team group chat. The app also includes a printable <strong>cipher reference sheet</strong> (alphabets and common word patterns) modeled on what solvers actually use.</p></div>
<p>A practical weekly rhythm: pick three puzzles (one Aristocrat, one Patristocrat, one Xenocrypt), print a class set with frequency tables on, and run it timed. Students who finish early re-solve without the table.</p>

<h2>Assign ciphers the way you assign events</h2>
<p>Most teams split the test: someone owns Xenocrypts, someone owns the math ciphers, everyone shares Aristocrats. The app's per-cipher packs mirror that. Have each student install the app (the Starter packs are free), then assign packs by role: your Xenocrypt specialist lives in the Xenocrypt packs, your speed solvers grind Aristocrats. Because helper settings are per-cipher, each student can train their event at their own difficulty.</p>

<h2>Progress you can actually check</h2>
<p>"Did you practice this week?" is an unanswerable question. "Show me your stats screen" is not.</p>
<div class="callout"><span class="tag">In the app</span>
<p>The <strong>Statistics</strong> screen shows solves this week and this month, per-cipher totals, hint usage, and fastest/average times. The <strong>daily streak</strong> on the main menu shows at a glance whether practice happened. Ask students to screenshot it at the end of each week: a 30-second accountability system.</p></div>
<p>Watch the <em>no-hints</em> numbers, not the totals. A student solving five Aristocrats a week without hints is closer to tournament-ready than one solving twenty with reveals.</p>

<h2>Why it works in a school setting</h2>
<ul>
  <li><strong>No accounts, no sign-ups</strong>: nothing for a school device policy to object to, no student data collected.</li>
  <li><strong>Works offline</strong>: practice rooms with no Wi-Fi, buses to tournaments, it doesn't matter.</li>
  <li><strong>No ads</strong>: nothing age-inappropriate appears, ever, because nothing appears at all.</li>
  <li><strong>Free to start</strong>: every cipher type has a free Starter pack, so the whole team can begin without a purchase.</li>
</ul>
""")

# ---------------------------------------------------------------- guide 3
G("aristocrat-practice",
  tag="Ciphers",
  title="Aristocrat Practice: From First Solve to K1 and K2 Keywords",
  page_title="Aristocrat Cipher Practice: K1 & K2 Keyword Cryptograms | Cipher Munch",
  desc="Practice Aristocrat cryptograms the smart way: a difficulty ladder from plain Aristocrats to K1 and K2 keyword ciphers, using Cipher Munch's frequency and highlighting tools.",
  dek="Aristocrats are the heart of every Codebusters test and every cryptogram book. Here's a practice ladder that takes you from your first solve to keyword-spotting.",
  cta_head="Thousands of Aristocrats are waiting",
  cta_sub="Plain, K1, and K2 packs: each with a free Starter pack and helpers you control.",
  related=["patristocrat-practice", "letter-frequency-analysis", "codebusters-practice-app"],
  body="""
<p>An Aristocrat is the classic cryptogram: every letter of a quote swapped for another letter, spaces and punctuation left intact. It's also the highest-value skill in Codebusters: Aristocrats are the bulk of most tests. Cipher Munch has dedicated packs for all three variants: plain Aristocrats, K1, and K2.</p>

<h2>The ladder: plain → K1 → K2</h2>
<p>In a <strong>plain Aristocrat</strong>, the substitution alphabet is random. In <strong>K1</strong>, the plaintext alphabet is built from a keyword; in <strong>K2</strong>, the ciphertext alphabet is. That keyword is a gift: once you've recovered part of the alphabet, the keyword's consecutive run lets you predict letters you haven't solved yet. Practicing all three teaches you to notice which kind you're holding: a real point-scorer in competition, where identifying the keyword can finish the puzzle for you.</p>
<div class="callout"><span class="tag">In the app</span>
<p>Cipher Munch's frequency grid arranges its rows the traditional way for each variant: for K1 the plain-letter row sits at the bottom, for K2 it sits on top, so you learn to look for the keyword where the convention puts it. The keyword always appears as a consecutive run; spotting it is a skill the grid layout quietly trains.</p></div>

<h2>Use the helpers as training wheels, deliberately</h2>
<p>Each helper answers one question you'd otherwise answer by hand:</p>
<ul>
  <li><strong>Letter frequencies</strong>: how often does each cipher letter appear? (Your <em>E</em>, <em>T</em>, and <em>A</em> candidates.)</li>
  <li><strong>Multiple-letter highlighting</strong>: where else does this letter occur? (Test a guess everywhere at once.)</li>
  <li><strong>Error highlighting</strong>: when the board is full, is anything wrong? (Instant feedback while learning.)</li>
</ul>
<p>The point isn't to keep them all on forever. Solve ten puzzles with everything on, then turn off error highlighting and re-check your own logic. When your accuracy holds, drop the frequency display and count patterns yourself. Every helper you remove converts app skill into paper skill.</p>

<h2>A 20-minute daily session</h2>
<ol>
  <li>One warm-up Aristocrat with all helpers on: get the pattern-brain moving.</li>
  <li>Two puzzles at your training level (helpers partially off), aiming for clean, hint-free solves.</li>
  <li>Check the stats screen: is your average time trending down this week?</li>
</ol>
<p>The app's daily streak counter makes the habit visible, and hints (10 free per day) are there when a puzzle has you truly stuck: better to reveal one letter and finish than to quit.</p>
""")

# ---------------------------------------------------------------- guide 4
G("patristocrat-practice",
  tag="Ciphers",
  title="Patristocrat Practice Without Word Boundaries",
  page_title="Patristocrat Practice: Cryptograms Without Spaces | Cipher Munch",
  desc="How to practice Patristocrats: cryptograms with no word boundaries, grouped in 5-letter blocks. Which helpers matter most, and how to move up from Aristocrats.",
  dek="Take away the spaces and a friendly Aristocrat becomes a Patristocrat: the puzzle that separates casual solvers from competitors. Here's how to train for it.",
  cta_head="Ready to lose the spaces?",
  cta_sub="Patristocrat K1 and K2 packs, presented in true 5-letter blocks. Free Starter pack included.",
  related=["aristocrat-practice", "letter-frequency-analysis", "codebusters-practice-app"],
  body="""
<p>A Patristocrat is an Aristocrat with the word spaces stripped out and the letters regrouped into blocks of five. Same cipher, same quote, but without word shapes, most beginner techniques (one-letter words, apostrophes, <em>THE</em>-hunting) vanish. What's left is pure frequency work and pattern recall, which is why Patristocrats carry high point values in Codebusters.</p>

<h2>What actually gets harder</h2>
<p>Without boundaries you lose entry points, not information. The letter frequencies are identical to an Aristocrat's; you just have to lean on them harder. Double letters, common digraphs (<em>TH</em>, <em>ER</em>, <em>IN</em>), and repeated trigrams become your handholds. Cipher Munch presents Patristocrats in authentic 5-letter blocks, so your eye learns to scan across block breaks: a small thing that matters, because a word can straddle two blocks on the real test too.</p>
<div class="callout"><span class="tag">In the app</span>
<p>Turn on <strong>letter frequencies</strong> and <strong>multiple-letter highlighting</strong> for Patristocrats even if you've turned them off for Aristocrats. Tapping a cell and seeing every occurrence light up across the blocks is how you find the repeated fragments that word spacing used to show you for free.</p></div>

<h2>Moving up from Aristocrats</h2>
<p>Don't start Patristocrats until plain Aristocrats feel comfortable. The frustration isn't worth it. When you're ready:</p>
<ol>
  <li>Solve a few with <strong>hints</strong>: reveal two letters up front (competition tests often give you one crib anyway) and finish from there.</li>
  <li>Then go hint-free with full helpers. Your first solves may take three times your Aristocrat pace. That's normal.</li>
  <li>As block-scanning becomes natural, strip the helpers the same way you did for Aristocrats.</li>
</ol>

<h2>K1 and K2 still apply</h2>
<p>Cipher Munch's Patristocrat packs come in K1 and K2 keyword variants, just like the competition. The keyword-recovery skill you built on Aristocrats transfers directly, and in a spaceless puzzle, recovering the keyword alphabet is often the fastest path to the finish, because it hands you letters that frequency analysis alone hasn't confirmed yet.</p>

<h2>Paper practice matters double here</h2>
<p>On paper you can't tap a letter to see its twins highlighted. You have to mark them up yourself. Print a few Patristocrats each week (Print / Share, frequency table on) and solve them with a pencil. The app builds the pattern instincts; the paper session proves they survive without the touchscreen.</p>
""")

# ---------------------------------------------------------------- guide 5
G("xenocrypt-practice",
  tag="Ciphers",
  title="Xenocrypt Practice: Spanish Cryptograms with the Ñ",
  page_title="Xenocrypt Practice: Spanish Cryptograms for Codebusters | Cipher Munch",
  desc="Practice Xenocrypts: Spanish-language cryptograms on the 27-letter alphabet with Ñ, the way they appear in Science Olympiad Codebusters. No fluent Spanish required.",
  dek="Every Codebusters test has at least one Spanish cryptogram, and most teams under-prepare for it. That's your opportunity.",
  cta_head="Own the Xenocrypt question",
  cta_sub="Spanish Aristocrats on the true 27-letter alphabet, with a free Starter pack to begin.",
  related=["codebusters-practice-app", "aristocrat-practice", "letter-frequency-analysis"],
  body="""
<p>A Xenocrypt is an Aristocrat in Spanish. It's guaranteed material on Science Olympiad Codebusters tests, and because most students practice it least, the team member who trains Xenocrypts seriously becomes disproportionately valuable. Cipher Munch has dedicated Xenocrypt packs built the way the competition builds them.</p>

<h2>The 27-letter alphabet is not a detail</h2>
<p>Spanish adds <strong>Ñ</strong> between N and O, making a 27-letter alphabet. A substitution over 27 letters behaves differently from one over 26: your alphabet-tracking habits need to account for the extra row. Many casual puzzle apps ignore this and just use English ciphers with Spanish words; Cipher Munch uses the genuine 27-letter alphabet, so what you practice is what you'll see on the test.</p>
<div class="callout"><span class="tag">In the app</span>
<p>Xenocrypt puzzles run on the full <strong>A–Z plus Ñ</strong> alphabet, with the custom keyboard adapted to match. Frequency counts and highlighting work exactly as they do in English Aristocrats: the tools transfer, only the language changes.</p></div>

<h2>You don't need fluent Spanish</h2>
<p>You need perhaps thirty words. <em>DE, LA, EL, QUE, EN, NO, ES, UN, SE, POR</em> do the work that <em>THE, AND, THAT</em> do in English. Spanish frequency order starts <strong>E-A-O-S</strong> (not E-T-A-O), vowels are unusually common, and <em>Q</em> is almost always followed by <em>UE</em> or <em>UI</em>. Those few facts, drilled across enough puzzles, solve competition Xenocrypts reliably. The app's built-in reference sheet includes common Spanish word patterns alongside the English ones, so the crib list is always one tap away.</p>

<h2>A realistic training plan</h2>
<ol>
  <li><strong>Weeks 1–2:</strong> solve with frequencies on and the reference sheet open. Expect to lean on hints; that's fine. You're memorizing the short-word vocabulary through use.</li>
  <li><strong>Weeks 3–4:</strong> hint-free with helpers on. Start noticing <em>-CIÓN</em>, <em>-MENTE</em>, and doubled <em>LL</em>/<em>RR</em> patterns without prompting.</li>
  <li><strong>Ongoing:</strong> two hint-free Xenocrypts per week keeps the vocabulary warm, and the per-cipher stats screen shows your times converging toward your English Aristocrat pace.</li>
</ol>

<h2>For the team</h2>
<p>If you're the designated Xenocrypt solver, print a couple of puzzles for paper practice before each tournament (Print / Share handles the Ñ and accents cleanly). If you're a coach, this is the single highest-leverage assignment you can make: one student, two puzzles a week, and the Xenocrypt points stop being a coin flip.</p>
""")

# ---------------------------------------------------------------- guide 6
G("cryptograms-for-beginners",
  tag="Start here",
  title="Cryptograms for Beginners: Your First Week of Solving",
  page_title="Cryptograms for Beginners: Learn to Solve Step by Step | Cipher Munch",
  desc="Never solved a cryptogram? A gentle first week: start with visual ciphers like Pigpen, use translation tables and hints, and work up to your first real Aristocrat.",
  dek="Cryptograms look like magic tricks until someone shows you the first move. Here's a first week that makes the magic learnable, no experience required.",
  cta_head="Solve your first cipher tonight",
  cta_sub="Free Starter packs, 10 free hints a day, and helpers that make the first puzzle a joy instead of a wall.",
  related=["letter-frequency-analysis", "improve-cryptogram-solving-speed", "printable-cryptogram-puzzles"],
  body="""
<p>The mistake most beginners make is starting with a hard puzzle, staring at it, and deciding cryptograms aren't for them. The fix is sequencing: start where the code is visible, and add difficulty only as each level starts to feel easy. Cipher Munch's twelve cipher types happen to form a perfect beginner's staircase.</p>

<h2>Days 1–2: visual ciphers, table on</h2>
<p>Start with <strong>Pigpen</strong> or the <strong>Dancing Men</strong> (the stick-figure cipher from Sherlock Holmes). Each symbol maps to one letter, and the app shows you the whole key:</p>
<div class="callout"><span class="tag">In the app</span>
<p>For visual ciphers, turn on <strong>Show translation table</strong> in Options → Display. The full symbol-to-letter key appears under the puzzle: solving becomes a satisfying lookup game while your brain quietly learns how substitution works.</p></div>
<p>This stage teaches the core loop (map a symbol, fill a cell, watch words appear) without any guessing.</p>

<h2>Days 3–4: Atbash and Caesar, decoder in hand</h2>
<p><strong>Atbash</strong> mirrors the alphabet (A↔Z, B↔Y). <strong>Caesar</strong> shifts it by a fixed amount. Both have a single "aha": find the rule and the whole puzzle opens. The app gives each one a proper tool: a translation table for Atbash, and for Caesar a manual <strong>decoder strip</strong> you rotate with +/− buttons until real words appear in the preview. Feeling the shift click into place teaches you what "breaking" a cipher actually means.</p>

<h2>Days 5–7: your first Aristocrat, all helpers on</h2>
<p>Now the real thing: a quote where every letter is swapped for another. Turn everything on: <strong>letter frequencies</strong>, <strong>multiple-letter highlighting</strong>, <strong>error highlighting</strong>. Then use the beginner's opening moves:</p>
<ul>
  <li>A single-letter word is <em>A</em> or <em>I</em>.</li>
  <li>The most frequent cipher letter is probably <em>E</em> or <em>T</em>.</li>
  <li>A three-letter word starting a sentence is very often <em>THE</em>, and if it is, you just earned three letters everywhere at once.</li>
</ul>
<p>Stuck anyway? Use a hint. You get <strong>10 free hints a day</strong>, and revealing one letter to keep momentum is better teaching than giving up. Nobody is grading your first week.</p>

<h2>What makes this a good place to learn</h2>
<p>No ads interrupt a solve. No account nags you. It works offline on a plane or in a waiting room. And every puzzle ends with a real quote worth reading, so even a slow solve pays you something. When the first Aristocrat falls, you'll know exactly what to do next: solve another one.</p>
""")

# ---------------------------------------------------------------- guide 7
G("printable-cryptogram-puzzles",
  tag="Print",
  title="Printable Cryptogram Puzzles, Straight from Your Phone",
  page_title="Printable Cryptogram Puzzles: Print Custom Cipher Sheets | Cipher Munch",
  desc="Print cryptogram puzzles with exactly the helpers you want: frequency tables on or off, answers included or blank. Perfect for classrooms, road trips, and competition practice.",
  dek="Sometimes the best solving surface is still a sheet of paper. Cipher Munch turns any of its thousands of puzzles into a print-ready page, with you choosing what appears on it.",
  cta_head="Your printer is about to get busier",
  cta_sub="Thousands of puzzles, each one print-ready with the helpers you choose.",
  related=["codebusters-team-practice", "cryptograms-for-beginners", "cryptogram-app-no-ads-offline"],
  body="""
<p>Search for printable cryptograms and you'll find worksheet sites with a dozen puzzles of unknown quality and a fixed format. Cipher Munch takes the opposite approach: every one of its thousands of hand-checked puzzles is printable, and <em>you</em> decide what the printed page includes.</p>

<h2>You control the sheet</h2>
<div class="callout"><span class="tag">In the app</span>
<p>Open any puzzle → <strong>Print / Share</strong>. The settings panel lets you toggle: <strong>frequency counts under each letter</strong>, a <strong>frequency table</strong> below the puzzle, <strong>your current answers</strong> filled into the boxes, and <strong>multiple-letter highlighting</strong>. Print via AirPrint or export a PDF to share.</p></div>
<p>That flexibility maps to real situations:</p>
<ul>
  <li><strong>Easy mode</strong> (frequency table on): great for kids, classrooms, and first-timers.</li>
  <li><strong>Competition mode</strong> (all helpers off): a bare cipher, exactly like a Codebusters test question.</li>
  <li><strong>Resume-on-paper</strong> (current answers on): started on the couch, finish at the kitchen table.</li>
  <li><strong>Answer key</strong>: solve it in the app first, then print with answers filled: instant key for whoever grades.</li>
</ul>

<h2>Who prints, and why</h2>
<p><strong>Coaches</strong> print class sets for timed paper sessions: Codebusters is a pencil event, and paper practice is the last mile of preparation. <strong>Teachers</strong> print Pigpen and Dancing Men sheets as puzzle-table activities; the visual ciphers print beautifully. <strong>Families</strong> print a stack for road trips and waiting rooms: the same puzzles work on paper with zero battery. And plenty of solvers simply think better with a pencil.</p>

<h2>The reference sheet</h2>
<p>The app also includes a printable <strong>cipher reference sheet</strong>: the cipher alphabets (including Pigpen and Dancing Men symbol keys), common English word patterns, and common Spanish patterns for Xenocrypt work. Print it once and it lives next to the puzzle stack: the same kind of aid competitive solvers build for themselves, already assembled.</p>

<h2>Print quality that respects the puzzle</h2>
<p>Printed sheets use a clean, high-contrast layout: answer boxes under each cipher letter, frequency numbers set small and unobtrusive, Spanish characters (Ñ, accents) rendered correctly. No web-page clutter, no URL headers full of ink: a sheet that looks like it came from a puzzle book, because the app was designed by people who solve on paper too.</p>
""")

# ---------------------------------------------------------------- guide 8
G("cryptogram-app-no-ads-offline",
  tag="Quality of life",
  title="A Cryptogram App with No Ads That Works Offline",
  page_title="Cryptogram App with No Ads: Works Offline, No Account | Cipher Munch",
  desc="Cipher Munch is a cryptogram app with no ads, no tracking, no account, and full offline play. Free Starter packs, one-time purchases, and private iCloud sync.",
  dek="Nothing breaks a solving trance like a video ad. Cipher Munch was built on a simple promise: the puzzle, the quote, and you: nothing else.",
  cta_head="No ads. No account. No Wi-Fi needed.",
  cta_sub="Download free and see what an interruption-free cryptogram app feels like.",
  related=["cryptograms-for-beginners", "printable-cryptogram-puzzles", "improve-cryptogram-solving-speed"],
  body="""
<p>Most free puzzle apps monetize your attention: an ad between puzzles, an ad for a hint, a banner crawling under the board. For a game that's entirely about concentration, that model is self-defeating. Cipher Munch has <strong>no ads at all</strong>: not "fewer," not "removable for a fee." None. The business model is puzzles: the content is what you can buy, never your attention.</p>

<h2>Fully offline, by design</h2>
<p>Every puzzle ships inside the app. There's no server to reach, no content to stream, no login to validate:</p>
<ul>
  <li><strong>Airplane mode</strong>: the entire app works, every feature, every puzzle.</li>
  <li><strong>School networks</strong>: nothing to block, because nothing is requested.</li>
  <li><strong>Cabins, campsites, subways</strong>: thousands of puzzles in your pocket, zero bars required.</li>
</ul>

<h2>No account, and nothing to leak</h2>
<p>There is no sign-up because there is nothing to sign up for. The app collects no personal data, uses no third-party analytics or advertising SDKs, and does no cross-app tracking: the App Store privacy label is the short kind. It's the sort of app you can put on a child's iPad or a school device without reading anything twice. (The full details are in the <a href="/privacy-policy.html">privacy policy</a>, which is refreshingly short.)</p>

<h2>Your progress still follows you</h2>
<p>No account doesn't mean no continuity:</p>
<div class="callout"><span class="tag">In the app</span>
<p>Progress and stats sync through <strong>your own private iCloud</strong>: automatically, with no login, invisible even to the developer. Get a new iPhone, open the app, and your streak, stats, and solved puzzles are already there. Turn it off anytime in iOS Settings if you'd rather stay fully local.</p></div>

<h2>What "free" actually means here</h2>
<p>Every one of the twelve cipher types includes a <strong>free Starter pack</strong>: enough for genuine daily practice, not a five-puzzle teaser. You also get <strong>10 free hints a day</strong>. When you want more volume, the upgrades are honest: buy one volume outright (a one-time purchase, yours forever), subscribe to a single cipher type, or get All Access. No energy meters, no timers, no "watch an ad to continue." You will never be interrupted mid-solve, because there is nothing in the app whose job is to interrupt you.</p>
""")

# ---------------------------------------------------------------- guide 9
G("improve-cryptogram-solving-speed",
  tag="Training",
  title="How to Get Faster at Cryptograms (and Prove It)",
  page_title="Get Faster at Cryptograms: Track Solve Times & Progress | Cipher Munch",
  desc="A training-log approach to cryptogram speed: baseline your solve times, practice on a streak, remove helpers progressively, and watch the stats curve bend.",
  dek="“Am I getting better?” shouldn't be a feeling. With per-cipher stats, solve times, and streaks, Cipher Munch turns practice into a training log.",
  cta_head="Start your streak today",
  cta_sub="Solve one puzzle a day and let the stats tell the story. Free to start.",
  related=["codebusters-practice-app", "aristocrat-practice", "letter-frequency-analysis"],
  body="""
<p>Runners don't guess whether they're getting faster: they have times. Cryptogram solvers mostly guess. Cipher Munch closes that gap: every solve is timed, every cipher type is tracked separately, and the app quietly builds the training log you'd never keep by hand.</p>

<h2>Step 1: get a baseline</h2>
<p>Solve five hint-free Aristocrats at your normal pace. Then open <strong>Statistics</strong>:</p>
<div class="callout"><span class="tag">In the app</span>
<p>The stats screen shows <strong>puzzles solved</strong> (today, this week, this month, all-time), your <strong>fastest and average solve times</strong>, an <strong>activity chart</strong> with hint-free and with-hints series shown separately, and per-cipher completion. That average time is your baseline: write it down, or just remember the chart's shape.</p></div>

<h2>Step 2: make practice unskippable</h2>
<p>Speed comes from frequency of practice more than from any technique. The <strong>daily streak</strong> counter sits on the main menu, and it only asks for one puzzle a day. One easy Atbash on a busy day keeps the chain alive; the chain keeps you opening the app; opening the app is 90% of practice. The achievement system layers on top: badges for totals, per-cipher milestones, and streak lengths, each shareable as a gold medallion when you want to gloat responsibly.</p>

<h2>Step 3: remove one helper at a time</h2>
<p>Speed you owe to the helpers isn't speed you own. Every few weeks, turn one off (error highlighting first, then frequency counts) and let your average time absorb the hit. It will recover within a week or two, and the recovered speed is real: it comes from pattern recall in your head, not tools on the screen. This is the single most reliable way to bend the curve, and the per-cipher toggle memory means you can run different levels for different ciphers (training wheels on Patristocrats, none on Aristocrats).</p>

<h2>Step 4: read the chart honestly</h2>
<p>Two things to watch in the activity chart: the <strong>hint-free share</strong> of your solves should grow over time, and your <strong>average time</strong> should fall <em>within a cipher type</em> (comparing Aristocrat times to Patristocrat times tells you nothing). A plateau isn't failure: it usually means the current difficulty has been absorbed and it's time to move up a volume, drop a helper, or add a harder cipher.</p>

<h2>Speed tools worth knowing</h2>
<p>On iPad or Mac, use a <strong>hardware keyboard</strong>: arrow keys move around the board and typing maps letters instantly, easily worth a minute per puzzle. On iPhone, the custom keyboard is tuned for letter-mapping with the editing cell and its matches shown in distinct colors, so you always know where you are mid-thought.</p>
""")

# ---------------------------------------------------------------- guide 10
G("letter-frequency-analysis",
  tag="Technique",
  title="Letter Frequency Analysis: The Solver's Superpower",
  page_title="Letter Frequency Analysis for Cryptograms: ETAOIN Explained | Cipher Munch",
  desc="How letter frequency analysis cracks substitution ciphers: ETAOIN in English, EAOS in Spanish, and how Cipher Munch's frequency tools train the skill into instinct.",
  dek="Every substitution cipher leaks the same secret: how often each letter appears. Learn to read the leak and no cryptogram is safe from you.",
  cta_head="Put frequency analysis to work",
  cta_sub="Frequency tools built into every puzzle: on while you learn, off when you don't need them anymore.",
  related=["aristocrat-practice", "patristocrat-practice", "xenocrypt-practice"],
  body="""
<p>Substitution ciphers hide <em>which</em> letter is which, but they can't hide <em>how often</em> each letter appears. English text is roughly 13% <em>E</em> and 9% <em>T</em>; those proportions survive encryption untouched. Frequency analysis (counting cipher letters and matching the counts to known language statistics) has been breaking these ciphers since the 9th century, and it's the first real technique every cryptogram solver learns.</p>

<h2>ETAOIN SHRDLU, and what to do with it</h2>
<p>The most common English letters, in order: <strong>E T A O I N S H R D L U</strong>. In a decent-length cryptogram, the most frequent cipher letter is very likely <em>E</em> or <em>T</em>. That single guess, tested against word shapes (does it make <em>THE</em> work? does a doubled pair become <em>EE</em> or <em>TT</em>?), starts the chain reaction that unravels the whole puzzle. Frequency gives you the hypothesis; the words confirm it.</p>
<div class="callout"><span class="tag">In the app</span>
<p>Cipher Munch can show the count <strong>under every cipher letter</strong> in the grid, or as a <strong>frequency table</strong> below the puzzle: your choice in Options → Display. No hand-tallying on scratch paper: the analysis layer is just <em>there</em>, so you can spend your attention on the deductions.</p></div>

<h2>It changes by language, and the app knows</h2>
<p>Spanish frequency order begins <strong>E A O S R N I</strong>: vowels are more common than in English, and <em>T</em> drops far down the list. If you carry English instincts into a Xenocrypt, your first guesses will be wrong in a consistent, fixable way. Practicing Spanish puzzles with frequencies visible recalibrates your instincts fast, and the built-in reference sheet keeps both languages' statistics one tap away.</p>

<h2>Where frequency analysis shines (and where it doesn't)</h2>
<p>It's strongest exactly where other techniques are weakest: <strong>Patristocrats</strong>, where no word boundaries exist and counting is most of what you have. It's least useful for <strong>Caesar</strong> ciphers: one confirmed letter reveals the entire shift, so counting is overkill. Cipher Munch reflects that honestly: the frequency table is hidden for Caesar puzzles, and you get a rotating decoder strip instead, because that's the tool that matches the cipher.</p>

<h2>The endgame: turning it off</h2>
<p>Competition solvers don't get an app-computed table: they count. But here's the twist: after a few hundred assisted solves, you barely need to. You'll recognize an <em>E</em>-shaped distribution at a glance, notice the suspiciously rare letters (hello, <em>Q</em> and <em>Z</em> candidates), and feel when a puzzle's statistics are lying to you (short quotes get weird). At that point, turn the frequency display off in Options and enjoy the strange new sensation of doing the analysis by instinct. The tool taught you; now the skill is yours.</p>
""")

# ---------------------------------------------------------------- render
def jsonld_article(g, canonical):
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": g["title"],
        "description": g["desc"],
        "image": DOMAIN + "/assets/img/og-image.jpg",
        "author": {"@type": "Organization", "name": "Learning Playground Apps"},
        "publisher": {"@type": "Organization", "name": "Learning Playground Apps",
                      "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/img/app-icon-512.png"}},
        "mainEntityOfPage": canonical,
        "about": {"@type": "MobileApplication", "name": "Cipher Munch",
                  "url": "https://apps.apple.com/us/app/cipher-munch/id6773527361"}
    }, ensure_ascii=False) + '</script>\n<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Cipher Munch", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": DOMAIN + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": g["title"], "item": canonical}
        ]
    }, ensure_ascii=False) + '</script>'

def card(slug):
    g = GUIDES[slug]
    return ('<a class="guide-card" href="/guides/%s/"><span class="tag">%s</span><h3>%s</h3>'
            '<p>%s</p><span class="more">Read the guide →</span></a>'
            % (slug, html.escape(g["tag"]), html.escape(g["title"]), html.escape(g["dek"].split(". ")[0] + ".")))

for slug, g in GUIDES.items():
    canonical = f"{DOMAIN}/guides/{slug}/"
    page = HEAD.format(title=html.escape(g["page_title"]), desc=html.escape(g["desc"]),
                       canonical=canonical, domain=DOMAIN, jsonld=jsonld_article(g, canonical),
                       guides_current=' aria-current="page"')
    page += f'''
  <main>
    <div class="article-hero">
      <div class="wrap">
        <p class="breadcrumb"><a href="/">Cipher Munch</a> / <a href="/guides/">Guides</a> / {html.escape(g["tag"])}</p>
        <p class="eyebrow">{html.escape(g["tag"])}</p>
        <h1>{html.escape(g["title"])}</h1>
        <p class="dek">{g["dek"]}</p>
      </div>
    </div>
    <article class="article wrap">
{g["body"]}
{CTA.format(cta_head=html.escape(g["cta_head"]), cta_sub=html.escape(g["cta_sub"]))}
    </article>
    <section class="related wrap">
      <h2>Keep reading</h2>
      <div class="guide-grid">
        {''.join(card(s) for s in g["related"])}
      </div>
    </section>
  </main>
'''
    page += FOOTER
    d = os.path.join(OUT, "guides", slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(page)
    print("wrote guides/%s/index.html" % slug)

# ---------------------------------------------------------------- guides hub
hub_cards = "\n        ".join(
    '<a class="guide-card" href="/guides/%s/"><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="more">Read the guide →</span></a>'
    % (slug, html.escape(g["tag"]), html.escape(g["title"]), html.escape(g["dek"])) for slug, g in GUIDES.items())

hub_jsonld = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "CollectionPage",
    "name": "Cipher Munch Guides",
    "description": "Practical guides to cryptogram solving and Codebusters practice with the Cipher Munch app.",
    "url": DOMAIN + "/guides/"}, ensure_ascii=False) + '</script>'

hub = HEAD.format(
    title="Guides: Cryptogram Solving & Codebusters Practice | Cipher Munch",
    desc="Practical guides to getting more from Cipher Munch: Codebusters practice for students and coaches, Aristocrats, Patristocrats, Xenocrypts, printing puzzles, and solving faster.",
    canonical=DOMAIN + "/guides/", domain=DOMAIN, jsonld=hub_jsonld, guides_current=' aria-current="page"')
hub += f'''
  <main>
    <div class="article-hero">
      <div class="wrap">
        <p class="breadcrumb"><a href="/">Cipher Munch</a> / Guides</p>
        <p class="eyebrow">Guides</p>
        <h1>Get more out of every solve</h1>
        <p class="dek">Short, practical guides on using Cipher Munch for competition prep, classroom practice, and plain cryptogram joy, from your first Pigpen to hint-free Patristocrats.</p>
      </div>
    </div>
    <section class="section" style="padding-top:20px;">
      <div class="wrap guide-grid">
        {hub_cards}
      </div>
    </section>
  </main>
'''
hub += FOOTER
with open(os.path.join(OUT, "guides", "index.html"), "w") as f:
    f.write(hub)
print("wrote guides/index.html")
print("total pages:", len(GUIDES) + 1)
