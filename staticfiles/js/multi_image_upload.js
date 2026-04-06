/**
 * multi_image_upload.js
 * Drag-and-drop + multi-select image uploader for Django Admin TabularInline.
 * Place this file in:  news/static/news/js/multi_image_upload.js
 */

(function ($) {
  "use strict";

  function initMultiUpload() {
    var $inline = $("#newsimage_set-group");
    if (!$inline.length) return;

    /* ── 1. Inject the drop zone above the inline table ── */
    var $dropZone = $(`
      <div id="gallery-dropzone">
        <div class="dz-inner">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"
               fill="none" stroke="currentColor" stroke-width="1.5"
               stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p><strong>Drag &amp; drop photos here</strong><br>
             or <label for="gallery-file-picker" class="dz-browse-link">browse to select</label>
             &nbsp;— you can pick as many as you like</p>
          <input type="file" id="gallery-file-picker"
                 accept="image/*" multiple style="display:none">
        </div>
        <div id="gallery-preview-strip"></div>
      </div>
    `);

    $inline.before($dropZone);

    /* ── 2. Styles (injected so no separate CSS file needed) ── */
    $("head").append(`
      <style>
        #gallery-dropzone {
          border: 2px dashed #79aec8;
          border-radius: 8px;
          background: #f8fcff;
          padding: 24px 20px 16px;
          margin-bottom: 16px;
          transition: background .2s, border-color .2s;
        }
        #gallery-dropzone.dz-over {
          background: #e3f2fd;
          border-color: #2196f3;
        }
        .dz-inner {
          text-align: center;
          color: #555;
        }
        .dz-inner svg { color: #79aec8; margin-bottom: 8px; }
        .dz-inner p { margin: 0; font-size: 14px; line-height: 1.6; }
        .dz-browse-link {
          color: #2196f3;
          cursor: pointer;
          text-decoration: underline;
          font-weight: 600;
        }
        #gallery-preview-strip {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          margin-top: 14px;
        }
        .dz-thumb {
          position: relative;
          width: 90px;
          height: 90px;
          border-radius: 6px;
          overflow: hidden;
          border: 2px solid #79aec8;
          box-shadow: 0 2px 6px rgba(0,0,0,.12);
        }
        .dz-thumb img {
          width: 100%; height: 100%;
          object-fit: cover;
        }
        .dz-thumb .dz-status {
          position: absolute; bottom: 0; left: 0; right: 0;
          background: rgba(0,0,0,.55);
          color: #fff; font-size: 10px;
          text-align: center; padding: 3px 2px;
        }
        .dz-thumb.dz-queued  { border-color: #79aec8; }
        .dz-thumb.dz-ready   { border-color: #4caf50; }
        .dz-thumb.dz-error   { border-color: #f44336; }
      </style>
    `);

    /* ── 3. Drag-over feedback ── */
    $dropZone
      .on("dragover dragenter", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass("dz-over");
      })
      .on("dragleave dragend drop", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass("dz-over");
      })
      .on("drop", function (e) {
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
      });

    /* ── 4. Browse-button click ── */
    $("#gallery-file-picker").on("change", function () {
      handleFiles(this.files);
      this.value = ""; // reset so same file can be re-added
    });

    /* ── 5. Core: assign each file to an inline row ── */
    function handleFiles(files) {
      if (!files || !files.length) return;

      $.each(files, function (i, file) {
        if (!file.type.match(/^image\//)) return; // skip non-images

        // Make sure there is a free empty row; add one if not
        ensureEmptyRow();

        // Find the LAST empty image input in the inline
        var $rows = $inline.find(".dynamic-newsimage_set");
        var $targetRow = null;
        $rows.each(function () {
          var $inp = $(this).find('input[type="file"]');
          // A row is "empty" if no file is assigned and it's not marked DELETE
          if ($inp.length && !$(this).find('[id$="-DELETE"]').prop("checked")) {
            // Check if its file input still has no file staged
            if (!$inp[0]._stagedFile) {
              $targetRow = $(this);
              return false; // break
            }
          }
        });

        if (!$targetRow) return; // safety

        var $fileInput = $targetRow.find('input[type="file"]');
        // Stage the file on the input via DataTransfer API
        try {
          var dt = new DataTransfer();
          dt.items.add(file);
          $fileInput[0].files = dt.files;
          $fileInput[0]._stagedFile = true; // mark as used
          $fileInput.trigger("change");
        } catch (err) {
          console.warn("DataTransfer not supported, falling back.", err);
        }

        // Show thumbnail preview
        addThumb(file, $fileInput[0]);
      });
    }

    /* ── 6. Ensure there is at least one empty row ── */
    function ensureEmptyRow() {
      var $rows = $inline.find(".dynamic-newsimage_set");
      var hasFree = false;
      $rows.each(function () {
        var $inp = $(this).find('input[type="file"]');
        if ($inp.length && !$inp[0]._stagedFile &&
            !$(this).find('[id$="-DELETE"]').prop("checked")) {
          hasFree = true;
          return false;
        }
      });
      if (!hasFree) {
        // Click Django's "Add another" link to generate a new row
        $inline.find(".add-row a, [id$='add_id']").first().trigger("click");
      }
    }

    /* ── 7. Thumbnail preview strip ── */
    function addThumb(file, inputEl) {
      var $strip = $("#gallery-preview-strip");
      var reader = new FileReader();
      reader.onload = function (e) {
        var $thumb = $(`
          <div class="dz-thumb dz-queued">
            <img src="${e.target.result}" alt="">
            <div class="dz-status">Queued</div>
          </div>
        `);
        $strip.append($thumb);

        // Update status when the form is submitted
        $(inputEl).closest("form").on("submit.dzthumb", function () {
          $thumb.removeClass("dz-queued").addClass("dz-ready");
          $thumb.find(".dz-status").text("Uploading…");
        });
      };
      reader.readAsDataURL(file);
    }

    /* ── 8. Keep unlimited rows: remove max_num cap visually ── */
    // Django enforces max_num server-side; we raised it to 100 in admin.py
    // but we also hide the "maximum reached" warning if it appears.
    var observer = new MutationObserver(function () {
      $inline.find(".help").filter(function () {
        return $(this).text().indexOf("maximum") !== -1;
      }).hide();
    });
    observer.observe($inline[0], { childList: true, subtree: true });
  }

  /* ── Run after Django's inline JS is ready ── */
  $(document).ready(function () {
    initMultiUpload();
  });

})(django.jQuery);