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

function genPageLink(currentPage, totalPage) {
    const maxPageBtn = 9 //must be odd
    let buttonElement = null;
    let pageLinkContentElement = document.getElementById("pageLinkSpan");
    let buttonCollection = document.createElement("span");

    let etcSymbolElement = document.createElement("span");
    etcSymbolElement.innerText = "...";

    // 3 cases
    // [1] [...] [a1], [a2] [currentpage] [ak] [ak+1]  [...] [lastpage]
    // [a0] [a1] [a2] [a3] [a4] [a5] [a6] [...] [lastpage] and curr page in a0 ~ a5
    // [1] [...] [a1] [a2] [a3] [a4] [a5] [a6] [a7] and curr page in a2 ~ a7
    let pageBtnRange = parseInt((maxPageBtn - 5) / 2);

    let continuousStartIndex = 1
    let continuousEndindex = totalPage
    let caseFlag = 0

    if(totalPage > maxPageBtn) {
        if(Math.abs(currentPage - continuousEndindex) + 3 < totalPage) {
            //case 3
            continuousStartIndex = continuousEndindex - (maxPageBtn - 3);
            caseFlag = 3;
        }
        else if(Math.abs(currentPage - continuousStartIndex) < maxPageBtn - 3) {
            //case 2
            continuousEndindex = continuousStartIndex + (maxPageBtn - 3);
            caseFlag = 2;
        }
        else {
            //case 1
            continuousStartIndex = currentpage - (maxPageBtn-5)/2;
            continuousEndindex = currentpage + (maxPageBtn-5)/2;
            caseFlag = 1;
        } 
    }

    if(caseFlag == 1 || caseFlag == 3) {
        //generate first page button and [...] text
        buttonElement = document.createElement("button");
        buttonElement.addEventListener("click", () => { reloadWindowPageNum(0) });
        buttonElement.setAttribute("id", "pageBtn1");
        buttonElement.innerText = "1";
        buttonCollection.appendChild(buttonElement);
        buttonCollection.appendChild(etcSymbolElement.cloneNode(true));
    }

    //add current page surrounding button
    for (let i = continuousStartIndex; i <= continuousEndindex; i++) {
        buttonElement = document.createElement("button");
        buttonElement.addEventListener("click", () => { reloadWindowPageNum(i) });
        buttonElement.setAttribute("id", "pageBtn" + String(i));
        buttonElement.innerText = String(i);
        if(i == currentPage) {
            buttonElement.style.color = "blue";
        }
        buttonCollection.appendChild(buttonElement);
    }

    if (caseFlag == 1 || caseFlag == 2) {
        //the case the current page is closer to the first page and the case the current page is in the middle : add [...] [lastpage]
        if (totalPage - currentPage - 1 > pageBtnRange) {
            buttonElement = document.createElement("button");
            buttonElement.addEventListener("click", () => { reloadWindowPageNum(totalPage) });
            buttonElement.setAttribute("id", "pageBtn" + String(totalPage));
            buttonElement.innerText = String(totalPage + 1);
            buttonCollection.appendChild(etcSymbolElement.cloneNode(true));
            buttonCollection.appendChild(buttonElement);
        }
    }

    //wrapper of text input elements
    let pageTextWrapper = document.createElement("span");

    //add text input to change page
    let pageTextInputLabel = document.createElement("span");
    pageTextInputLabel.innerText = "Go Page: ";

    let pageTextInputErrorElement = document.createElement("span");
    pageTextInputErrorElement.innerText = "Not Valid Number";
    pageTextInputErrorElement.setAttribute("id", "page-valid-error-text")
    pageTextInputErrorElement.style.color = "red";
    pageTextInputErrorElement.style.opacity = 0.0;

    let pageTextInputElement = document.createElement("input");
    pageTextInputElement.setAttribute("type", "text");
    //fixed width
    pageTextInputElement.style.width = "50px";

    //page number validation
    pageTextInputElement.addEventListener("keyup", ({ key }) => {
        if (key === "Enter") {
            if (!isNaN(parseFloat(pageTextInputElement.value))) {
                if (parseInt(pageTextInputElement.value) < 1 || parseInt(pageTextInputElement.value) > totalPage + 1 || pageTextInputElement.value.includes(".")) {
                    console.log("wrong input")
                    $('#page-valid-error-text').fadeTo("slow", 1.0);
                    $('#page-valid-error-text').fadeTo(1200, 0.0);
                }
                else {
                    reloadWindowPageNum(parseInt(pageTextInputElement.value) - 1);
                }
            }
            else {
                console.log("wrong input")
                $('#page-valid-error-text').fadeTo("normal", 1.0);
                $('#page-valid-error-text').fadeTo("normal", 0.0);
            }
        }
    })
    pageTextWrapper.appendChild(pageTextInputLabel);
    pageTextWrapper.appendChild(pageTextInputElement);
    pageTextWrapper.appendChild(pageTextInputErrorElement);

    //dummy node for alignment need
    let dummyPageTextWrapper = document.createElement("span");
    dummyPageTextWrapper.style.visibility = "hidden";
    
    let dummyTextErrorMsg = pageTextInputErrorElement.cloneNode(true);
    dummyTextErrorMsg.setAttribute("id", "dummyErrorPagetext")
    dummyPageTextWrapper.appendChild(pageTextInputLabel.cloneNode(true));
    dummyPageTextWrapper.appendChild(pageTextInputElement.cloneNode(true));
    dummyPageTextWrapper.appendChild(dummyTextErrorMsg);

    pageLinkContentElement.appendChild(dummyPageTextWrapper);
    pageLinkContentElement.appendChild(buttonCollection);
    pageLinkContentElement.appendChild(pageTextWrapper);
}

function clear_page_content() {
    document.getElementById("images-container").innerHTML = "";
    document.getElementById("pageLink").innerHTML = "";
}

function load_page_content() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let urlParamAllParam = {}
    for(const entry of urlParams.entries()) {
        urlParamAllParam[entry[0]] = entry[1];
    }

    $.ajax({
        url:"img_management/get_images",
        method:"GET",
        data: urlParamAllParam,
        
        success:function(res){
            genContent(res.img_objs);
            genPageLink(1, 2);
        },
        error:function(err){console.log(err)},
    });
}

load_page_content();