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

  let allcolr = document.querySelectorAll(".color-for-attr");

  allcolr.forEach((element) => {
    let colr = element.attributes[2].value;

    element.style.backgroundColor = colr;
  });

  function changeVal(el) {
    var qt = parseFloat(el.parent().children(".qt").val());
    var price = parseFloat(el.parent().parent().children(".price").html());
    var eq = Math.round(price * qt * 100) / 100;

    el.parent()
      .parent()
      .children(".full-price")
      .html(eq + "$");

    changeTotal();
  }

  function changeTotal() {
    var price = 0;

    $(".full-price").each(function (index) {
      price += parseFloat($(".full-price").eq(index).html());
    });

    price = Math.round(price * 100) / 100;
    var shipping = parseFloat($(".shipping span").html());
    var fullPrice = Math.round((price + shipping) * 100) / 100;

    if (price == 0) {
      fullPrice = 0;
    }

    $(".subtotal span").html(price);
    $(".total span").html(fullPrice);
  }

  changeTotal();

  $(".qt-plus")
    .off("click")
    .click(function () {
      $(this)
        .parent()
        .children(".input-quan")
        .val(parseInt($(this).parent().children(".input-quan").val()) + 1);

      $(this).parent().parent().children(".full-price").addClass("added");

      var el = $(this);
      window.setTimeout(function () {
        el.parent().children(".full-price").removeClass("added");
        changeVal(el);
      }, 150);

      $.ajax({
        type: "POST",
        url: "/updateCart/",
        headers: { "X-CSRFToken": csrftoken },
        data: {
          action: "add",
          sku: $(this).attr("data-sku"),
        },
      });
    });

  $(".qt-minus")
    .off("click")
    .click(function () {
      child = $(this).parent().children(".qt");

      if (parseInt(child.val()) > 1) {
        child.val(parseInt(child.val()) - 1);

        $.ajax({
          type: "POST",
          url: "/updateCart/",
          headers: { "X-CSRFToken": csrftoken },
          data: {
            action: "remove",
            sku: $(this).attr("data-sku"),
          },
        });
      }

      $(this).parent().children(".full-price").addClass("minused");

      var el = $(this);
      window.setTimeout(function () {
        el.parent().children(".full-price").removeClass("minused");
        changeVal(el);
      }, 150);
    });

  $(".input-quan")
    .off("input")
    .on("input", function () {
      let child = $(this).parent().children(".qt");
      if (parseInt(child.val()) > 0) {
        $(this).parent().children(".full-price").addClass("inputed");

        var el = $(this);
        window.setTimeout(function () {
          el.parent().children(".full-price").removeClass("inputed");
          changeVal(el);
        }, 150);
      }
    });

  let remove_items = document.querySelectorAll(".remove-item");

  remove_items.forEach((element) => {
    element.addEventListener("click", function () {
      // this.closest(".item-length").style.display = "none";
      let sku = this.previousElementSibling.textContent;

      let cart_total_value = parseInt($(".cart-total").text());
      if ($(".item-length").length === 1) {
        document.cookie =
          "cart_items=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

        $(".delete-after-product").removeClass("deactivate");
        $(".delete-before-product").removeClass("active");
        $(".delete-before-product1").removeClass("active");

        $(".cart-total").text(0);

        setTimeout(function () {
          location.reload();
        }, 500); // Reload the page after a short delay (100 milliseconds)
      } else if ($(".item-length").length > 1) {
        var cartItems = document.cookie
          .split(";")
          .find((cookie) => cookie.trim().startsWith("cart_items="));

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
              (item) => item.sku !== sku
            );

            cart_total_value += 1;

            // Update the cart_items cookie with the modified array
            document.cookie =
              "cart_items=" +
              JSON.stringify(parsedCartItems) +
              "; expires=Thu, 01 Jan 2070 00:00:00 UTC; path=/;";

            $(".cart-total").text(cart_total_value - 1);

            $(`div[name="product-${$(".item-sku").text()}"]`).removeClass(
              "active"
            );

            setTimeout(function () {
              location.reload();
            }, 500); // Reload the page after a short delay (100 milliseconds)
          }
        }
      }
    });
  });
});
