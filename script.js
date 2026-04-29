/* ================================================================
   RADKA RANIAKOVÁ — Swiss Minimalism — JavaScript
   SPA pages, multi-level gallery, scroll reveal, lightbox
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* ── SCROLL REVEAL OBSERVER ── */
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    function observeReveals() {
        document.querySelectorAll('.scroll-reveal:not(.visible)').forEach(el => {
            revealObserver.observe(el);
        });
    }

    /* ── Remove loading class (opacity fade-in) ── */
    requestAnimationFrame(() => {
        document.body.classList.remove('loading');
        const firstPage = document.querySelector('.page.active');
        if (firstPage) requestAnimationFrame(() => firstPage.classList.add('visible'));
        observeReveals();
    });

    /* ── DATA: PORTFOLIO (Case Studies) ── */
    const caseStudies = {
        spartan: {
            title: 'Spartan Race SK',
            desc: 'Spartan Race je ultimátny test vytrvalosti a odvahy. Fotila som závodníkov v ich najťažších momentoch — v blate, cez oheň a na prekážkach. Každý záber zachytáva boj, odhodlanie a víťazstvo nad samým sebou.',
            meta: ['Klient: Spartan Race SK', 'Dátum: Júl 2024', 'Služba: Event foto'],
            images: ['images/portrait_5_1774420941641.png', 'images/portrait_1_1774420752942.png']
        },
        krajina: {
            title: 'Outdoor kampane',
            desc: 'Slovenská krajina je plná dramatických scenérií. Tieto zábery zachytávajú pokojné ráno, hmlisté lesy a západ slnka nad Tatrami. Využité priamo v TV / Online grepe.',
            meta: ['Klient: Outdoor Značka', 'Rok: 2024', 'Služba: Foto & Promo Video'],
            images: ['images/portrait_3_1774420845476.png', 'images/portrait_4_1774420868506.png']
        },
        eshop: {
            title: 'E-commerce klient',
            desc: 'Prepojenie výkonnostného marketingu s poctivou produktovou fotografiou. Po audite účtov sme menili vizuálnu identitu komunikácie a škálovali ROAS.',
            meta: ['Focus: E-shop', 'Rok: 2024', 'Služba: Kompletná správa PPC'],
            images: ['images/portrait_1_1774420752942.png', 'images/portrait_6_1774421106069.png']
        },
        social: {
            title: 'Reštaurácia & Gastronómia',
            desc: 'Komplexná sociálna komunikácia pre lokálnu reštauráciu. Tvorba organických UGC videí a vysokokvalitné food fotenie menu prinieslo nárast rezervácií stola o 140%.',
            meta: ['Focus: Gastro', 'Rok: 2023–2024', 'Služba: Social + Foto + UGC'],
            images: ['images/portrait_2_1774420801237.png', 'images/portrait_4_1774420868506.png']
        }
    };

    /* ── DATA: GALLERY (Categories & Albums) ── */
    const galleryData = {
        svadba: {
            title: 'Svadba',
            albums: [
                { id: 'sv1', title: 'Lucia & Jakub | 2025', desc: 'Svadba v Tatrách', thumb: 'images/portrait_6_1774421106069.png', images: ['images/portrait_6_1774421106069.png', 'images/portrait_3_1774420845476.png'] },
                { id: 'sv2', title: 'Michaela & Peter | 2024', desc: 'Zámocký park', thumb: 'images/portrait_4_1774420868506.png', images: ['images/portrait_4_1774420868506.png', 'images/portrait_2_1774420801237.png'] }
            ]
        },
        sport: {
            title: 'Šport',
            albums: [
                { id: 'sp1', title: 'Spartan Race | 2024', desc: 'Extrémny beh', thumb: 'images/portrait_5_1774420941641.png', images: ['images/portrait_5_1774420941641.png', 'images/portrait_1_1774420752942.png'] }
            ]
        },
        portrety: {
            title: 'Portréty',
            albums: [
                { id: 'po1', title: 'Ateliér & Business', desc: 'Headshoty 2024', thumb: 'images/portrait_2_1774420801237.png', images: ['images/portrait_2_1774420801237.png', 'images/portrait_1_1774420752942.png'] }
            ]
        },
        krajina: {
            title: 'Krajina',
            albums: [
                { id: 'kr1', title: 'Tatry & Fatra', desc: 'Osobný projekt', thumb: 'images/portrait_3_1774420845476.png', images: ['images/portrait_3_1774420845476.png', 'images/portrait_4_1774420868506.png'] }
            ]
        },
        lifestyle: {
            title: 'Lifestyle',
            albums: [
                { id: 'ls1', title: 'Rodinné fotenie', desc: 'Jesenné farby', thumb: 'images/portrait_4_1774420868506.png', images: ['images/portrait_4_1774420868506.png', 'images/portrait_6_1774421106069.png'] }
            ]
        },
        jedlo: {
            title: 'Jedlo',
            albums: [
                { id: 'je1', title: 'Menu Fotenie', desc: 'Food styling', thumb: 'images/portrait_1_1774420752942.png', images: ['images/portrait_1_1774420752942.png', 'images/portrait_2_1774420801237.png'] }
            ]
        }
    };

    /* ── PAGE SWITCHING ── */
    const pages = document.querySelectorAll('.page');
    const navLinks = document.querySelectorAll('.sidebar__link');

    function showPage(pageId) {
        const current = document.querySelector('.page.active.visible');
        if (current) current.classList.remove('visible');

        setTimeout(() => {
            pages.forEach(p => p.classList.remove('active', 'visible'));
            const target = document.getElementById('page-' + pageId);
            if (target) {
                target.classList.add('active');
                void target.offsetWidth;
                requestAnimationFrame(() => target.classList.add('visible'));
            }

            navLinks.forEach(l => l.classList.remove('active'));
            const link = document.querySelector(`.sidebar__link[data-page="${pageId === 'albums' || pageId === 'project' ? 'fotogaleria' : pageId}"]`);
            if (link) link.classList.add('active');

            window.scrollTo(0, 0);
            observeReveals();
        }, 200);
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(link.dataset.page);
            closeSidebar();
        });
    });

    document.querySelectorAll('.breadcrumb-link').forEach(link => {
        link.addEventListener('click', () => showPage(link.dataset.page));
    });

    /* ── MOBILE SIDEBAR ── */
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    function closeSidebar() {
        hamburger.classList.remove('active');
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        document.body.classList.remove('no-scroll');
    }

    hamburger.addEventListener('click', () => {
        const open = sidebar.classList.contains('open');
        if (open) closeSidebar();
        else {
            hamburger.classList.add('active');
            sidebar.classList.add('open');
            overlay.classList.add('active');
            document.body.classList.add('no-scroll');
        }
    });

    overlay.addEventListener('click', closeSidebar);

    /* ── PORTFOLIO: CASE STUDIES LOGIC ── */
    document.querySelectorAll('.proj-card').forEach(card => {
        card.addEventListener('click', () => {
            const key = card.dataset.proj;
            const proj = caseStudies[key];
            if (!proj) return;

            document.getElementById('proj-title').textContent = proj.title;
            document.getElementById('proj-split').style.display = 'grid';
            document.getElementById('proj-photos-masonry').style.display = 'none';
            document.getElementById('proj-breadcrumbs').style.display = 'none';
            document.getElementById('back-btn').style.display = 'inline-block';

            const infoEl = document.getElementById('proj-info');
            infoEl.innerHTML = `
                <p>${proj.desc}</p>
                <div class="info-meta">
                    ${proj.meta.map(m => `<span>${m}</span>`).join('')}
                </div>
            `;

            const photosEl = document.getElementById('proj-photos-split');
            photosEl.innerHTML = '';
            proj.images.forEach((src, i) => {
                const img = document.createElement('img');
                img.src = src;
                img.classList.add('scroll-reveal');
                img.loading = 'lazy';
                img.addEventListener('click', () => openLightbox(proj.images, i));
                photosEl.appendChild(img);
            });

            showPage('project');
        });
    });

    document.getElementById('back-btn').addEventListener('click', () => showPage('portfolio'));

    /* ── GALLERY: LEVEL 1 (Categories) -> LEVEL 2 (Albums) ── */
    let currentCategory = null;

    document.querySelectorAll('.cat-click').forEach(tile => {
        tile.addEventListener('click', () => {
            const catKey = tile.dataset.cat;
            currentCategory = galleryData[catKey];
            if (!currentCategory) return;

            document.getElementById('albums-category-name').textContent = currentCategory.title;
            document.getElementById('albums-title').textContent = currentCategory.title;
            document.getElementById('bc-category-link').textContent = currentCategory.title;
            document.getElementById('bc-category-link').onclick = () => showPage('albums');

            const grid = document.getElementById('albums-grid');
            grid.innerHTML = '';

            currentCategory.albums.forEach(album => {
                const div = document.createElement('div');
                div.className = 'album-card scroll-reveal';
                div.innerHTML = `
                    <div class="album-card__img-wrap">
                        <div class="album-card__img" style="background-image:url('${album.thumb}')"></div>
                    </div>
                    <div class="album-card__info">
                        <h3>${album.title}</h3>
                        <p>${album.desc}</p>
                    </div>
                `;
                div.addEventListener('click', () => openGalleryAlbum(album));
                grid.appendChild(div);
            });

            showPage('albums');
        });
    });

    /* ── GALLERY: LEVEL 2 (Albums) -> LEVEL 3 (Photos) ── */
    function openGalleryAlbum(album) {
        document.getElementById('proj-title').textContent = album.title;
        document.getElementById('bc-album-name').textContent = album.title;
        
        document.getElementById('proj-split').style.display = 'none';
        document.getElementById('back-btn').style.display = 'none';
        document.getElementById('proj-breadcrumbs').style.display = 'flex';
        document.getElementById('proj-photos-masonry').style.display = 'grid';

        const masonry = document.getElementById('proj-photos-masonry');
        masonry.innerHTML = '';

        album.images.forEach((src, i) => {
            const img = document.createElement('img');
            img.src = src;
            img.classList.add('scroll-reveal');
            img.loading = 'lazy';
            img.addEventListener('click', () => openLightbox(album.images, i));
            masonry.appendChild(img);
        });

        showPage('project');
    }

    /* ── LIGHTBOX ── */
    const lightbox = document.getElementById('lightbox');
    const lbImg = document.getElementById('lb-img');
    const lbCount = document.getElementById('lb-count');
    let lbItems = [], lbIdx = 0;

    function openLightbox(items, idx) {
        lbItems = items;
        lbIdx = idx;
        refreshLb();
        lightbox.classList.add('active');
        document.body.classList.add('no-scroll');
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.classList.remove('no-scroll');
    }

    function refreshLb() {
        lbImg.src = lbItems[lbIdx];
        lbCount.textContent = (lbIdx + 1) + ' / ' + lbItems.length;
    }

    function lbNext() { lbIdx = (lbIdx + 1) % lbItems.length; refreshLb(); }
    function lbPrev() { lbIdx = (lbIdx - 1 + lbItems.length) % lbItems.length; refreshLb(); }

    document.getElementById('lb-close').addEventListener('click', closeLightbox);
    document.getElementById('lb-next').addEventListener('click', lbNext);
    document.getElementById('lb-prev').addEventListener('click', lbPrev);

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowRight') lbNext();
        if (e.key === 'ArrowLeft') lbPrev();
    });

    // Touch swipe
    let swipeX = 0;
    lightbox.addEventListener('touchstart', (e) => { swipeX = e.changedTouches[0].screenX; }, { passive: true });
    lightbox.addEventListener('touchend', (e) => {
        const diff = swipeX - e.changedTouches[0].screenX;
        if (Math.abs(diff) > 50) { diff > 0 ? lbNext() : lbPrev(); }
    }, { passive: true });

    /* ── FORM ── */
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = document.getElementById('submit-btn');
            btn.textContent = 'ODOSIELAM...';
            btn.disabled = true;
            btn.style.opacity = '0.6';
            setTimeout(() => {
                btn.textContent = 'ODOSLANÉ ✓';
                btn.style.opacity = '1';
                setTimeout(() => {
                    e.target.reset();
                    btn.textContent = 'Odoslať správu';
                    btn.disabled = false;
                }, 2000);
            }, 1200);
        });
    }

});
