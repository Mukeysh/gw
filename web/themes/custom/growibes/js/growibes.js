/**
 * Growibes theme behaviors: mega menu + HTML/CSS island isolation.
 */
(() => {
  const toHost = (css) =>
    String(css || "").replace(
      /(^|}|,)(\s*)(html|body|:root)(?=[\s,{])/g,
      "$1$2:host"
    );

  const mountHtmlIsland = (el) => {
    if (el.shadowRoot) {
      return;
    }
    el.querySelectorAll("style").forEach((style) => {
      style.textContent = toHost(style.textContent);
    });
    const shadow = el.attachShadow({ mode: "open" });
    while (el.firstChild) {
      shadow.appendChild(el.firstChild);
    }
  };

  const closeItem = (item) => {
    item.classList.remove("is-open");
    item.querySelectorAll(":scope > .gw-nav__trigger, :scope > .gw-nav__parent-link").forEach((trigger) => {
      trigger.setAttribute("aria-expanded", "false");
      if (document.activeElement === trigger) {
        trigger.blur();
      }
    });
  };

  const closeAll = (header, except) => {
    header.querySelectorAll(".gw-nav__item.is-open").forEach((item) => {
      if (item !== except) {
        closeItem(item);
      }
    });
  };

  const initHeaderMenu = (header) => {
    const toggle = header.querySelector(".gw-header__toggle");
    const nav = header.querySelector(".gw-header__links");
    if (!nav || header.dataset.gwBound) {
      return;
    }
    header.dataset.gwBound = "true";

    if (toggle) {
      if (!nav.id) {
        nav.id = "gw-header-nav-" + Math.random().toString(36).slice(2, 8);
      }
      toggle.setAttribute("aria-controls", nav.id);
      toggle.addEventListener("click", (event) => {
        event.stopPropagation();
        const open = !header.classList.contains("is-open");
        header.classList.toggle("is-open", open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        if (!open) {
          closeAll(header);
        }
      });
    }

    const alignMega = (item) => {
      const panel = item.querySelector(":scope > .gw-nav__panel--mega");
      if (!panel) {
        return;
      }
      if (window.matchMedia("(max-width: 1080px)").matches) {
        panel.style.left = "";
        panel.style.width = "";
        panel.style.transform = "";
        return;
      }
      const headerRect = header.getBoundingClientRect();
      const itemRect = item.getBoundingClientRect();
      panel.style.transform = "none";
      panel.style.left = `${Math.round(headerRect.left - itemRect.left)}px`;
      panel.style.width = `${Math.round(headerRect.width)}px`;
    };

    header.querySelectorAll(".gw-nav__item--parent").forEach((item) => {
      const trigger = item.querySelector(":scope > .gw-nav__trigger, :scope > .gw-nav__parent-link");
      if (!trigger) {
        return;
      }

      const isMobile = () => window.matchMedia("(max-width: 1080px)").matches;
      let leaveTimer = 0;
      const openItem = () => {
        window.clearTimeout(leaveTimer);
        closeAll(header, item);
        alignMega(item);
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      };
      const scheduleClose = () => {
        window.clearTimeout(leaveTimer);
        leaveTimer = window.setTimeout(() => closeItem(item), 160);
      };

      item.addEventListener("mouseenter", () => {
        if (!isMobile()) {
          openItem();
        }
      });
      item.addEventListener("mouseleave", () => {
        if (!isMobile()) {
          scheduleClose();
        }
      });

      trigger.addEventListener("click", (event) => {
        if (!isMobile() && trigger.tagName === "A") {
          return;
        }
        event.preventDefault();
        event.stopPropagation();
        if (!isMobile()) {
          if (!item.classList.contains("is-open")) {
            openItem();
          }
          return;
        }
        const alreadyOpen = item.classList.contains("is-open");
        closeAll(header);
        if (!alreadyOpen) {
          openItem();
        }
      });
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a") && window.matchMedia("(max-width: 1080px)").matches) {
        header.classList.remove("is-open");
        if (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        }
        closeAll(header);
      }
    });

    document.addEventListener("click", (event) => {
      if (!header.contains(event.target)) {
        header.classList.remove("is-open");
        if (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        }
        closeAll(header);
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        header.classList.remove("is-open");
        if (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        }
        closeAll(header);
      }
    });

    window.addEventListener("resize", () => {
      header.querySelectorAll(".gw-nav__item--mega.is-open").forEach(alignMega);
    });
  };

  const visibleClients = () => {
    const width = window.innerWidth;
    if (width <= 600) {
      return 1;
    }
    if (width <= 950) {
      return 2;
    }
    return 4;
  };

  const initClientCarousel = (scope) => {
    if (!scope || !scope.querySelectorAll) {
      return;
    }
    scope.querySelectorAll("[data-client-carousel]").forEach((carousel) => {
      if (carousel.dataset.gwReady === "1") {
        return;
      }
      carousel.dataset.gwReady = "1";

      const viewport = carousel.querySelector(".client-viewport");
      const track = carousel.querySelector(".clientgrid");
      const prev = carousel.querySelector(".client-nav--prev");
      const next = carousel.querySelector(".client-nav--next");
      if (!viewport || !track) {
        return;
      }

      const originals = Array.from(track.children);
      const total = originals.length;
      if (!total) {
        return;
      }
      originals.forEach((node) => track.appendChild(node.cloneNode(true)));

      const gap = 10;
      let index = 0;
      let timer = null;
      let hovering = false;
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      const itemWidth = () => {
        const visible = visibleClients();
        return (viewport.clientWidth - gap * (visible - 1)) / visible;
      };

      const layout = () => {
        const width = itemWidth();
        Array.from(track.children).forEach((item) => {
          item.style.flex = `0 0 ${width}px`;
          item.style.maxWidth = `${width}px`;
        });
        goTo(index, false);
      };

      const goTo = (nextIndex, animate) => {
        index = nextIndex;
        track.style.transition = animate && !reduce ? "transform .45s cubic-bezier(.2,.8,.2,1)" : "none";
        const offset = index * (itemWidth() + gap);
        track.style.transform = `translateX(-${offset}px)`;
      };

      const nextSlide = () => {
        goTo(index + 1, true);
        if (index >= total) {
          window.setTimeout(() => goTo(index - total, false), reduce ? 0 : 460);
        }
      };

      const prevSlide = () => {
        if (index <= 0) {
          goTo(total, false);
          window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => goTo(total - 1, true));
          });
          return;
        }
        goTo(index - 1, true);
      };

      const stop = () => {
        if (timer) {
          window.clearInterval(timer);
          timer = null;
        }
      };

      const play = () => {
        stop();
        if (reduce || hovering) {
          return;
        }
        timer = window.setInterval(nextSlide, 3200);
      };

      prev?.addEventListener("click", () => {
        prevSlide();
        play();
      });
      next?.addEventListener("click", () => {
        nextSlide();
        play();
      });
      carousel.addEventListener("mouseenter", () => {
        hovering = true;
        stop();
      });
      carousel.addEventListener("mouseleave", () => {
        hovering = false;
        play();
      });
      carousel.addEventListener("focusin", stop);
      carousel.addEventListener("focusout", play);

      let startX = 0;
      viewport.addEventListener("pointerdown", (event) => {
        startX = event.clientX;
      });
      viewport.addEventListener("pointerup", (event) => {
        const delta = event.clientX - startX;
        if (Math.abs(delta) < 40) {
          return;
        }
        delta < 0 ? nextSlide() : prevSlide();
        play();
      });

      window.addEventListener("resize", layout);
      layout();
      play();
    });
  };

  const headerOffset = () => {
    const header = document.querySelector(".gw-header");
    return header ? header.getBoundingClientRect().height + 24 : 88;
  };

  const findPageId = (id) => {
    if (!id) {
      return null;
    }
    const light = document.getElementById(id);
    if (light) {
      return light;
    }
    for (const el of document.querySelectorAll(".gw-html")) {
      const found = el.shadowRoot && el.shadowRoot.getElementById(id);
      if (found) {
        return found;
      }
    }
    return null;
  };

  const scrollToPageId = (id) => {
    const target = findPageId(id);
    if (!target) {
      return false;
    }
    const top = target.getBoundingClientRect().top + window.scrollY - headerOffset();
    window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
    return true;
  };

  const boundHashRoots = new WeakSet();
  const bindHashLinks = (root) => {
    if (!root || boundHashRoots.has(root)) {
      return;
    }
    boundHashRoots.add(root);
    root.addEventListener("click", (event) => {
      const link = event.target.closest && event.target.closest('a[href^="#"]');
      if (!link) {
        return;
      }
      const href = link.getAttribute("href");
      if (!href || href === "#") {
        return;
      }
      const id = decodeURIComponent(href.slice(1));
      if (scrollToPageId(id)) {
        event.preventDefault();
        if (history.replaceState) {
          history.replaceState(null, "", href);
        }
      }
    });
  };

  const scrollFromLocationHash = () => {
    if (!location.hash || location.hash === "#") {
      return;
    }
    scrollToPageId(decodeURIComponent(location.hash.slice(1)));
  };

  const attach = (context) => {
    const root = context && context.querySelectorAll ? context : document;
    root.querySelectorAll(".gw-html").forEach((el) => {
      mountHtmlIsland(el);
      if (el.shadowRoot) {
        initClientCarousel(el.shadowRoot);
        bindHashLinks(el.shadowRoot);
      }
    });
    if (context && context.classList && context.classList.contains("gw-html")) {
      mountHtmlIsland(context);
      if (context.shadowRoot) {
        initClientCarousel(context.shadowRoot);
        bindHashLinks(context.shadowRoot);
      }
    }
    root.querySelectorAll(".gw-header").forEach(initHeaderMenu);
    if (context && context.classList && context.classList.contains("gw-header")) {
      initHeaderMenu(context);
    }
  };

  if (window.Drupal && Drupal.behaviors) {
    Drupal.behaviors.growibes = {
      attach(context) {
        attach(context);
      },
    };
  }

  attach(document);
  window.addEventListener("hashchange", scrollFromLocationHash);
  window.addEventListener("load", scrollFromLocationHash);
  window.setTimeout(scrollFromLocationHash, 50);
})();
