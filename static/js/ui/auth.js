const authCookieName = "auth-data";
const tokenKey = "auth-token"
const emailKey = "auth-email"

$(document).ready(function () {
    applyListeners();
});


function applyListeners() {
    $(".login-button").click(loginUser);
    $(".register-button").click(registerUser);
}

function loginUser() {
    let userEmail = $("input.user-email").val();
    let userPassword = $("input.user-password").val();

    if (["", null, undefined].includes(userEmail)) {
        alert("Prazno polje za elektronski naslov");
        return;
    }

    if (["", null, undefined].includes(userPassword)) {
        alert("Prazno polje za geslo");
        return;
    }

    $.ajax({
        url: "/ajax/login",
        type: "POST",
        data: {
            "user": userEmail,
            "password": userPassword
        },

        success: function (token) {
            saveAuthToken(userEmail, token);
            window.location.href = "/items"
        },

        error: function (response) {
            alert("Napaka: " + response.responseJSON.Error);
        }
    });
}

function registerUser() {
    let userEmail = $(".register-input.user-email").val();
    let userPassword = $(".register-input.user-password").val();
    let repeatPassword = $(".register-input.repeat-password").val();

    let invVal = ["", null, undefined];
    if (invVal.includes(userEmail) || invVal.includes(userPassword) || invVal.includes(repeatPassword)) {
        alert("Polja ne smejo biti prazna")
        return;
    }
    if (userPassword !== repeatPassword) {
        alert("Ponovljeno geslo se ne ujema.")
        return;
    }

    $.ajax({
        url: "/ajax/register",
        type: "POST",
        data: {
            "user": userEmail,
            "password": userPassword,
            "repeatPassword": repeatPassword
        },

        success: function () {
            alert("Uspešno ste se registrirali v aplikacijo primerjalnik.\n" +
                "Preverite naveden elektronski naslov za potrditev vašega računa.");
            location.reload();
        },

        error: function (response) {
            alert("Napaka: " + response.responseJSON.Error);
        }
    });
}

function saveAuthToken(email, authToken) {
    let cookieDict = getAuthCookie();
    cookieDict[emailKey] = email;
    cookieDict[tokenKey] = authToken;
    $.cookie(authCookieName, JSON.stringify(cookieDict), {expires: 180, path: '/'});
}

function getAuthToken() {
    return getAuthCookie()[tokenKey];
}

function getAuthCookie() {
    let filtersCookie = $.cookie(authCookieName);
    if ([undefined, null].includes(filtersCookie)) {
        return {}
    }

    return JSON.parse(filtersCookie);
}