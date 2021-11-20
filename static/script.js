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
    // console.log(movie.id)


    // if (script === '') {
    //     script = '\n\n\n\nNO SCRIPT AVAILABLE'
        
    // }
    // console.log(script);

    // see if popup already there for the selected movie
    let div = movie.parentElement.parentElement.lastElementChild

    // if there's already a popup
    if (div.className === 'selected') {
        // check if it's for the selected movie, toggle
        if (div.id === movie.id) {
            div.remove();
            // div.className.toggle('hidden');
        
        // if different movie, replace popup
        } else {
            div.id = movie.id;
            div.lastElementChild.innerHTML = script;
        } 
    
    // create popup
    }  else {
        
        // let popUp = document.createElement('div');    

        // popUp.className = 'selected';
        // popUp.id = movie.id;

        // // using text

        let span = document.createElement('pre');

        span.innerHTML = script;
        // popUp.appendChild(span);
      
        let container = movie.parentNode.parentNode.lastElementChild

        // div.appendChild(popUp);
        // console.log(container)

        container.classList.remove('hidden');
        container.className = 'selected';


        // let sections = container.children
        
        // console.log(sections)

        // sections[3].appendChild(span);

        // let scriptDiv = container.firstElementChild;
        // scriptDiv.appendChild(span);

        let detailDiv = container.firstElementChild;
  

        detailDiv.innerHTML = 
        details.release_date.slice(0,4).bold() + '\t' +
        '🎥 ' + details.runtime + 'min' + '\t' + 
        // 'Runtime: '.bold() + details.runtime + 'min' + '\t' +
        '⭐ '.bold() + details.vote_average;

        // detailDiv.appendChild(detailSpan);

        // detailDiv.appendChild(details.release_date.slice(0,4).bold() + '\t');
        // detailDiv.appendChild('🎥 ' + details.runtime + 'min' + '\t');
        // detailDiv.appendChild('⭐ '.bold() + details.vote_average);


        let castDiv = detailDiv.nextElementSibling;
        // castDiv.innerText = details.genres
        details.genres.forEach(function (genre) {
            castDiv.innerText += (genre['name']) + '\n';
        }) 

        console.log(details.genres);

        let overviewDiv = castDiv.nextElementSibling;
        overviewDiv.innerHTML = details.overview;
        console.log(details.overview)

        let scriptDiv = overviewDiv.nextElementSibling;

        if (script !== '') {
            scriptDiv.appendChild(span) }
            else {
                scriptDiv.firstElementChild.src = '/static/script.jpg'
                scriptDiv.lastElementChild.innerHTML = 'Script Unavailable'.italics();
            }
       
        


    }
}
