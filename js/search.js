var searchBaseUrl = "https://api.github.com/search/code?q=repo:Lyrics/lyrics path:database/ "
var dBWebsitePrefix = "/db"

function formatURL (input) {
    input = encodeURI(input).replace(/\?/g, "%3F")
    return dBWebsitePrefix + input + "/"
}

function getQueryVariable(variableName) {
    const params = new URLSearchParams(window.location.search);
    return params.get(variableName);
}

function reset() {
    appNode.innerHTML = "";
}

function displayLoading() {
    reset();

    var loadingNode = document.createElement("div");
    loadingNode.className = "loading";
    loadingNode.innerText = "Loading…";

    appNode.appendChild(loadingNode);
}

function displayError(reason) {
    reset();

    var errorNode = document.createElement("div");
    errorNode.className = "error";
    errorNode.innerText = reason;

    appNode.appendChild(errorNode);
}

function displayResults(items) {
    reset();

    var contentNode = document.createElement("div");
    contentNode.className = "content";

    if (items.length > 0) {
        var listNode = document.createElement("ul");
        listNode.className = "l";

        for (var i = 0; i < items.length; i++) {
            var item = items[i];

            var listItemNode = document.createElement("li");
            var listItemAnchorNode = document.createElement("a");

            listItemAnchorNode.className = "t4";
            listItemAnchorNode.innerText = item.path.split("/")[2] + " – " + item.name;
            listItemAnchorNode.href = formatURL(item.path.substring(8));

            listItemNode.appendChild(listItemAnchorNode);
            listNode.appendChild(listItemNode);
        }

        contentNode.appendChild(listNode);
    } else {
        var noResultsNode = document.createElement("p");
        noResultsNode.innerText = "No results";
        contentNode.appendChild(noResultsNode);
    }

    appNode.appendChild(contentNode);
}

var queryString = getQueryVariable("q");

// Need to wait for the search field to be appended to the DOM tree
setTimeout(function () {
    document.forms[0].firstChild.lastChild.value = queryString;
});

var appNode = document.getElementById("app");

// Put the loading indicator up

displayLoading();

// Proceed to retrieving results from the server

if (queryString.length > 2) {
    // Make a HTTP Request
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = processHttpResponse;
    xhr.open("GET", searchBaseUrl + queryString);
    xhr.send();

    function processHttpResponse() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
                displayResults(JSON.parse(xhr.responseText).items)
            } else {
                displayError(
                    xhr.status == 403 ?
                    "Search API rate limit exceeded, please try again in a bit" :
                    "Something went wrong"
                );
            }
        }
    }
} else {
    displayError("Query too short");
}
