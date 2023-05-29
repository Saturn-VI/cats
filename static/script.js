let current_url = '';

async function copy_to_clipboard() {
    console.log('yippee');
    try {
        const imgURL = current_url;
        const data = await fetch(imgURL);
        const blob = await data.blob();
        await navigator.clipboard.write([
          new ClipboardItem({
            // The key is determined dynamically based on the blob's type.
            [blob.type]: blob
          })
        ]);
        console.log('Image copied.');
      } catch (err) {
        console.error(err.name, err.message);
      }
}

function reqlistener() {
    console.log(this.responseText);
    let post = JSON.parse(this.responseText);
    document.getElementById('title').innerHTML = post.title;
    document.getElementById('image').src = post.url;
    current_url = post.url;
    console.log(current_url);
    document.getElementById('main').innerHTML = document.getElementById('main').innerHTML;
    document.getElementById('main').style.visibility = 'visible';
}

function httpGet(theUrl)
{
    document.getElementById('main').style.visibility = 'hidden';
    var req = new XMLHttpRequest();
    req.addEventListener('load', reqlistener);
    req.open( "GET", theUrl, true );
    req.send();
    return req.responseText;
}

async function get_image() {
    let post = JSON.parse(httpGet('/api'));
    // html_title = document.getElementById('title');
    // html_image = document.getElementById('image');
    // html_title.innerHTML = post.title;
    // html_image.src = post.url;
    console.log(post);
}