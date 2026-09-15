// ==UserScript==
// @name         JioLite for JioSaavn
// @namespace    com.thompcha.jiolite
// @version      1.2.0
// @description  Adds JioLite controls and removes JioSaavn's non-Pro visual clutter.
// @match        https://www.jiosaavn.com/*
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(() => {
  "use strict";

  const BUTTON_CLASS = "jiolite-download";
  let updateScheduled = false;

  const style = document.createElement("style");
  style.textContent = `
    .jiolite-download-cell {
      align-items: center;
      display: flex;
      justify-content: center;
    }

    .jiolite-download {
      align-items: center;
      background: transparent;
      border: 0;
      border-radius: 50%;
      box-sizing: border-box;
      color: #2bc5b4 !important;
      cursor: pointer;
      display: inline-flex;
      height: 32px;
      justify-content: center;
      padding: 6px;
      transition: background-color 120ms ease, color 120ms ease, transform 120ms ease;
      width: 32px;
    }

    .jiolite-download:hover,
    .jiolite-download:focus-visible,
    .jiolite-download--sent {
      background: #2bc5b4;
      color: #fff !important;
      outline: none;
      transform: scale(1.06);
    }

    .jiolite-download svg {
      fill: none;
      height: 20px;
      stroke: currentColor;
      stroke-linecap: round;
      stroke-linejoin: round;
      stroke-width: 2;
      width: 20px;
    }

    .jiolite-dismissed {
      display: none !important;
    }

    .jiolite-pro-only {
      display: none !important;
    }

    article.o-snippet.jiolite-full-brightness,
    article.o-snippet.jiolite-full-brightness * {
      filter: none !important;
      opacity: 1 !important;
    }
  `;
  document.head.appendChild(style);

  function dismissObstructions() {
    const cookieToast = document.querySelector(".c-toast.c-toast--gdpr");
    if (cookieToast && !cookieToast.dataset.jioliteDismissed) {
      cookieToast.dataset.jioliteDismissed = "true";
      cookieToast.classList.add("jiolite-dismissed");
      cookieToast.querySelector(".c-toast__btn")?.click();
    }

    document.querySelectorAll(".c-banner.active").forEach(banner => {
      if (banner.dataset.jioliteDismissed) return;
      const bannerText = banner.textContent.toLowerCase();
      if (!bannerText.includes("free trial") && !bannerText.includes("jiosaavn pro")) return;

      banner.dataset.jioliteDismissed = "true";
      banner.classList.add("jiolite-dismissed");
      banner.querySelector(".c-banner__close")?.click();
    });
  }

  function makeButton(songURL, title) {
    const button = document.createElement("a");
    button.className = BUTTON_CLASS;
    button.href = `jiolite://download?url=${encodeURIComponent(songURL)}`;
    button.title = `Download ${title || "track"} with JioLite`;
    button.setAttribute("aria-label", button.title);
    button.setAttribute("role", "button");
    button.innerHTML = `
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M12 3v11m0 0 4-4m-4 4-4-4M5 19h14" />
      </svg>`;

    button.addEventListener("mousedown", event => event.stopPropagation());
    button.addEventListener("dragstart", event => event.preventDefault());
    button.addEventListener("click", event => {
      event.stopPropagation();
      button.classList.add("jiolite-download--sent");
      window.setTimeout(() => button.classList.remove("jiolite-download--sent"), 1800);
    });
    return button;
  }

  function addButtons() {
    updateScheduled = false;
    dismissObstructions();
    document.querySelectorAll("article.o-snippet").forEach(article => {
      if (article.querySelector(`.${BUTTON_CLASS}`)) return;

      const songLink = article.querySelector(
        'a.o-flag__img[href*="/song/"], .o-flag__body a[href*="/song/"]'
      );
      if (!songLink) return;

      const songURL = new URL(songLink.href);
      if (songURL.hostname !== "www.jiosaavn.com") return;

      article.classList.add("jiolite-full-brightness");
      Array.from(article.querySelectorAll(".o-snippet__item")).forEach(item => {
        if (item.textContent.trim().toLowerCase() === "pro only") {
          item.classList.add("jiolite-pro-only");
        }
      });

      const emptyActionCell = Array.from(
        article.querySelectorAll(".o-snippet__item.u-align-center")
      ).find(cell => cell.children.length === 0);
      const target = emptyActionCell || article.lastElementChild;
      if (!target) return;

      target.classList.add("jiolite-download-cell");
      target.appendChild(makeButton(songURL.href, songLink.textContent.trim()));
    });
  }

  function scheduleUpdate() {
    if (updateScheduled) return;
    updateScheduled = true;
    window.requestAnimationFrame(addButtons);
  }

  addButtons();
  new MutationObserver(scheduleUpdate).observe(document.documentElement, {
    childList: true,
    subtree: true
  });
})();
