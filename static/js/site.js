(function () {
  function wrapCodeBlocks() {
    document.querySelectorAll("pre").forEach(function (pre) {
      if (pre.closest(".pre-wrap")) return;
      if (pre.querySelector("code.language-mermaid, code[data-lang='mermaid']")) return;
      var wrap = document.createElement("div");
      wrap.className = "pre-wrap";
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.addEventListener("click", function () {
        var text = pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = "Copied";
          btn.classList.add("copied");
          setTimeout(function () {
            btn.textContent = "Copy";
            btn.classList.remove("copied");
          }, 1600);
        });
      });
      wrap.appendChild(btn);
    });
  }

  function wireDemos() {
    document.querySelectorAll("[data-demo-root]").forEach(function (root) {
      var btn = root.querySelector("[data-demo-load]");
      var host = root.querySelector("[data-demo-host]");
      if (!btn || !host) return;
      btn.addEventListener("click", function () {
        var src = root.getAttribute("data-demo-src");
        if (!src) return;
        var iframe = document.createElement("iframe");
        iframe.src = src;
        iframe.title = root.getAttribute("data-demo-title") || "Live demo";
        iframe.loading = "lazy";
        iframe.allow = "fullscreen; gamepad; clipboard-read; clipboard-write";
        iframe.referrerPolicy = "no-referrer-when-downgrade";
        host.innerHTML = "";
        host.appendChild(iframe);
        iframe.focus();
      });
    });
  }

  function boot() {
    wrapCodeBlocks();
    wireDemos();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
