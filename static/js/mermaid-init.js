(function () {
  function collectMermaidBlocks() {
    var nodes = [];
    document.querySelectorAll("pre code.language-mermaid, pre code[data-lang='mermaid']").forEach(function (code) {
      nodes.push(code);
    });
    // Some highlight themes wrap differently
    document.querySelectorAll("pre.language-mermaid code, pre.mermaid code").forEach(function (code) {
      if (nodes.indexOf(code) === -1) nodes.push(code);
    });
    return nodes;
  }

  function upgrade() {
    var blocks = collectMermaidBlocks();
    if (!blocks.length || typeof mermaid === "undefined") return;
    mermaid.initialize({
      startOnLoad: false,
      theme: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "default",
      securityLevel: "loose",
    });
    blocks.forEach(function (code, i) {
      var pre = code.closest("pre") || code.parentElement;
      var graph = code.textContent;
      var div = document.createElement("div");
      div.className = "mermaid";
      div.textContent = graph;
      div.setAttribute("data-mermaid-id", "m-" + i);
      pre.replaceWith(div);
    });
    mermaid.run({ querySelector: ".mermaid" });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", upgrade);
  } else {
    upgrade();
  }
})();
