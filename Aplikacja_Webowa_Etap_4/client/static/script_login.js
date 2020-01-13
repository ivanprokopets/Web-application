function validateForm() {
    var un = document.Form.login.value;
    var pw = document.Form.password.value;
    if ((un == "ivan") && (pw == "ivan")) {
        return true;
    } else if ((un == "test") && (pw == "test")) {
        return true;
    } else if ((un == "login") && (pw == "password")) {
        return true;
    } else {
        alert("Login was unsuccessful, please check your username and password");
        return false;
    }
}