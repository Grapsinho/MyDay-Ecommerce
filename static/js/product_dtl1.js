$(document).ready(function () {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Check if this cookie string begins with the name provided
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

  // Set up variables
  var mainImage = $(".main-image");
  var thumbnails = $(".thumbnail");

  // Add click event to thumbnails
  thumbnails.click(function () {
    // Change the source of the main image to the clicked thumbnail's source
    var imgSrc = $(this).attr("src");
    mainImage.attr("src", imgSrc);

    // Toggle the "active" class on the clicked thumbnail
    $(this).toggleClass("active");

    // Remove the "active" class and border from other thumbnails
    thumbnails.not(this).removeClass("active").css("border", "none");

    // Add or remove border based on the presence of the "active" class
    if ($(this).hasClass("active")) {
      $(this).css("border", "2px solid #008CBA");
    }
  });

  // Initial sorting option
  var product_name = $(".name").text();

  // var filterAttribute = "";
  var filterValue = "";

  let filters = [];

  var filtersString = JSON.stringify(filters);

  // Function to update the product list
  function updateProductList() {
    $.ajax({
      type: "GET",
      url: "/filter_products_for_productDtl/",

      data: {
        "product_name": product_name,
        // "attribute": filterAttribute,
        "value": filterValue,
        "filters": filtersString,
      },

      success: function (data) {
        // Handle the response data (filtered products) here
        var products = data.products;
        var values = data.values;

        for (let index = 0; index < $(".filter-value-sty").length; index++) {
          const element = $(".filter-value-sty")[index];

          if (values.includes(element.innerText.trim())) {
            $(element).css({
              "background": "#f0ad4e",
              "color": "#fff",
              "border-radius": "5px",
              "border-color": "#f0ad4e",
            });
          } else {
            $(element).css({
              "background": "#0d6efd",
              "color": "#fff",
              "border-radius": "5px",
              "border-color": "#0d6efd",
              "pointer-events": "none",
            });
          }
        }

        // Clear the product list before appending new data
        $(".name").empty();
        $(".price").empty();
        $(".description").empty();
        $(".code32").empty();
        $(".main-image").empty();

        $(".code32").text(`${products.code}`);
        $(".price").text(`$${products.price}`);
        $(".name").text(`${products.name}`);
        $(".description").text(`${products.desc}`);
        $(".unit").text(`${products.stock}`);
        $('input[name="quantity"]').attr("max", products.stock);

        if (products.img_url == "/static/images/No Image.svg") {
          $(".defaultimg-div").append(
            `<img src="/static/images/No Image.svg" alt="">`
          );
        } else {
          $(".main-image").attr("src", products.img_url);
        }

        //This code uses the .off() method to first unbind any existing click events on the .minus element before binding the click event again.
        $(".minus")
          .off("click")
          .on("click", function () {
            let value = parseInt($('input[name="quantity"]').val());

            if (value > 1) {
              // Ensure the value is decremented by 1
              $('input[name="quantity"]').val(value - 1);
            }
          });

        //This code uses the .off() method to first unbind any existing click events on the .minus element before binding the click event again.
        $(".plus")
          .off("click")
          .on("click", function () {
            let value = parseInt($('input[name="quantity"]').val());

            if (value <= parseInt(products.stock) - 1) {
              // Ensure the value is incremented by 1
              $('input[name="quantity"]').val(value + 1);
            }
          });

        $(".add-to-cart")
          .off("click")
          .on("click", function () {
            // these if else statement is for check if quantity is correct or not
            if (
              parseInt($('input[name="quantity"]').val()) >
              parseInt(products.stock)
            ) {
              $(".add-to-cart").text("Not Enough Unit");

              $(".add-to-cart").css({
                "pointer-events": "none",
              });

              $('input[name="quantity"]').on("input", function () {
                if (
                  parseInt($('input[name="quantity"]').val()) >
                  parseInt(products.stock)
                ) {
                  $(".add-to-cart").text("Not Enough Unit");

                  $(".add-to-cart").css({
                    "pointer-events": "none",
                  });
                } else {
                  $(".add-to-cart").text("Add To Cart");

                  $(".add-to-cart").css({
                    "pointer-events": "all",
                  });
                }
              });
            } else if (parseInt($('input[name="quantity"]').val()) <= 0) {
              $(".add-to-cart").text("Not Enough Unit");

              $(".add-to-cart").css({
                "pointer-events": "none",
              });

              $('input[name="quantity"]').on("input", function () {
                if (parseInt($('input[name="quantity"]').val()) <= 0) {
                  $(".add-to-cart").text("Not Enough Unit");

                  $(".add-to-cart").css({
                    "pointer-events": "none",
                  });
                } else {
                  $(".add-to-cart").text("Add To Cart");

                  $(".add-to-cart").css({
                    "pointer-events": "all",
                  });
                }
              });
            } else {
              $.ajax({
                type: "POST",
                url: "/add_to_cart/",
                headers: { "X-CSRFToken": csrftoken },
                data: {
                  "sku": products.code,
                  "quantity": $('input[name="quantity"]').val(),
                  // Add other product data as needed
                },
                success: function (data) {
                  $(".cart-modal").addClass("show");
                  $(".delete-after-product").addClass("deactivate");
                  $(".delete-before-product").addClass("active");
                  $(".delete-before-product1").addClass("active");

                  let cart_total_value = parseInt($(".cart-total").text());

                  $(".cart-total").text(cart_total_value + 1);

                  let lost = [];

                  for (
                    let index = 0;
                    index < $(".for_photo-images").length;
                    index++
                  ) {
                    const element = $(".for_photo-images")[index];
                    lost.push(element.src);
                  }

                  if (
                    !lost.includes(
                      `http://127.0.0.1:8000/static/images/${data.img_url}`
                    ) &&
                    data.img_url != undefined
                  ) {
                    $(".delete-before-product").append(
                      `<div class='col gap-5 delete-before-product-product' name="product-${data.sku}" style='width: 100%; align-items: center; justify-content: center;'>
            
                            <div class="for_photo" style='max-width: 100%; display: flex;'>
                            <img src="/static/images/${data.img_url}" style='max-width: 100%; max-height: 100px; margin:0 auto;' class="for_photo-images" alt="">
                            </div>
              
                            <span class="price-name"><span class="price-spn">$${data.price}</span> <span>${data.name}</span></span?> 
              
                            <button class="delete-cart-cookie-btn" name="${data.sku}">Delete</button>
                            </div>
                            `
                    );
                  }

                  $(".delete-before-product-product").addClass("active");

                  let sum = 0;

                  let valuesArray = $(".price-spn")
                    .text()
                    .split("$")
                    .filter(Boolean);

                  sum = valuesArray.reduce(
                    (acc, val) => acc + parseFloat(val, 2),
                    0
                  );

                  if ($(".price-spn").length === 1) {
                    $(".sum-of-product").text(`Sum: $${data.price}`);
                  } else {
                    $(".sum-of-product").text(`Sum: $${sum.toFixed(2)}`);
                  }

                  let btn_name = `button[name="${data.sku}"]`;

                  $(btn_name)
                    .off("click")
                    .on("click", function () {
                      if (
                        $(".delete-before-product-product.active").length === 1
                      ) {
                        document.cookie =
                          "cart_items=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

                        $(".delete-after-product").removeClass("deactivate");
                        $(".delete-before-product").removeClass("active");
                        $(".delete-before-product1").removeClass("active");

                        $(".cart-total").text(0);

                        setTimeout(function () {
                          location.reload();
                        }, 500); // Reload the page after a short delay (100 milliseconds)
                      } else if (
                        $(".delete-before-product-product.active").length > 1
                      ) {
                        var cartItems = document.cookie
                          .split(";")
                          .find((cookie) =>
                            cookie.trim().startsWith("cart_items=")
                          );

                        if (cartItems) {
                          // Extract the value of cart_items from the cookie string
                          cartItems = cartItems.split("=")[1];

                          // Replace '\054' (non-standard character) with ',' in the JSON string
                          cartItems = cartItems.replace(/\\054/g, ",");

                          // Extract individual items from the complex string format
                          var items = cartItems.match(/\{[^}]*\}/g);

                          if (items) {
                            // Convert the matched items into an array of objects
                            var parsedCartItems = items.map((item) =>
                              JSON.parse(item.replace(/'/g, '"'))
                            );

                            // Filter out the item with the SKU 'SKU003'
                            parsedCartItems = parsedCartItems.filter(
                              (item) => item.sku !== data.sku
                            );

                            cart_total_value += 1;

                            // Update the cart_items cookie with the modified array
                            document.cookie =
                              "cart_items=" +
                              JSON.stringify(parsedCartItems) +
                              "; expires=Thu, 01 Jan 2070 00:00:00 UTC; path=/;";

                            $(".cart-total").text(cart_total_value - 1);

                            $(`div[name="product-${data.sku}"]`).removeClass(
                              "active"
                            );

                            setTimeout(function () {
                              location.reload();
                            }, 500); // Reload the page after a short delay (100 milliseconds)
                          }
                        }
                      }
                    });
                },
                error: function (error) {
                  console.log(error);
                },
              });
            }
          });
      },
    });
  }

  // // Event delegation for filter clicks
  // $(".filter-products-values").click(function () {
  //   filterAttribute = $(this).attr("data-filter");
  //   filterValue = $(this).attr("data-value");

  //   // Toggle the filter on or off
  //   if (filters.includes(filterValue)) {
  //     filters.splice(filters.indexOf(filterValue), 1);

  //     $(this).children().children().css({
  //       "background": "#0d6efd",
  //       "color": "#fff",
  //       "border-radius": "5px",
  //       "border-color": "#0d6efd",
  //     });
  //   } else {
  //     filters.push(filterValue);
  //     $(this).children().children().css({
  //       "background": "#f0ad4e",
  //       "color": "#fff",
  //       "border-radius": "5px",
  //       "border-color": "#f0ad4e",
  //     });
  //   }

  //   filtersString = JSON.stringify(filters);

  //   // console.log(filterValue, filterAttribute);

  //   updateProductList();
  // });

  $(".filter-products-values").click(function () {
    filterAttribute = $(this).attr("data-filter");
    filterValue = $(this).attr("data-value");

    // Check if the filter with the same attribute is already selected
    var index = filters.findIndex((item) => item.attribute === filterAttribute);

    // Toggle the filter on or off
    if (index !== -1) {
      // Remove the previous filter with the same attribute
      filters.splice(index, 1);

      // Reset the style of the button
      $(`.filter-products-values[data-filter="${filterAttribute}"]`)
        .children()
        .children()
        .css({
          "background": "#0d6efd",
          "color": "#fff",
          "border-radius": "5px",
          "border-color": "#0d6efd",
        });
    }

    // Add the current filter to the list
    filters.push({
      attribute: filterAttribute,
      value: filterValue,
    });

    // Set the style for the current button
    $(this).children().children().css({
      "background": "#f0ad4e",
      "color": "#fff",
      "border-radius": "5px",
      "border-color": "#f0ad4e",
    });

    filtersString = JSON.stringify(filters);

    updateProductList();
  });

  // Initial product list load
  updateProductList();
});
