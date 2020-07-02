class Model {
    async make_post_options(body_data){
        let headers = new Headers();
        headers.append(
            'Authorization',
            'Bearer ' + localStorage.getItem('token')
        );
        headers.append(
            'Content-Type',
            'application/json'
        );
        let options = {
            method: "POST",
            cache: "no-cache",
            headers: headers,
            body: JSON.stringify(body_data)
        };
        return options;
    }
    async search(body_data){
        let options = await this.make_post_options(body_data);    
        let response = await fetch("/api/devices/search", options);
        let data = await response.json();
        return data;
    }

    async remove_single_device(body_data){
        let options = await this.make_post_options(body_data);    
        let response = await fetch("/api/devices/remove", options);
        let data = await response.json();
        return data;
    }
}

class View {
    constructor(){
        this.devicename = document.getElementById("devicename");
        // this.searchbase = document.getElementById("searchbase");
        // this.searchbase = document.getElementsByName("searchbase");
        this.searchButton = document.getElementById("search");
        this.cancelButton = document.getElementById("cancel");
        this.searchbase = document.querySelector('input[name=searchbase]:checked');
        this.table = document.querySelector(".devices table");
        this.error = document.querySelector(".error");
    }

    setInitState(){
        this.devicename.value = "";
        // this.searchbase.value = "_Workstations";
        // console.log(this.searchbase);
        this.devicename.focus();
    }

    buildTable(devices){
        let tbody, 
            html = "";

        if(devices.length>0){
            devices.forEach((device)=>{
                html += `
                <tr data-device_id="${device.name}"> 
                    <td>${device.name}</td> 
                    <td>${device.operatingSystem}</td> 
                    <td>${device.lastLogon}</td>
                    <td>
                        <button data-btn_id="${device.name}" class="btn btn-outline-warning">remove
                        </button>
                    </td>
                </tr>`;
            });
        }

        if (this.table.tBodies.length !== 0){
            this.table.removeChild(this.table.getElementsByTagName("tbody")[0]);
        }
        tbody = this.table.createTBody();
        tbody.innerHTML = html;
    }

    errorMessage(message){
        this.error.innerHTML = message;
        this.error.classList.add("visible", "alert", "alert-warning");
        this.error.classList.remove("hidden");
        setTimeout(() => {
            this.error.classList.add("hidden");
            this.error.classList.remove("visible", "alert", "alert-warning");
        }, 2000);
    }
}

class Controller {
    constructor(model, view){
        this.model = model;
        this.view = view;

        this.initialize();
    }
    async initialize(){
        this.view.setInitState();
        this.initializeSearchEvent();
        this.initializeCancelEvent();
    }

    initializeSearchEvent(){
        document.getElementById("search").addEventListener("click", async (evt)=>{
            let devicename = document.getElementById("devicename").value,
                searchbase = document.querySelector('input[name=searchbase]:checked').value;
            
            console.log('clicked me', devicename, searchbase);
            evt.preventDefault();
            try {
                let devices = await this.model.search({
                    devicename: devicename,
                    searchbase: searchbase
                });
                if(devices&&devices.error){
                    window.location = "/client/login";
                }
                // console.log(devices);
                this.view.buildTable(devices);
            } catch(err) {
                this.view.errorMessage(err);
            }

            document.querySelector("table tbody").addEventListener("dblclick", (evt)=>{
                let target = evt.target,
                    parent = target.parentElement;
    
                // console.log(parent.getAttribute("data-device_id"));
            });
            let buttons = document.querySelectorAll("td button");
            buttons.forEach((button)=>{
                button.addEventListener("click", async (evt)=>{
                    let target = evt.target,
                        devicename_to_remove = target.getAttribute("data-btn_id"),
                        tr_selector = "[data-device_id='" + devicename_to_remove + "']",
                        tr_to_remove = document.querySelector(tr_selector),
                        tr_to_remove_jq = $(tr_selector);
                    evt.preventDefault();
                    // console.log("clicked remove", devicename_to_remove);
                    // console.log("parent: ", tr_to_remove);
                    tr_to_remove.style.background = '#fb6c6c';
                    try {
                        let data = await this.model.remove_single_device({
                            devicename: devicename_to_remove
                        });
                        if(data.result == 0){
                            // console.log("try block check result: ", data);
                            this.view.errorMessage(devicename_to_remove + ": " + data.type + " -- " + data.description);
                            // tr_to_remove.style.background = 'black';
                            // tr_to_remove.hide('slow', ()=>{
                            //     tr_to_remove.remove();
                            // });
                            tr_to_remove_jq.hide(1600, ()=>{
                                tr_to_remove_jq.remove();
                            });
                            // setTimeout(()=>{
                            //     tr_to_remove.remove();
                            // }, 30);
                        }
                        // console.log("try block: ", data);
                    } catch(err) {
                        this.view.errorMessage(err);
                        console.log("catch block: ", err);
                    }
                });
            });
            // console.log(buttons.length);
        });
    }

    initializeCancelEvent(){
        document.getElementById("cancel").addEventListener("click", async (evt)=>{
            evt.preventDefault();
            this.view.setInitState();
        });
    }
}

const model = new Model();
const view = new View();
const controller = new Controller(model, view);

export default{
    model,
    view,
    controller
};
