/**
 * DAMIR VARLAMOV - PREMIUM PORTFOLIO
 * Modern Interactive JavaScript
 */

// ========================================
// INITIALIZATION
// ========================================
document.addEventListener('DOMContentLoaded', () => {
  initCursor();
  initThemeToggle();
  initMobileMenu();
  initScrollEffects();
  initSmoothScroll();
  // initTiltEffect(); // Disabled - removed 3D tilt effect
  initRippleEffect();
  initScrollTop();
  initFormSubmit();
  initNavbarScroll();
  // initRevealAnimations(); // Disabled - removed block appearance animations
  initParallax();
});

// ========================================
// THROTTLE HELPER
// ========================================
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

function isMobile() {
  return window.innerWidth <= 768;
}

// ========================================
// CUSTOM CURSOR
// ========================================
function initCursor() {
  if (window.matchMedia('(pointer: fine)').matches) {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    cursor.innerHTML = '<div class="cursor-dot"></div><div class="cursor-ring"></div>';
    document.body.appendChild(cursor);
    
    const dot = cursor.querySelector('.cursor-dot');
    const ring = cursor.querySelector('.cursor-ring');
    
    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let ringX = 0, ringY = 0;
    
    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });
    
    function animate() {
      dotX += (mouseX - dotX) * 0.15;
      dotY += (mouseY - dotY) * 0.15;
      ringX += (mouseX - ringX) * 0.08;
      ringY += (mouseY - ringY) * 0.08;
      
      dot.style.transform = `translate(${dotX}px, ${dotY}px)`;
      ring.style.transform = `translate(${ringX}px, ${ringY}px)`;
      
      requestAnimationFrame(animate);
    }
    animate();
    
    // Add hover effect to interactive elements
    const interactiveElements = 'a, button, .project-card, .service-card, .review-card, .tech-item, .trait, .contact-card, .btn';
    document.querySelectorAll(interactiveElements).forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('hover'));
      el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
    });
    
    // Hide cursor when leaving window
    document.addEventListener('mouseleave', () => cursor.style.opacity = '0');
    document.addEventListener('mouseenter', () => cursor.style.opacity = '1');
  }
}

// ========================================
// THEME TOGGLE
// ========================================
function initThemeToggle() {
  const toggle = document.getElementById('themeToggle');
  const icon = toggle.querySelector('i');
  
  // Check saved preference or system preference
  const savedTheme = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
  } else if (!systemPrefersDark) {
    document.documentElement.setAttribute('data-theme', 'light');
    updateThemeIcon('light');
  }
  
  toggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Add transition effect
    document.documentElement.style.transition = 'background 0.5s ease, color 0.5s ease';
  });
  
  function updateThemeIcon(theme) {
    if (theme === 'light') {
      icon.className = 'fas fa-sun';
    } else {
      icon.className = 'fas fa-moon';
    }
  }
}

// ========================================
// MOBILE MENU
// ========================================
function initMobileMenu() {
  const menuToggle = document.getElementById('menuToggle');
  const nav = document.getElementById('nav');
  
  menuToggle.addEventListener('click', () => {
    nav.classList.toggle('active');
    menuToggle.classList.toggle('active');
  });
  
  // Close menu when clicking on a link
  nav.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('active');
      menuToggle.classList.remove('active');
    });
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
      nav.classList.remove('active');
      menuToggle.classList.remove('active');
    }
  });
}

// ========================================
// SCROLL EFFECTS
// ========================================
function initScrollEffects() {
  if (isMobile()) return;
  
  const scrolled = () => window.pageYOffset;
  const orbs = document.querySelectorAll('.orb');
  
  window.addEventListener('scroll', throttle(() => {
    const offset = scrolled();
    orbs.forEach((orb, index) => {
      const speed = 0.1 + (index * 0.05);
      orb.style.transform = `translateY(${offset * speed}px)`;
    });
  }, 50));
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
        
        const headerHeight = document.querySelector('.header').offsetHeight;
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
// 3D TILT EFFECT
// ========================================
function initTiltEffect() {
  const cards = document.querySelectorAll('.project-card, .service-card, .review-card');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = (y - centerY) / 15;
      const rotateY = (centerX - x) / 15;
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
    });
  });
}

