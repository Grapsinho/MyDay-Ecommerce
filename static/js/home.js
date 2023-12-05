$(document).ready(function () {
  $("[id^='owl-carousel']").each(function () {
    $(this).owlCarousel({
      items: 5, // Number of items to show in the carousel
      nav: false, // Show navigation arrows
      navText: [
        '<i class="fa fa-chevron-left"></i>',
        '<i class="fa fa-chevron-right"></i>',
      ], // Custom arrow icons
      dots: false, // Hide navigation dots
      mouseDrag: true, // Enable dragging with the mouse
      touchDrag: true, // Enable touch navigation
      responsive: {
        // Define responsive breakpoints
        0: {
          items: 1, // Number of items to show on smaller screens
        },
        600: {
          items: 3,
        },
        768: {
          items: 3, // Number of items to show on medium screens
        },
        992: {
          items: 5, // Number of items to show on larger screens
        },
      },
    });

    // Show navigation arrows on hover
    $(this)
      .mouseenter(function () {
        $(".owl-prev, .owl-next", this).show();
      })
      .mouseleave(function () {
        $(".owl-prev, .owl-next", this).hide();
      });
  });
});

$(document).ready(function () {
  // Initial sorting option
  var sortOption = "low_to_high";
  var product_name = $(".q_for_search").text();

  // Function to update the product list
  function updateProductList() {
    $.ajax({
      type: "GET",
      url: "/filter_products/",
      data: {
        "sort": sortOption, // Send the sorting option to the server
        "product_name": product_name,
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
          // Example using jQuery to append to a container with id 'product-list':
          $("#product-list").append(
            `<div class='col col-for-grd'>

            <img
                src="/static/images/No Image.svg"
                alt=""
              />

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

  // Initial product list load
  updateProductList();
});
