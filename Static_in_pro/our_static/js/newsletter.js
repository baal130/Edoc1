 $(document).ready(function(){
//   NEWSLETTER              
  var newsletterForm = $(".ulockd-mailchimp")
  var newsletterFormMessage=$(".show-alert-news")
 /* console.log("faffafaf")*/
  newsletterForm.submit(function(event){
  event.preventDefault();
 /* console.log("Form is not sending")*/
  var thisForm = $(this)
  var actionEndpoint = thisForm.attr("action"); // API Endpoint
  var actionEndpoint = thisForm.attr("data-endpoint");
  var httpMethod = thisForm.attr("method");
  var formData = thisForm.serialize();

  $.ajax({
    url: actionEndpoint,
    method: httpMethod,
    data: formData,
    success: function(data){
   
     newsletterFormMessage.html("<span class='col-12  alert alert-success'> You have signed for newsletter </span>") 
        if(language="es"){
          newsletterFormMessage.html("<span class='col-12  alert alert-success'>Te has suscrito al boletín </span>")
        }
        newsletterFormMessage.addClass(" slideInDown animated3s")
        
        
      

    
    },
     error: function(error){
      console.log(error.responseJSON)
      var jsonData = error.responseJSON
      var msg = ""

      $.each(jsonData, function(key, value){ // key, value  array index / object
        msg += key + ": " + value[0].message + "<br/>"
      })
       newsletterFormMessage.addClass(" slideInDown animated3s")
       newsletterFormMessage.html("<span class='col-12  alert alert-danger'> Error </span>") 
        if(language="es"){
          newsletterFormMessage.html("<span class='col-12  alert alert-danger'>Tu mensaje  no ha sido enviado </span>")
        }
      

     

    }
    
  })
    
})            
//NEWSLETTER end

//CONTACT

   

var contactForm = $(".contact-ajax")
var contactFormSubmitBtn = contactForm.find("[type='submit']")
var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()  
var contactFormMessage=$(".show-alert")

    contactForm.submit(function(event){
    event.preventDefault();
    
    var thisForm = $(this)
    var actionEndpoint = thisForm.attr("action"); // API Endpoint
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();
    var language = thisForm.attr("language")
    setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, true)
        }, 100)     
        
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        contactForm[0].reset() 
        console.log('proslo')
        contactFormMessage.html("<span class='col-12  alert alert-success'> Your messsage has been send </span>") 
        if(language="es"){
          contactFormMessage.html("<span class='col-12  alert alert-success'>Tu mensaje ha sido enviado </span>")
        }
        contactFormMessage.addClass(" slideInDown animated3s")
        
        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 500) 
        

      
      },
      error: function(error){
      console.log(error.responseJSON)
      var jsonData = error.responseJSON
      var msg = ""

      $.each(jsonData, function(key, value){ // key, value  array index / object
        msg += key + ": " + value[0].message + "<br/>"
      })
       contactFormMessage.addClass(" slideInDown animated3s")
       contactFormMessage.html("<span class='col-12  alert alert-danger'> Your messsage has not been send </span>") 
        if(language="es"){
          contactFormMessage.html("<span class='col-12  alert alert-danger'>Tu mensaje  no ha sido enviado </span>")
        }
      

      setTimeout(function(){
        displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
      }, 500)

    }
      
    })
      
  })  //CONTACT END   
function displaySubmitting(submitBtn, defaultText, doSubmit){
    if (doSubmit){
       console.log("ggg")
      submitBtn.addClass("disabled")
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> ")
    } else {
      console.log("gsgssggsg")
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }
    
  }

}) //end ready           