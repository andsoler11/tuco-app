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

  // Check if all required inputs on current tab have been filled before moving to the next tab
  var requiredInputs = x[currentTab].querySelectorAll('[required]');

  var allInputsFilled = true;

  if(n === 1){
    requiredInputs.forEach(input => {
      if (input.value.trim() === '') {
        allInputsFilled = false;
        input.parentElement.classList.add('error');
      } else {
        input.parentElement.classList.remove('error');
      }
    });

    if (!allInputsFilled) {
      // Show error message
      var errorMessage = document.getElementsByClassName("error-general-message");
      $(errorMessage).text("Por favor, complete todos los campos requeridos antes de continuar.");
      $(errorMessage).css("display", "block")
      //errorMessage[0].innerText = "Por favor, complete todos los campos requeridos antes de continuar.";
      //errorMessage[0].style.display = "block";
      return;
    }

    // Hide error message if previously displayed
    var errorMessage = document.getElementsByClassName("error-general-message");
    //errorMessage.style.display = "none";
    $(errorMessage).css("display", "none");

    // Validate weight input
    var weightInput = x[currentTab].querySelector('input[name="weight"]');
    if (weightInput) {
      var weightValue = weightInput.value.trim();
      if (weightValue === '' || weightValue === '0') {
        // Show error message if it's not already displayed
        if (errorMessage.style.display === 'none') {
          errorMessage.innerText = "Por favor, ingrese un peso válido.";
          errorMessage.style.display = "block";
        }
        weightInput.classList.add('error');
        return;
      } else {
        weightInput.classList.remove('error');
      }
    }
  }

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

function toggleMenu() {
  const menu = document.querySelector(".header__menu");
  const hamburger = document.querySelector(".hamburger");
  if (menu.classList.contains('header__menu--open')) {
    menu.classList.remove('header__menu--open');
    hamburger.classList.remove('hamburger--menu-open');
    document.body.classList.remove('body--menu-open');
  } else {
    menu.classList.add('header__menu--open');
    hamburger.classList.add('hamburger--menu-open');
    document.body.classList.add('body--menu-open');
  }
}

const getName = () => {
  let name = document.getElementById('input_name').value;
  $(".name_container").replaceWith(name);
  //let nameContainer = document.getElementsByClassName('name_container');
  //nameContainer.innerHTML = name;
}


// Fn Accordion Preguntas Frecuentes Home
var acc = document.getElementsByClassName("accordion-tab");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}

