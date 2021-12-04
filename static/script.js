// For collapsible search field
var collapseElementList = [].slice.call(document.querySelectorAll(".collapse"));
var collapseList = collapseElementList.map(function(collapseEl) {
    return new bootstrap.Collapse(collapseEl);
});

// responsive search button
window.onload = function() {
    var x = this.matchMedia("(max-width: 480px");
    if (x.matches) {
        let searchButton = document.getElementsByClassName("search_icon")[0];
        searchButton.removeAttribute("data-bs-toggle");
        searchButton.removeAttribute("data-bs-target");
        searchButton.onclick = () => (window.location.href = "/search");
    }
};

/* Creates a popout with trailer and details when user selects movie/show */
async function select(media, mediaType = "movie") {
    // get details
    let detailResponse = await fetch(`/select/${mediaType}/${media.id}`);
    let detailsJSON = await detailResponse.text();
    const details = JSON.parse(detailsJSON);

    // get script
    let scriptResponse = await fetch(`/script/${media.alt}`);
    let script = await scriptResponse.text();

    // get trailer
    let response = await fetch(`/clips/${mediaType}/${media.id}`);
    let key = await response.text();

    // if popout currently on screen, hide popout
    let popUp = document.getElementsByClassName("selected");
    if (popUp.length !== 0) popUp[0].className = "hidden";

    createPopup(details, key, script);
}

/* Creates popout element with trailer, details, and script (if available) */
function createPopup(details, key, script = "") {
    let container = document.getElementsByClassName("hidden")[0];

    container.classList.remove("hidden");
    container.className = "selected";

    createTrailerDiv(key);
    createDetailDiv(details);
    createCastDiv(details);
    createGenresDiv(details);

    // create overview
    let overviewDiv = document.getElementsByClassName("overview")[0];
    let overview = details.overview;
    overviewDiv.innerHTML = overview;

    //create scriptDiv if script is available
    let scriptDiv = document.getElementsByClassName("script")[0];
    scriptDiv.innerHTML = "";
    if (script !== "") {
        let span = document.createElement("pre");
        span.innerHTML = script;
        scriptDiv.appendChild(span);
        scriptDiv.style.minHeight = "20px";
    }
}

function createTrailerDiv(key) {
    baseURL = "https://www.youtube.com/embed/";

    let trailerDiv = document.getElementsByClassName("trailer")[0];

    trailerDiv.innerHTML = "";

    if (key === "") {
        trailerDiv.innerHTML = "No Trailer Available";
    } else {
        let youTubeVideo = document.createElement("iframe");
        youTubeVideo.width = "100%";
        youTubeVideo.height = "390";
        youTubeVideo.src = baseURL + key + "?autoplay=1&mute=1&encryped-media=1";
        trailerDiv.appendChild(youTubeVideo);
    }
}

function createDetailDiv(details) {
    let detailDiv = document.getElementsByClassName("details")[0];

    let year = details.year;
    let runtime = details.runtime !== "" ? "🎬 " + details.runtime + " min" : "";
    let rating = "⭐ " + details.rating;

    const detailText = new Array(year, runtime, rating);
    let detailSpan = Array.from(detailDiv.children);

    for (let i = 0; i < detailText.length; i++) {
        detailSpan[i].innerHTML = "";
        detailSpan[i].appendChild(document.createTextNode(detailText[i]));
    }
}

function createCastDiv(details) {
    let castDiv = document.getElementsByClassName("cast")[0];
    let cast = details.cast.join(", ");
    castDiv.innerHTML = "Cast: " + cast;
}

function createGenresDiv(details) {
    let genresDiv = document.getElementsByClassName("genres")[0];
    let genres = details.genres.join(", ");
    genresDiv.innerHTML = "Genres: " + genres;
}