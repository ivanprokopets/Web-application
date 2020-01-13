function validateForm() {
  var x = document.forms["myForm"]["file"].value;
  if (x === "") {
    alert("Prosze wybrac plik");
    return false;
  }
}

function show(input) {
        var validExtensions = ['pdf']; //array of valid extensions
        var fileName = input.files[0].name;
        var fileNameExt = fileName.substr(fileName.lastIndexOf('.') + 1);
        if ($.inArray(fileNameExt, validExtensions) === -1) {
            input.type = ''
            input.type = 'file'
            $('#user_img').attr('src', "");
            alert("Only these file types are accepted : " + validExtensions.join(', '));
        } else {
            if (input.files && input.files[0]) {
                var filerdr = new FileReader();
                filerdr.onload = function (e) {
                    $('#user_img').attr('src', e.target.result);
                }
                filerdr.readAsDataURL(input.files[0]);
            }
        }
}