$(document).ready(function(){
  // Add active class to menu link
  activeMenu();

  //Construye carousel How It Works
  $('#how-it-works .owl-carousel').owlCarousel({
    margin:20,
    nav:false,
    responsive:{
        0:{
          items:1.3,
          loop:true
        },
        580:{
          items:2
        },
        768:{
          items:3,
          loop: false
      }
    }
  });

  // Construye carousel Conoce Nuestro Dogtor
  $('#meet-our-dogtor .owl-carousel').owlCarousel({
    margin:20,
    nav:false,
    items: 1,
    loop: true,
    autoplay: true,
    autoplayHoverPause: true,
    autoplaySpeed: 2000
  });

  // Construye carousel Por Qué Elegirnos
  $('#why-choose .owl-carousel').owlCarousel({
    margin:20,
    nav:true,
    center: true,
    loop: true,
    autoplay: true,
    autoplayHoverPause: true,
    autoplaySpeed: 4000,
    responsive:{
      0:{
          items:1
      },
      600:{
        items: 2
      },
      990:{
        items: 3.5
      }
    }
  });

  // Construye carousel Testimonios
  $('#testimonials .owl-carousel').owlCarousel({
    margin:20,
    nav:false,
    center: false,
    loop: true,
    autoplay: true,
    autoplayHoverPause: true,
    autoplaySpeed: 2000,
    responsive:{
      0:{
          items:2
      },
      600:{
        items: 3
      },
      990:{
        items: 4
      }
    }
  });

  //Construye carousel How It Works
  $('#make-transition .owl-carousel').owlCarousel({
    margin:20,
    nav:false,
    responsive:{
        0:{
          items:1.3,
          loop:true
        },
        580:{
          items:2
        },
        768:{
          items:3,
          loop: false
      }
    }
  });

  // Agrega clase focused a elemento padre de input para animar label de formularios
  $('.form input, .form textarea').focus(function(){
    $(this).parents('.field').addClass('focused');
  });
  // Valida input blur y elimina clase focused si el campo del formulario está vacío
  $('.form input, .form textarea').blur(function(){
    var inputValue = $(this).val();
    if ( inputValue == "" ) {
      $(this).parents('.field').removeClass('focused');  
    }
  });

  // Valida valor de input y agrega clase focused si el campo del formulario NO está vacío
  checkValInputsForms();


  // MENSAJES DE VALIDACIÓN
  var messageRequired = "Este campo es requerido";
  var messageSelectRequired = "Selecciona una opción";
  var messageEmail = "No es un correo válido, ejemplo: ejemplo@mail.com";
  var messageEqualTo = "La contraseña no coincide";
  var messageNumber = "Ingresa un valor en números";

  // Login usuarios
  $("#login-form").validate({
    rules: {
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
      },
    },
    messages: {
      password: {
        required: messageRequired,
      },
      email: {
        required: messageRequired,
        email: messageEmail,
      }
    }
  });

  // Registro usuarios
  $("#register-form").validate({
    rules: {
      full_name: {
        required: true,
      },
      email: {
        required: true,
        email: true,
      },
      phone_number: {
        required: true,
        number: true,
      },
      password1: {
        required: true,
      },
      password2: {
        required: true,
        equalTo: "#password1"
      },
    },
    messages: {
      full_name: {
        required: messageRequired,
      },
      email: {
        required: messageRequired,
        email: messageEmail,
      },
      phone_number: {
        required: messageRequired,
        number: messageNumber,
      },
      password1: {
        required: messageRequired,
      },
      password2: {
        required: messageRequired,
        equalTo: messageEqualTo
      }
    }
  });

  // Recuperar contraseña
  $("#password-form").validate({
    rules: {
      email: {
        required: true,
        email: true,
      },
    },
    messages: {
      email: {
        required: messageRequired,
        email: messageEmail,
      }
    }
  });

  // Nueva contraseña
  $("#newpassword-form").validate({
    rules: {
      password1: {
        required: true,
      },
      password2: {
        required: true,
        equalTo: "#password1"
      },
    },
    messages: {
      password1: {
        required: messageRequired,
      },
      password2: {
        required: messageRequired,
        equalTo: messageEqualTo
      }
    }
  });

  // Formulario de formulación
  $("#diet-form").validate({
    rules: {
      name: {
        required: true,
      },
      age: {
        required: true,
      },
      weight: {
        required: true,
      },
      name_contact: {
        required: true,
      },
      email_contact: {
        required: true,
        email: true,
      },
    },
    messages: {
      name: {
        required: messageRequired,
      },
      age: {
        required: messageRequired,
      },
      weight: {
        required: messageRequired,
      },
      name_contact: {
        required: messageRequired,
      },
      email_contact: {
        required: messageRequired,
        email: messageEmail
      }
    }
  });

  // Formulario de editar mascota
  $("#edit-pet-form").validate({
    rules: {
      name: {
        required: true,
      },
      age: {
        required: true,
      },
      weight: {
        required: true,
      },
      name_contact: {
        required: true,
      },
      email_contact: {
        required: true,
        email: true,
      },
    },
    messages: {
      name: {
        required: messageRequired,
      },
      age: {
        required: messageRequired,
      },
      weight: {
        required: messageRequired,
      },
      name_contact: {
        required: messageRequired,
      },
      email_contact: {
        required: messageRequired,
        email: messageEmail
      }
    }
  });

  // Editar Mis datos
  $("#account-form").validate({
    rules: {
      name: {
        required: true,
      },
      email: {
        required: true,
        email: true,
      },
      phone: {
        required: true,
        number: true,
      },
    },
    messages: {
      name: {
        required: messageRequired,
      },
      email: {
        required: messageRequired,
        email: messageEmail,
      },
      phone: {
        required: messageRequired,
        number: messageNumber,
      }
    }
  });

  // Agregar Dirección
  $("#address-form").validate({
    ignore: [],
    errorPlacement: function(error, element) {
      error.insertAfter(element);
    },
    rules: {
      name_address: {
        required: true,
      },
      address: {
        required: true,
      },
      additional_info: {
        required: true,
      },
      depto: {
        required: true,
      },
      city: {
        required: true,
      },
      user_phone: {
        required: true,
        number: true,
      },
    },
    messages: {
      name_address: {
        required: messageRequired,
      },
      address: {
        required: messageRequired,
      },
      additional_info: {
        required: messageRequired,
      },
      depto: {
        required: messageRequired,
      },
      city: {
        required: messageRequired,
      },
      user_phone: {
        required: messageRequired,
        number: messageNumber,
      }
    }
  });

  // Agregar Método de pago
  $("#paymentMethod-form").validate({
    ignore: [],
    errorPlacement: function(error, element) {
      error.insertAfter(element);
    },
    rules: {
      number_card: {
        required: true,
        number: true,
      },
      due_date: {
        required: true,
      },
      ccv: {
        required: true,
        number: true,
      },
      document_type: {
        required: true,
      },
      document_number: {
        required: true,
      },
    },
    messages: {
      number_card: {
        required: messageRequired,
        number: messageNumber,
      },
      due_date: {
        required: messageRequired,
      },
      ccv: {
        required: messageRequired,
        number: messageNumber,
      },
      document_type: {
        required: messageRequired,
      },
      document_number: {
        required: messageRequired,
      }
    }
  });

  // Personaliza select field
  $(".form .field select").niceSelect();
  $(".cart-item-group .item select").niceSelect();
  //$(".form_breed_sex_input .breed-input .list").prepend(`<input type="text" class="nice-select-search" placeholder="Escribe la raza de tu mascota">`);

  //Ajusta altura de textos en cards de menú
  if($('.diet-card-list').length){
    heightTitleCards();
  }

  // // Selecciona menú para realizar compra
  // $('.diet-card.select-option .check').click(function(){
  //   $('.diet-card.select-option').removeClass('checked');
  //   $(this).parent().addClass('checked');

  //   // Habilita btn de compra
  //   $('.wrapper-button.button-buy-now a.link-button').removeAttr('disabled');
  // });
  $('.diet-card.select-option .check').click(function() {
    $('.diet-card.select-option').removeClass('checked');
    $(this).parent().addClass('checked');

    var menuUrl = $(this).parent().data('menu-url');

    // Set the updated URL to the "Buy Now" button
    $('.wrapper-button.button-buy-now a.link-button').attr('href', menuUrl);
    
    // Enable the button
    $('.wrapper-button.button-buy-now a.link-button').removeAttr('disabled');
  });


  // Habilita edición de formularios
  var arrayDataForm = {};
  $('#editDataForm').click(function(){
    var thisForm = $('.main_container--form form').attr('id');
    var inputs = $('#'+thisForm).find('input, select, textarea').not('[type="hidden"], [type="submit"], [type="button"], [noChange]');

    $(inputs).removeAttr('disabled');

    $(this).parent().addClass('hidden');
    $('.wrapper-submit-button').removeClass('hidden');

    $.each(inputs, function(i, val){
      if($(val).is('select')){
        $(val).parent().find('.nice-select').removeClass('disabled');
      }
      var idVal = $(val).attr('id');
      arrayDataForm[idVal] = $(val).val();
    });
    //console.log(arrayDataForm);
  });

  // Cancela edición de formularios
  $('#cancel-edit-form').click(function(){
    var thisForm = $('.main_container--form form').attr('id');
    var inputs = $('#'+thisForm).find('input, select, textarea').not('[type="hidden"], [type="submit"], [type="button"], [noChange]');

    $(inputs).attr('disabled', 'disabled');
    $(inputs).removeClass('error');
    $(inputs).parent().addClass('focused');
    $('label.error').remove();

    $(this).parents('.wrapper-submit-button').addClass('hidden');
    $('.wrapper-edit-button').removeClass('hidden');

    $.each(arrayDataForm, function(keyArray, valueArray){
      $.each(inputs, function(i, val){
        if($(val).is('select')){
          $(val).parent().find('.nice-select').addClass('disabled');
          returnSelectValue(val);
        }
        
        var valInput = $(val).attr('id');
        if(keyArray === valInput){
          $(val).val(valueArray);
        }
      });
    });
    arrayDataForm = {};
  });
});

