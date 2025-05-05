function exisiting_customer(){
    document.getElementById("existing-customer-div").style.display = "block";
    document.getElementById("new-customer-div").style.display = "none";
}


function new_customer(){
    document.getElementById("new-customer-div").style.display = "block";
    document.getElementById("existing-customer-div").style.display = "none";
}

function add_tr(){
    const table=document.getElementById("table").getElementsByTagName("tbody")[0];

    const newRow=table.insertRow();
    const cell1=newRow.insertCell(0);
    const cell2=newRow.insertCell(1);
    const cell3=newRow.insertCell(2);
    const cell4=newRow.insertCell(3);

    cell1.innerHTML='<div class="mb-3 d-flex"><button type="button"  style="margin: 0px 5px;" class="btn btn-danger btn-sm"><i class="fa-solid fa-xmark"></i></button><input type="text" id="product" name="product" required></div>'
    cell2.innerHTML='<div class="mb-3"><input type="number" id="qty" name="qty" required></div>'
    cell3.innerHTML='<div class="mb-3"><input type="number" id="price" name="price" disabled></div>'
    cell4.innerHTML='<div class="mb-3"><input type="number" id="sub_total" name="sub_total" disabled></div>'
}