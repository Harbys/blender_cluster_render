document.getElementById("edit_button").addEventListener("click", function () {
    document.getElementById("hwid").disabled = false;
    document.getElementById("ip_addr").disabled = false;
    document.getElementById("port").disabled = false;
    document.getElementById("performance").disabled = false;

    document.getElementById("save_button").style.display = 'inline';
    document.getElementById("edit_button").style.display = 'none';
});

document.getElementById("save_button").addEventListener("click", function () {
    let data = {
        "hwid_old": device["hwid"],
        "hwid": document.getElementById("hwid").value,
        "ip_addr": document.getElementById("ip_addr").value,
        "port": Number(document.getElementById("port").value),
        "performance": Number(document.getElementById("performance").value)
    };
    $.post("/edit_device", data)
        .done(function () {
            if (data["hwid"] !== device.hwid){
                document.location.href = `/device/${data["hwid"]}`
            }
        });


    document.getElementById("hwid").disabled = true;
    document.getElementById("ip_addr").disabled = true;
    document.getElementById("port").disabled = true;
    document.getElementById("performance").disabled = true;

    document.getElementById("save_button").style.display = 'none';
    document.getElementById("edit_button").style.display = 'inline';
});


async function load_device_values() {
    document.getElementById("hwid").value = device["hwid"];
    document.getElementById("ip_addr").value = device["ip_addr"];
    document.getElementById("port").value = device["port"];
    document.getElementById("performance").value = device["performance"];
}

load_device_values();