async function load_devices() {
    $.get("/get_devices", function (devices) {
        for (let key in Object.keys(devices)){
            document.getElementById("dev_container").innerHTML += `<a href=\"/device/${devices[Object.keys(devices)[key]]['hwid']}\" class=\"device\">\n` +
                `        <span>hwid: ${devices[Object.keys(devices)[key]]['hwid']}</span><br>\n` +
                `        <span>port: ${devices[Object.keys(devices)[key]]['port']}</span><br>\n` +
                `        <span>ip addr: ${devices[Object.keys(devices)[key]]['ip_addr']}</span><br>\n` +
                `        <span>performance: ${devices[Object.keys(devices)[key]]['performance']}</span>\n` +
                "    </a>"
            console.log(devices[Object.keys(devices)[key]])
        }
    })
}

load_devices();