//i know jquery is outdated, but it fits this application

document.getElementById("edit_button").addEventListener("click", function () {
    document.getElementById("hwid").disabled = false;
    document.getElementById("ip_addr").disabled = false;
    document.getElementById("port").disabled = false;
    document.getElementById("performance").disabled = false;

    document.getElementById("save_button").style.display = 'inline';
    document.getElementById("edit_button").style.display = 'none';
});

document.getElementById("save_button").addEventListener("click", async function () {
    let data = {
        "hwid_old": device["hwid"],
        "hwid": document.getElementById("hwid").value,
        "ip_addr": document.getElementById("ip_addr").value,
        "port": Number(document.getElementById("port").value),
        "performance": Number(document.getElementById("performance").value)
    };

    if (data["hwid"] !== device["hwid"] || data["ip_addr"] !== device["ip_addr"] || data["performance"] !== Number(device["performance"]) || data["port"] !== Number(device["port"])){

        let ret = await $.post("/edit_device", data);
        if (ret === "Success"){
            if (data["hwid"] !== device.hwid){
                document.location.href = `/device/${data["hwid"]}`
            }
            device["hwid"] = data["hwid"];
            device["ip_addr"] = data["ip_addr"];
            device["performance"] = data["performance"];
            device["port"] = data["port"];

        }
        else{
            window.location.href = window.location.href + "#error";
        }
        console.log(ret);
    }

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