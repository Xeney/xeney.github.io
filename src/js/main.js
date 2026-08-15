/**
 * Portfolio - DAMIR VARLAMOV
 * Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initCursor();
    initMobileMenu();
    initHeaderScroll();
    initSmoothScroll();
    initScrollTop();
    initScrollProgress();
    initMarquee();
    initFormSubmit();
    initRevealAnimations();
    initFaqToggle();
    initTestimonials();
    initPriceCalculator();
});

// ========================================
// THEME TOGGLE
// ========================================
function initThemeToggle() {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
        document.documentElement.setAttribute('data-theme', 'light');
    }
    
    updateThemeIcon();
    
    btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateThemeIcon();
    });
    
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            document.documentElement.setAttribute('data-theme', e.matches ? 'light' : 'dark');
            updateThemeIcon();
        }
    });
}

function updateThemeIcon() {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    btn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    btn.setAttribute('aria-label', isDark ? 'Светлая тема' : 'Тёмная тема');
}

// ========================================
// CURSOR
// ========================================
function initCursor() {
    if (!window.matchMedia('(pointer: fine)').matches) return;
    
    const dot = document.querySelector('.cursor-dot');
    const ring = document.querySelector('.cursor-ring');
    
    if (!dot || !ring) return;
    
    const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    let cursorEnabled = !reducedMotionQuery.matches;
    
    function setCursorVisibility(visible) {
        cursorEnabled = visible;
        dot.style.display = visible ? '' : 'none';
        ring.style.display = visible ? '' : 'none';
    }
    
    reducedMotionQuery.addEventListener('change', (e) => {
        setCursorVisibility(!e.matches);
    });
    
    if (!cursorEnabled) {
        setCursorVisibility(false);
        return;
    }
    
    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let ringX = 0, ringY = 0;
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    function animate() {
        if (!cursorEnabled) return;
        
        dotX += (mouseX - dotX) * 0.3;
        dotY += (mouseY - dotY) * 0.3;
        ringX += (mouseX - ringX) * 0.12;
        ringY += (mouseY - ringY) * 0.12;
        
        dot.style.left = dotX + 'px';
        dot.style.top = dotY + 'px';
        ring.style.left = ringX + 'px';
        ring.style.top = ringY + 'px';
        
        requestAnimationFrame(animate);
    }
    animate();
    
    document.querySelectorAll('a, button, .work-card, .service-card, .stack-item, .case-card-mini').forEach(el => {
        el.addEventListener('mouseenter', () => { if (cursorEnabled) ring.classList.add('hover'); });
        el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
    });
}

// ========================================
// MOBILE MENU
// ========================================
function initMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const nav = document.getElementById('nav');
    
    if (!menuToggle || !nav) return;
    
    menuToggle.addEventListener('click', () => {
        const isActive = nav.classList.toggle('active');
        menuToggle.classList.toggle('active');
        
        if (isActive) {
            window.scrollTo(0, 0);
            setTimeout(() => {
                document.body.style.overflow = 'hidden';
            }, 350);
        } else {
            document.body.style.overflow = '';
        }
    });
    
    const closeMenu = () => {
        nav.classList.remove('active');
        menuToggle.classList.remove('active');
        document.body.style.overflow = '';
    };
    
    nav.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeMenu);
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && nav.classList.contains('active')) {
            closeMenu();
        }
    });
}

// ========================================
// HEADER SCROLL
// ========================================
function initHeaderScroll() {
    const header = document.getElementById('header');
    if (!header) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// ========================================
// SMOOTH SCROLL
// ========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerHeight = document.getElementById('header')?.offsetHeight || 80;
                const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========================================
// SCROLL TOP
// ========================================
function initScrollTop() {
    const scrollBtn = document.getElementById('scrollTop');
    if (!scrollBtn) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });
    
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ========================================
// SCROLL PROGRESS BAR
// ========================================
function initScrollProgress() {
    const header = document.getElementById('header');
    if (!header) return;
    
    const progress = document.createElement('div');
    progress.className = 'scroll-progress';
    progress.setAttribute('aria-hidden', 'true');
    header.appendChild(progress);
    
    function updateProgress() {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const percent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progress.style.width = percent + '%';
    }
    
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress, { passive: true });
    updateProgress();
}

// ========================================
// MARQUEE
// ========================================
function initMarquee() {
    const track = document.getElementById('marqueeTrack');
    if (!track) return;
    
    const content = track.innerHTML;
    const minClones = 4;
    let clones = 1;
    while (track.scrollWidth < window.innerWidth * 2 && clones < minClones) {
        track.insertAdjacentHTML('beforeend', content);
        clones++;
    }
}

// ========================================
// FORM SUBMIT
// ========================================
function initFormSubmit() {
    const form = document.getElementById('contactForm');
    if (!form) return;
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const groups = form.querySelectorAll('.form-group');
        let valid = true;
        
        groups.forEach(g => {
            const input = g.querySelector('input, textarea');
            if (input && !input.value.trim()) {
                g.classList.add('invalid');
                valid = false;
            } else {
                g.classList.remove('invalid');
            }
        });
        
        if (!valid) return;
        
        const submitBtn = form.querySelector('.form-submit-btn');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        
        btnText.style.display = 'none';
        btnLoader.style.display = '';
        submitBtn.disabled = true;
        
        setTimeout(() => {
            const formData = new FormData(form);
            const name = formData.get('name');
            const contact = formData.get('contact');
            const message = formData.get('message');
            
            const subject = encodeURIComponent(`Портфолио: сообщение от ${name}`);
            const body = encodeURIComponent(`Имя: ${name}\nКонтакт: ${contact}\n\nСообщение:\n${message}`);
            
            showNotification('Почтовый клиент открыт! Нажмите «Отправить».', 'success');
            
            btnText.style.display = '';
            btnLoader.style.display = 'none';
            submitBtn.disabled = false;
            
            window.location.href = `mailto:damir.itwar@yandex.ru?subject=${subject}&body=${body}`;
            form.reset();
        }, 600);
    });
    
    form.querySelectorAll('input, textarea').forEach(input => {
        input.addEventListener('input', () => {
            const group = input.closest('.form-group');
            if (group && input.value.trim()) {
                group.classList.remove('invalid');
            }
        });
    });
}

// ========================================
// NOTIFICATION
// ========================================
function showNotification(message, type) {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    if (!document.querySelector('#notification-style')) {
        const style = document.createElement('style');
        style.id = 'notification-style';
        style.textContent = `
            .notification {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                background: #1a1a1a;
                border: 1px solid var(--accent-secondary);
                padding: 16px 24px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                gap: 16px;
                z-index: 10000;
                box-shadow: 0 8px 30px rgba(0,0,0,0.5);
                animation: slideUp 0.3s ease;
            }
            .notification button {
                background: none;
                border: none;
                color: rgba(240,234,220,0.4);
                cursor: pointer;
            }
            @keyframes slideUp {
                from { opacity: 0; transform: translateX(-50%) translateY(20px); }
                to { opacity: 1; transform: translateX(-50%) translateY(0); }
            }
        `;
        document.head.appendChild(style);
    }
    
    setTimeout(() => notification.remove(), 5000);
}

// ========================================
// REVEAL ANIMATIONS
// ========================================
function initRevealAnimations() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const revealElements = document.querySelectorAll(
        '.stack-item, .work-card, .service-card, .testimonial-card, .about-text, .about-image, .case-card-mini, .process-step'
    );
    
    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    const style = document.createElement('style');
    style.textContent = `
        .revealed {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
}

// ========================================
// FAQ TOGGLE
// ========================================
function initFaqToggle() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    function updateAria() {
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            if (question) {
                question.setAttribute('aria-expanded', item.classList.contains('active'));
            }
        });
    }
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (!question) return;
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            faqItems.forEach(i => i.classList.remove('active'));
            
            if (!isActive) {
                item.classList.add('active');
            }
            
            updateAria();
        });
    });
    
    updateAria();
}

// ========================================
// TESTIMONIALS EXPAND
// ========================================
function initTestimonials() {
    const cards = document.querySelectorAll('.testimonial-card');
    
    cards.forEach(card => {
        const toggle = card.querySelector('.testimonial-toggle');
        const toggleText = card.querySelector('.testimonial-toggle-text');
        if (!toggle) return;
        
        toggle.addEventListener('click', () => {
            const isExpanded = card.classList.toggle('expanded');
            toggle.setAttribute('aria-expanded', isExpanded);
            if (toggleText) {
                toggleText.textContent = isExpanded ? 'Свернуть' : 'Читать полностью';
            }
        });
    });
}

// ========================================
// PRICE CALCULATOR (WIZARD)
// ========================================
function initPriceCalculator() {
    const wizard = document.querySelector('.calc-wizard');
    if (!wizard) return;

    const steps = wizard.querySelectorAll('.calc-step');
    const progressSteps = wizard.querySelectorAll('.calc-progress-step');
    const prevBtn = document.getElementById('calcPrev');
    const nextBtn = document.getElementById('calcNext');
    const detailsContainer = document.getElementById('calcDetails');
    const totalEl = document.getElementById('calcTotal');
    const summaryEl = document.getElementById('calcSummary');

    let currentStep = 1;
    const totalSteps = steps.length;

    const projectData = {
        vizitka: {
            title: 'Сайт-визитка',
            base: 10000,
            questions: [
                {
                    id: 'sections',
                    title: 'Сколько секций планируется?',
                    options: [
                        { value: 0, label: '3–4 секции' },
                        { value: 3000, label: '5–6 секций' },
                        { value: 6000, label: '7 и более' }
                    ]
                },
                {
                    id: 'form',
                    title: 'Нужна форма обратной связи?',
                    options: [
                        { value: 0, label: 'Нет' },
                        { value: 1000, label: 'Да, простая форма' },
                        { value: 3000, label: 'Да, с интеграцией в мессенджер' }
                    ]
                }
            ]
        },
        landing: {
            title: 'Landing Page',
            base: 15000,
            questions: [
                {
                    id: 'screens',
                    title: 'Количество экранов',
                    options: [
                        { value: 0, label: 'До 5 экранов' },
                        { value: 3000, label: '6–8 экранов' },
                        { value: 6000, label: '9 и более' }
                    ]
                },
                {
                    id: 'analytics',
                    title: 'Нужна настройка аналитики?',
                    options: [
                        { value: 0, label: 'Нет' },
                        { value: 2000, label: 'Метрика + цели' },
                        { value: 4000, label: 'Метрика + цели + Яндекс Директ' }
                    ]
                }
            ]
        },
        corp: {
            title: 'Корпоративный сайт',
            base: 35000,
            questions: [
                {
                    id: 'pages',
                    title: 'Количество страниц',
                    options: [
                        { value: 0, label: 'До 5 страниц' },
                        { value: 5000, label: '6–10 страниц' },
                        { value: 10000, label: '11 и более' }
                    ]
                },
                {
                    id: 'catalog',
                    title: 'Нужен каталог услуг/товаров?',
                    options: [
                        { value: 0, label: 'Нет' },
                        { value: 5000, label: 'Да, до 20 позиций' },
                        { value: 10000, label: 'Да, много позиций' }
                    ]
                }
            ]
        },
        shop: {
            title: 'Интернет-магазин',
            base: 25000,
            questions: [
                {
                    id: 'products',
                    title: 'Количество товаров',
                    options: [
                        { value: 0, label: 'До 50 товаров' },
                        { value: 5000, label: '51–200 товаров' },
                        { value: 10000, label: 'Более 200' }
                    ]
                },
                {
                    id: 'import',
                    title: 'Нужен импорт товаров?',
                    options: [
                        { value: 0, label: 'Нет, добавлю вручную' },
                        { value: 5000, label: 'Да, из Excel / CSV' }
                    ]
                }
            ]
        },
        bot: {
            title: 'Чат-бот Telegram',
            base: 12000,
            questions: [
                {
                    id: 'scenarios',
                    title: 'Количество сценариев/разделов',
                    options: [
                        { value: 0, label: 'До 5 сценариев' },
                        { value: 3000, label: '6–10 сценариев' },
                        { value: 6000, label: 'Более 10' }
                    ]
                },
                {
                    id: 'botAi',
                    title: 'Нужно подключение ИИ (ChatGPT)?',
                    options: [
                        { value: 0, label: 'Нет' },
                        { value: 10000, label: 'Да, интеграция ChatGPT' }
                    ]
                }
            ]
        },
        custom: {
            title: 'Разработка на заказ',
            base: 0,
            hourly: true,
            questions: [
                {
                    id: 'taskType',
                    title: 'Тип задачи',
                    options: [
                        { value: 0, label: 'Backend / API' },
                        { value: 0, label: 'Интеграция сервисов' },
                        { value: 0, label: 'Автоматизация процессов' },
                        { value: 0, label: 'Доработка существующего проекта' }
                    ]
                },
                {
                    id: 'hours',
                    title: 'Оценочный объём работ',
                    options: [
                        { value: 10000, label: '10–20 часов' },
                        { value: 30000, label: '20–40 часов' },
                        { value: 60000, label: '40+ часов' }
                    ]
                }
            ]
        }
    };

    const addonLabels = {
        admin: 'Панель управления (Админка)',
        crm: 'Интеграция с CRM / Telegram-уведомления',
        payments: 'Приём платежей',
        interactive: 'Сложные интерактивные элементы',
        ai: 'Интеграция API / Нейросетей'
    };

    function formatPrice(value) {
        return value.toLocaleString('ru-RU').replace(/\s/g, ' ');
    }

    function getSelectedType() {
        const checked = wizard.querySelector('input[name="projectType"]:checked');
        return checked ? checked.value : 'vizitka';
    }

    function renderDetails() {
        const type = getSelectedType();
        const data = projectData[type];
        if (!data || !data.questions) {
            detailsContainer.innerHTML = '';
            return;
        }

        detailsContainer.innerHTML = data.questions.map((q, qIndex) => `
            <div class="calc-detail-group">
                <h4>${q.title}</h4>
                <div class="calc-detail-options">
                    ${q.options.map((opt, i) => `
                        <label class="calc-detail-option">
                            <input type="radio" name="detail_${q.id}" value="${opt.value}" ${i === 0 ? 'checked' : ''}>
                            <span>${opt.label}</span>
                        </label>
                    `).join('')}
                </div>
            </div>
        `).join('');

        detailsContainer.querySelectorAll('.calc-detail-option input').forEach(input => {
            input.addEventListener('change', updateSelectedState);
        });
        updateSelectedState();
    }

    function updateSelectedState() {
        wizard.querySelectorAll('.calc-card').forEach(card => {
            const input = card.querySelector('input');
            card.classList.toggle('selected', input.checked);
        });
        wizard.querySelectorAll('.calc-detail-option').forEach(label => {
            const input = label.querySelector('input');
            label.classList.toggle('selected', input.checked);
        });
        wizard.querySelectorAll('.calc-option').forEach(label => {
            const input = label.querySelector('input');
            label.classList.toggle('selected', input.checked);
        });
    }

    function calculate() {
        const type = getSelectedType();
        const data = projectData[type];
        let base = data.base;
        const summaryItems = [];

        summaryItems.push({ label: data.title, value: base });

        // Details
        data.questions.forEach(q => {
            const checked = wizard.querySelector(`input[name="detail_${q.id}"]:checked`);
            if (checked) {
                const val = parseInt(checked.value, 10);
                const label = checked.nextElementSibling.textContent;
                base += val;
                if (val > 0 || data.hourly) {
                    summaryItems.push({ label: `${q.title}: ${label}`, value: val });
                }
            }
        });

        // Addons
        let addonsTotal = 0;
        wizard.querySelectorAll('input[name="addon"]:checked').forEach(input => {
            const val = parseInt(input.value, 10);
            const id = input.getAttribute('data-id');
            addonsTotal += val;
            summaryItems.push({ label: addonLabels[id], value: val });
        });

        const total = base + addonsTotal;

        if (totalEl) totalEl.textContent = '~' + formatPrice(total) + ' ₽';

        if (summaryEl) {
            const list = summaryItems.map(item => `
                <li><span>${item.label}</span><strong>${item.value > 0 ? '+' + formatPrice(item.value) + ' ₽' : 'включено'}</strong></li>
            `).join('');
            summaryEl.innerHTML = `<ul>${list}<li class="calc-summary-total"><span>Примерная стоимость</span><strong>~${formatPrice(total)} ₽</strong></li></ul>`;
        }
    }

    function goToStep(step) {
        currentStep = step;
        steps.forEach(s => s.classList.toggle('active', parseInt(s.getAttribute('data-step'), 10) === currentStep));
        progressSteps.forEach(ps => ps.classList.toggle('active', parseInt(ps.getAttribute('data-step'), 10) <= currentStep));

        prevBtn.style.visibility = currentStep === 1 ? 'hidden' : 'visible';
        nextBtn.innerHTML = currentStep === totalSteps
            ? '<i class="fas fa-redo"></i> Пересчитать'
            : 'Далее <i class="fas fa-arrow-right"></i>';

        if (currentStep === 2) renderDetails();
        if (currentStep === totalSteps) calculate();

        wizard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    wizard.querySelectorAll('input[name="projectType"]').forEach(input => {
        input.addEventListener('change', () => {
            updateSelectedState();
            if (currentStep === 2) renderDetails();
            if (currentStep === totalSteps) calculate();
        });
    });

    wizard.addEventListener('change', e => {
        if (e.target.matches('input[name^="detail_"], input[name="addon"]')) {
            updateSelectedState();
            if (currentStep === totalSteps) calculate();
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 1) goToStep(currentStep - 1);
    });

    nextBtn.addEventListener('click', () => {
        if (currentStep < totalSteps) {
            goToStep(currentStep + 1);
        } else {
            goToStep(1);
        }
    });

    renderDetails();
    updateSelectedState();
    calculate();
}

