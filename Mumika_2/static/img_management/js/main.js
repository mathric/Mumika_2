function imageCardFactory(item) {
    let cardElement = document.createElement("div");
    let cardBody = document.createElement("div");

    cardElement.classList.add("card", "col-xs-6", "col-sm-2", "col-md-2");
    cardBody.classList.add("card-body");

    let base64_data = item['base64_data'];
    cardElement.innerHTML = '<img class="card-img-top" src="data:image/jpg;base64,' + base64_data + '" alt="no image"></img>';

    let ulListElement = document.createElement("ul");
    ulListElement.classList.add("list-group", "list-group-flush");

    for (let i =0; i < 3; i++) {
        let listItem = document.createElement("li");
        listItem.classList.add("list-group-item");
        listItem.innerText = `abc:def`;
        ulListElement.appendChild(listItem);
    }

    cardBody.appendChild(ulListElement);
    cardElement.appendChild(cardBody);
    return cardElement;
}

//generator the items in container 3 rows 5 col
function genContent(itemList) {
    let itemcounter = 0;
    let currentRowElement = null;
    const ITEMS_ONE_ROW = 5;

    let firstColMargin = document.createElement("div");
    firstColMargin.classList.add("col-xs-0", "col-sm-1", "col-md-1");

    for (let item of itemList) {
        console.log(item)
        if (itemcounter % ITEMS_ONE_ROW == 0) {
            if (currentRowElement != null) {
                //finish current row, append to container
                document.getElementById("images-container").appendChild(currentRowElement);
            }
            currentRowElement = document.createElement("div");
            currentRowElement.classList.add("row");
            currentRowElement.appendChild(firstColMargin.cloneNode(true));
        }
        currentRowElement.appendChild(imageCardFactory(item));
        itemcounter += 1;
    }
    //last row
    if (currentRowElement != null) {
        document.getElementById("images-container").appendChild(currentRowElement);
    }
}


$.ajax({
    url:"",
    method:"GET",
    data:{
        "action":"GET_IMAGES",
    },
    
    success:function(res){
        console.log(res.img_objs)
        genContent(res.img_objs);
    },
    error:function(err){console.log(err)},
});