$(document).ready(function () {
    $(".navigation-item#items").addClass("selected");
    $(".button-confirm-filters.button-item-filters").click(getItems);
    getItems();
});

function updateDisplayedItems() {

}

function getItems() {
    let nameFilter = $(".filter-name input").val();
    let selectedStore = $(".filter-store").find(":selected").val();

    $.ajax({
        url: "/ajax/items",
        data: {
            "nameFilter": nameFilter,
            "storeFilter": selectedStore
        },
        type: "GET",
        success: function (items) {
            console.log(items)
            loadItems(items);
        },
        error: function (r) {
            alert("Prišlo je do napake!");
            console.log("error");
            console.log(r);
        }
    });
}


function loadItems(items) {
    console.log(items)
    let itemRowsContainer = $(".main-content");
    itemRowsContainer.empty();

    for (let [itemId, item] of Object.entries(items)) {
        console.log(item);
        let itemName = item.Item.itemName;
        let itemBarcode = item.Item.barcode;

        console.log(itemName);
        console.log(itemBarcode);
        let divItemRow = document.createElement("div");
        let aItemText = document.createElement("a");
        let divItemNameIndicator = document.createElement("div");
        let divItemName = document.createElement("div");
        let divItemBarcodeIndicator = document.createElement("div");
        let divItemBarcode = document.createElement("div");
        let divItemRowButtons = document.createElement("div");
        let divIconHeart = document.createElement("div");
        let imgIconHeart = document.createElement("img");

        $(divItemRow).addClass("item-row row");
        $(aItemText).addClass("text-style items");
        $(divItemNameIndicator).addClass("item-row-name-indicator row");
        $(divItemName).addClass("text-style-bold");
        $(divItemBarcodeIndicator).addClass("item-row-barcode-indicator row");
        $(divItemBarcode).addClass("text-style-bold");
        $(divItemRowButtons).addClass("item-row-buttons items row");
        $(divIconHeart).addClass("icon-heart");

        $(aItemText).attr("href", "/items/" + itemBarcode)
        $(imgIconHeart).attr("src", "static/icons/heart_white.svg");
        $(imgIconHeart).attr("alt", "Priljubljeno");
        $(imgIconHeart).attr("title", "Dodaj med priljubljene");
        $(imgIconHeart).attr("data-id", itemId);

        $(divItemNameIndicator).html("Ime:");
        $(divItemName).html(itemName);
        $(divItemBarcodeIndicator).html("Črtna koda:");
        $(divItemBarcode).html(itemBarcode);

        divItemNameIndicator.append(divItemName);
        divItemBarcodeIndicator.append(divItemBarcode);
        aItemText.append(divItemNameIndicator)
        aItemText.append(divItemBarcodeIndicator)

        divIconHeart.append(imgIconHeart);
        divItemRowButtons.append(divIconHeart);

        divItemRow.append(aItemText);
        divItemRow.append(divItemRowButtons)

        itemRowsContainer.append(divItemRow)
    }
}