const authCookieName = "auth-data";
const tokenKey = "auth-token"
const emailKey = "auth-email"

$(document).ready(function () {
    applyListeners();
});


function applyListeners() {
    $(".login-button").click(loginUser);
}

function loginUser() {
    let userEmail = $("input.user-email").val();
    let userPassword = $("input.user-password").val();

    if (["", null, undefined].includes(userEmail)) {
        console.log("empty email");
        return;
    }

    if (["", null, undefined].includes(userPassword)) {
        console.log("empty password");
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
            console.log(response.responseJSON);
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