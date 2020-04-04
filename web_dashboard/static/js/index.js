async function wrong_creds() {
    if(window.location.hash && window.location.hash.substr(1) === "wrong_credentials"){
        $("#credbox.wrong_creds").show()
    }
}

async function create_buttons() {
    document.getElementById("close").addEventListener("click", function () {
        $("#credbox.wrong_creds").hide()
    })
}
wrong_creds();
create_buttons();