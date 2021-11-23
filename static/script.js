async function select(movie) {
    // console.log(movie.id);
    // console.log('clicked');

    // get details
    let detailResponse = await fetch(`/select/${movie.id}`);
    let detailsJSON = await detailResponse.text();

    console.log(detailsJSON)

    // console.log(overview);
    const details = JSON.parse(detailsJSON)
    // const cast = json.parse(detailsJSON[1])

    // console.log(details);

    // get script
    let scriptResponse = await fetch(`/script/${movie.alt}`);
    let script = await scriptResponse.text();

    // get trailer
    let response = await fetch(`/clips/${movie.id}`);
    let key = await response.text();

    // see if popup already there for the selected movie
    let div = movie.parentElement.parentElement.lastElementChild

    // // if for the selected movie, toggle
    // if (div.id == movie.id) {
    //     if (div.className == 'hidden') div.class
    // }
    // check if there is a popup somewhere on screen
    // check for popup
    let popUp = document.getElementsByClassName('selected')
    

    // if there's already a pop up
    // if (popUp.length !== 0) {
        
    //     popUp[0].className = 'hidden';
    //     div.id = movie.id;
    //     createPopup(movie, details, key, script)
            
    //     // popUp[0].firstElementChild.firstElementChild.src = '';
    // } else createPopup(movie, details, key, script)


    if (popUp.length !== 0) popUp[0].className = 'hidden';

    if (div.id !== movie.id){
        div.id = movie.id
        createPopup(movie, details, key, script)
    } else (div.className = 'hidden')
    
    // if there's a popup, 
    //      if it's the same movie, hide the popup
    //      if it's not the same movie, still hide it
    //      then build the popup you want
    

    // if there's already a popup
    // if (div.className !== 'hidden') {
    //     // check if it's for the selected movie, toggle
    //     if (div.id === movie.id) {
    //         div.className = 'hidden';
    //         div.firstElementChild.firstElementChild.src = '';
        
    //     // if different movie, replace popup
    //     } else {
    //         div.id = movie.id;
    //         createPopup(movie, details, key, script);
    //     } 
    // } else {
    //     div.id = movie.id;
    //     createPopup(movie, details, key, script);
    // }
}


function createPopup(movie, details, key, script='') {

    // container for script
    let span = document.createElement('pre');

    span.innerHTML = script;
    
    let container = movie.parentNode.parentNode.lastElementChild

    container.classList.remove('hidden');
    container.className = 'selected';


    let closeButton = container.firstElementChild;
    let trailerDiv = closeButton.nextElementSibling;
    // console.log(trailerDiv);
    let detailDiv = trailerDiv.nextElementSibling;
    // console.log(detailDiv)
    let castDiv = detailDiv.nextElementSibling;
    let genreDiv = castDiv.nextElementSibling;
    // console.log(genreDiv)
    let overviewDiv = genreDiv.nextElementSibling;
    // console.log(overviewDiv)
    let scriptDiv = overviewDiv.nextElementSibling;

    // detailDiv.innerHTML = 
    // details.release_date.slice(0,4).bold() + '\t' +
    // '🎬 ' + details.runtime + ' min' + '\t' + 
    // '⭐ ' + details.vote_average + '/10' + '\t' +  
    // '📄 ' 

    // scriptText = (script !== '') ? '📄 Read Script' : '';

    let year = details.year;
    let runtime = '🎬 ' + details.runtime + ' min';
    let rating = '⭐ ' + details.rating;
    let cast = details.cast.join(', ')
    let overview = details.overview
    let genres = details.genres.join(', ')

    // console.log(cast);
    // castList = '' += cast.forEach(actor)

    const detailText = new Array(year, runtime, rating)
    let detailSpan = Array.from(detailDiv.children)


    for (let i = 0; i < detailText.length; i++) {
        detailSpan[i].innerHTML = '';
        detailSpan[i].appendChild(document.createTextNode(detailText[i]))
    }
  
    genreDiv.innerHTML = 'Genres: ' + genres;


    castDiv.innerHTML = 'Cast: ' + cast;

    overviewDiv.innerHTML = overview;


    if (script !== '') {
        scriptDiv.innerHTML = ''
        scriptDiv.appendChild(span) 
        scriptDiv.style.minHeight = "500px";
    }
   

    baseURL = 'https://www.youtube.com/embed/'
    
    let youTubeVideo = trailerDiv.firstElementChild
    console.log(youTubeVideo);

    console.log(key);

    youTubeVideo.src = baseURL + key + '?autoplay=1&mute=1&encryped-media=1'

    // if (key === '') {
    //     trailerDiv.innerHTML = 'Trailer Unavailable' 
    // } else {
    //     youTubeVideo.src = baseURL + key + '?autoplay=1&mute=1&encryped-media=1'
    // }

    // console.log(youTubeVideo);

}

async function getTrailer(movie) {
    let response = await fetch(`/clips/${movie.id}`);
    let key = await response.text();

    return key;
}
