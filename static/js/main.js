// const prevBtns = document.querySelectorAll(".btn-prev");
// const nextBtns = document.querySelectorAll(".btn-next");
// const progress = document.getElementById("progress");
// const formSteps = document.querySelectorAll(".form-step");
// const progressSteps = document.querySelectorAll(".progress-step");

// let formStepsNum = 0;

// nextBtns.forEach((btn) => {
//   btn.addEventListener("click", () => {
//     formStepsNum++;
//     updateFormSteps();
//     updateProgressbar();
//   });
// });

// prevBtns.forEach((btn) => {
//   btn.addEventListener("click", () => {
//     formStepsNum--;
//     updateFormSteps();
//     updateProgressbar();
//   });
// });

// function updateFormSteps() {
//   formSteps.forEach((formStep) => {
//     formStep.classList.contains("form-step-active") &&
//       formStep.classList.remove("form-step-active");
//   });

//   formSteps[formStepsNum].classList.add("form-step-active");
// }

// function updateProgressbar() {
//   progressSteps.forEach((progressStep, idx) => {
//     if (idx < formStepsNum + 1) {
//       progressStep.classList.add("progress-step-active");
//     } else {
//       progressStep.classList.remove("progress-step-active");
//     }
//   });

//   const progressActive = document.querySelectorAll(".progress-step-active");

//   progress.style.width =
//     ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
// }


let currentTab = 0;
showTab(currentTab);


function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("multistep_form_tab");

  x[n].style.display = "block";

  // // ... and fix the Previous/Next buttons:
  // if (n == 0) {
  //   document.getElementById("prevBtn").style.display = "none";
  // } else {
  //   document.getElementById("prevBtn").style.display = "inline";
  // }
  // if (n == (x.length - 1)) {
  //   document.getElementById("nextBtn").innerHTML = "Submit";
  // } else {
  //   document.getElementById("nextBtn").innerHTML = "Next";
  // }
  // ... and run a function that displays the correct step indicator:
  // fixStepIndicator(n)
}


function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("multistep_form_tab");
  // Exit the function if any field in the current tab is invalid:
  // if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}



// function fixStepIndicator(n) {
//   // This function removes the "active" class of all steps...
//   var i, x = document.getElementsByClassName("step");
//   for (i = 0; i < x.length; i++) {
//     x[i].className = x[i].className.replace(" active", "");
//   }
//   //... and adds the "active" class to the current step:
//   x[n].className += " active";
// }







// activity script
function changeImg(elementValue) {
  if (elementValue == "bajo") {
    let image_container = document.getElementById("activity_image_container");
    image_container.setAttribute("src", "/static/images/sedentario.svg");
  }

  if (elementValue == "medio") {
    let image_container = document.getElementById("activity_image_container");
    image_container.setAttribute("src", "/static/images/activo.svg");
  }

  if (elementValue == "alto") {
    let image_container = document.getElementById("activity_image_container");
    image_container.setAttribute("src", "/static/images/muy_activo.svg");
  }
}






function selectImgCarousel(element){
  document.getElementById('input_weight_image').value = element.id;
}



function changeImgCarousel(elementId) {
  let carouselItems = document.getElementsByClassName("carousel-item");


  if (elementId == 'next') {
    for (let i = 0; i < carouselItems.length; i++) {
      if (carouselItems[i].classList.contains('active')) {
        carouselItems[i].classList.remove('active');
        if (i == carouselItems.length - 1) {
          carouselItems[0].classList.add('active');
        } else {
          carouselItems[i + 1].classList.add('active');
        }
        break;
      }
    }
  } else {
    for (let i = 0; i < carouselItems.length; i++) {
      if (carouselItems[i].classList.contains('active')) {
        carouselItems[i].classList.remove('active');
        if (i == 0) {
          carouselItems[carouselItems.length - 1].classList.add('active');
        } else {
          carouselItems[i - 1].classList.add('active');
        }
        break;
      }
    }
  }

  let activeValue = document.querySelector(".carousel-item.active");
  let value = activeValue.childNodes[1].id;
  document.getElementById('input_weight_image').setAttribute('value', value);
}




function openMenu() {
  const menu = document.querySelector(".homepage_header__nav");

  if (menu.style.display == 'none' || menu.style.display == '') {
    menu.style.display = 'flex';
  } else {
    menu.style.display = 'none';
  }
}




const getName = () => {
  let name = document.getElementById('input_name').value;
  let nameContainer = document.getElementById('name_container');
  nameContainer.innerHTML = name;
}