// ========================================
// RIPPLE EFFECT
// ========================================
function initRippleEffect() {
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const ripple = document.createElement('span');
      ripple.style.cssText = `
        position: absolute;
        width: 20px;
        height: 20px;
        background: rgba(255,255,255,0.4);
        border-radius: 50%;
        left: ${x}px;
        top: ${y}px;
        transform: translate(-50%, -50%) scale(0);
        animation: ripple 0.8s linear;
        pointer-events: none;
      `;
      
      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 800);
    });
  });
  
  // Add ripple animation
  if (!document.querySelector('#ripple-style')) {
    const style = document.createElement('style');
    style.id = 'ripple-style';
    style.textContent = `
      @keyframes ripple {
        to {
          transform: translate(-50%, -50%) scale(30);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
  }
}

// ========================================
// SCROLL TO TOP
// ========================================
function initScrollTop() {
  const scrollBtn = document.getElementById('scrollTop');
  
  window.addEventListener('scroll', throttle(() => {
    if (window.scrollY > 500) {
      scrollBtn.classList.add('visible');
    } else {
      scrollBtn.classList.remove('visible');
    }
  }, 100));
  
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
    
    const formData = new FormData(form);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');
    
    const subject = encodeURIComponent(`Портфолио: сообщение от ${name}`);
    const body = encodeURIComponent(`Имя: ${name}\nEmail/Telegram: ${email}\n\nСообщение:\n${message}`);
    
    window.location.href = `mailto:damir.itwar@yandex.ru?subject=${subject}&body=${body}`;
    
    showNotification('Почтовый клиент открыт! Нажмите "Отправить".', 'success');
    
    form.reset();
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
  
  // Add notification styles
  if (!document.querySelector('#notification-style')) {
    const style = document.createElement('style');
    style.id = 'notification-style';
    style.textContent = `
      .notification {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--bg-card);
        border: 1px solid var(--border);
        padding: 16px 24px;
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        gap: 16px;
        z-index: 10000;
        box-shadow: var(--shadow-md);
        animation: slideInUp 0.3s ease;
      }
      .notification-success {
        border-color: var(--accent-success);
      }
      .notification-success span {
        color: var(--accent-success);
      }
      .notification button {
        background: none;
        border: none;
        color: var(--text-muted);
        cursor: pointer;
      }
    `;
    document.head.appendChild(style);
  }
  
  setTimeout(() => notification.remove(), 5000);
}

// ========================================
// NAVBAR SCROLL
// ========================================
function initNavbarScroll() {
  const header = document.querySelector('.header');
  
  window.addEventListener('scroll', throttle(() => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, 100));
}

// ========================================
// REVEAL ANIMATIONS
// ========================================
function initRevealAnimations() {
  // Check for reduced motion preference
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -100px 0px',
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
  
  // Observe elements with reveal class
  document.querySelectorAll('.project-card, .service-card, .review-card, .trait, .tech-item, .about-info, .about-stack').forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(40px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    el.style.transitionDelay = `${index * 0.1}s`;
    observer.observe(el);
  });
  
  // Add revealed class styles
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
// PARALLAX BACKGROUND
// ========================================
function initParallax() {
  if (isMobile()) return;
  
  const bgElements = document.querySelectorAll('.bg-gradient, .bg-grid');
  
  window.addEventListener('scroll', throttle(() => {
    const scrolled = window.pageYOffset;
    bgElements.forEach(el => {
      el.style.transform = `translateY(${scrolled * 0.3}px)`;
    });
  }, 50));
}

// ========================================
// ACTIVE NAV LINK
// ========================================
function initActiveNavLink() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  
  window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      const headerHeight = document.querySelector('.header').offsetHeight;
      
      if (window.scrollY >= sectionTop - headerHeight - 200) {
        current = section.getAttribute('id');
      }
    });
    
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', initActiveNavLink);