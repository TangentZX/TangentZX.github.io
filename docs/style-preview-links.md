---
hide:
  - navigation
  - toc
---

# 友链样式对比

三套方案使用相同的 10 条真实友链数据和统一的新配色。可以切换深浅主题并缩窄窗口比较响应式表现。

<style>
.friend-preview {
  --fl-surface: rgba(255, 255, 255, .82);
  --fl-surface-strong: #fff;
  --fl-border: rgba(57, 70, 84, .12);
  --fl-text: #26323b;
  --fl-muted: #73808a;
  --fl-accent: #ef6f91;
  --fl-accent-2: #4bb7ad;
  --fl-accent-soft: rgba(239, 111, 145, .12);
  --fl-shadow: 0 12px 34px rgba(50, 65, 75, .09);
  display: grid;
  gap: 3.2rem;
  margin-top: 1.4rem;
}
[data-md-color-scheme="slate"] .friend-preview {
  --fl-surface: rgba(36, 40, 47, .86);
  --fl-surface-strong: #292e36;
  --fl-border: rgba(227, 234, 241, .12);
  --fl-text: #eef3f5;
  --fl-muted: #a8b2ba;
  --fl-accent: #ff8aaa;
  --fl-accent-2: #72d8cd;
  --fl-accent-soft: rgba(255, 138, 170, .13);
  --fl-shadow: 0 14px 38px rgba(0, 0, 0, .24);
}
.friend-option {
  padding: 1.2rem;
  border: 1px solid var(--fl-border);
  border-radius: 22px;
  background: color-mix(in srgb, var(--fl-surface) 76%, transparent);
}
.friend-option > h2 { margin: 0 0 .25rem; color: var(--fl-text); }
.friend-option > p { margin: 0 0 1.1rem; color: var(--fl-muted); }
.friend-grid { display: grid; gap: 1rem; }
.friend-card {
  position: relative;
  color: var(--fl-text) !important;
  text-decoration: none !important;
  transition: transform .24s ease, border-color .24s ease, box-shadow .24s ease, background .24s ease;
}
.friend-card img { display: block; object-fit: cover; background: var(--fl-accent-soft); }
.friend-copy { min-width: 0; }
.friend-copy strong,
.friend-copy small,
.friend-desc { display: block; }
.friend-copy strong { overflow-wrap: anywhere; font-size: .9rem; line-height: 1.35; }
.friend-copy small { margin-top: .14rem; color: var(--fl-accent-2); font-size: .64rem; font-weight: 700; }
.friend-desc { margin-top: .55rem; color: var(--fl-muted); font-size: .7rem; line-height: 1.55; }
.friend-card:hover { transform: translateY(-4px); border-color: color-mix(in srgb, var(--fl-accent) 45%, var(--fl-border)); box-shadow: var(--fl-shadow); }
.friend-card:focus-visible { outline: 3px solid color-mix(in srgb, var(--fl-accent-2) 62%, transparent); outline-offset: 3px; }

.friends-a { grid-template-columns: repeat(3, minmax(0, 1fr)); padding-top: 2.35rem; }
.friends-a .friend-card {
  min-height: 9.8rem;
  padding: 3.25rem 1rem 1.15rem;
  border: 1px solid var(--fl-border);
  border-radius: 20px;
  background:
    radial-gradient(circle at 50% -10%, var(--fl-accent-soft), transparent 43%),
    var(--fl-surface);
  text-align: center;
}
.friends-a img {
  position: absolute;
  top: -2.25rem;
  left: 50%;
  width: 4.5rem;
  height: 4.5rem;
  border: 5px solid var(--fl-surface-strong);
  border-radius: 50%;
  box-shadow: 0 7px 20px rgba(50, 65, 75, .15);
  transform: translateX(-50%);
}
.friends-a .friend-card:hover img { border-color: color-mix(in srgb, var(--fl-accent) 35%, var(--fl-surface-strong)); }

