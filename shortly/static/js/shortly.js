const URL = "/api";

function requestURL() {
    var request = new XMLHttpRequest();
    request.onload = function () {
        console.log("Ready state: " + this.readyState);
        if (this.status === 201) {
            var shortenedURL = JSON.parse(this.responseText).url;
            $("#shortened-url-link").val(shortenedURL);
            $("#url-container").removeClass("hidden");
        }
    }
    request.open("POST", URL);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify({"url": document.getElementById("url-input-field").value}));
}

function copy() {
    var urlInput = $("#shortened-url-link");
    urlInput.select();
    // urlInput.setSelectionRange(0, 99999);
    // document.execCommand("copy");
    $("#main").append(
        $('<div class="alert alert-success alert-dismissible fade show" role="alert"></div>')
            .append('<strong>Copied!</strong>')
            .append($('<button type="button" class="close" data-dismiss="alert" aria-label="Close"></button>')
                .append('<span aria-hidden="true">&times;</span>'))
    )
    $(".alert").alert();
    setTimeout(function () {
        $(".alert").alert("close");
    }, 2000);
}