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

  const attach = (context) => {
    const root = context && context.querySelectorAll ? context : document;
    root.querySelectorAll(".gw-html").forEach(mountHtmlIsland);
    if (context && context.classList && context.classList.contains("gw-html")) {
      mountHtmlIsland(context);
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
})();
