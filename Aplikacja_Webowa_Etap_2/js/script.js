var firstnameRegexp = new RegExp("^[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+$");
var peselRegexp = new RegExp("^\\d{11}$");
var birthdayRegexp = new RegExp("^(((19|20)([2468][048]|[13579][26]|0[48])|2000)[/-]02[/-]29|((19|20)[0-9]{2}[/-](0[469]|11)[/-](0[1-9]|[12][0-9]|30)|(19|20)[0-9]{2}[/-](0[13578]|1[02])[/-](0[1-9]|[12][0-9]|3[01])|(19|20)[0-9]{2}[/-]02[/-](0[1-9]|1[0-9]|2[0-8])))$");
var loginRegexp = new RegExp("^[a-z]{3,12}$");
var passwordRegexp = new RegExp("^[A-Za-z].{7,40}$");
//var passwordRegexp = new RegExp("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])$");
$(document).ready(function () {

    $("#firstname").blur(function() {
        var input = $(this).val();
        var value = $("#firstname").val();
        var error_string = document.createElement("small");
        error_string.append("Firstname is invalid: must begin with [A-Z] or a Polish character, followed by at least one lowercase [a-z] or a Polish character."); 
        l = document.getElementById("li_firstname");
        if (value == "") {
            return;
        }
        if (!firstnameRegexp.test(input)) {
            if (l.childElementCount == 2)
                l.appendChild(error_string);
        }
        else {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }
    });

    $("#lastname").blur(function() {
        var input = $(this).val();
        var value = $("#lastname").val();
        var error_string = document.createElement("small");
        error_string.append("Lastname is invalid: must begin with [A-Z] or a Polish character, followed by at least one lowercase [a-z] or a Polish character.");
        l = document.getElementById("li_lastname");
        if (value == "") {
            return;
        }
        if (!firstnameRegexp.test(input)) {
            if (l.childElementCount == 2)
                l.appendChild(error_string);
        }
        else {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }
    });

    function peselValidation(input) {
        if (peselRegexp.test(input) == false) {
            return false;
        }
        else {
            var pes = input.split("");
            var kontrola = (parseInt(pes[0]) + 3 * parseInt(pes[1]) + 7 * parseInt(pes[2])
                + 9 * parseInt(pes[3]) + parseInt(pes[4]) + 3 * parseInt(pes[5])
                + 7 * parseInt(pes[6]) + 9 * parseInt(pes[7]) + parseInt(pes[8]) + 3 * parseInt(pes[9])) % 10;
            if (kontrola == 0)
                kontrola = 10;
            kontrola = 10 - kontrola;
            return parseInt(pes[10]) == kontrola;
        }
    }

    $("#pesel").blur(function () {
        var input = $(this).val();
        var error_string = document.createElement("small");
        error_string.append("PESEL is is invalid. Must consist of 11 digits with correct checksum");
        l = document.getElementById("li_pesel");
        if (input === "" || peselValidation(input)) {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }
        else {
            if (l.childElementCount == 2)
                l.appendChild(error_string);
        }
        if (parseInt(input.charAt(9)) % 2 == 1) {
            $('input:radio[name="sex"]').filter('[value="M"]').attr('checked', true);
            $('input:radio[name="sex"]').filter('[value="F"]').attr('checked', false);
        }
        else {
            $('input:radio[name="sex"]').filter('[value="M"]').attr('checked', false);
            $('input:radio[name="sex"]').filter('[value="F"]').attr('checked', true);
        }
    });

    $("#birthdate").blur(function() {
        var input = $(this).val();
        var error_string = document.createElement("small");
        error_string.append("A birthday is invalid: year must be >= 1900 and format YYYY-MM-DD");
        l = document.getElementById("li_birthdate");
        if (input === "") {
            return;
        }
        if (!birthdayRegexp.test(input)) {
            if (l.childElementCount == 2)
                l.appendChild(error_string);
        }
        else {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }
    });

    $("#login").blur(function () {
        var input = $(this).val();
        var error_string = document.createElement("small");
        error_string.append("Login is already taken");
        var error_string1 = document.createElement("small");
        error_string1.append("The login must contain at least 3 at most 12 characters and only lowercase letters from a to z without digits.");
        l = document.getElementById("li_login");
        if (!loginRegexp.test(input)) {
            if (l.childElementCount == 2) 
                l.appendChild(error_string1);
        }
        else {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }

        $.ajax({
            type: "GET",
            url: "https://pi.iem.pw.edu.pl/user/" + $("#login").val(),
            success: function (request) {
                if(window.XMLHttpRequest)
                    request = new XMLHttpRequest();
                else
                request = new XMLHttpRequest();
                request.open('GET', 'https://pi.iem.pw.edu.pl/user/' + $("#login").val(), false);
                request.send();
                if (request.status === 200) {
                    if (l.childElementCount == 2)
                        l.appendChild(error_string);
                }
                else {
                    if (l.childElementCount > 2)
                        l.lastChild.remove();
                }
            },
            timeout: 60000,
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(textStatus);
            }
        })
    });

    $("#password").blur(function () {
        var input = $(this).val();
        var error_string = document.createElement("small");
        error_string.append("Password is invalid: must be at least 8 characters (including small and capital letters without digits)");
        l = document.getElementById("li_password");
        if (!passwordRegexp.test(input)) {
            if (l.childElementCount == 2)
                l.appendChild(error_string);
        }
        else {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }
    });

    $("#confirm_password").blur(function () {
        var input = $(this).val();
        var error_string = document.createElement("small");
        error_string.append("Passwords don't match.");
        l = document.getElementById("li_confirm_password");
        if (input !== $("#password").val()) {
            if (l.childElementCount == 2)
                l.appendChild(error_string);
        }
        else {
            if (l.childElementCount > 2)
                l.lastChild.remove();
        }
    });

    $("#Submit").click(function() {
        var error_string = document.createElement("p");
        l = document.getElementById("li_submit");
        if (document.getElementsByTagName("small").length != 0) {
            error_string.append("The form is not valid");
            if (l.childElementCount == 1)
                l.appendChild(error_string);
            else
                l.replaceChild(error_string,l.lastChild);
        }
        else {
            var empty = false;
            error_string.append("Please fill in all fields");
            $(':input[required]', $("#registration")).each(function () {
                if (this.value.trim() === '') {
                    empty = true;
                    if (l.childElementCount == 1)
                        l.appendChild(error_string);
                    else
                        l.replaceChild(error_string,l.lastChild);
                }
            });
            if (!empty)
                $("#registration").submit();
        }
    });
})
    function show(input) {
        debugger;
        var validExtensions = ['jpg','png','jpeg','gif','svg','bmp']; //array of valid extensions
        var fileName = input.files[0].name;
        var fileNameExt = fileName.substr(fileName.lastIndexOf('.') + 1);
        if ($.inArray(fileNameExt, validExtensions) == -1) {
            input.type = ''
            input.type = 'file'
            $('#user_img').attr('src',"");
            alert("Only these file types are accepted : "+validExtensions.join(', '));
        }
        else {
            if (input.files && input.files[0]) {
                var filerdr = new FileReader();
                filerdr.onload = function (e) {
                    $('#user_img').attr('src', e.target.result);
                }
            filerdr.readAsDataURL(input.files[0]);
            }
        }
}

