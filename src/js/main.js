/**
 * Portfolio - DAMIR VARLAMOV
 * Interactive JavaScript
 */

const projectsData = [
    {
        title: 'CarInSight',
        task: 'Разработать полноценную платформу v2.0 для автоматизации приёма и диагностики автомобилей в автосервисах с AI-анализом дефектов кузова.',
        solution: 'Реализовано веб-приложение на Go 1.25 с SQLite (WAL): авторизация и регистрация через bcrypt, сессии в HttpOnly cookie, CSRF-защита и rate limiter. 19 маршрутов — лендинг, личный кабинет, полный CRUD осмотров, фото и дефектов, экспресс-осмотр из 6 шагов, админка пользователей и заявок. Интегрирован AI-микросервис на YOLOv8 для распознавания царапин, вмятин и трещин. Адаптивный UI на Bootstrap 5 в glassmorphism-стилистике.',
        tags: ['Go', 'SQLite', 'Bootstrap 5', 'YOLOv8', 'AI', 'Docker'],
        images: 15
    },
    {
        title: 'ServiceDesk РЖД',
        task: 'Дипломный проект: разработать платформу для подачи и отслеживания технических заявок внутри компании (например, сломался принтер или требуется ремонт оборудования).',
        solution: 'Реализована тикет-система на PHP + PostgreSQL с ролевой моделью (сотрудник / исполнитель / администратор). Личный кабинет с dashboard, отслеживание статусов, уведомления на email, генерация отчётов.',
        tags: ['PHP', 'PostgreSQL', 'AJAX', 'Dashboard', 'Diploma'],
        images: 5
    },
    {
        title: 'Кафе-бар «Истанбул»',
        task: 'Турецкая кухня в Самаре для любого повода. Лендинг для заведения с дурумом, лахмаджуном, пиде, искендером, кебабами на мангале и традиционными десертами.',
        solution: 'Адаптивный лендинг с анимированными секциями, фотогалереей блюд и интерьера. Форма бронирования столика с отправкой заявки в мессенджер. Интегрированы Яндекс.Карты, блок с акциями и спецпредложениями.',
        tags: ['HTML/CSS', 'JavaScript', 'Chat API', 'Mobile First'],
        images: 11
    },
    {
        title: 'Кафе «Черника»',
        task: 'Лаундж-бар «Черника» на Ленинградской, 31 — популярное заведение с панорамным видом на пешеходную улицу, кальянами и смешанной кухней.',
        solution: 'Реализован многостраничный сайт на PHP + JavaScript. Меню подгружается из JSON, фотогалерея с лайтбоксом. Интегрированы Яндекс.Карты, форма обратной связи. Адаптивная сетка на CSS Grid.',
        tags: ['PHP', 'JavaScript', 'JSON', 'CSS Grid', 'Lightbox'],
        images: 14
    },
    {
        title: 'Сайт-визитка',
        task: 'Разработать персональный сайт-портфолио для Backend Developer с тёмной темой и интерактивными элементами.',
        solution: 'Одностраничный сайт на Vanilla JS с кастомным курсором, reveal-анимациями при скролле, переключением тёмной/светлой темы. Стек технологий, карточки проектов, контактная форма через mailto.',
        tags: ['HTML', 'CSS', 'Vanilla JS', 'Dark Theme', 'Portfolio'],
        images: 12
    }
];

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initCursor();
    initMobileMenu();
    initHeaderScroll();
    initSmoothScroll();
    initScrollTop();
    initFormSubmit();
    initRevealAnimations();
    initFaqToggle();
    initCaseCards();
    initCaseModal();
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
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (!question) return;
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            faqItems.forEach(i => i.classList.remove('active'));
            
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

// ========================================
// CASE CARDS - OPEN MODAL
// ========================================
function initCaseCards() {
    const cards = document.querySelectorAll('.case-card-mini');
    
    cards.forEach(card => {
        card.addEventListener('click', () => {
            const projectIndex = parseInt(card.getAttribute('data-project'));
            openCaseModal(projectIndex);
        });
    });
}

