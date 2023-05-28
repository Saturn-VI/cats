function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function get_image() {
    let post = JSON.parse(httpGet('/api'));
    html_title = document.getElementById('title');
    html_image = document.getElementById('image');
    html_title.innerHTML = post.title;
    html_image.src = post.url;
}