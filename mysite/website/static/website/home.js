document.addEventListener ('DOMContentLoaded', function () {
    
    document.querySelector('#prev-home').addEventListener ('click', () => change_slide(-1));
    document.querySelector('#next-home').addEventListener ('click', () => change_slide (1));
    document.querySelector('#dropdown').addEventListener('click', () => open_dropdown());
    document.addEventListener('click', close_dropdown);

    //default
    load_home();
})

var current_slide = 0;

function load_home () {
    show_slide(current_slide);
}

function loadScript(url)
{    
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    //script.type = 'text/javascript';
    script.src = url;
    head.appendChild(script);
}

function show_slide (current_slide){
    var dots = document.getElementsByClassName("dot");
    for (var i = 0; i < dots.length; i++){
        dots[i].removeAttribute('id');
    }

    dots[current_slide].setAttribute('id', 'clicked-dot');

    slides = document.getElementsByClassName("slides");

    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slides[current_slide].style.display = "block";
}

function change_slide (n){

    slides = document.getElementsByClassName("slides");
    current_slide = current_slide + n;

    if (current_slide > slides.length - 1){
        current_slide = 0;
    }
    else if (current_slide < 0){
        current_slide = slides.length-1;
    }
    show_slide(current_slide);
}

function open_dropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function close_dropdown(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
