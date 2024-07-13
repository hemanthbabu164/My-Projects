let movies = [
  {
    name: "loki",
    des:
      'The mercurial villain Loki resumes his role as the God of Mischief in a new series that takes place after the events of "Avengers: Endgame."',
    image:
      "https://img1.hotstarext.com/image/upload/f_auto,t_web_m_1x/sources/r1/cms/prod/1681/1011681-h-ac6ee255f074.png"
  },
  {
    name: "falcon and the winter soldier",
    des:
      'Following the events of "Avengers: Endgame, Sam Wilson and Bucky Barnes team up in a global adventure that tests their abilities and their patience.',
    image:
      "https://img1.hotstarext.com/image/upload/f_auto,t_web_m_1x/sources/r1/cms/prod/6362/936362-h.png"
  },
  {
    name: "wandavision",
    des:
      "Wanda Maximoff and Vision-two super-powered beings living idealized suburban lives-begin suspect that everything is not as it seems.",
    image:
      "https://img1.hotstarext.com/image/upload/f_auto,t_web_m_1x/sources/r1/cms/prod/1819/911819-h.png"
  },
  {
    name: "raya and the last dragon",
    des:
      "Raya, a fallen princess, must track down the legendary last dragon to stop the evil forces that have returned and threaten her world.",
    image:
      "https://img1.hotstarext.com/image/upload/f_auto,t_web_m_1x/sources/r1/cms/prod/7089/1037089-h-af0efbe1e4a7.png"
  },
  {
    name: "luca",
    des:
      "The movie is a coming-of-age story about one young boy experiencing an unforgettable summer filled with gelato, pasta and endless scoater rides.",
    image:
      "https://img1.hotstarext.com/image/upload/f_auto,t_web_m_1x/sources/r1/cms/prod/9298/1039298-h-4cac45a71e03.png"
  }
];

const carousel = document.querySelector(".carousel");
let sliders = [];

let slideIndex = 0; //to track the current slide

const createSlide = () => {
  carousel.innerHTML = " ";
  if (slideIndex >= movies.length) {
    slideIndex = 0;
  }

  //creating DOM Elements
  let slide = document.createElement("div");
  var imgElement = document.createElement("img");
  let content = document.createElement("div");
  let h1 = document.createElement("h1");
  let p = document.createElement("p");

  //attaching all elements
  imgElement.appendChild(document.createTextNode(""));
  h1.appendChild(document.createTextNode(movies[slideIndex].name));
  p.appendChild(document.createTextNode(movies[slideIndex].des));
  content.appendChild(h1);
  content.appendChild(p);
  slide.appendChild(imgElement);
  slide.appendChild(content);
  carousel.appendChild(slide);

  //setting up the images
  imgElement.src = movies[slideIndex].image;
  slideIndex++;

  //setting elements classnames
  slide.className = "slider";
  content.className = "slide-content";
  h1.className = "movie-title";
  p.className = "movie-des";

  sliders.push(slide);

  if (sliders.length) {
    sliders[0].style.marginLeft = `calc(-${100 * (sliders.length - 2)}%-${
      30 * (sliders.length - 2)
    }%)`;
  }
};

for (let i = 0; i < 3; i++) {
  createSlide();
}
setInterval(() => {
  createSlide();
}, 3000);

//video cards

const videoCards = [...document.querySelector];

videoCards.forEach((item) => {
  item.addEventListener("mouseover", () => {
    let video = item.children[1];
    video.play();
  });
  item.addEventListener("mouseleave", () => {
    let video = item.children[1];
    video.pause();
  });
});

//card sliders

let cardContainers = [...document.querySelectorAll(".card-container")];
let preBtns = [...document.querySelectorAll(".pre-btn")];
let nxtBtns = [...document.querySelectorAll(".nxt-btn")];

cardContainers.forEach((item, i) => {
  let containerDimensions = item.getBoundinngClientRect();
  let containerWidth = containerDimensions.width;

  nxtBtns[i].addEventListener("click", () => {
    item.scrollLeft += containerWidth - 100;
  });
  preBtns[i].addEventListener("click", () => {
    item.scrollLeft -= containerWidth + 100;
  });
});