// ========================================
// PRICE CALCULATOR
// ========================================
function initPriceCalculator() {
    const totalEl = document.getElementById('calcTotal');
    const projectInputs = document.querySelectorAll('input[name="projectType"]');
    const addonInputs = document.querySelectorAll('input[name="addon"]');
    if (!totalEl || projectInputs.length === 0) return;

    function formatPrice(value) {
        return value.toLocaleString('ru-RU').replace(/\s/g, ' ');
    }

    function calculate() {
        let base = 0;
        projectInputs.forEach(input => {
            if (input.checked) base = parseInt(input.value, 10);
        });

        if (base === 0) {
            totalEl.textContent = 'от 1 000 ₽/час';
            return;
        }

        let addons = 0;
        addonInputs.forEach(input => {
            if (input.checked) addons += parseInt(input.value, 10);
        });

        totalEl.textContent = '~' + formatPrice(base + addons) + ' ₽';
    }

    function updateVisualState() {
        projectInputs.forEach(input => {
            input.closest('.calc-option').classList.toggle('selected', input.checked);
        });
        addonInputs.forEach(input => {
            input.closest('.calc-option').classList.toggle('selected', input.checked);
        });
    }

    projectInputs.forEach(input => input.addEventListener('change', () => {
        calculate();
        updateVisualState();
    }));
    addonInputs.forEach(input => input.addEventListener('change', () => {
        calculate();
        updateVisualState();
    }));
    calculate();
    updateVisualState();
}

// ========================================
// CASE MODAL
// ========================================
let currentProject = 0;
let currentSlide = 0;

function initCaseModal() {
    const modal = document.getElementById('caseModal');
    if (!modal) return;
    
    const closeBtn = modal.querySelector('.case-modal-close');
    const backdrop = modal.querySelector('.case-modal-backdrop');
    
    closeBtn.addEventListener('click', closeCaseModal);
    backdrop.addEventListener('click', closeCaseModal);
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeCaseModal();
        }
    });
}

function openCaseModal(index) {
    const modal = document.getElementById('caseModal');
    const project = projectsData[index];
    currentProject = index;
    currentSlide = 0;
    
    modal.querySelector('.case-modal-title').textContent = project.title;
    modal.querySelector('.case-modal-task').textContent = project.task;
    modal.querySelector('.case-modal-solution').textContent = project.solution;
    
    const tagsContainer = modal.querySelector('.case-modal-tags');
    tagsContainer.innerHTML = project.tags.map(t => `<span>${t}</span>`).join('');
    
    const prefixes = ['carinsight', 'rzd', 'istanbul', 'chernika', 'visitka'];
    const prefix = prefixes[index];
    const totalImages = project.images;
    
    const track = modal.querySelector('.carousel-track');
    const dotsContainer = modal.querySelector('.carousel-dots');
    
    track.innerHTML = '';
    dotsContainer.innerHTML = '';
    
    for (let i = 1; i <= totalImages; i++) {
        const img = document.createElement('img');
        img.dataset.src = `assets/img/projects/${prefix}-${String(i).padStart(2, '0')}.webp`;
        img.alt = `${project.title} — скриншот ${i}`;
        track.appendChild(img);
        
        const dot = document.createElement('button');
        dot.className = 'carousel-dot';
        dot.ariaLabel = `Слайд ${i}`;
        dot.addEventListener('click', () => goToSlide(i - 1));
        dotsContainer.appendChild(dot);
    }
    
    loadSlideImages(0);
    goToSlide(0);
    
    const prevBtn = modal.querySelector('.carousel-prev');
    const nextBtn = modal.querySelector('.carousel-next');
    
    prevBtn.onclick = () => {
        if (currentSlide > 0) goToSlide(currentSlide - 1);
    };
    nextBtn.onclick = () => {
        if (currentSlide < totalImages - 1) goToSlide(currentSlide + 1);
    };
    
    document.body.style.overflow = 'hidden';
    modal.classList.add('active');
}

function closeCaseModal() {
    const modal = document.getElementById('caseModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

function loadSlideImages(slideIndex) {
    const modal = document.getElementById('caseModal');
    const track = modal.querySelector('.carousel-track');
    const images = track.querySelectorAll('img');
    
    images.forEach((img, i) => {
        if (i >= slideIndex - 1 && i <= slideIndex + 1) {
            if (!img.src || img.src !== img.dataset.src) {
                img.src = img.dataset.src;
            }
        } else {
            img.removeAttribute('src');
        }
    });
}

function goToSlide(index) {
    const modal = document.getElementById('caseModal');
    const track = modal.querySelector('.carousel-track');
    currentSlide = index;
    
    loadSlideImages(index);
    
    track.style.transform = `translateX(-${index * 100}%)`;
    
    const dots = modal.querySelectorAll('.carousel-dot');
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
    
    const prevBtn = modal.querySelector('.carousel-prev');
    const nextBtn = modal.querySelector('.carousel-next');
    const totalSlides = dots.length;
    
    prevBtn.style.opacity = index === 0 ? '0.3' : '1';
    nextBtn.style.opacity = index === totalSlides - 1 ? '0.3' : '1';
}
