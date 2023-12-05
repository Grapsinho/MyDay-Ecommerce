const cart = document.querySelector(".cart");
const cart_modal = document.querySelector(".cart-modal");
const fa_cart_shopping = document.querySelector(".fa-cart-shopping");
const cart_total = document.querySelector(".cart-total");

let cart_modal_children = cart_modal.childNodes;

cart.addEventListener("click", () => {
  cart_modal.classList.toggle("show");
});

// window.onclick = function (event) {
//   if (
//     event.target !== cart &&
//     event.target !== fa_cart_shopping &&
//     event.target !== cart_total &&
//     !cart_modal_children.includes(event.target)
//   ) {
//     cart_modal.classList.remove("show");
//   } else {
//     return;
//   }
// };

let host = window.location.host;
let socket = new WebSocket(`ws://${host}/ws/live_search/`);
let search_results = document.getElementById("search_results");

search_results.style.display = "none";
const type_button = document.querySelector(".type-button");

type_button.style.pointerEvents = "none";

socket.onmessage = function (event) {
  let data = JSON.parse(event.data);
  let searchResults = data.search_results;
  let product_name = document.querySelector(".product_detail");
  spinner.style.display = "none";

  // Update your UI with the search results, e.g., by adding them to a div or list.
  let resultsContainer = document.getElementById("search-results");
  //resultsContainer.innerHTML = "";

  for (let i = 0; i < searchResults.length; i++) {
    let result = searchResults[i];

    if (searchResults.length < 3) {
      type_button.style.pointerEvents = "none";
    } else {
      type_button.style.pointerEvents = "all";
    }

    if (result.slug) {
      // let baseUrl = `{% with base_url="/product_detail/" %}{{ base_url }}{% endwith %} ${baseUrl + result.slug + "/"}`;
      product_name.innerHTML += `<a href="/product_detail/${result.slug}"><img
                src="/static/images/${result.img}"
                alt=""
                style="max-width: 70px"
              /> <span class="result-span">
                
                <span> ${result.name} </span>
                <span class="price"> ${result.price}$ </span>

                </span>
                
                </a>
            `;

      search_results.style.display = "block";
    } else {
      product_name.innerHTML = result.message;
    }

    searchInput.addEventListener("input", function () {
      product_name.innerHTML = "";
    });

    if (searchInput.value == "") {
      product_name.innerHTML = "";
      type_button.style.pointerEvents = "none";
      search_results.style.display = "none";
    }
  }
};

let timeout;
let spinner = document.getElementById("spinner");

// Send search queries when the user types
let searchInput = document.getElementById("search-input");
searchInput.addEventListener("input", function () {
  spinner.style.display = "block";
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    let searchQuery = this.value;
    socket.send(searchQuery);
  }, 1000);
});
