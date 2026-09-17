/**
 * After contact Webform submit, scroll to the form / confirmation.
 */
(() => {
  const headerOffset = () => {
    const header = document.querySelector(".gw-header");
    return header ? header.getBoundingClientRect().height + 28 : 96;
  };

  const scrollToForm = () => {
    const target =
      document.querySelector(".webform-confirmation") ||
      document.querySelector(".gw-contact-thanks") ||
      document.querySelector(".messages--status") ||
      document.querySelector("[data-drupal-messages]") ||
      document.querySelector("#form");
    if (!target) {
      return;
    }
    const wrap = document.querySelector("#form") || target;
    const top = wrap.getBoundingClientRect().top + window.scrollY - headerOffset();
    window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
  };

  Drupal.behaviors.growibesContactConfirm = {
    attach(context) {
      const root = context.querySelectorAll ? context : document;
      const confirmation =
        root.querySelector(".webform-confirmation") ||
        document.querySelector(".webform-confirmation") ||
        document.querySelector(".messages--status");
      if (!confirmation || confirmation.dataset.gwScrolled === "1") {
        return;
      }
      confirmation.dataset.gwScrolled = "1";
      window.requestAnimationFrame(scrollToForm);
    },
  };

  const start = () => {
    if (
      document.querySelector(".webform-confirmation") ||
      document.querySelector(".messages--status") ||
      location.hash === "#form"
    ) {
      scrollToForm();
    }
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  }
  else {
    start();
  }
})();
