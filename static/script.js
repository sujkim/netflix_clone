async function select(movie) {
    // console.log(movie.id);
    // console.log('clicked');

    // get details
    let detailResponse = await fetch(`/select/${movie.id}`);
    let detailsJSON = await detailResponse.text();

    // console.log(overview);
    const details = JSON.parse(detailsJSON)

    console.log(details);

    // get script
    let scriptResponse = await fetch(`/script/${movie.alt}`);
    let script = await scriptResponse.text();

    // get trailer
    let response = await fetch(`/clips/${movie.id}`);
    let key = await response.text();

    // see if popup already there for the selected movie
    let div = movie.parentElement.parentElement.lastElementChild

    // if there's already a popup
    if (div.className !== 'hidden') {
        // check if it's for the selected movie, toggle
        if (div.id === movie.id) {
            div.className = 'hidden';
            div.lastElementChild.src = '';
        
        // if different movie, replace popup
        } else {
            div.id = movie.id;
            createPopup(movie, details, key, script);
        } 
    } else {
        div.id = movie.id;
        createPopup(movie, details, key, script);
    }
}


function createPopup(movie, details, key, script='') {

    // container for script
    let span = document.createElement('pre');

    span.innerHTML = script;
    
    let container = movie.parentNode.parentNode.lastElementChild

    container.classList.remove('hidden');
    container.className = 'selected';

    let detailDiv = container.firstElementChild;

    detailDiv.innerHTML = 
    details.release_date.slice(0,4).bold() + '\t' +
    '🎬 ' + details.runtime + ' min' + '\t' + 
    '⭐ ' + details.vote_average;


    let castDiv = detailDiv.nextElementSibling;

    // remove any current text inside
    castDiv.innerHTML = ''
    // let genres = document.createElement('span');
    details.genres.forEach(function (genre) {
        castDiv.innerText += (genre['name']) + '\n';
    }) 

    // castDiv.innerText = genres;
   
    

    // console.log(details.genres);

    let overviewDiv = castDiv.nextElementSibling;
    overviewDiv.innerHTML = details.overview;
    console.log(details.overview)

    let trailerDiv = overviewDiv.nextElementSibling;

    // if (script !== '') {
    //     trailerDiv.appendChild(span) }
    // else {
    //     // scriptDiv.firstElementChild.src = '/static/script.jpg'
    //     scriptDiv.innerHTML = 'Script Unavailable'.italics();
    //     }

    baseURL = 'https://www.youtube.com/embed/'
    
    let youTubeVideo = trailerDiv.firstElementChild
    youTubeVideo.src = baseURL + key + '?autoplay=1'

    console.log(youTubeVideo);

}

async function getTrailer(movie) {
    let response = await fetch(`/clips/${movie.id}`);
    let key = await response.text();

    return key;
}
