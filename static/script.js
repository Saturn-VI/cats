function reqlistener() {
    console.log(this.responseText);
    let post = JSON.parse(this.responseText);
    document.getElementById('title').innerHTML = post.title;
    document.getElementById('image').src = post.url
}

function httpGet(theUrl)
{
    var req = new XMLHttpRequest();
    req.addEventListener('load', reqlistener);
    req.open( "GET", theUrl, true );
    req.send();
    return req.responseText;
}

async function get_image() {
    let post = JSON.parse(httpGet('/api'));
    html_title = document.getElementById('title');
    html_image = document.getElementById('image');
    html_title.innerHTML = post.title;
    html_image.src = post.url;
}