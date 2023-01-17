$(document).ready(function () {
    $(".navigation-item#items").addClass("selected");
    $(".button-confirm-new-item").click(addItem);
});


function addItem() {
    let barcode = $(".new-item-barcode").val();
    let name = $(".new-item-name").val();
    let store = $(".new-item-store").find(":selected").val();
    let price = parseFloat($(".new-item-price").val());

    let invalid = ["", undefined, null]
    if (invalid.includes(barcode) || invalid.includes(name) || invalid.includes(store)) {
        alert("Polja ne smejo biti prazna")
        return;
    }
    if ([undefined, null].includes(price) || price === 0) {
        alert("Cena ne sme biti prazna ali enaka 0")
        return;
    }

    $.ajax({
        url: "/ajax/add-item",
        type: "POST",
        data: {
            "barcode": barcode,
            "itemName": name,
            "storeName": store,
            "price": price,
        },
        success: function () {
            window.location.href = "/items/" + barcode;
        },
        error: function (r) {
            alert("Napaka:\n" + r.responseJSON[0].Error);
        }
    });
}