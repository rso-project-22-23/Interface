$(document).ready(function () {
    $(".navigation-item#stores").addClass("selected");
    displayStores();
    toggleAddNewStore();
    $(".button-add-store").click(addNewStore);
    $(".button-confirm-filters.button-store-filters").click(displayStores);
});

function displayStores() {
    let storeFilter = $("input.store-name-filter").val();

    $.ajax({
        url: "/ajax/stores",
        type: "GET",
        data: {
            "storeFilter": storeFilter
        },
        success: function (response) {
            loadStores(response);
        },
        error: function (response) {
            alert("Prišlo je do napake!");
            console.log("error");
            console.log(response);
        }
    });
}

function toggleAddNewStore() {
    $(".button-add-new-item").click(function () {
        let addStoreRow = $(".add-new-store.store-row");
        if (addStoreRow.hasClass("hidden")) {
            addStoreRow.removeClass("hidden");
        } else {
            addStoreRow.addClass("hidden");
            addStoreRow.find("input.store-name").val("");
        }
    });
}

function loadStores(stores) {
    let rowsContainer = $(".store-rows-container");
    rowsContainer.empty();
    for (let storeDict of stores) {
        let storeId = storeDict.id;
        let storeName = storeDict.storeName;

        let divStoreRow = document.createElement("div");
        let divStoreNameIndicator = document.createElement("div");
        let divStoreName = document.createElement("div");

        $(divStoreRow).addClass("store-row row");
        $(divStoreNameIndicator).addClass("store-name-indicator");
        $(divStoreName).addClass("store-name");

        $(divStoreNameIndicator).html("Ime:")
        $(divStoreName).html(storeName);

        divStoreRow.append(divStoreNameIndicator);
        divStoreRow.append(divStoreName);

        rowsContainer.append(divStoreRow);
    }
}

function addNewStore() {
    let newStoreName = $("input.store-name").val();
    $.ajax({
        url: "/ajax/add-store",
        data: {
            "storeName": newStoreName
        },
        type: "POST",
        success: function () {
            location.reload();
        },
        error: function (response) {
            let errorMessage = response.responseJSON[0].Error;
            alert("Prišlo je do napake!\n" + errorMessage);
        }
    });
}
