
//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

//Booleans to validate data 1:1
let=validatecif=false
let validatephone=false
let validatemail=false

$(".next").click(function(ev){

  var phone = document.getElementById("id_company_phone")
  var mail = document.getElementById("id_company_email") 
  let cif = document.getElementById("id_cif")
  var dir = document.getElementById("id_company_address")
  var patternphone=/^[679]{1}[0-9]{8}$/;
  var patternmail=/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  var patterncif=/^([A-Z])(\d{7})([0-9A-J])$/;
  var patterndir=/^[a-zA-Z0-9\s]{1,}$/;

  console.log(phone.value);
  console.log(mail.value);
  console.log(cif.value);
  console.log(dir.value);

  //Pattern validator for the CIF
  if(patterncif.test(cif.value))
  {
    validatecif=true;
    console.log("true");
  }else{  
    validatecif=false;
    console.log("false");
    cif.style.borderColor="red";
    ev.preventDefault();
  }
  
  //Pattern validator for the phone
  if(patternphone.test(phone.value))
  {
    validatephone=true;
    console.log("true");
    phone.style.borderColor="#ccc";
  }else{  
    validatephone=false;
    ev.preventDefault();
    console.log("false");
    phone.style.borderColor="red";
  }

  //Pattern validator for the mail
  if(patternmail.test(mail.value))
  {
    validatemail=true;
    console.log("true");
  }else{  
    validatemail=false;
    ev.preventDefault();
    console.log("false");
    mail.style.borderColor="red";
  }
  if (validatecif==true && validatephone==true && validatemail==true){

    cif.style.borderColor  ="#ccc";
    if(animating) return false;
    animating = true;

    current_fs = $(this).parent();
    next_fs = $(this).parent().next();

    //activate next step on progressbar using the index of next_fs
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show(); 
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
    step: function(now, mx) {
    //as the opacity of current_fs reduces to 0 - stored in "now"
    //1. scale current_fs down to 80%
    scale = 1 - (1 - now) * 0.2;
    //2. bring next_fs from the right(50%)
    left = (now * 50)+"%";
    //3. increase opacity of next_fs to 1 as it moves in
    opacity = 1 - now;
    current_fs.css({
    'transform': 'scale('+scale+')',
    'position': 'absolute'
      });
      next_fs.css({'left': left, 'opacity': opacity});
    }, 
    duration: 800, 
    complete: function(){
      current_fs.hide();
      animating = false;
    }, 
    //this comes from the custom easing plugin
    easing: 'easeInOutBack'
    });
    }
    if(cif.value.length !=9 ){
    console.log("CIF "+ cif.value.length)
      cif.style.borderColor  ="red";
        
        
          }else{
        
            cif.style.borderColor  ="#ccc";
        
          }
        
          if(phone.value.length !=9){
        
        
        
            phone.style.borderColor  ="red";
        
            console.log("COMPANY "+ phone.value.length)
        
        
        
          }else{
        
            phone.style.borderColor  ="#ccc";
        
          }
        
    });

$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

const $phone = document.getElementById("id_phone")
const $cphone= document.getElementById("id_company_phone")
const $cform = document.getElementById("clientForm")
const $pform = document.getElementById("proForm")

$cform.addEventListener(next_fs,function(e){
  e.preventDefault();
})


$pform.addEventListener('submit',function(e){
  e.preventDefault();
})

// $("#submit").click(function(){
// 	let phone = document.getElementById("id_phone");
//   patternphone=/^[0-9]{9}$/;
//   if(patternphone.test(phone)){
//     alert('[Valido]');
//   }else{  
//     alert('[Error]');
    
//   }
// })