.friends-b { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.friends-b .friend-card {
  display: flex;
  align-items: center;
  gap: .9rem;
  min-height: 6.2rem;
  padding: .9rem 1rem;
  overflow: hidden;
  border: 1px solid var(--fl-border);
  border-radius: 18px;
  background: var(--fl-surface);
}
.friends-b .friend-card::before {
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: linear-gradient(var(--fl-accent), var(--fl-accent-2));
  content: "";
}
.friends-b img {
  flex: 0 0 auto;
  width: 3.6rem;
  height: 3.6rem;
  border: 2px solid color-mix(in srgb, var(--fl-accent-2) 32%, transparent);
  border-radius: 50%;
}

.friends-c { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .72rem; }
.friends-c .friend-card {
  display: grid;
  grid-template-columns: 2.35rem minmax(0, 1fr);
  gap: .68rem;
  min-height: 5.15rem;
  padding: .78rem;
  border: 1px solid transparent;
  border-radius: 15px;
  background: color-mix(in srgb, var(--fl-surface) 68%, transparent);
}
.friends-c img {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 12px;
  filter: saturate(.84);
}
.friends-c .friend-desc {
  display: -webkit-box;
  overflow: hidden;
  opacity: .68;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  transition: opacity .2s ease;
}
.friends-c .friend-card:hover,
.friends-c .friend-card:focus-visible { background: var(--fl-surface); }
.friends-c .friend-card:hover .friend-desc,
.friends-c .friend-card:focus-visible .friend-desc { opacity: 1; }

@media screen and (max-width: 44rem) {
  .friend-option { padding: .85rem; }
  .friends-a,
  .friends-b,
  .friends-c { grid-template-columns: 1fr; }
  .friends-a { padding-top: 1.9rem; }
  .friends-a .friend-card { min-height: 8.8rem; }
}
@media (prefers-reduced-motion: reduce) {
  .friend-card { transition: none; }
  .friend-card:hover { transform: none; }
}
</style>

<div class="friend-preview">
  <section class="friend-option">
    <h2>A · 漂浮头像卡</h2>
    <p>头像成为视觉中心，整体更轻松、活泼。</p>
    <div class="friend-grid friends-a">
      <a class="friend-card" href="https://www.zt2misay2.cn/" target="_blank" rel="noopener noreferrer"><img src="../images/eveonecat1.jpg" alt="Misay 的头像" loading="lazy"><span class="friend-copy"><strong>Misay's Blog</strong><small>@Misay</small><span class="friend-desc">呃啊</span></span></a>
      <a class="friend-card" href="https://lunereal.1kal0vic.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_ika.jpg" alt="ikalovic 的头像" loading="lazy"><span class="friend-copy"><strong>ika's blog</strong><small>@ikalovic</small><span class="friend-desc">想混吃等死却睡死了过去</span></span></a>
      <a class="friend-card" href="https://0n3-0.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_one.jpg" alt="one 的头像" loading="lazy"><span class="friend-copy"><strong>one's blog</strong><small>@one</small><span class="friend-desc">Pwn everything.</span></span></a>
      <a class="friend-card" href="https://kuri.jwmc.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Kuri.jpg" alt="Kuri 的头像" loading="lazy"><span class="friend-copy"><strong>Kuri's Blog</strong><small>@Kuri</small><span class="friend-desc">早安咕，午安咕，晚安咕咕咕</span></span></a>
      <a class="friend-card" href="https://oldmaple.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_M4ple.jpg" alt="Maple 的头像" loading="lazy"><span class="friend-copy"><strong>Maple's Blog</strong><small>@Maple</small><span class="friend-desc">独坐青天钓沧海，空依月桂看合离</span></span></a>
      <a class="friend-card" href="https://b1ank799.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Blank.jpg" alt="Blank 的头像" loading="lazy"><span class="friend-copy"><strong>Blank's Blog</strong><small>@Blank</small><span class="friend-desc">困</span></span></a>
      <a class="friend-card" href="https://lightcloveyou.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_lightc.jpg" alt="LightC 的头像" loading="lazy"><span class="friend-copy"><strong>LightC's Blog</strong><small>@LightC</small><span class="friend-desc">PWN your Heart</span></span></a>
      <a class="friend-card" href="https://crisq.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Crisq.jpg" alt="Cris.Q 的头像" loading="lazy"><span class="friend-copy"><strong>Cris.Q's Blog</strong><small>@Cris.Q</small><span class="friend-desc">你没有义务成为天才</span></span></a>
      <a class="friend-card" href="https://huangoxygen.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/oxygen.jpg" alt="huangoxygen 的头像" loading="lazy"><span class="friend-copy"><strong>huangoxygen's blog</strong><small>@huangoxygen</small><span class="friend-desc">一口吃不成个胖子，但一口一口可以</span></span></a>
      <a class="friend-card" href="https://dicaeopolis.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Dicaeopolis.png" alt="Dicaeopolis 的头像" loading="lazy"><span class="friend-copy"><strong>Dicaeopolis's Wiki</strong><small>@Dicaeopolis</small><span class="friend-desc">覚めるのであれば、どんな現実だって、夢でしかありません。覚めないとしたら、それが現実…</span></span></a>
    </div>
  </section>

  <section class="friend-option">
    <h2>B · 横向身份卡</h2>
    <p>头像与信息并列，长短简介都更容易阅读。</p>
    <div class="friend-grid friends-b">
      <a class="friend-card" href="https://www.zt2misay2.cn/" target="_blank" rel="noopener noreferrer"><img src="../images/eveonecat1.jpg" alt="Misay 的头像" loading="lazy"><span class="friend-copy"><strong>Misay's Blog</strong><small>@Misay</small><span class="friend-desc">呃啊</span></span></a>
      <a class="friend-card" href="https://lunereal.1kal0vic.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_ika.jpg" alt="ikalovic 的头像" loading="lazy"><span class="friend-copy"><strong>ika's blog</strong><small>@ikalovic</small><span class="friend-desc">想混吃等死却睡死了过去</span></span></a>
      <a class="friend-card" href="https://0n3-0.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_one.jpg" alt="one 的头像" loading="lazy"><span class="friend-copy"><strong>one's blog</strong><small>@one</small><span class="friend-desc">Pwn everything.</span></span></a>
      <a class="friend-card" href="https://kuri.jwmc.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Kuri.jpg" alt="Kuri 的头像" loading="lazy"><span class="friend-copy"><strong>Kuri's Blog</strong><small>@Kuri</small><span class="friend-desc">早安咕，午安咕，晚安咕咕咕</span></span></a>
      <a class="friend-card" href="https://oldmaple.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_M4ple.jpg" alt="Maple 的头像" loading="lazy"><span class="friend-copy"><strong>Maple's Blog</strong><small>@Maple</small><span class="friend-desc">独坐青天钓沧海，空依月桂看合离</span></span></a>
      <a class="friend-card" href="https://b1ank799.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Blank.jpg" alt="Blank 的头像" loading="lazy"><span class="friend-copy"><strong>Blank's Blog</strong><small>@Blank</small><span class="friend-desc">困</span></span></a>
      <a class="friend-card" href="https://lightcloveyou.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_lightc.jpg" alt="LightC 的头像" loading="lazy"><span class="friend-copy"><strong>LightC's Blog</strong><small>@LightC</small><span class="friend-desc">PWN your Heart</span></span></a>
      <a class="friend-card" href="https://crisq.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Crisq.jpg" alt="Cris.Q 的头像" loading="lazy"><span class="friend-copy"><strong>Cris.Q's Blog</strong><small>@Cris.Q</small><span class="friend-desc">你没有义务成为天才</span></span></a>
      <a class="friend-card" href="https://huangoxygen.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/oxygen.jpg" alt="huangoxygen 的头像" loading="lazy"><span class="friend-copy"><strong>huangoxygen's blog</strong><small>@huangoxygen</small><span class="friend-desc">一口吃不成个胖子，但一口一口可以</span></span></a>
      <a class="friend-card" href="https://dicaeopolis.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Dicaeopolis.png" alt="Dicaeopolis 的头像" loading="lazy"><span class="friend-copy"><strong>Dicaeopolis's Wiki</strong><small>@Dicaeopolis</small><span class="friend-desc">覚めるのであれば、どんな現実だって、夢でしかありません。覚めないとしたら、それが現実…</span></span></a>
    </div>
  </section>

  <section class="friend-option">
    <h2>C · 极简名片墙</h2>
    <p>信息更紧凑，悬停或键盘聚焦时加强当前卡片。</p>
    <div class="friend-grid friends-c">
      <a class="friend-card" href="https://www.zt2misay2.cn/" target="_blank" rel="noopener noreferrer"><img src="../images/eveonecat1.jpg" alt="Misay 的头像" loading="lazy"><span class="friend-copy"><strong>Misay's Blog</strong><small>@Misay</small><span class="friend-desc">呃啊</span></span></a>
      <a class="friend-card" href="https://lunereal.1kal0vic.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_ika.jpg" alt="ikalovic 的头像" loading="lazy"><span class="friend-copy"><strong>ika's blog</strong><small>@ikalovic</small><span class="friend-desc">想混吃等死却睡死了过去</span></span></a>
      <a class="friend-card" href="https://0n3-0.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_one.jpg" alt="one 的头像" loading="lazy"><span class="friend-copy"><strong>one's blog</strong><small>@one</small><span class="friend-desc">Pwn everything.</span></span></a>
      <a class="friend-card" href="https://kuri.jwmc.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Kuri.jpg" alt="Kuri 的头像" loading="lazy"><span class="friend-copy"><strong>Kuri's Blog</strong><small>@Kuri</small><span class="friend-desc">早安咕，午安咕，晚安咕咕咕</span></span></a>
      <a class="friend-card" href="https://oldmaple.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_M4ple.jpg" alt="Maple 的头像" loading="lazy"><span class="friend-copy"><strong>Maple's Blog</strong><small>@Maple</small><span class="friend-desc">独坐青天钓沧海，空依月桂看合离</span></span></a>
      <a class="friend-card" href="https://b1ank799.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Blank.jpg" alt="Blank 的头像" loading="lazy"><span class="friend-copy"><strong>Blank's Blog</strong><small>@Blank</small><span class="friend-desc">困</span></span></a>
      <a class="friend-card" href="https://lightcloveyou.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_lightc.jpg" alt="LightC 的头像" loading="lazy"><span class="friend-copy"><strong>LightC's Blog</strong><small>@LightC</small><span class="friend-desc">PWN your Heart</span></span></a>
      <a class="friend-card" href="https://crisq.top/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Crisq.jpg" alt="Cris.Q 的头像" loading="lazy"><span class="friend-copy"><strong>Cris.Q's Blog</strong><small>@Cris.Q</small><span class="friend-desc">你没有义务成为天才</span></span></a>
      <a class="friend-card" href="https://huangoxygen.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/oxygen.jpg" alt="huangoxygen 的头像" loading="lazy"><span class="friend-copy"><strong>huangoxygen's blog</strong><small>@huangoxygen</small><span class="friend-desc">一口吃不成个胖子，但一口一口可以</span></span></a>
      <a class="friend-card" href="https://dicaeopolis.github.io/" target="_blank" rel="noopener noreferrer"><img src="../images/avatar_Dicaeopolis.png" alt="Dicaeopolis 的头像" loading="lazy"><span class="friend-copy"><strong>Dicaeopolis's Wiki</strong><small>@Dicaeopolis</small><span class="friend-desc">覚めるのであれば、どんな現実だって、夢でしかありません。覚めないとしたら、それが現実…</span></span></a>
    </div>
  </section>
</div>
