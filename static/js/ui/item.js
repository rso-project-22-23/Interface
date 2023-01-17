$(document).ready(function () {
    $(".navigation-item#items").addClass("selected");
    $(".button-add-price").click(toggleAddPrice)
    $(".button-confirm-price").click(addPrice);
});

function toggleAddPrice() {
    let button = $(".add-price")
    if (button.hasClass("hidden")) {
        button.removeClass("hidden")
    } else {
      button.addClass("hidden")
    }
}


function addPrice() {
    let price = parseFloat($(".input-price").val());
    let store = $(".store-names").find(":selected").val();
    let barcode = $(".barcode.row .data-box").html();
    if (["", undefined, null].includes(store)) {
        return;
    }
    if ([undefined, null].includes(price) || price === 0) {
        return;
    }

    $.ajax({
        url: "/ajax/add-price",
        type: "POST",
        data: {
            "barcode": barcode,
            "storeName": store,
            "price": price,
        },
        success: function () {
            location.reload();
        },
        error: function (r) {
            alert("Napaka:\n" + r.responseJSON[0].Error);
        }
    });


}