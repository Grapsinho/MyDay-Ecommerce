$(document).ready(function () {
  // Initial sorting option
  var sortOption = "low_to_high";
  var product_name = $(".category_slug").text();

  // var filterAttribute = "";
  var filterValue = "";

  let filters = [];

  var filtersString = JSON.stringify(filters);

  // Function to update the product list
  function updateProductList() {
    $.ajax({
      type: "GET",
      url: "/filter_products_for_collections/",

      data: {
        "sort": sortOption, // Send the sorting option to the server
        "product_name": product_name,
        // "attribute": filterAttribute,
        "value": filterValue,
        "filters": filtersString,
      },

      success: function (data) {
        // Handle the response data (filtered products) here
        var products = data.products;

        // Clear the product list before appending new data
        $("#product-list").empty();

        for (var i = 0; i < products.length; i++) {
          var product = products[i];

          // Perform an action for each product, such as displaying it

          // You can append this data to your HTML as needed
          // For example, you can create HTML elements to display the products
          // Example using jQuery to append to a container with id 'product-list':/static/images/${images[i]}
          $("#product-list").append(
            `<div class='col col-for-grd'>

                <div class="for_photo" style='max-width: 100%; display: flex;'>
                <img src="/static/images/${product.img_url}" style='max-width: 100%; max-height: 185px; margin:0 auto;' alt="">
                </div>
  
                <span class="price-name"><span class="price-spn">$${product.price}</span> <span>${product.name}</span></span?> 
  
                <a href="/product_detail/${product.slug}" class="option"> Choose Option  </a>
                </div>`
          );
        }
      },
    });
  }

  // Handle the "Price, low to high" button click
  $(".low_to_high").click(function () {
    if (sortOption !== "low_to_high") {
      sortOption = "low_to_high";
      // Update the button text
      $(".menu_span_for_sort").text("Price, low to high");
      // Update the product list
      updateProductList();
    }
  });

  // Handle the "Price, high to low" button click
  $(".high_to_low").click(function () {
    if (sortOption !== "high_to_low") {
      sortOption = "high_to_low";
      // Update the button text
      $(".menu_span_for_sort").text("Price, high to low");
      // Update the product list
      updateProductList();
    }
  });

  // $(".filter-products-values").click(function () {
  //   filterAttribute = $(this).attr("data-filter");
  //   filterValue = $(this).attr("data-value");

  //   $(this).children().children().css({
  //     "background": "#f0ad4e",
  //     "color": "#fff",
  //     "border-radius": "5px",
  //   });

  //   filters[filterAttribute] = filterValue;

  //   console.log(filters);

  //   updateProductList();
  // });

  // Event delegation for filter clicks
  $(".filter-products-values").click(function () {
    // filterAttribute = $(this).attr("data-filter");
    filterValue = $(this).attr("data-value");

    // Toggle the filter on or off
    if (filters.includes(filterValue)) {
      filters.splice(filters.indexOf(filterValue), 1);

      $(this).children().children().css({
        "background": "#0d6efd",
        "color": "#fff",
        "border-radius": "5px",
        "border-color": "#0d6efd",
      });
    } else {
      filters.push(filterValue);
      $(this).children().children().css({
        "background": "#f0ad4e",
        "color": "#fff",
        "border-radius": "5px",
        "border-color": "#f0ad4e",
      });
    }

    filtersString = JSON.stringify(filters);

    updateProductList();
  });

  // Initial product list load
  updateProductList();
});
