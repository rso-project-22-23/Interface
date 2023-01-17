$(document).ready(function () {
    $(".user-menu-button").click(toggleUserDropdown);
    $(".button-logout").click(logoutUser);
});

function toggleUserDropdown() {
    let menu = $(".user-menu-dropdown");
    if (menu.hasClass("hidden")) {
        menu.removeClass("hidden")
    } else {
        menu.addClass("hidden")
    }
}

function logoutUser() {
        $.ajax({
        url: "/ajax/logout",
        type: "POST",
        success: function (r) {
            let successful = r[0];
            if (typeof successful === "boolean" && successful) {
                window.location.href = "/login";
            }
        },
        error: function (r) {
            alert("Prišlo je do napake!");
            console.log("error");
            console.log(r);
        }
    });
}