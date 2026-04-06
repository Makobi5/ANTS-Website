/**
 * multi_image_upload.js
 * Place at: static/js/multi_image_upload.js
 *
 * Features:
 *  - Drag & drop MULTIPLE images at once
 *  - "Browse" button supports multi-select
 *  - Auto-creates new inline rows as needed
 *  - Thumbnail previews
 */

(function () {
  "use strict";

  function waitForInline(callback) {
    var attempts = 0;
    var timer = setInterval(function () {
      attempts++;
      var inline = document.getElementById("newsimage_set-group");
      if (inline) {
        clearInterval(timer);
        callback(inline);
      }
      if (attempts > 40) clearInterval(timer);
    }, 100);
  }

  function init(inlineGroup) {

    /* ── Inject CSS ── */
    var style = document.createElement("style");
    style.textContent = `
      #gallery-dropzone {
        border: 2px dashed #79aec8;
        border-radius: 8px;
        background: #f0f8ff;
        padding: 28px 20px 20px;
        margin-bottom: 18px;
        text-align: center;
        transition: background .2s, border-color .2s;
        cursor: pointer;
      }
      #gallery-dropzone.dz-over {
        background: #dceefb;
        border-color: #2196f3;
      }
      #gallery-dropzone svg {
        display: block;
        margin: 0 auto 10px;
        color: #79aec8;
      }
      #gallery-dropzone p {
        margin: 0 0 10px;
        font-size: 14px;
        color: #444;
        line-height: 1.7;
      }
      #gallery-browse-btn {
        display: inline-block;
        padding: 7px 20px;
        background: #417690;
        color: #fff;
        border: none;
        border-radius: 4px;
        font-size: 13px;
        cursor: pointer;
        font-weight: 600;
        letter-spacing: .3px;
      }
      #gallery-browse-btn:hover { background: #2c5f7a; }
      #gallery-preview-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 16px;
        justify-content: center;
      }
      .dz-thumb {
        position: relative;
        width: 86px;
        height: 86px;
        border-radius: 6px;
        overflow: hidden;
        border: 2px solid #4caf50;
        box-shadow: 0 2px 6px rgba(0,0,0,.15);
      }
      .dz-thumb img {
        width: 100%; height: 100%;
        object-fit: cover; display: block;
      }
      .dz-thumb-label {
        position: absolute; bottom: 0; left: 0; right: 0;
        background: rgba(0,0,0,.55);
        color: #fff; font-size: 9px;
        text-align: center; padding: 3px 2px;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      }
      #gallery-count-badge {
        display: inline-block;
        margin-left: 8px;
        background: #4caf50;
        color: #fff;
        border-radius: 10px;
        padding: 1px 8px;
        font-size: 12px;
        font-weight: bold;
        vertical-align: middle;
      }
    `;
    document.head.appendChild(style);

    /* ── Build the drop zone HTML ── */
    var dz = document.createElement("div");
    dz.id = "gallery-dropzone";
    dz.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 24 24"
           fill="none" stroke="currentColor" stroke-width="1.5"
           stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
        <circle cx="8.5" cy="8.5" r="1.5"/>
        <polyline points="21 15 16 10 5 21"/>
      </svg>
      <p>
        <strong>Drag &amp; drop photos here</strong><br>
        or click the button below to browse &mdash; select as many as you want at once
      </p>
      <button type="button" id="gallery-browse-btn">&#128247; Choose Photos</button>
      <input type="file" id="gallery-file-input" accept="image/*" multiple
             style="display:none">
      <div id="gallery-preview-strip"></div>
    `;

    inlineGroup.parentNode.insertBefore(dz, inlineGroup);

    var fileInput = document.getElementById("gallery-file-input");
    var browseBtn = document.getElementById("gallery-browse-btn");
    var previewStrip = document.getElementById("gallery-preview-strip");

    /* ── Browse button ── */
    browseBtn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      fileInput.click();
    });

    fileInput.addEventListener("change", function () {
      processFiles(this.files);
      this.value = "";
    });

    /* ── Drag events ── */
    dz.addEventListener("dragover", function (e) {
      e.preventDefault();
      dz.classList.add("dz-over");
    });
    dz.addEventListener("dragleave", function (e) {
      if (!dz.contains(e.relatedTarget)) dz.classList.remove("dz-over");
    });
    dz.addEventListener("drop", function (e) {
      e.preventDefault();
      dz.classList.remove("dz-over");
      processFiles(e.dataTransfer.files);
    });

    dz.addEventListener("click", function (e) {
      if (e.target !== browseBtn && e.target !== fileInput) {
        fileInput.click();
      }
    });

    /* ── Process a FileList ── */
    function processFiles(files) {
      if (!files || !files.length) return;
      var imageFiles = Array.from(files).filter(function (f) {
        return f.type.startsWith("image/");
      });
      processNext(imageFiles, 0);
    }

    /* Process one file at a time, waiting for new rows to render */
    function processNext(files, index) {
      if (index >= files.length) {
        updateCountBadge();
        return;
      }
      var file = files[index];
      var freeRow = findFreeRow();

      if (freeRow) {
        stageFile(freeRow, file);
        addThumb(file);
        processNext(files, index + 1);
      } else {
        clickAddRow();
        /* Wait for Django to render the new row */
        setTimeout(function () {
          var newRow = findFreeRow();
          if (newRow) {
            stageFile(newRow, file);
            addThumb(file);
          }
          processNext(files, index + 1);
        }, 150);
      }
    }

    function findFreeRow() {
      var rows = inlineGroup.querySelectorAll(".dynamic-newsimage_set");
      for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var deleteChk = row.querySelector('input[id$="-DELETE"]');
        if (deleteChk && deleteChk.checked) continue;
        var fileInp = row.querySelector('input[type="file"]');
        if (fileInp && !fileInp._dzUsed) {
          return row;
        }
      }
      return null;
    }

    function stageFile(row, file) {
      var fileInp = row.querySelector('input[type="file"]');
      if (!fileInp) return;
      try {
        var dt = new DataTransfer();
        dt.items.add(file);
        fileInp.files = dt.files;
        fileInp._dzUsed = true;
        fileInp.dispatchEvent(new Event("change", { bubbles: true }));
      } catch (err) {
        console.error("Could not stage file:", err);
      }
    }

    function clickAddRow() {
      var addLink = inlineGroup.querySelector(".add-row a");
      if (addLink) addLink.click();
    }

    function addThumb(file) {
      var reader = new FileReader();
      reader.onload = function (e) {
        var thumb = document.createElement("div");
        thumb.className = "dz-thumb";
        thumb.innerHTML = `
          <img src="${e.target.result}" alt="">
          <div class="dz-thumb-label">${file.name}</div>
        `;
        previewStrip.appendChild(thumb);
      };
      reader.readAsDataURL(file);
    }

    function updateCountBadge() {
      var header = inlineGroup.querySelector("h2");
      if (!header) return;
      var existing = header.querySelector("#gallery-count-badge");
      if (existing) existing.remove();
      var count = inlineGroup.querySelectorAll("input[type='file']._dzUsed, input[type='file'][_dzUsed]").length;
      // Count via _dzUsed property
      var inputs = inlineGroup.querySelectorAll("input[type='file']");
      count = 0;
      inputs.forEach(function (inp) { if (inp._dzUsed) count++; });
      if (count > 0) {
        var badge = document.createElement("span");
        badge.id = "gallery-count-badge";
        badge.textContent = count + " queued";
        header.appendChild(badge);
      }
    }

    /* ── Upgrade existing Choose File buttons to also support multi-select ── */
    function upgradeExistingInputs() {
      inlineGroup.querySelectorAll('input[type="file"]').forEach(function (inp) {
        inp.setAttribute("multiple", "multiple");
        inp.setAttribute("accept", "image/*");
      });
    }

    upgradeExistingInputs();

    var observer = new MutationObserver(upgradeExistingInputs);
    observer.observe(inlineGroup, { childList: true, subtree: true });
  }

  /* ── Boot ── */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { waitForInline(init); });
  } else {
    waitForInline(init);
  }

})();