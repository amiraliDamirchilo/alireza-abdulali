(() => {
  'use strict';

  const root = document.documentElement;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gsap = window.gsap;

  const dictionary = {
    en: {
      navHome: 'HOME', navWork: 'WORK', navAbout: 'ABOUT', navServices: 'SERVICES', navContact: 'CONTACT',
      heroKicker: 'MOTION DESIGNER / FILM EDITOR', heroTitleOne: 'MOTION', heroTitleTwo: 'MADE TO', heroTitleThree: 'STAY WITH YOU.', heroCopy: 'I turn clear ideas into motion, edits and visual systems people remember.', viewWork: 'VIEW SELECTED WORK', startProject: 'START A PROJECT', availability: 'AVAILABLE FOR SELECT PROJECTS · 2026', portraitCaption: 'BASED IN TEHRAN · WORKING WORLDWIDE', selectedWork: 'SELECTED WORK',
      workKicker: 'SELECTED PROJECTS / 2025—2026', workTitle: 'WORK WITH A POINT OF VIEW.', workCopy: 'A focused selection across motion identities, edits, brand films and CGI.',
      aboutKicker: 'THE PERSON BEHIND THE FRAMES', aboutTitleOne: 'TECHNICAL CRAFT.', aboutTitleTwo: 'HUMAN FEELING.', aboutCopy: 'Technology makes motion possible. Taste makes it worth watching. I combine both to turn a clear strategy into frames people remember.', aboutStatement: 'Every frame should earn its place — through clarity, rhythm or emotion.', years: 'YEARS OF EXPERIENCE', projects: 'PROJECTS DELIVERED', countries: 'COUNTRIES REACHED', principleOneTitle: 'CLARITY FIRST', principleOneCopy: 'The idea stays legible, even when the motion gets ambitious.', principleTwoTitle: 'RHYTHM WITH PURPOSE', principleTwoCopy: 'Timing and sound guide attention instead of decorating it.', principleThreeTitle: 'CRAFT THAT LASTS', principleThreeCopy: 'A refined system keeps every frame consistent.',
      servicesKicker: 'WHAT I CAN BUILD FOR YOU', servicesTitle: 'FROM FIRST IDEA TO FINAL FRAME.', servicesCopy: 'One clear creative route, shaped around the message and finished with care.', motionDesign: 'MOTION DESIGN', motionDescription: 'Motion identities, title sequences and campaign systems built to hold attention.', motionDeliverables: 'IDENTITY · TITLES · CAMPAIGNS', filmEditing: 'FILM EDITING', editDescription: 'Story, pacing and sound brought together in one deliberate editorial rhythm.', editDeliverables: 'STORY · RHYTHM · SOUND', artDirection: 'ART DIRECTION', artDescription: 'A distinct visual language that stays coherent from concept to delivery.', artDeliverables: 'CONCEPT · STYLE · SYSTEM', cgi: 'CGI / 3D', cgiDescription: 'Purposeful digital worlds and product visuals with convincing material detail.', cgiDeliverables: 'WORLDS · PRODUCT · SIMULATION', serviceCtaCopy: 'HAVE SOMETHING DIFFERENT IN MIND?', startConversation: 'LET’S TALK',
      contactKicker: 'YOUR MOVE', contactTitleOne: 'LET’S MAKE', contactTitleTwo: 'SOMETHING MATTER.', contactCopy: 'Share the goal, timeline and scope. I’ll reply with a clear creative route.', nameLabel: 'NAME', emailLabel: 'EMAIL', companyLabel: 'COMPANY', serviceLabel: 'SERVICE', chooseService: 'Choose service', other: 'Something else', budgetLabel: 'BUDGET', chooseBudget: 'Choose range', messageLabel: 'PROJECT BRIEF', sendBrief: 'SEND THE BRIEF', sending: 'SENDING…', formSuccess: 'BRIEF RECEIVED. I’LL REPLY SHORTLY.', formError: 'Please check the highlighted fields.'
    },
    fa: {
      navHome: 'خانه', navWork: 'نمونه‌کارها', navAbout: 'درباره من', navServices: 'خدمات', navContact: 'تماس',
      heroKicker: 'طراح موشن / تدوینگر فیلم', heroTitleOne: 'موشن', heroTitleTwo: 'ساخته‌شده', heroTitleThree: 'برای ماندن.', heroCopy: 'ایده‌های روشن را به موشن، تدوین و سیستم‌های بصری ماندگار تبدیل می‌کنم.', viewWork: 'دیدن نمونه‌کارها', startProject: 'شروع یک پروژه', availability: 'آمادهٔ همکاری برای پروژه‌های منتخب · ۲۰۲۶', portraitCaption: 'تهران · همکاری با سراسر جهان', selectedWork: 'نمونه‌کارهای منتخب',
      workKicker: 'پروژه‌های منتخب / ۲۰۲۵—۲۰۲۶', workTitle: 'کارهایی با نگاه مشخص.', workCopy: 'گزیده‌ای هدفمند از هویت‌های متحرک، تدوین، فیلم برند و CGI.',
      aboutKicker: 'کسی که پشت فریم‌هاست', aboutTitleOne: 'مهارت فنی.', aboutTitleTwo: 'احساس انسانی.', aboutCopy: 'تکنولوژی حرکت را ممکن می‌کند؛ سلیقه تماشای آن را ارزشمند می‌کند. این دو را ترکیب می‌کنم تا یک استراتژی روشن به فریم‌هایی ماندگار تبدیل شود.', aboutStatement: 'هر فریم باید جای خودش را با وضوح، ریتم یا احساس به دست بیاورد.', years: 'سال تجربه', projects: 'پروژهٔ تحویل‌شده', countries: 'کشور', principleOneTitle: 'اول وضوح', principleOneCopy: 'حتی در جسورانه‌ترین حرکت‌ها، ایده واضح و خوانا می‌ماند.', principleTwoTitle: 'ریتم هدفمند', principleTwoCopy: 'زمان‌بندی و صدا، توجه را هدایت می‌کنند؛ نه اینکه فقط تزئین باشند.', principleThreeTitle: 'اجرای ماندگار', principleThreeCopy: 'یک سیستم دقیق، همهٔ فریم‌ها را منسجم نگه می‌دارد.',
      servicesKicker: 'چیزی که برای شما می‌سازم', servicesTitle: 'از اولین ایده تا آخرین فریم.', servicesCopy: 'یک مسیر خلاق روشن، متناسب با پیام شما و اجراشده با دقت.', motionDesign: 'طراحی موشن', motionDescription: 'هویت متحرک، تیتراژ و سیستم‌های کمپین برای جلب و حفظ توجه.', motionDeliverables: 'هویت · تیتراژ · کمپین', filmEditing: 'تدوین فیلم', editDescription: 'ترکیب داستان، ریتم و صدا در یک تدوین دقیق و هدفمند.', editDeliverables: 'داستان · ریتم · صدا', artDirection: 'هدایت هنری', artDescription: 'یک زبان بصری متمایز و منسجم، از ایده تا خروجی نهایی.', artDeliverables: 'ایده · استایل · سیستم', cgi: 'سه‌بعدی و CGI', cgiDescription: 'دنیاها و تصاویر محصول با جزئیات متریال باورپذیر و هدفمند.', cgiDeliverables: 'دنیا · محصول · شبیه‌سازی', serviceCtaCopy: 'ایدهٔ متفاوتی در ذهن دارید؟', startConversation: 'گفت‌وگو کنیم',
      contactKicker: 'حرکت بعدی با شماست', contactTitleOne: 'بیایید چیزی', contactTitleTwo: 'اثرگذار بسازیم.', contactCopy: 'هدف، زمان‌بندی و محدودهٔ پروژه را بفرستید؛ با یک مسیر خلاق روشن پاسخ می‌دهم.', nameLabel: 'نام', emailLabel: 'ایمیل', companyLabel: 'شرکت', serviceLabel: 'خدمت', chooseService: 'انتخاب خدمت', other: 'یک کار متفاوت', budgetLabel: 'بودجه', chooseBudget: 'انتخاب بازه', messageLabel: 'بریف پروژه', sendBrief: 'ارسال بریف', sending: 'در حال ارسال…', formSuccess: 'بریف دریافت شد؛ به‌زودی پاسخ می‌دهم.', formError: 'لطفاً فیلدهای مشخص‌شده را بررسی کنید.'
    }
  };

  const managedCopy = document.getElementById('site-copy-data');
  if (managedCopy) {
    try {
      const copy = JSON.parse(managedCopy.textContent);
      Object.entries(copy).forEach(([key, value]) => {
        if (value?.en) dictionary.en[key] = value.en;
        if (value?.fa) dictionary.fa[key] = value.fa;
      });
    } catch (_) {}
  }

  const managedBindings = {
    '.work-filters button[data-filter="all"] span': 'allWork',
    '.empty-work > span': 'emptyEyebrow',
    '.empty-work h3': 'emptyTitle',
    '.empty-work > p': 'emptyCopy',
    '.empty-work > a': 'openAdmin'
  };
  Object.entries(managedBindings).forEach(([selector, key]) => {
    document.querySelector(selector)?.setAttribute('data-i18n', key);
  });
  const filterLabel = document.querySelector('.filter-label');
  if (filterLabel) {
    [...filterLabel.childNodes].filter(node => node.nodeType === Node.TEXT_NODE).forEach(node => node.remove());
    const text = document.createElement('b');
    text.dataset.i18n = 'filterLabel';
    filterLabel.append(text);
  }

  const storage = {
    get(key, fallback) { try { return localStorage.getItem(key) || fallback; } catch (_) { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch (_) {} }
  };

  function setLanguage(language) {
    const lang = dictionary[language] ? language : 'en';
    root.lang = lang;
    root.dir = lang === 'fa' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const value = dictionary[lang][element.dataset.i18n];
      if (value) element.textContent = value;
    });
    document.querySelectorAll('[data-en][data-fa]').forEach(element => { element.textContent = element.dataset[lang] || element.dataset.en; });
    document.querySelectorAll('[data-placeholder-en][data-placeholder-fa]').forEach(element => { element.placeholder = element.dataset[lang === 'fa' ? 'placeholderFa' : 'placeholderEn']; });
    const toggle = document.querySelector('.language-toggle');
    if (toggle) { toggle.querySelector('span').textContent = lang === 'fa' ? 'EN' : 'FA'; toggle.setAttribute('aria-label', lang === 'fa' ? 'تغییر زبان به انگلیسی' : 'Switch language to Persian'); }
    storage.set('alireza-tech-lang', lang);
  }

  function setTheme(theme) {
    const next = theme === 'light' ? 'light' : 'dark';
    root.dataset.theme = next;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', next === 'light' ? '#f4f0f5' : '#0a090d');
    document.querySelector('.theme-toggle')?.setAttribute('aria-pressed', String(next === 'light'));
    storage.set('alireza-tech-theme', next);
  }

  function animatePageIn() {
    if (!gsap || reducedMotion) return;
    const timeline = gsap.timeline({ defaults: { duration: .72, ease: 'power3.out' } });
    timeline.from('.site-header', { y: -20, opacity: 0, duration: .48 })
      .from('[data-animate="eyebrow"]', { y: 14, opacity: 0 }, '-=.2')
      .from('.home-page .title-line > b', { yPercent: 115, rotate: 1.5, stagger: .09 }, '-=.5')
      .from('[data-animate="copy"]', { y: 18, opacity: 0, stagger: .08 }, '-=.4')
      .from('[data-animate="actions"]', { y: 18, opacity: 0 }, '-=.55')
      .from('[data-animate="visual"]', { x: root.dir === 'rtl' ? -28 : 28, opacity: 0, scale: .97 }, '-=.75');
    const rail = document.querySelector('[data-animate="rail"]');
    if (rail) timeline.from(rail, { y: 16, opacity: 0 }, '-=.45');

    const visual = document.querySelector('.hero-visual');
    if (visual && matchMedia('(pointer:fine)').matches) {
      const moveX = gsap.quickTo(visual, 'x', { duration: .7, ease: 'power3.out' });
      const moveY = gsap.quickTo(visual, 'y', { duration: .7, ease: 'power3.out' });
      addEventListener('pointermove', event => { moveX((event.clientX / innerWidth - .5) * 14); moveY((event.clientY / innerHeight - .5) * 10); }, { passive: true });
    }
  }

  function initMenu() {
    const button = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.mobile-navigation');
    if (!button || !menu) return;
    let open = false;
    button.addEventListener('click', () => {
      open = !open;
      button.setAttribute('aria-expanded', String(open));
      button.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      menu.setAttribute('aria-hidden', String(!open));
      document.body.style.overflow = open ? 'hidden' : '';
      if (gsap && !reducedMotion) {
        if (open) gsap.timeline().set(menu, { visibility: 'visible' }).to(menu, { autoAlpha: 1, duration: .3 }).fromTo(menu.querySelectorAll('a'), { x: root.dir === 'rtl' ? 24 : -24, opacity: 0 }, { x: 0, opacity: 1, stagger: .06, duration: .35 }, '-=.15');
        else gsap.to(menu, { autoAlpha: 0, duration: .22, onComplete: () => gsap.set(menu, { visibility: 'hidden' }) });
      } else { menu.style.visibility = open ? 'visible' : 'hidden'; menu.style.opacity = open ? '1' : '0'; }
    });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      if (!open) return;
      open = false; button.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = ''; menu.style.visibility = 'hidden'; menu.style.opacity = '0';
    }));
  }

  function initWorkFilters() {
    const buttons = document.querySelectorAll('[data-filter]');
    const cards = document.querySelectorAll('.project-card[data-category]');
    const count = document.querySelector('.filter-count b');
    buttons.forEach(button => button.addEventListener('click', () => {
      buttons.forEach(item => item.classList.toggle('is-active', item === button));
      cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
      if (count) count.textContent = [...cards].filter(card => !card.hidden).length;
      if (gsap && !reducedMotion) gsap.fromTo([...cards].filter(card => !card.hidden), { y: 18, opacity: 0 }, { y: 0, opacity: 1, stagger: .07, duration: .45, ease: 'power2.out' });
    }));
  }

  function initScrollMotion() {
    if (reducedMotion) return;
    const items = document.querySelectorAll('.work-page .page-heading, .filter-panel, .project-card, .about-intro, .about-statement, .stats-grid, .services-page .page-heading, .service-card, .contact-copy, .brief-form');
    items.forEach(item => item.classList.add('reveal-item'));
    if ('IntersectionObserver' in window) {
      const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-revealed');
        reveal.unobserve(entry.target);
      }), { threshold: .12, rootMargin: '0px 0px -7%' });
      items.forEach(item => reveal.observe(item));
    } else items.forEach(item => item.classList.add('is-revealed'));

    if (matchMedia('(pointer:fine)').matches) {
      document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('pointermove', event => {
          const box = card.getBoundingClientRect();
          const rotateY = ((event.clientX - box.left) / box.width - .5) * 2.5;
          const rotateX = -((event.clientY - box.top) / box.height - .5) * 2.5;
          card.style.transform = `translateY(-8px) perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        card.addEventListener('pointerleave', () => { card.style.transform = ''; });
      });
      document.querySelectorAll('.work-filters button').forEach(button => button.addEventListener('pointermove', event => {
        const box = button.getBoundingClientRect();
        button.style.transform = `translate(${(event.clientX - box.left - box.width / 2) * .08}px, ${(event.clientY - box.top - box.height / 2) * .1}px)`;
      }));
      document.querySelectorAll('.work-filters button').forEach(button => button.addEventListener('pointerleave', () => { button.style.transform = ''; }));
    }
  }

  function initSectionNavigation() {
    const links = document.querySelectorAll('.desktop-nav a');
    const sections = document.querySelectorAll('.scroll-section[id]');
    if (!('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      links.forEach(link => link.classList.toggle('is-active', link.hash === `#${entry.target.id}`));
      const number = { home: '00', work: '01', about: '02', services: '03', contact: '04' }[entry.target.id];
      const counter = document.querySelector('.page-number');
      if (counter && number) counter.firstChild.textContent = number;
    }), { rootMargin: '-35% 0px -55%' });
    sections.forEach(section => observer.observe(section));
  }

  function initPageTransitions() {
    if (!gsap || reducedMotion) return;
    document.addEventListener('click', event => {
      const link = event.target.closest('a');
      if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target || link.hasAttribute('download')) return;
      const url = new URL(link.href, location.href);
      if (url.origin !== location.origin || url.pathname === location.pathname || url.protocol === 'mailto:') return;
      event.preventDefault();
      gsap.timeline({ onComplete: () => { location.href = url.href; } }).to('.site-main, .site-footer', { opacity: 0, y: -12, duration: .24, ease: 'power2.in' }).to('.page-wipe', { scaleY: 1, duration: .42, ease: 'power3.inOut' }, '-=.1');
    });
  }

  function initForm() {
    const form = document.querySelector('.brief-form');
    if (!form) return;
    const initialStatus = form.querySelector('.form-status');
    if (initialStatus?.textContent.trim()) {
      initialStatus.classList.add(initialStatus.classList.contains('error') ? 'is-error' : 'is-success');
      form.classList.add(initialStatus.classList.contains('error') ? 'has-error' : 'has-success');
    }
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const status = form.querySelector('.form-status');
      const button = form.querySelector('button[type="submit"]');
      const label = button.querySelector('span');
      form.querySelectorAll('[aria-invalid="true"]').forEach(field => field.removeAttribute('aria-invalid'));
      button.disabled = true; label.textContent = dictionary[root.lang].sending; status.textContent = '';
      status.classList.remove('error', 'is-error', 'is-success');
      form.classList.remove('has-error', 'has-success');
      try {
        const response = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        const result = await response.json();
        if (!response.ok || !result.ok) {
          Object.keys(result.errors || {}).forEach(name => form.elements[name]?.setAttribute('aria-invalid', 'true'));
          form.querySelector('[aria-invalid="true"]')?.focus();
          throw new Error('invalid');
        }
        form.reset(); status.textContent = dictionary[root.lang].formSuccess;
        status.classList.add('is-success'); form.classList.add('has-success');
        if (gsap && !reducedMotion) gsap.fromTo(status, { y: 16, opacity: 0, scale: .96 }, { y: 0, opacity: 1, scale: 1, duration: .55, ease: 'back.out(1.7)' });
      } catch (_) {
        status.textContent = dictionary[root.lang].formError;
        status.classList.add('error', 'is-error'); form.classList.add('has-error');
        if (gsap && !reducedMotion) gsap.fromTo(status, { x: -9, opacity: 0 }, { x: 0, opacity: 1, duration: .5, ease: 'elastic.out(1,.35)' });
      }
      finally { button.disabled = false; label.textContent = dictionary[root.lang].sendBrief; }
    });
  }

  setTheme(storage.get('alireza-tech-theme', 'dark'));
  setLanguage(storage.get('alireza-tech-lang', root.lang === 'fa' ? 'fa' : 'en'));
  document.querySelector('.theme-toggle')?.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  document.querySelector('.language-toggle')?.addEventListener('click', () => setLanguage(root.lang === 'fa' ? 'en' : 'fa'));
  initMenu(); initPageTransitions(); initForm(); initWorkFilters(); initSectionNavigation(); initScrollMotion(); animatePageIn();
})();
