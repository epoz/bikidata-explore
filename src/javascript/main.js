document.addEventListener("DOMContentLoaded", function () {
  init();
});

function init() {
  me(".block_add").addEventListener("click", addQueryBlock);

  me("#go").addEventListener("click", function (event) {
    event.preventDefault();
    doSearch();
  });
  inputObj = me("input.uk-input.obj");
  if (inputObj) {
    inputObj.focus();
  }
}

function doSearch() {
  me("#results").innerHTML = "<p>Searching...</p>";

  const ops = document.querySelectorAll(".op");
  const preds = document.querySelectorAll(".pred");
  const objs = document.querySelectorAll(".obj");

  let opts = {};
  ops.forEach((op, i) => {
    const hiddenSelect = op.querySelector("input");
    if (hiddenSelect) {
      opts[i] = { op: hiddenSelect.value };
    }
  });
  preds.forEach((pred, i) => {
    const hiddenInput = pred.querySelector("input");
    if (hiddenInput) {
      if (hiddenInput.value !== "_") {
        opts[i]["p"] = hiddenInput.value;
      }
    }
  });
  objs.forEach((obj, i) => {
    if (obj.value) {
      opts[i]["o"] = obj.value;
    }
  });
  opts = { filters: Object.values(opts) };

  any(".agg")?.forEach((agg) => {
    const hiddenSelect = agg.querySelector("input");
    if (hiddenSelect) {
      opts["aggregates"] = opts["aggregates"] || [];
      opts["aggregates"].push(hiddenSelect.value);
    }
  });

  me("#excludes")
    ?.value.split(" ")
    .forEach((ex) => {
      if (ex.trim() && ex.trim().startsWith("<") && ex.trim().endsWith(">")) {
        opts["exclude_properties"] = opts["excludes"] || [];
        opts["exclude_properties"].push(ex.trim());
      }
    });
  opts["format"] = "html";

  fetch("/fragments_query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(opts),
  })
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("results").innerHTML = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

async function addQueryBlock(event) {
  event.preventDefault();

  block = event.target.parentElement.parentElement;
  try {
    let response = await fetch("/fragments_query_block");
    if (response.ok) {
      let new_block = document.createElement("div");
      new_block.innerHTML = await response.text();
      new_block.querySelector(".block_remove").onclick = removeQueryBlock;
      new_block.querySelector(".block_add").onclick = addQueryBlock;
      block.parentElement.insertBefore(new_block, block.nextSibling);
      return new_block;
    } else console.warn("fetch(): Bad response");
  } catch (error) {
    console.warn(`fetch(): ${error}`);
  }
}

function removeQueryBlock(event) {
  event.preventDefault();
  existing = document.querySelectorAll(".block_remove");
  if (existing.length > 1) {
    block = event.target.parentElement.parentElement;
    block.parentElement.removeChild(block);
  }
}