// FN return select value
function returnSelectValue(obj){
  var valSelect = $(obj).val();
  var optNiceSelect = $(obj).parent().find('.nice-select li');

  $.each(optNiceSelect, function(i, val){
    var optDataValue = $(val).attr('data-value');
    if(optDataValue === valSelect){
      $(val).trigger('click');
    }
  });
}

// FN Add active class to menu link
function activeMenu(){
  var pathname = window.location.pathname;

  var linksMenu = $('.header__nav__item a');
  $.each(linksMenu, function(i, val){
    var attrHref = $(val).attr('href');
    if(attrHref === pathname){
      $(this).addClass('active');
    }
  });
}

// FN Ajusta altura de textos en cards de menú
function heightTitleCards(){
  var cardsMenu = $('.diet-card-list .diet-card');
  var arrayTitles = [];

  // Recorre listado para calcular añtura de titulo mayor
  $.each(cardsMenu, function(i, val){
    var titleCard = $(val).find('h2').height();
    arrayTitles.push(titleCard);
  });
  var maxHTitle = Math.max(...arrayTitles);

  // Asigna css a titulos para estandarizar altura
  $(cardsMenu).find('h2').css('min-height', maxHTitle+'px');
}

// FN Valida valor de input y agrega clase focused si el campo del formulario NO está vacío
function checkValInputsForms(){
  var thisForm = $('.main_container--form form').attr('id');
  var inputs = $('#'+thisForm).find('input, select, textarea').not('[type="hidden"], [type="submit"]');

  $.each(inputs, function(i, val){
    var valThisInput = $(val).val();

    if(valThisInput != ""){
      $(val).parent().addClass('focused');
    }
  });
}



// MODAL DELETE PET
// Get the modal
var modal = document.getElementById("myModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// Get the form
var deleteForm = document.getElementById("deleteForm");

// Get the pet ID from the clicked button and set the form action URL
function showModal(petId) {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
/*span.onclick = function() {
    hideModal();
}*/

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        hideModal();
    }
}

// Hide the modal
function hideModal() {
    modal.style.display = "none";
}