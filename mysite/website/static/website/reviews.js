document.addEventListener ('DOMContentLoaded', () => {
    document.querySelector('#compose-form').addEventListener('submit', post_review);
    document.querySelector('#filter-item').addEventListener('change', () =>{
        current_page = 0;
        filter_item();
    });
    document.querySelector('#leave-review-btn').addEventListener('click', () => leave_review())
    document.querySelector('#prev-reviews').addEventListener ('click', () => change_page(-1));
    document.querySelector('#next-reviews').addEventListener ('click', () => change_page (1));
    document.querySelector('#dropdown').addEventListener('click', () => open_dropdown());
    document.addEventListener('click', close_dropdown);
    
    show_reviews();
})

var current_page = 0;
var max_pages = 1;

function show_reviews (){
    view = document.querySelector("#review-view");
    fetch ("/getReviews/all")
        .then (response => response.json())
        .then (reviews => {
            get_reviews(reviews, current_page);
        });
}

function checked (n) {
    stars = document.getElementsByClassName("fa fa-star star-review rating-star");
    for (var i = 0; i < stars.length; i++){
        stars[i].classList.remove ('checked');
    }
    for (var i = 0; i < n; i++){
        stars[i].classList.add('checked');
    }
}

function post_review() {
    //event.preventDefault();

    //get required fields
    var name = document.querySelector('#reviewer').value;
    var content = document.querySelector('#content-form').value;
    var menu_item = document.getElementById('select-item').selectedOptions[0].value;
    var stars = document.getElementsByClassName('fa fa-star rating-star checked').length;

    fetch ("/reviewsAPI", {
        method: 'POST',
        body: JSON.stringify ({
            name: name,
            content: content,
            product_bought: menu_item,
            stars: stars,
        }),
    })
    var review =  document.querySelector('#compose-view');
    review.style.display = "none";

}

function filter_item(){
    console.log("HERE2");
    var menu_item = document.getElementById('filter-item').selectedOptions[0].value;
    document.querySelector('#review-view').innerHTML = "";
    //current_page = 0;
    if (menu_item === "All"){
        show_reviews();
    }
    else{
        fetch (`/getReviews/${menu_item}`)
            .then (response => response.json())
            .then (reviews => {
                get_reviews(reviews, current_page);
            })
    }
}

function get_reviews (reviews, current_page){
    max_pages = Math.ceil(reviews.length/8)
    view = document.querySelector('#review-view');
    starting_review = current_page * 8;
    var j = starting_review;

    while (j < starting_review + 8 && reviews[j]){
            var user = document.createElement("div");
            user.innerHTML = reviews[j]["user"];
            user.style.fontWeight = "bold";
        
            var product_bought = document.createElement("div");
            product_bought.innerHTML = reviews[j]["product_bought"];
            product_bought.style.color = "#9fa9a3";
            product_bought.style.fontSize = "12px";
            product_bought.style.fontFamily = "Georgia, 'Times New Roman', Times, serif";
            product_bought.style.fontStyle = "italic";
        
            var rating = document.createElement("div");
            var num_stars = reviews[j]["stars"];
        
            for (var i = 0; i < 5; i++){
                var checked_star = document.createElement("span");
                checked_star.classList.add("fa");
                checked_star.classList.add("fa-star");
                if (i < num_stars){
                    checked_star.classList.add("checked");
                }
                rating.appendChild(checked_star);
            }
        
            var content = document.createElement("div");
            content.innerHTML = reviews[j]['content'];
        
            var review = document.createElement("li");

            review.appendChild(user);
            review.appendChild(product_bought);
            review.appendChild(rating);
            review.appendChild(content);
            //review.appendChild(document.createElement("br"));
            review.classList.add("review");
            view.appendChild(review);

            j++;
        }
    var page_num = document.createElement("div");
    page_num.innerHTML = `Page ${current_page + 1} of ${max_pages}` 
    page_num.style.color = "#9fa9a3";
    page_num.style.fontFamily = "Georgia, 'Times New Roman', Times, serif";
    view.appendChild(page_num);
}

function leave_review() {
    var review = document.querySelector('#compose-view');
    review.style.display = "block";
}

function change_page (num){
    console.log("HERE");
    if (current_page + num >= max_pages){
        current_page = 0;
    }
    else if (current_page + num < 0){
        current_page = max_pages-1;
    }
    else{
        current_page += num;
    }
    filter_item();
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